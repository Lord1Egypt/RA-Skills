' Windowless launcher for keepalive.ps1 (run by Task Scheduler MyLikeFavChromeKeepalive).
' wscript.exe is a GUI-subsystem host, so no console window is ever created;
' Run(..., 0, False) starts powershell fully hidden and does not wait.
Dim sh
Set sh = CreateObject("WScript.Shell")
sh.Run "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""D:\Tools\mylike-fav-import\keepalive.ps1""", 0, False
Set sh = Nothing
