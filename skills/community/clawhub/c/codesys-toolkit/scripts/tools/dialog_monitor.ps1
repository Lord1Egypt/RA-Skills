# dialog_monitor.ps1
# Monitor InoProShop dialogs via WinEvent Hook (EVENT_OBJECT_SHOW).
# Zero polling - callback fires only when a window appears.
#
# Usage (as Start-Job):
#   $job = Start-Job -FilePath $monitor -ArgumentList $proc.Id, $logPath, "InoProShop", 120

param(
    [int]   $WatchPid    = 0,
    [string]$LogPath     = "",
    [string]$TitleFilter = "InoProShop",
    [int]   $MaxSeconds  = 120
)

if (-not $LogPath) {
    Write-Error "LogPath is required"
    exit 1
}

$logDir = Split-Path $LogPath
if ($logDir -and !(Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }

function Write-Log([string]$msg) {
    $line = "[$(Get-Date -Format 'HH:mm:ss')] $msg"
    Write-Host $line
    [System.IO.File]::AppendAllText($LogPath, "$line`n", [System.Text.UTF8Encoding]::new($false))
}

# ── C# core: WinEvent hook + message loop ─────────────────────────────────
try {
Add-Type @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

public class DlgMonitor {
    // Win32 imports
    [DllImport("user32.dll")] static extern IntPtr SetWinEventHook(
        uint eventMin, uint eventMax, IntPtr hmod,
        WinEventProc pfnWinEventProc, uint idProcess, uint idThread, uint dwFlags);
    [DllImport("user32.dll")] static extern bool UnhookWinEvent(IntPtr hHook);
    [DllImport("user32.dll")] static extern bool GetMessage(ref MSG msg, IntPtr hwnd, uint f, uint l);
    [DllImport("user32.dll")] static extern bool TranslateMessage(ref MSG msg);
    [DllImport("user32.dll")] static extern IntPtr DispatchMessage(ref MSG msg);
    [DllImport("user32.dll")] static extern void PostThreadMessage(uint tid, uint msg, IntPtr wp, IntPtr lp);
    [DllImport("user32.dll")] static extern int  GetWindowText(IntPtr h, StringBuilder sb, int max);
    [DllImport("user32.dll")] static extern int  GetClassName(IntPtr h, StringBuilder sb, int max);
    [DllImport("user32.dll")] static extern bool EnumChildWindows(IntPtr p, EnumCB cb, IntPtr lp);
    [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();

    public delegate bool EnumCB(IntPtr h, IntPtr lp);
    delegate void WinEventProc(IntPtr hHook, uint evt, IntPtr hwnd,
                               int idObj, int idChild, uint tid, uint time);

    const uint EVENT_OBJECT_SHOW    = 0x8002;
    const uint WINEVENT_OUTOFCONTEXT = 0x0000;
    const uint WM_QUIT              = 0x0012;

    [StructLayout(LayoutKind.Sequential)]
    struct MSG {
        public IntPtr hwnd; public uint message;
        public IntPtr wParam; public IntPtr lParam;
        public uint time; public int ptX; public int ptY;
    }

    // Shared state
    static int    s_watchPid;
    static string s_titleFilter;
    static Action<string> s_log;
    static HashSet<IntPtr> s_seen = new HashSet<IntPtr>();
    static uint   s_loopThreadId;

    public static void Run(int watchPid, string titleFilter,
                           Action<string> log, int maxSeconds) {
        s_watchPid    = watchPid;
        s_titleFilter = titleFilter ?? "";
        s_log         = log;

        s_loopThreadId = GetCurrentThreadId();

        WinEventProc cb = OnWinEvent;
        IntPtr hook = SetWinEventHook(
            EVENT_OBJECT_SHOW, EVENT_OBJECT_SHOW,
            IntPtr.Zero, cb,
            (uint)(watchPid > 0 ? watchPid : 0), 0,
            WINEVENT_OUTOFCONTEXT);

        // Timeout thread
        if (maxSeconds > 0) {
            int ms = maxSeconds * 1000;
            uint tid = s_loopThreadId;
            new Thread(() => {
                Thread.Sleep(ms);
                PostThreadMessage(tid, WM_QUIT, IntPtr.Zero, IntPtr.Zero);
            }) { IsBackground = true }.Start();
        }

        // Watch-pid exit thread
        if (watchPid > 0) {
            uint tid = s_loopThreadId;
            new Thread(() => {
                try {
                    var p = System.Diagnostics.Process.GetProcessById(watchPid);
                    p.WaitForExit();
                } catch {}
                PostThreadMessage(tid, WM_QUIT, IntPtr.Zero, IntPtr.Zero);
            }) { IsBackground = true }.Start();
        }

        MSG msg = new MSG();
        while (GetMessage(ref msg, IntPtr.Zero, 0, 0)) {
            TranslateMessage(ref msg);
            DispatchMessage(ref msg);
        }

        UnhookWinEvent(hook);
        GC.KeepAlive(cb);
    }

    static void OnWinEvent(IntPtr hHook, uint evt, IntPtr hwnd,
                           int idObj, int idChild, uint tid, uint time) {
        if (hwnd == IntPtr.Zero) return;
        if (!IsWindowVisible(hwnd)) return;

        // Check class == #32770
        var sbCls = new StringBuilder(64);
        GetClassName(hwnd, sbCls, 64);
        if (sbCls.ToString() != "#32770") return;

        // Check PID ownership
        if (s_watchPid > 0) {
            uint ownerPid = 0;
            GetWindowThreadProcessId(hwnd, out ownerPid);
            if ((int)ownerPid != s_watchPid) return;
        }

        // Title filter
        var sbTitle = new StringBuilder(512);
        GetWindowText(hwnd, sbTitle, 512);
        string title = sbTitle.ToString();
        if (s_titleFilter.Length > 0 && !title.Contains(s_titleFilter)) return;

        // Only log once per handle
        if (s_seen.Contains(hwnd)) return;
        s_seen.Add(hwnd);

        // Read child controls
        var statics = new List<string>();
        var buttons = new List<string>();
        EnumChildWindows(hwnd, (child, lp) => {
            var sbT = new StringBuilder(1024);
            var sbC = new StringBuilder(64);
            GetWindowText(child, sbT, 1024);
            GetClassName(child, sbC, 64);
            string t = sbT.ToString().Trim();
            string c = sbC.ToString();
            if (t.Length > 0) {
                if (c == "Static") statics.Add(t);
                if (c == "Button") buttons.Add(t);
            }
            return true;
        }, IntPtr.Zero);

        string body   = string.Join(" | ", statics.ToArray());
        string btnStr = string.Join(", ", buttons.ToArray());

        s_log("DIALOG DETECTED: [" + title + "]");
        s_log("  Body   : " + body);
        s_log("  Buttons: " + btnStr);
    }
}
"@
} catch { <# already loaded #> }

# ── Start ──────────────────────────────────────────────────────────────────
$mode = if ($WatchPid -gt 0) { "WatchPid=$WatchPid" } else { "MaxSeconds=$MaxSeconds" }
Write-Log "=== dialog_monitor started (Filter='$TitleFilter', $mode) ==="

[DlgMonitor]::Run(
    $WatchPid,
    $TitleFilter,
    [Action[string]]{ param($m) Write-Log $m },
    $MaxSeconds
)

Write-Log "=== dialog_monitor stopped ==="
