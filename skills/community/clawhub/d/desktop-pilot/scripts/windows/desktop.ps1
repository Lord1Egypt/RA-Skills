# Desktop Pilot - Windows backend (PowerShell 5.1+ / 7, no installs).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File desktop.ps1 <action> [options]
param(
  [Parameter(Position = 0)]
  [ValidateSet('screenshot', 'windows', 'buttons', 'click', 'close', 'focus', 'type', 'key', 'mouse', 'help')]
  [string]$Action = 'help',
  [string]$Process,          # process name without .exe (e.g. notepad, chrome)
  [string]$Title,            # alternative to -Process: substring of the window title
  [string]$Name,             # visible control name for click
  [string]$Text,             # text for type
  [string]$TextB64,          # same as -Text, UTF-8 base64 (safe for any character through WSL/shells)
  [string]$Keys,             # SendKeys syntax for key, e.g. "{ENTER}", "^c", "%{F4}"
  [int]$X = -1, [int]$Y = -1,
  [ValidateSet('left', 'right', 'double', 'move')][string]$Button = 'left',
  [string]$Out               # screenshot output path
)
$ErrorActionPreference = 'Stop'
if ($TextB64) { $Text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($TextB64)) }
Add-Type -AssemblyName System.Windows.Forms, System.Drawing, UIAutomationClient, UIAutomationTypes
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class DpNative {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] static extern bool AttachThreadInput(uint a, uint b, bool attach);
  [DllImport("user32.dll")] static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
  [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
  public static string ForegroundTitle() { var sb = new System.Text.StringBuilder(256); GetWindowText(GetForegroundWindow(), sb, 256); return sb.ToString(); }
  public static uint ForegroundPid() { uint p; GetWindowThreadProcessId(GetForegroundWindow(), out p); return p; }
  static bool IsFg(IntPtr h, uint tpid) { IntPtr fg = GetForegroundWindow(); if (fg == h) return true; uint p; GetWindowThreadProcessId(fg, out p); return tpid != 0 && p == tpid; }
  // Windows refuses SetForegroundWindow from background processes ("foreground lock"): try plain, then thread-attach, then the ALT trick,
  // and only report success when the target (or one of its process's windows) really is in the foreground.
  public static bool BringToFront(IntPtr h) {
    ShowWindow(h, IsIconic(h) ? 9 : 5);
    uint tpid; GetWindowThreadProcessId(h, out tpid);
    for (int attempt = 0; attempt < 3; attempt++) {
      if (IsFg(h, tpid)) return true;
      SetForegroundWindow(h); System.Threading.Thread.Sleep(80);
      if (IsFg(h, tpid)) return true;
      uint fpid; uint fth = GetWindowThreadProcessId(GetForegroundWindow(), out fpid); uint me = GetCurrentThreadId();
      if (fth != 0 && fth != me) { AttachThreadInput(me, fth, true); BringWindowToTop(h); SetForegroundWindow(h); AttachThreadInput(me, fth, false); }
      System.Threading.Thread.Sleep(80);
      if (IsFg(h, tpid)) return true;
      if (attempt == 1) { keybd_event(0x12, 0, 0, UIntPtr.Zero); keybd_event(0x12, 0, 2, UIntPtr.Zero); SetForegroundWindow(h); }
      System.Threading.Thread.Sleep(100);
    }
    return IsFg(h, tpid);
  }
  [StructLayout(LayoutKind.Sequential)] struct KBD { public ushort vk, scan; public uint flags, time; public IntPtr extra; }
  [StructLayout(LayoutKind.Explicit, Size = 40)] struct INPUT { [FieldOffset(0)] public uint type; [FieldOffset(8)] public KBD ki; }
  [DllImport("user32.dll", SetLastError = true)] static extern uint SendInput(uint n, INPUT[] i, int size);
  // Unicode key events: independent of the keyboard layout (SendKeys breaks symbols on non-US layouts).
  public static void TypeUnicode(string s) {
    foreach (char c in s) {
      var down = new INPUT { type = 1 }; down.ki.scan = c; down.ki.flags = 0x0004;
      var up = new INPUT { type = 1 }; up.ki.scan = c; up.ki.flags = 0x0004 | 0x0002;
      SendInput(2, new[] { down, up }, Marshal.SizeOf(typeof(INPUT)));
      System.Threading.Thread.Sleep(5);
    }
  }
}
"@
[DpNative]::SetProcessDPIAware() | Out-Null
$A = [System.Windows.Automation.AutomationElement]
$S = [System.Windows.Automation.TreeScope]
function Cond($p, $v) { New-Object System.Windows.Automation.PropertyCondition($p, $v) }

function Get-TargetProcs {
  if ($Process) { $ps = Get-Process -Name $Process -ErrorAction SilentlyContinue }
  elseif ($Title) { $ps = Get-Process | Where-Object { $_.MainWindowTitle -like "*$Title*" } }
  else { throw 'Specify -Process <name> or -Title <text>' }
  if (-not $ps) { throw "No process matches $Process$Title" }
  $ps
}
function Get-TargetWindows {
  $wins = foreach ($p in Get-TargetProcs) { $A::RootElement.FindAll($S::Children, (Cond $A::ProcessIdProperty $p.Id)) }
  $wins = @($wins | Where-Object { $_ -and (-not $Title -or $_.Current.Name -like "*$Title*") })
  if (-not $wins) { throw 'No visible window (app may be hidden in the tray: relaunch its exe, then retry)' }
  $wins
}
# Portable combos (ctrl+c, alt+f4, enter) -> SendKeys; raw SendKeys ({ENTER}, ^c) passes through.
function Convert-Combo([string]$k) {
  if ($k -notmatch '^[A-Za-z0-9]+(\+[A-Za-z0-9]+)*$') { return $k }
  $mods = @{ ctrl = '^'; control = '^'; alt = '%'; shift = '+' }
  $named = @{ enter = '{ENTER}'; return = '{ENTER}'; tab = '{TAB}'; esc = '{ESC}'; escape = '{ESC}'; space = ' ';
    backspace = '{BS}'; delete = '{DEL}'; del = '{DEL}'; home = '{HOME}'; end = '{END}'; pageup = '{PGUP}'; pagedown = '{PGDN}';
    up = '{UP}'; down = '{DOWN}'; left = '{LEFT}'; right = '{RIGHT}'; insert = '{INS}' }
  $parts = $k.ToLower().Split('+'); $prefix = ''
  foreach ($m in $parts[0..($parts.Count - 2)]) { if ($parts.Count -gt 1) { if (-not $mods[$m]) { throw "Unsupported modifier '$m' on Windows" }; $prefix += $mods[$m] } }
  $last = $parts[-1]
  if ($named[$last]) { $key = $named[$last] } elseif ($last -match '^f([1-9]|1[0-6])$') { $key = "{$($last.ToUpper())}" } else { $key = $last }
  "$prefix$key"
}
# Returns $true only when the window really ended up in the foreground.
function Focus-Window($w) {
  $h = [IntPtr]$w.Current.NativeWindowHandle
  if ($h -ne [IntPtr]::Zero) { return [DpNative]::BringToFront($h) }
  try { $w.SetFocus() } catch {}
  Start-Sleep -Milliseconds 150
  return ([DpNative]::ForegroundPid() -eq [uint32]$w.Current.ProcessId)
}
# Input must never land in the wrong window: abort instead of typing blind.
function Require-Focus($w) {
  if (-not (Focus-Window $w)) {
    throw "FOCUS_FAILED: could not bring '$($w.Current.Name)' to the foreground; the foreground window is '$([DpNative]::ForegroundTitle())'. Nothing was typed or clicked. Ask the user to click the target window, or click its taskbar icon, then retry."
  }
}

switch ($Action) {
  'help' {
    'actions: screenshot [-Out path] | windows | buttons -Process|-Title | click -Process|-Title -Name <label>'
    '         close -Process|-Title | focus -Process|-Title | type -Text <s> [-Process|-Title]'
    '         key -Keys <SendKeys> [-Process|-Title] | mouse -X -Y [-Button left|right|double|move]'
  }
  'screenshot' {
    $b = [System.Windows.Forms.SystemInformation]::VirtualScreen
    if (-not $Out) { $Out = Join-Path $env:TEMP 'desktop-pilot.png' }
    $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
    [System.Drawing.Graphics]::FromImage($bmp).CopyFromScreen($b.Left, $b.Top, 0, 0, $bmp.Size)
    $bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
    "OK screenshot $($b.Width)x$($b.Height) $Out"
  }
  'windows' {
    Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle } |
      ForEach-Object { "$($_.Id)`t$($_.Name)`t$($_.MainWindowTitle)" }
  }
  'buttons' {
    $types = 'Button', 'MenuItem', 'Hyperlink', 'CheckBox', 'RadioButton', 'TabItem', 'ListItem'
    foreach ($w in Get-TargetWindows) {
      "[window] $($w.Current.Name)"
      foreach ($t in $types) {
        $ct = [System.Windows.Automation.ControlType]::$t
        $w.FindAll($S::Descendants, (Cond $A::ControlTypeProperty $ct)) |
          ForEach-Object { if ($_.Current.Name) { "  $t`t$($_.Current.Name)" } }
      }
    }
  }
  'click' {
    if (-not $Name) { throw 'Specify -Name <visible label>' }
    foreach ($w in Get-TargetWindows) {
      $el = $w.FindFirst($S::Descendants, (Cond $A::NameProperty $Name))
      if (-not $el) { continue }
      $pat = $null
      foreach ($p in [System.Windows.Automation.InvokePattern]::Pattern, [System.Windows.Automation.TogglePattern]::Pattern,
                     [System.Windows.Automation.SelectionItemPattern]::Pattern, [System.Windows.Automation.ExpandCollapsePattern]::Pattern) {
        if ($el.TryGetCurrentPattern($p, [ref]$pat)) {
          switch ($pat.GetType().Name) {
            'InvokePattern' { $pat.Invoke() } 'TogglePattern' { $pat.Toggle() }
            'SelectionItemPattern' { $pat.Select() } 'ExpandCollapsePattern' { $pat.Expand() }
          }
          "OK clicked '$Name' ($($pat.GetType().Name))"; return
        }
      }
      # Fallback: physical click at the element center.
      $r = $el.Current.BoundingRectangle
      Require-Focus $w
      [DpNative]::SetCursorPos([int]($r.X + $r.Width / 2), [int]($r.Y + $r.Height / 2)) | Out-Null
      [DpNative]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero); [DpNative]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
      "OK clicked '$Name' (mouse fallback)"; return
    }
    throw "Control not found: '$Name' (run 'buttons' to list exact labels)"
  }
  'close' {
    foreach ($w in Get-TargetWindows) {
      $pat = $null
      if ($w.TryGetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern, [ref]$pat)) { $pat.Close(); "OK closed '$($w.Current.Name)'" }
    }
  }
  'focus' { $w = (Get-TargetWindows)[0]; Require-Focus $w; "OK focused '$($w.Current.Name)' (verified: foreground)" }
  'type' {
    if (-not $Text) { throw 'Specify -Text' }
    if ($Process -or $Title) { Require-Focus (Get-TargetWindows)[0]; Start-Sleep -Milliseconds 300 }
    else { "NOTE: no -Process/-Title given; typing into the foreground window '$([DpNative]::ForegroundTitle())'" }
    [DpNative]::TypeUnicode($Text); "OK typed $($Text.Length) chars into '$([DpNative]::ForegroundTitle())'"
  }
  'key' {
    if (-not $Keys) { throw 'Specify -Keys (ctrl+c, alt+f4, enter... or raw SendKeys like {ENTER})' }
    if ($Process -or $Title) { Require-Focus (Get-TargetWindows)[0]; Start-Sleep -Milliseconds 250 }
    else { "NOTE: no -Process/-Title given; sending keys to the foreground window '$([DpNative]::ForegroundTitle())'" }
    $sk = Convert-Combo $Keys
    [System.Windows.Forms.SendKeys]::SendWait($sk); "OK keys $Keys -> $sk (foreground: '$([DpNative]::ForegroundTitle())')"
  }
  'mouse' {
    if ($X -lt 0 -or $Y -lt 0) { throw 'Specify -X and -Y (screen pixels, from the screenshot)' }
    [DpNative]::SetCursorPos($X, $Y) | Out-Null
    $flags = @{ left = @(2, 4); right = @(8, 16); double = @(2, 4, 2, 4); move = @() }[$Button]
    foreach ($f in $flags) { [DpNative]::mouse_event($f, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 40 }
    "OK mouse $Button at $X,$Y"
  }
}
