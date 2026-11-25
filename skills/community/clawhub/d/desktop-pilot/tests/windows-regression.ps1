# Real Windows test. Operates a scratch window and isolated temporary state.
# Full-desktop capture is opt-in; it can include other private windows/notifications.
param([switch]$CaptureDesktop)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$ps=Join-Path $PSHOME 'powershell.exe'
$backend=Join-Path $root 'scripts\windows\desktop.ps1'
$overlay=Join-Path $root 'scripts\windows\overlay.ps1'
$launcher=Join-Path $root 'scripts\windows\launch-overlay.ps1'
$originalTemp=$env:TEMP; $originalTmp=$env:TMP
$scratch=Join-Path $originalTemp ('desktop-pilot-test-'+[guid]::NewGuid().ToString('N'))
$state=Join-Path $scratch 'desktop-pilot\overlay'
New-Item -ItemType Directory -Path $state -Force | Out-Null
$flag=Join-Path $state 'stop.flag'
$checks=0; $fixture=$null
function Check($name,$ok) {if(-not $ok){throw "FAIL: $name | backend exit=$script:code | output=$script:lastOutput"};$script:checks++;Write-Output "PASS: $name"}
function Backend([string[]]$arguments) {
  $result=& $ps -NoProfile -ExecutionPolicy Bypass -File $backend @arguments 2>&1
  $script:code=$LASTEXITCODE; $script:lastOutput=($result -join "`n"); return $script:lastOutput
}
try {
  $env:TEMP=$scratch; $env:TMP=$scratch
  # Parse every bundled PowerShell file before executing UI tests.
  Get-ChildItem (Join-Path $root 'scripts\windows') -Filter '*.ps1' | ForEach-Object {
    $tokens=$null;$errors=$null
    [void][Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$tokens,[ref]$errors)
    Check ("parse "+$_.Name) ($errors.Count -eq 0)
  }
  Set-Content $flag 'test cancellation'
  foreach($action in @('windows','type','key','mouse','screenshot')) {
    $out=Backend @($action)
    Check ("direct backend Stop: "+$action) ($code -eq 3 -and $out -match 'STOPPED_BY_USER')
  }
  $out=& $ps -NoProfile -ExecutionPolicy Bypass -File $overlay -Dir $state 2>&1
  Check 'direct overlay preserves Stop' ($LASTEXITCODE -eq 3 -and (Test-Path $flag))
  # Launcher refuses before spawning; no output file needed.
  $out=& $ps -NoProfile -ExecutionPolicy Bypass -File $launcher -Dir $state 2>&1
  Check 'launcher refuses stopped session' ($LASTEXITCODE -ne 0 -and (Test-Path $flag))
  Remove-Item $flag  # test owns this isolated cancellation flag
  $out=& $ps -NoProfile -ExecutionPolicy Bypass -File $overlay -Dir $state -SelfTest 2>&1
  Check 'input-lock decision logic and hooks' ($LASTEXITCODE -eq 0 -and ($out -join '') -match 'SELFTEST PASS')
  # Load only help/definitions in this isolated test process, then exercise handle-less policy.
  . $backend help | Out-Null
  $noHandle=[pscustomobject]@{Current=[pscustomobject]@{NativeWindowHandle=0;ProcessId=$PID}}
  Check 'handle-less target fails closed even with matching process' (-not (Focus-Window $noHandle))
  # Start a dedicated scratch window, never an existing editor or browser.
  $title='Desktop Pilot regression '+[guid]::NewGuid().ToString('N')
  $fixtureScript=Join-Path $PSScriptRoot 'windows-fixture.ps1'
  $fixture=Start-Process $ps -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-STA','-File',('"'+$fixtureScript+'"'),'-WindowTitle',('"'+$title+'"')) -PassThru
  Start-Sleep -Seconds 2
  $out=Backend @('windows');Check 'scratch window listed' ($code -eq 0 -and $out.Contains($title))
  $out=Backend @('buttons','-Title',$title);Check 'scratch button discovered' ($code -eq 0 -and $out.Contains('Audit action'))
  $out=Backend @('focus','-Title',$title);Check 'scratch focus verified' ($code -eq 0 -and $out.Contains('OK focused'))
  $text='Hola '+[char]0x00f1+' '+[char]0x20ac+' '+[char]0x6f22
  $b64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($text))
  $out=Backend @('type','-Title',$title,'-TextB64',$b64);Check 'Unicode typing completed' ($code -eq 0 -and $out.Contains('OK typed'))
  Add-Type -AssemblyName UIAutomationClient,UIAutomationTypes
  $A=[Windows.Automation.AutomationElement];$S=[Windows.Automation.TreeScope]
  $window=$A::RootElement.FindFirst($S::Children,(New-Object Windows.Automation.PropertyCondition($A::NameProperty,$title)))
  $editor=$window.FindFirst($S::Descendants,(New-Object Windows.Automation.PropertyCondition($A::NameProperty,'Audit editor')))
  $value=$editor.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern)
  Check 'Unicode value verified through UIA' ($value.Current.Value -eq $text)
  $out=Backend @('key','-Title',$title,'-Keys','ctrl+a');Check 'targeted key combo' ($code -eq 0)
  $out=Backend @('click','-Title',$title,'-Name','Audit action');Check 'named accessibility click' ($code -eq 0 -and $value.Current.Value -eq 'CLICKED')
  Set-Content $flag 'cancel before input'
  $out=Backend @('type','-Title',$title,'-Text','MUST NOT TYPE')
  Check 'cancelled input leaves scratch text unchanged' ($code -eq 3 -and $value.Current.Value -eq 'CLICKED')
  Remove-Item $flag
  # Observe actual text entry before latching cancellation (not just pre-call rejection).
  $value.SetValue('')
  $watchScript=Join-Path $PSScriptRoot 'windows-cancel-after-typing.ps1'
  $watcher=Start-Process $ps -PassThru -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',('"'+$watchScript+'"'),'-WindowTitle',('"'+$title+'"'),'-StopFile',('"'+$flag+'"'))
  $longText='x'*2000
  $longB64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($longText))
  $out=Backend @('type','-Title',$title,'-TextB64',$longB64)
  [void]$watcher.WaitForExit(25000)
  Check 'Stop interrupts in-flight typing' ($code -eq 3 -and $value.Current.Value.Length -ge 50 -and $value.Current.Value.Length -lt 2000)
  Check 'typing cancellation watcher completed' ($watcher.HasExited -and $watcher.ExitCode -eq 0)
  Remove-Item $flag
  if ($CaptureDesktop) {
    $shot=Join-Path $scratch 'screen.png'
    $out=Backend @('screenshot','-Out',$shot)
    Check 'explicitly opted-in full desktop screenshot' ($code -eq 0 -and (Test-Path $shot) -and (Get-Item $shot).Length -gt 1000)
  } else { Write-Output 'SKIP: full-desktop screenshot (requires explicit -CaptureDesktop)' }
  # Overlay starts without locking physical input, then externally latched Stop closes it.
  & $ps -NoProfile -ExecutionPolicy Bypass -File $launcher -Dir $state -IdleSeconds 10
  Check 'typed overlay launcher' ($LASTEXITCODE -eq 0)
  Start-Sleep -Seconds 2
  $pidPath=Join-Path $state 'pid'
  Check 'native overlay running' (Test-Path $pidPath)
  $overlayPid=[int](Get-Content $pidPath)
  $overlayWindow=$A::RootElement.FindFirst($S::Children,(New-Object Windows.Automation.AndCondition(
    (New-Object Windows.Automation.PropertyCondition($A::ProcessIdProperty,$overlayPid)),
    (New-Object Windows.Automation.PropertyCondition($A::NameProperty,'Desktop Pilot status')))))
  $stopControl=$overlayWindow.FindFirst($S::Descendants,(New-Object Windows.Automation.PropertyCondition($A::NameProperty,'Stop Desktop Pilot')))
  Check 'real Stop button exposed through accessibility' ($null -ne $stopControl)
  $stopControl.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
  Start-Sleep -Seconds 2
  Check 'overlay exits on Stop' (-not (Test-Path $pidPath))
  Check 'Stop survives overlay exit' (Test-Path $flag)
  Write-Output "RESULT: $checks checks passed"
} finally {
  if($fixture -and -not $fixture.HasExited) { [void]$fixture.CloseMainWindow(); $fixture.WaitForExit(3000) | Out-Null }
  # Close only this test's overlay gracefully, including failure paths.
  Set-Content (Join-Path $state 'quit.flag') 'cleanup'
  $env:TEMP=$originalTemp; $env:TMP=$originalTmp
  Start-Sleep -Milliseconds 500
  Remove-Item $scratch -Recurse -Force -ErrorAction SilentlyContinue
}
