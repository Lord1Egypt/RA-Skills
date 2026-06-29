param(
  [string]$WorkspacePath = ".",
  [string]$CheckerPath = "",
  [string]$LoopCommand = "",
  [int]$MaxLoops = 20,
  [int]$PollDelaySeconds = 0,
  [switch]$NoStrict,
  [string]$RunnerLogPath = ""
)

$ErrorActionPreference = "Stop"

function Resolve-Workspace {
  param([string]$Path)
  try {
    return (Resolve-Path -LiteralPath $Path).Path
  } catch {
    throw "WorkspacePath not found: $Path"
  }
}

function Resolve-Checker {
  param(
    [string]$CheckerPath
  )

  if ($CheckerPath) {
    if (Test-Path -LiteralPath $CheckerPath -PathType Leaf) {
      return (Resolve-Path -LiteralPath $CheckerPath).Path
    }
    throw "CheckerPath not found: $CheckerPath"
  }

  $defaultChecker = Join-Path (Split-Path -Parent $PSScriptRoot) "agent-loop-check.ps1"
  if (Test-Path -LiteralPath $defaultChecker -PathType Leaf) {
    return (Resolve-Path -LiteralPath $defaultChecker).Path
  }

  throw "No checker found. Set -CheckerPath to a valid scripts\\agent-loop-check.ps1."
}

function Normalize-Status {
  param([string]$Status)
  switch -Regex ($Status.Trim()) {
    '^Continue$' { "Continue"; break }
    '^Done with Risk$' { "Done with Risk"; break }
    '^Done$' { "Done"; break }
    '^Blocked$' { "Blocked"; break }
    '^Invalid State$' { "Invalid State"; break }
    default { "Invalid State" }
  }
}

function Write-RunnerLog {
  param(
    [string]$RunnerLogPath,
    [hashtable]$Record
  )
  try {
    $json = [pscustomobject]$Record | ConvertTo-Json -Depth 8 -Compress
    Add-Content -LiteralPath $RunnerLogPath -Value $json -Encoding UTF8
  } catch {
    Write-Warning "Failed to write runner log: $($_.Exception.Message)"
  }
}

function Run-Checker {
  param(
    [string]$CheckerPath,
    [string]$WorkspacePath,
  [bool]$Strict
  )

  $args = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $CheckerPath, "-WorkspacePath", $WorkspacePath, "-Json")
  if ($Strict) {
    $args += "-Strict"
  }
  $raw = & powershell @args 2>&1
  if ($LASTEXITCODE -is [int]) {
    $exitCode = $LASTEXITCODE
  } else {
    $exitCode = 0
  }
  $text = if ($raw -is [string]) { $raw } else { ($raw | Out-String).Trim() }
  $result = $null
  try {
    $result = $text | ConvertFrom-Json
  } catch {
    $result = $null
  }

  return [pscustomobject]@{
    ExitCode = $exitCode
    Raw = $text
    Json = $result
  }
}

function Run-OneLoop {
  param(
    [string]$WorkspacePath,
    [string]$LoopCommand
  )

  $command = $LoopCommand.Trim()
  if ([string]::IsNullOrWhiteSpace($command)) {
    return [pscustomobject]@{
      ExitCode = 2
      Command = ""
      Raw = "LoopCommand is empty"
    }
  }

  $startTime = Get-Date
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = "powershell.exe"
  $psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command $command"
  $psi.WorkingDirectory = $WorkspacePath
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true

  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $psi
  $null = $process.Start()
  $stdout = $process.StandardOutput.ReadToEnd()
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()
  $exitCode = $process.ExitCode

  return [pscustomobject]@{
    ExitCode = $exitCode
    Command = $command
    StartedAt = $startTime.ToString("o")
    FinishedAt = (Get-Date).ToString("o")
    DurationMs = [int]((Get-Date) - $startTime).TotalMilliseconds
    Raw = ($stdout + "`n" + $stderr).Trim()
  }
}

$workspace = Resolve-Workspace $WorkspacePath
$checker = Resolve-Checker -CheckerPath $CheckerPath

$runnerLog = if ([string]::IsNullOrWhiteSpace($RunnerLogPath)) {
  Join-Path $workspace "Docs\RUNNER_LOG.jsonl"
} else {
  $RunnerLogPath
}
$runnerLogDir = Split-Path -Parent $runnerLog
if (-not (Test-Path -LiteralPath $runnerLogDir -PathType Container)) {
  New-Item -ItemType Directory -Path $runnerLogDir -Force | Out-Null
}
$strictMode = -not $NoStrict.IsPresent

$loopIndex = 0

while ($loopIndex -lt $MaxLoops) {
  $loopIndex++

  $checkerResult = Run-Checker -CheckerPath $checker -WorkspacePath $workspace -Strict $strictMode
  $status = "Invalid State"
  $checkerStatus = ""
  $checkerWarnings = @()
  $checkerIssues = @()

  if ($checkerResult.Json -ne $null) {
    $checkerStatus = [string]$checkerResult.Json.status
    if ([string]::IsNullOrWhiteSpace($checkerStatus)) {
      $status = "Invalid State"
    } else {
      $status = Normalize-Status $checkerStatus
    }
    $checkerWarnings = @($checkerResult.Json.warnings)
    $checkerIssues = @($checkerResult.Json.issues)
  } else {
    $status = "Invalid State"
  }

  $checkEvent = @{
    timestamp = (Get-Date).ToString("o")
    event = "runner_check"
    loop = $loopIndex
    workspace = $workspace
    checker_status = $status
    checker_exit_code = $checkerResult.ExitCode
    strict_mode = $strictMode
    checker_warnings = $checkerWarnings
    checker_issues = $checkerIssues
    checker_raw = $checkerResult.Raw
  }
  Write-RunnerLog -RunnerLogPath $runnerLog -Record $checkEvent

  switch ($status) {
    "Continue" {
      Write-Output "Loop ${loopIndex}: checker=${status}. Start one-loop command."
      $loopRun = Run-OneLoop -WorkspacePath $workspace -LoopCommand $LoopCommand
      $loopEvent = @{
        timestamp = (Get-Date).ToString("o")
        event = "runner_loop_command"
        loop = $loopIndex
        workspace = $workspace
        command = $loopRun.Command
        exit_code = [int]$loopRun.ExitCode
        started_at = $loopRun.StartedAt
        finished_at = $loopRun.FinishedAt
        duration_ms = [int]$loopRun.DurationMs
        output = if ([string]::IsNullOrWhiteSpace($loopRun.Raw)) { "<empty>" } else { $loopRun.Raw.Substring(0, [Math]::Min(1000, $loopRun.Raw.Length)) }
      }
      Write-RunnerLog -RunnerLogPath $runnerLog -Record $loopEvent

      if ($loopRun.ExitCode -ne 0) {
        $stopEvent = @{
          timestamp = (Get-Date).ToString("o")
          event = "runner_stop"
          reason = "loop_command_failed"
          loop = $loopIndex
          workspace = $workspace
          status = "Blocked"
          details = "loop command exitCode=$($loopRun.ExitCode)"
        }
        Write-RunnerLog -RunnerLogPath $runnerLog -Record $stopEvent
        Write-Output "Stop: loop command failed. ExitCode=$($loopRun.ExitCode)"
        exit 4
      }

      if ($PollDelaySeconds -gt 0) {
        Start-Sleep -Seconds $PollDelaySeconds
      }
      continue
    }
    "Done" {
      $doneEvent = @{
        timestamp = (Get-Date).ToString("o")
        event = "runner_stop"
        loop = $loopIndex
        workspace = $workspace
        status = "Done"
        reason = "Checker returned Done."
      }
      Write-RunnerLog -RunnerLogPath $runnerLog -Record $doneEvent
      Write-Output "Stop: Done"
      exit 0
    }
    "Done with Risk" {
      $riskEvent = @{
        timestamp = (Get-Date).ToString("o")
        event = "runner_stop"
        loop = $loopIndex
        workspace = $workspace
        status = "Done with Risk"
        reason = "Checker returned Done with Risk."
      }
      Write-RunnerLog -RunnerLogPath $runnerLog -Record $riskEvent
      Write-Output "Stop: Done with Risk"
      exit 0
    }
    "Blocked" {
      $blockEvent = @{
        timestamp = (Get-Date).ToString("o")
        event = "runner_stop"
        loop = $loopIndex
        workspace = $workspace
        status = "Blocked"
        reason = "Checker returned Blocked."
      }
      Write-RunnerLog -RunnerLogPath $runnerLog -Record $blockEvent
      Write-Output "Stop: Blocked"
      exit 3
    }
    default {
      $invalidEvent = @{
        timestamp = (Get-Date).ToString("o")
        event = "runner_stop"
        loop = $loopIndex
        workspace = $workspace
        status = "Invalid State"
        reason = "Checker returned $status"
        checker_raw = $checkerResult.Raw
      }
      Write-RunnerLog -RunnerLogPath $runnerLog -Record $invalidEvent
      Write-Output "Stop: Invalid State"
      exit 2
    }
  }
}

$budgetEvent = @{
  timestamp = (Get-Date).ToString("o")
  event = "runner_stop"
  loop = $loopIndex
  workspace = $workspace
  status = "BudgetExhausted"
  reason = "max loops reached"
  max_loops = $MaxLoops
}
Write-RunnerLog -RunnerLogPath $runnerLog -Record $budgetEvent
Write-Output "Stop: budget exhausted ($MaxLoops loops)."
exit 5
