# Start only the bundled overlay, with typed arguments (no caller-supplied code).
param(
  [Parameter(Mandatory=$true)][string]$Dir,
  [ValidateRange(1,3600)][int]$IdleSeconds=120,
  [ValidateRange(1,3600)][int]$LockIdleSeconds=8,
  [switch]$VisibleInCapture
)
$ErrorActionPreference='Stop'
if (Test-Path (Join-Path $Dir 'stop.flag')) { Write-Output 'STOPPED_BY_USER'; exit 3 }
$scriptPath=Join-Path $PSScriptRoot 'overlay.ps1'
# Windows paths cannot contain double quotes; quote paths for Start-Process argument joining.
if ($Dir.Contains('"') -or $scriptPath.Contains('"')) { throw 'Invalid path' }
$argsList=@('-NoProfile','-STA','-File',('"'+$scriptPath+'"'),'-Dir',('"'+$Dir+'"'),'-IdleSeconds',$IdleSeconds,'-LockIdleSeconds',$LockIdleSeconds)
if ($VisibleInCapture) { $argsList += '-VisibleInCapture' }
Start-Process -WindowStyle Hidden -FilePath (Join-Path $PSHOME 'powershell.exe') -ArgumentList $argsList
