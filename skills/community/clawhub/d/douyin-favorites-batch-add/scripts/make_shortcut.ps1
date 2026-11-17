$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('Desktop')
$lnkPath = Join-Path $desktop '抖音入夹进度.lnk'
$ws = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut($lnkPath)
$lnk.TargetPath = 'D:\Tools\mylike-fav-import\progress.cmd'
$lnk.WorkingDirectory = 'D:\Tools\mylike-fav-import'
$lnk.IconLocation = "$env:SystemRoot\System32\cmd.exe,0"
$lnk.Description = '抖音收藏夹批量入夹进度看板（双击打开，5秒自动刷新）'
$lnk.Save()
$check = $ws.CreateShortcut($lnkPath)
"shortcut=" + $lnkPath
"target=" + $check.TargetPath
"workdir=" + $check.WorkingDirectory
"exists=" + (Test-Path $lnkPath)
