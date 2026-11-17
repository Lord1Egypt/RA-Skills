#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the Windows Startup VBS launcher for the DingTalk auto-reply monitor.

WHY THIS EXISTS
---------------
The .vbs launcher is MACHINE-SPECIFIC glue. It must NOT be shipped with the
skill (it is listed in .gitignore). Instead the launcher is REGENERATED on the
target machine by this script, so the skill stays portable: copy the skill dir
to any Windows machine, run `python gen_launcher.py` once (or let the monitor
auto-generate it on first run), and the Startup shortcut appears.

The generated VBS derives ALL paths from the current user profile via
WScript.Shell.SpecialFolders("Profile") -- no hardcoded username -- so the same
VBS works on any machine.

Generated file (per-user interactive Startup folder):
  %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\dingtalk_auto_reply_launcher.vbs
"""
import os
import sys

# ---- VBS content (pure English comments to avoid WSH UTF-8/ANSI 800A0400) ----
VBS_CONTENT = r'''Option Explicit
' ============================================================
' DingTalk Auto-Reply Launcher -- Login Autostart + Crash Watchdog
' Double-click to start; copy to Startup folder for auto-launch.
' Portable: all paths derived from the current user profile (~/.workbuddy),
'   no hardcoded username -- works on any machine with WorkBuddy.
' Watchdog logic:
'   1) Monitor process missing -> launch immediately;
'   2) Process exists but debug log not updated for MAX_STALE_SEC
'      -> stuck (e.g. dws child hung / silent spin) -> kill + relaunch next cycle.
' ============================================================

Dim objShell, objFSO
Dim PROFILE, HOME_WB, SKILL_DIR, PY, PY_CMD, LOG, MAX_STALE_SEC, sCmd

' 单个 WScript.Shell 实例（ExpandEnvironmentStrings / SpecialFolders / Run / CurrentDirectory 全用它）
Set objShell = CreateObject("WScript.Shell")
Set objFSO  = CreateObject("Scripting.FileSystemObject")

' Current user profile root -- use %USERPROFILE% env-var expansion
'   (SpecialFolders("Profile") can return EMPTY in some WSH contexts,
'    e.g. double-clicked from Explorer or launched by task scheduler)
PROFILE  = objShell.ExpandEnvironmentStrings("%USERPROFILE%")
If PROFILE = "%USERPROFILE%" Or PROFILE = "" Then
    ' Fallback: try SpecialFolders
    PROFILE  = objShell.SpecialFolders("Profile")
End If
If PROFILE = "" Or Right(PROFILE, 1) = "\" Then
    ' Last resort: hardcode common pattern
    PROFILE = objShell.ExpandEnvironmentStrings("%HOMEDRIVE%%HOMEPATH%")
End If
HOME_WB  = PROFILE & "\.workbuddy"
SKILL_DIR = HOME_WB & "\skills\dingtalk-auto-reply"

' WorkBuddy managed python venv + skill script (auto-detected, no hardcoded path)
PY     = HOME_WB & "\binaries\python\envs\default\Scripts\python.exe"
PY_CMD = SKILL_DIR & "\dingtalk_unread_monitor.py"
LOG    = HOME_WB & "\dingtalk_auto_debug.log"
MAX_STALE_SEC = 180   ' log stale > 180s = monitor stuck, kill + restart

' Run with the skill dir as CWD so .env resolves even if launched elsewhere
On Error Resume Next
objShell.CurrentDirectory = SKILL_DIR
On Error GoTo 0

Function IsRunning(img, cmdpart)
    Dim p, col, found
    found = False
    On Error Resume Next
    Set col = GetObject("winmgmts:").ExecQuery("SELECT * FROM Win32_Process WHERE Name='" & img & "'")
    If Err.Number = 0 Then
        For Each p In col
            If InStr(p.CommandLine, cmdpart) > 0 Then found = True : Exit For
        Next
    End If
    On Error GoTo 0
    IsRunning = found
End Function

Sub KillByCmd(img, cmdpart)
    Dim p, col
    On Error Resume Next
    Set col = GetObject("winmgmts:").ExecQuery("SELECT * FROM Win32_Process WHERE Name='" & img & "'")
    If Err.Number = 0 Then
        For Each p In col
            If InStr(p.CommandLine, cmdpart) > 0 Then p.Terminate(0)
        Next
    End If
    On Error GoTo 0
End Sub

Function LogStale()
    Dim f, sec
    LogStale = False
    On Error Resume Next
    If objFSO.FileExists(LOG) Then
        Set f = objFSO.GetFile(LOG)
        sec = DateDiff("s", f.DateLastModified, Now)
        If sec > MAX_STALE_SEC Then LogStale = True
    End If
    On Error GoTo 0
End Function

Do
    If Not IsRunning("python.exe", PY_CMD) Then
        ' --- pre-flight checks: verify all required files exist ---
        Dim missing, diag
        missing = ""
        diag = "PROFILE=" & PROFILE & vbNewLine
        diag = diag & "HOME_WB=" & HOME_WB & vbNewLine
        diag = diag & "SKILL_DIR=" & SKILL_DIR & vbNewLine
        diag = diag & "PY=" & PY & vbNewLine
        diag = diag & "PY_CMD=" & PY_CMD & vbNewLine
        If Not objFSO.FileExists(PY) Then missing = missing & "PY(python) " End If
        If Not objFSO.FileExists(PY_CMD) Then missing = missing & "PY_CMD(monitor) " End If
        If Not objFSO.FolderExists(HOME_WB) Then missing = missing & "HOME_WB " End If
        If Not objFSO.FolderExists(SKILL_DIR) Then missing = missing & "SKILL_DIR " End If
        If missing <> "" Then
            MsgBox "DingTalk launcher MISSING FILES:" & vbNewLine & missing & vbNewLine & vbNewLine & diag, 16, "DingTalk Launcher Error"
            WScript.Quit
        End If
        ' --- launch monitor as a HIDDEN window ---
        ' Window style 0 = SW_HIDE: no visible console window.
        ' We use python.exe (console subsystem), NOT pythonw.exe (windows
        ' subsystem). Console subsystem is preferred for runtime stability,
        ' clearer debugging, and an invisible window (SW_HIDE == pythonw UX).
        ' The launcher/console choice does NOT affect whether dws works --
        ' that depends solely on dws being on the system PATH (User env var).
        ' (Technical note: dws is a Node-packed binary that drops its stdout
        '  pipe asynchronously on exit, so a PIPE read returns empty. This
        '  happens under BOTH python.exe and pythonw -- the pythonw-console
        '  theory was disproven by a reboot test on 2026-07-15. The monitor
        '  works around it by redirecting dws stdout to a temp FILE, so the
        '  pipe issue is fully handled in Python regardless of launcher.)
        On Error Resume Next
        sCmd = Chr(34) & PY & Chr(34) & " " & Chr(34) & PY_CMD & Chr(34)
        objShell.Run sCmd, 0, False
        If Err.Number <> 0 Then
            MsgBox "DingTalk launcher Run FAILED:" & vbNewLine & _
                   "Error " & Err.Number & ": " & Err.Description & vbNewLine & vbNewLine & _
                   "Command: " & sCmd, 16, "DingTalk Launcher Error"
            WScript.Quit
        End If
        On Error GoTo 0
    Else
        ' Process alive but log stale = stuck (silent spin) -> force restart
        If LogStale() Then
            KillByCmd "python.exe", PY_CMD
        End If
    End If
    WScript.Sleep 30000
Loop
'''


def startup_dir():
    """Return the Windows Startup folder path (per-user, interactive session)."""
    appdata = os.environ.get("APPDATA")
    if appdata:
        return os.path.join(
            appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )
    # Fallback via ctypes SHGetFolderPathW(CSIDL_STARTUP = 0x0007)
    try:
        import ctypes

        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0007, None, 0, buf)
        return buf.value
    except Exception:
        return os.path.expanduser(
            "~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        )


def ensure_dws_on_path():
    """把 dws / node 所在目录追加到当前用户的 PATH（HKCU\\Environment），
    让任何交互式会话（含本启动器拉起的 python）都能直接敲出 `dws`。
    幂等：已包含则跳过；写后广播 WM_SETTINGCHANGE 让当前会话立即生效（无需重登）。

    背景（2026-07-15 排查石锤）：dws 不在系统 PATH 上时，终端/进程
    都找不到 dws —— 这正是「后台/开机自启实例 unread_now 恒为 0」的
    真实根因（与窗口样式无关）。本函数把 dws 固化进 PATH，从根上消除。

    注：监控脚本本体走绝对路径 NODE+DWS_ENTRY，本函数主要为了让用户
    能手动用 dws、并保证 DWS_CMD 兜底路径可达。"""
    if not sys.platform.startswith("win"):
        return False
    home = os.path.expanduser("~")
    dws_dir = os.path.join(home, ".workbuddy", "binaries", "node", "cli-connector-packages")
    node_dir = os.path.join(home, ".workbuddy", "binaries", "node")
    targets = [d for d in (dws_dir, node_dir) if os.path.isdir(d)]
    if not targets:
        return False
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0,
                              winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            cur, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            cur = ""
        cur = cur if isinstance(cur, str) else ""
        cur_dirs = [p.strip().rstrip("\\").lower() for p in cur.split(";") if p.strip()]
        to_add = [t for t in targets if t.rstrip("\\").lower() not in cur_dirs]
        if not to_add:
            winreg.CloseKey(key)
            return False  # 已在 PATH，无需改动
        new_path = (cur.rstrip(";") + ";" + ";".join(to_add)) if cur.strip() else ";".join(to_add)
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        # 广播环境变更，让已打开的会话立即刷新 PATH（无需重登）
        try:
            import ctypes
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, None)
        except Exception:
            pass
        print("[gen_launcher] 已把 dws/node 目录追加到用户 PATH（HKCU\\Environment），新会话可直接用 dws")
        return True
    except Exception as e:
        print(f"[gen_launcher] PATH 追加失败（需手动加 dws 目录到用户 PATH）：{e}")
        return False


def ensure_launcher(force=False):
    """Create the Startup VBS if missing. Returns (path, created_bool).

    Written as **plain ASCII** (all comments are English; avoids WSH
    800A0400 'missing statement' from UTF-8 Chinese, and avoids
    rare 80070003 'path not found' from some UTF-16 edge cases).
    """
    dst = os.path.join(startup_dir(), "dingtalk_auto_reply_launcher.vbs")
    if os.path.exists(dst) and not force:
        return dst, False
    # Plain ASCII — zero encoding risk for Windows Script Host
    with open(dst, "w", encoding="ascii") as f:
        f.write(VBS_CONTENT)
    # 顺带确保 dws/node 在用户 PATH 上（今天排查的根因：PATH 缺失致 dws 找不到）
    ensure_dws_on_path()
    return dst, True


def main():
    added = ensure_dws_on_path()
    if not added:
        print("[gen_launcher] dws/node 已在用户 PATH 中（无需改动）")
    dst, created = ensure_launcher()
    if created:
        print("[gen_launcher] created: " + dst)
    else:
        print("[gen_launcher] already exists: " + dst)
    print(
        "[gen_launcher] next Windows login will auto-start the DingTalk auto-reply monitor."
    )


if __name__ == "__main__":
    main()
