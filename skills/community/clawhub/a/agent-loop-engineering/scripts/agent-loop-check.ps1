param(
  [string]$WorkspacePath = ".",
  [switch]$Json,
  [switch]$Strict
)

$ErrorActionPreference = "Stop"
$checkerVersion = "0.2.0"

$allowedStatuses = @(
  "Continue",
  "Done",
  "Done with Risk",
  "Blocked",
  "Invalid State"
)

$allowedScenarioGuesses = @(
  "Small",
  "Medium",
  "Large",
  "Product",
  "Unknown"
)

$allowedCheckerResults = @(
  "Continue",
  "Done",
  "Done with Risk",
  "Blocked",
  "Invalid State",
  "Not run"
)

$allowedVerificationKinds = @(
  "automatic",
  "functional",
  "other"
)

$codeExtensions = @(
  ".astro", ".c", ".cc", ".cpp", ".cs", ".css", ".go", ".h", ".hpp",
  ".html", ".java", ".js", ".jsx", ".kt", ".mjs", ".php", ".ps1",
  ".py", ".rb", ".rs", ".scss", ".sh", ".sql", ".svelte", ".swift",
  ".ts", ".tsx", ".vue"
)

$excludedDirectoryNames = @(
  ".git", ".hg", ".svn", ".next", ".nuxt", ".turbo", ".venv", "venv",
  "node_modules", "dist", "build", "coverage", "target", "vendor",
  "__pycache__", ".cache", ".pytest_cache", ".mypy_cache"
)

function Resolve-WorkspacePath {
  param([string]$Path)
  try {
    return (Resolve-Path -LiteralPath $Path).Path
  } catch {
    Write-Result "Invalid State" @("Workspace path does not exist: $Path") @() 2 $null $null
    exit 2
  }
}

function Get-FileText {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    return $null
  }
  return Get-Content -LiteralPath $Path -Raw -Encoding UTF8
}

function Test-MeaningfulText {
  param([string]$Text)
  if ([string]::IsNullOrWhiteSpace($Text)) {
    return $false
  }

  $meaningful = $Text -split "`r?`n" | Where-Object {
    $line = $_.Trim()
    $line -and
      -not $line.StartsWith("<!--") -and
      -not $line.StartsWith("-->") -and
      -not ($line -match "^#+\s+") -and
      -not ($line -match "^Use this file") -and
      -not ($line -match "^Choose one:") -and
      -not ($line -match "^One clear sentence") -and
      -not ($line -match "^List ") -and
      -not ($line -match "^Example:")
  }

  return @($meaningful).Count -gt 0
}

function Get-MarkdownSection {
  param(
    [string]$Text,
    [string]$Heading
  )

  if ([string]::IsNullOrWhiteSpace($Text)) {
    return ""
  }

  $pattern = "(?ms)^##\s+$([regex]::Escape($Heading))\s*$\s*(.*?)(?=^##\s+|\z)"
  $match = [regex]::Match($Text, $pattern)
  if (-not $match.Success) {
    return ""
  }
  return $match.Groups[1].Value.Trim()
}

function Get-MeaningfulLines {
  param([string]$Text)
  if ([string]::IsNullOrWhiteSpace($Text)) {
    return @()
  }

  return @($Text -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object {
    $_ -and
      -not $_.StartsWith("<!--") -and
      -not $_.StartsWith("-->") -and
      -not ($_ -eq "None") -and
      -not ($_ -eq "-") -and
      -not ($_ -eq "- [ ]") -and
      -not ($_ -match "^(Command|Result|Functional check|Logs / screenshots / files|Reason):\s*$")
  })
}

function Test-LoopLog {
  param([string]$Path)
  $lineNumber = 0
  $records = New-Object System.Collections.Generic.List[object]
  $scenarioGuesses = New-Object System.Collections.Generic.HashSet[string]
  $successfulAutomatic = 0
  $successfulFunctional = 0
  $successfulVerification = 0
  $failedVerification = 0
  $missingVerifiedAt = 0
  $verificationErrors = New-Object System.Collections.Generic.List[string]
  foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
    $lineNumber += 1
    if ([string]::IsNullOrWhiteSpace($line)) {
      continue
    }
    try {
      $record = $line | ConvertFrom-Json
    } catch {
      return [pscustomobject]@{
        error = "Invalid JSON on line $lineNumber"
        records = $records
        scenarioGuesses = @($scenarioGuesses)
      }
    }

    foreach ($field in @("timestamp", "event", "scenario_guess", "skill_used")) {
      if (-not $record.PSObject.Properties[$field] -or [string]::IsNullOrWhiteSpace([string]$record.$field)) {
        return [pscustomobject]@{
          error = "Missing required field '$field' on line $lineNumber"
          records = $records
          scenarioGuesses = @($scenarioGuesses)
        }
      }
    }

    if ($allowedScenarioGuesses -notcontains $record.scenario_guess) {
      return [pscustomobject]@{
        error = "Invalid scenario_guess '$($record.scenario_guess)' on line $lineNumber"
        records = $records
        scenarioGuesses = @($scenarioGuesses)
      }
    }

    if ($record.PSObject.Properties["checker_result"] -and
      -not [string]::IsNullOrWhiteSpace([string]$record.checker_result) -and
      $allowedCheckerResults -notcontains $record.checker_result) {
      return [pscustomobject]@{
        error = "Invalid checker_result '$($record.checker_result)' on line $lineNumber"
        records = $records
        scenarioGuesses = @($scenarioGuesses)
      }
    }

    if ($record.PSObject.Properties["verification_commands"] -and $null -ne $record.verification_commands) {
      foreach ($verificationCommand in @($record.verification_commands)) {
        $kind = [string]$verificationCommand.kind
        $command = [string]$verificationCommand.command
        $hasExitCode = $verificationCommand.PSObject.Properties["exit_code"]
        $exitCodeText = [string]$verificationCommand.exit_code
        $verifiedAt = if ($verificationCommand.PSObject.Properties["verified_at"]) {
          [string]$verificationCommand.verified_at
        } elseif ($record.PSObject.Properties["verified_at"]) {
          [string]$record.verified_at
        } else {
          ""
        }

        if ([string]::IsNullOrWhiteSpace($kind)) {
          $kind = "other"
        }

        if ($allowedVerificationKinds -notcontains $kind) {
          $verificationErrors.Add("Invalid verification kind '$kind' on line $lineNumber") | Out-Null
          continue
        }

        if ([string]::IsNullOrWhiteSpace($command)) {
          $verificationErrors.Add("Missing verification command on line $lineNumber") | Out-Null
          continue
        }

        if (-not $hasExitCode -or -not ($exitCodeText -match "^-?\d+$")) {
          $verificationErrors.Add("Missing numeric exit_code for verification command '$command' on line $lineNumber") | Out-Null
          continue
        }

        if ([string]::IsNullOrWhiteSpace($verifiedAt)) {
          $missingVerifiedAt += 1
        }

        if ([int]$verificationCommand.exit_code -eq 0) {
          $successfulVerification += 1
          if ($kind -eq "automatic") {
            $successfulAutomatic += 1
          }
          if ($kind -eq "functional") {
            $successfulFunctional += 1
          }
        } else {
          $failedVerification += 1
        }
      }
    }

    $null = $scenarioGuesses.Add([string]$record.scenario_guess)
    $records.Add($record) | Out-Null
  }
  return [pscustomobject]@{
    error = $null
    records = $records
    scenarioGuesses = @($scenarioGuesses)
    successfulVerification = $successfulVerification
    successfulAutomatic = $successfulAutomatic
    successfulFunctional = $successfulFunctional
    failedVerification = $failedVerification
    missingVerifiedAt = $missingVerifiedAt
    verificationErrors = @($verificationErrors)
  }
}

function Get-CodeSizeInfo {
  param([string]$Workspace)

  $files = New-Object System.Collections.Generic.List[System.IO.FileInfo]

  foreach ($file in Get-ChildItem -LiteralPath $Workspace -Recurse -File -Force -ErrorAction SilentlyContinue) {
    $relative = $file.FullName.Substring($Workspace.Length).TrimStart("\", "/")
    $parts = $relative -split "[\\/]+"
    $isExcluded = $false
    foreach ($part in $parts) {
      if ($excludedDirectoryNames -contains $part) {
        $isExcluded = $true
        break
      }
    }
    if ($isExcluded) {
      continue
    }
    if ($relative.StartsWith("Docs\")) {
      continue
    }
    if ($codeExtensions -contains $file.Extension.ToLowerInvariant()) {
      $files.Add($file) | Out-Null
    }
  }

  $lineCount = 0
  foreach ($file in $files) {
    try {
      $lineCount += @(Get-Content -LiteralPath $file.FullName -Encoding UTF8 -ErrorAction Stop).Count
    } catch {
      try {
        $lineCount += @(Get-Content -LiteralPath $file.FullName -ErrorAction Stop).Count
      } catch {
        # Ignore unreadable files in size estimation.
      }
    }
  }

  $codeFileCount = $files.Count
  $sizeClass = "Small"
  if ($codeFileCount -gt 500 -or $lineCount -gt 100000) {
    $sizeClass = "Product"
  } elseif ($codeFileCount -gt 100 -or $lineCount -gt 20000) {
    $sizeClass = "Large"
  } elseif ($codeFileCount -gt 20 -or $lineCount -gt 3000) {
    $sizeClass = "Medium"
  }

  $changedFileCount = $null
  $gitPath = Join-Path $Workspace ".git"
  if (Test-Path -LiteralPath $gitPath) {
    try {
      $gitOutput = & git -C $Workspace status --short 2>$null
      $changedFileCount = @($gitOutput | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count
    } catch {
      $changedFileCount = $null
    }
  }

  return [pscustomobject]@{
    sizeClass = $sizeClass
    codeFileCount = $codeFileCount
    codeLineCount = $lineCount
    changedFileCount = $changedFileCount
  }
}

function Write-Result {
  param(
    [string]$Status,
    [string[]]$Issues,
    [string[]]$Warnings,
    [int]$ExitCode,
    [object]$CodeSize,
    [object]$LogInfo
  )

  if ($Json) {
    [pscustomobject]@{
      checkerVersion = $checkerVersion
      status = $Status
      issues = $Issues
      warnings = $Warnings
      strict = [bool]$Strict
      codeSize = $CodeSize
      log = $LogInfo
      exitCode = $ExitCode
    } | ConvertTo-Json -Depth 4
  } else {
    Write-Output $Status
    if ($CodeSize) {
      $changed = if ($null -eq $CodeSize.changedFileCount) { "unknown" } else { $CodeSize.changedFileCount }
      Write-Output "Code Size: $($CodeSize.sizeClass) ($($CodeSize.codeFileCount) code files, $($CodeSize.codeLineCount) lines, $changed changed files)"
    }
    if ($LogInfo) {
      $scenarios = if ($LogInfo.scenarioGuesses.Count -gt 0) { ($LogInfo.scenarioGuesses -join ", ") } else { "None" }
      Write-Output "Loop Log: $($LogInfo.recordCount) records, scenario_guess: $scenarios"
    }
    if ($Warnings.Count -gt 0) {
      Write-Output "Warnings:"
      foreach ($warning in $Warnings) {
        Write-Output "- $warning"
      }
    }
    if ($Issues.Count -gt 0) {
      Write-Output "Issues:"
      foreach ($issue in $Issues) {
        Write-Output "- $issue"
      }
    }
  }
}

$workspace = Resolve-WorkspacePath $WorkspacePath
$codeSize = Get-CodeSizeInfo $workspace
$logInfo = $null
$docsPath = Join-Path $workspace "Docs"
$targetPath = Join-Path $docsPath "TARGET.md"
$acceptancePath = Join-Path $docsPath "ACCEPTANCE.md"
$loopStatePath = Join-Path $docsPath "LOOP_STATE.md"
$loopLogPath = Join-Path $docsPath "LOOP_LOG.jsonl"

$issues = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

if (-not (Test-Path -LiteralPath $docsPath -PathType Container)) {
  $issues.Add("Docs directory is missing")
  Write-Result "Invalid State" $issues.ToArray() $warnings.ToArray() 2 $codeSize $logInfo
  exit 2
}

$targetText = Get-FileText $targetPath
$acceptanceText = Get-FileText $acceptancePath
$loopStateText = Get-FileText $loopStatePath
$loopLogText = Get-FileText $loopLogPath

if (-not (Test-MeaningfulText $targetText)) {
  $issues.Add("TARGET.md is missing or empty")
}

if (-not (Test-MeaningfulText $acceptanceText)) {
  $issues.Add("ACCEPTANCE.md is missing or empty")
}

if (-not (Test-MeaningfulText $loopStateText)) {
  $issues.Add("LOOP_STATE.md is missing or empty")
}

if (-not (Test-MeaningfulText $loopLogText)) {
  $issues.Add("LOOP_LOG.jsonl is missing or empty in test mode")
} elseif (Test-Path -LiteralPath $loopLogPath -PathType Leaf) {
  $loopLogResult = Test-LoopLog $loopLogPath
  $logInfo = [pscustomobject]@{
    recordCount = $loopLogResult.records.Count
    scenarioGuesses = @($loopLogResult.scenarioGuesses)
    successfulVerification = $loopLogResult.successfulVerification
    successfulAutomatic = $loopLogResult.successfulAutomatic
    successfulFunctional = $loopLogResult.successfulFunctional
    failedVerification = $loopLogResult.failedVerification
    missingVerifiedAt = $loopLogResult.missingVerifiedAt
  }
  if ($loopLogResult.error) {
    $issues.Add("LOOP_LOG.jsonl is not valid: $($loopLogResult.error)")
  }
  foreach ($verificationError in @($loopLogResult.verificationErrors)) {
    $issues.Add("LOOP_LOG.jsonl verification evidence is not valid: $verificationError")
  }
}

if ($issues.Count -gt 0) {
  Write-Result "Invalid State" $issues.ToArray() $warnings.ToArray() 2 $codeSize $logInfo
  exit 2
}

$goalSection = Get-MarkdownSection $targetText "Goal"
$mustPassSection = Get-MarkdownSection $acceptanceText "Must Pass"

if ((Get-MeaningfulLines $goalSection).Count -eq 0) {
  $issues.Add("TARGET.md Goal is missing")
}

if ((Get-MeaningfulLines $mustPassSection).Count -eq 0) {
  $issues.Add("ACCEPTANCE.md Must Pass is missing")
}

$statusSection = Get-MarkdownSection $loopStateText "Status"
$status = (Get-MeaningfulLines $statusSection | Select-Object -First 1)

if (-not $status) {
  $issues.Add("LOOP_STATE.md Status is missing")
} elseif ($allowedStatuses -notcontains $status) {
  $issues.Add("LOOP_STATE.md Status is not allowed: $status")
}

$evidenceSection = Get-MarkdownSection $loopStateText "Evidence"
$failedChecksSection = Get-MarkdownSection $loopStateText "Failed Checks"
$nextActionSection = Get-MarkdownSection $loopStateText "Next Action"
$stopRuleSection = Get-MarkdownSection $loopStateText "Stop Rule Triggered"

$evidenceLines = Get-MeaningfulLines $evidenceSection
$failedCheckLines = Get-MeaningfulLines $failedChecksSection
$nextActionLines = Get-MeaningfulLines $nextActionSection
$stopRuleLines = Get-MeaningfulLines $stopRuleSection

$stopRuleYes = $false
foreach ($line in $stopRuleLines) {
  if ($line -match "^Yes$") {
    $stopRuleYes = $true
  }
}

$stopReasonLines = @($stopRuleLines | Where-Object {
  $_ -ne "Yes" -and $_ -ne "No" -and -not ($_ -match "^Reason:\s*$") -and -not ($_ -match "^Reason:\s*None$")
})

if ($status -eq "Done") {
  if ($evidenceLines.Count -eq 0) {
    $issues.Add("Status is Done but Evidence is empty")
  }
  if ($failedCheckLines.Count -gt 0) {
    $issues.Add("Status is Done but Failed Checks is not empty")
  }
  if ($Strict) {
    if (-not $logInfo -or $logInfo.successfulVerification -lt 1) {
      $issues.Add("Strict mode: Status is Done but no successful verification command is recorded in LOOP_LOG.jsonl")
    }
    if (-not $logInfo -or $logInfo.successfulAutomatic -lt 1) {
      $issues.Add("Strict mode: Status is Done but no successful automatic verification is recorded")
    }
    if (-not $logInfo -or $logInfo.successfulFunctional -lt 1) {
      $issues.Add("Strict mode: Status is Done but no successful functional verification is recorded")
    }
    if ($logInfo -and $logInfo.missingVerifiedAt -gt 0) {
      $issues.Add("Strict mode: verification command is missing verified_at")
    }
  }
}

if ($status -eq "Continue") {
  if ($nextActionLines.Count -eq 0) {
    $issues.Add("Status is Continue but Next Action is missing")
  } elseif ($nextActionLines.Count -gt 1) {
    $issues.Add("Status is Continue but Next Action has multiple meaningful lines")
  }
}

if ($status -eq "Blocked") {
  $hasReason = ($stopReasonLines.Count -gt 0) -or ($failedCheckLines.Count -gt 0) -or ($nextActionLines.Count -gt 0)
  if (-not $hasReason) {
    $issues.Add("Status is Blocked but no reason is recorded")
  }
}

if ($stopRuleYes -and ($status -eq "Continue" -or $status -eq "Done")) {
  $issues.Add("Stop Rule Triggered is Yes but Status is $status")
}

if ($logInfo -and $logInfo.scenarioGuesses.Count -eq 1) {
  $scenarioGuess = [string]@($logInfo.scenarioGuesses)[0]
  if ($scenarioGuess -ne "Unknown" -and $scenarioGuess -ne $codeSize.sizeClass) {
    $warnings.Add("scenario_guess is $scenarioGuess but code size estimate is $($codeSize.sizeClass); this may be valid when task size differs from repository size") | Out-Null
  }
}

if ($issues.Count -gt 0) {
  Write-Result "Invalid State" $issues.ToArray() $warnings.ToArray() 2 $codeSize $logInfo
  exit 2
}

Write-Result $status @() $warnings.ToArray() 0 $codeSize $logInfo
exit 0
