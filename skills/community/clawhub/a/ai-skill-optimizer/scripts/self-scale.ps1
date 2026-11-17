<#
========================================================================================
 self-scale.ps1 - Self-scaling evaluator and proposal generator (micro tier)
 Package : ai-company | Version : 1.0.0 | scale_tier : micro
========================================================================================
 Governance model : PROPOSE-ONLY, three-stage architecture (references/scaling.md #1).

 CAN do :
   - read {SKILL_DIR} (read-only)
   - read / update .scaling-state.json (operational records only - the single
     permitted write inside {SKILL_DIR}, per README-FOR-AI.md sec 12.6)
   - collect the four scaling metrics and evaluate thresholds T1-T4
   - generate an upgrade package under {WORKSPACE_ROOT}/.skill-upgrade/<timestamp>/
   - run gates G1-G6 on the generated package (README-FOR-AI.md sec 12.3)
   - write UPGRADE-PROPOSAL.md into the package directory (README-FOR-AI.md sec 12)
   - record the proposal in .scaling-state.json -> pending_proposals

 CANNOT do (hard boundary, README-FOR-AI.md sec 9.5) :
   - write any other file under {SKILL_DIR}
   - modify the permissions block, tests/**, or this script's own gate logic
   - install, apply, or commit anything (no such Action value exists - P36)
   - request additional permissions

 Compatibility : Windows PowerShell 5.1 (no &&, no ternary operator, no ?? operator).
 Paths         : all derived from $PSScriptRoot; no hardcoded absolute user paths (P18).
 Deletion      : no Remove-Item -Recurse -Force pattern anywhere (P23); rejected
                 packages are quarantined by move, not destroyed.
 Line endings  : this script itself is CRLF (.editorconfig [*.ps1]); every .md
                 and .json artifact it writes is normalized to LF (.editorconfig
                 [*] = lf) - see Write-TextFileNoBom.
 Copy policy   : upgrade packages exclude build residues (__pycache__/ and
                 *.pyc) so the file count and gate hashes never depend on
                 environment noise.
========================================================================================
#>

param(
  [ValidateSet('evaluate','propose','report','status')]
  [string]$Action = 'evaluate',      # no install / apply / commit values (P36)
  [switch]$DryRun,                   # only output what would be done, no package
  [switch]$Force                     # propose even when no threshold is hit (SCL_001)
)

$ErrorActionPreference = 'Stop'

# --------------------------------------------------------------------------------------
# Constants and paths (derived from $PSScriptRoot only)
# --------------------------------------------------------------------------------------

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$SkillDir      = Split-Path -Parent $PSScriptRoot        # {SKILL_DIR} (parent of scripts/)
$WorkspaceRoot = Split-Path -Parent $SkillDir            # {WORKSPACE_ROOT}
$StateFile     = Join-Path $SkillDir '.scaling-state.json'
$ConfigFile    = Join-Path $PSScriptRoot 'scaling-config.json'
$DepartmentsDir = Join-Path (Join-Path $SkillDir 'references') 'departments'

# Tier data (R3 audited values). Only the micro -> small edge is implemented by
# this build; any other tier correctly fails with SCL_002 (no mapping defined).
$TierAgentCaps = @{
  'micro' = 3; 'small' = 10; 'medium' = 50; 'large' = 200; 'group' = 200
}
$TierBlockMean = @{ 'micro' = 9.0; 'small' = 3.6; 'medium' = 2.0; 'large' = 1.0; 'group' = 1.0 }
$TargetFileCount = @{ 'small' = 29 }   # 28 spec files + README-FOR-AI.md (package-local
                                      # generation spec, user-approved spec deviation)

# The deterministic micro -> small split mapping (merge tree, README-FOR-AI.md sec 10.1).
# Split order = page order of FB sections inside each legacy D2 file (scaling.md 4.3).
$UpgradeEdge = @{
  From = 'micro'
  To   = 'small'
  NewVersion = '2.0.0'
  OldVersion = '1.0.0'
  ExpectedBlocks = 18
  Split = @(
    @{ Slug = 'governance-and-operations'; Prefix = 'CEO_';  Source = 'governance-and-delivery'; Blocks = 6 },
    @{ Slug = 'quality-and-delivery';      Prefix = 'CQO_';  Source = 'governance-and-delivery'; Blocks = 2 },
    @{ Slug = 'technology-and-platform';   Prefix = 'CTO_';  Source = 'engineering-and-safety';  Blocks = 3 },
    @{ Slug = 'security-and-compliance';   Prefix = 'CISO_'; Source = 'engineering-and-safety';  Blocks = 3 },
    @{ Slug = 'people-and-growth';         Prefix = 'CHO_';  Source = 'engineering-and-safety';  Blocks = 4 }
  )
}

# --------------------------------------------------------------------------------------
# Logging and termination helpers
# --------------------------------------------------------------------------------------

function Write-Log {
  # Uses Write-Host (not Write-Output) so that log lines never pollute the
  # return values of functions whose results are assigned to variables.
  param([string]$Message)
  Write-Host ("{0} [{1}] {2}" -f (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'), $PID, $Message)
}

function Stop-WithCode {
  param([string]$Code, [string]$Message)
  Write-Log "FATAL $Code : $Message"
  Write-Log "Execution stopped. No content file under the skill directory was modified."
  exit 2
}

function Get-UtcNowIso {
  return (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
}

# --------------------------------------------------------------------------------------
# Text / hash helpers
# --------------------------------------------------------------------------------------

function Get-TextSha256 {
  param([string]$Text)
  if ($null -eq $Text) { return '' }
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
    return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
  } finally { $sha.Dispose() }
}

function Read-TextFile {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return $null }
  return [System.IO.File]::ReadAllText($Path)
}

function Write-TextFileNoBom {
  # E15 : every .md / .json artifact written by this script keeps LF line
  # endings (.editorconfig [*] = lf), even though the script itself is CRLF
  # ([*.ps1] = crlf). Here-strings lifted from a CRLF file are normalized.
  param([string]$Path, [string]$Text)
  if ($null -eq $Text) { $Text = '' }
  $normalized = $Text -replace "`r`n", "`n"
  [System.IO.File]::WriteAllText($Path, $normalized, $Utf8NoBom)
}

# --------------------------------------------------------------------------------------
# Configuration (scripts/scaling-config.json, falls back to documented defaults)
# --------------------------------------------------------------------------------------

function Load-Config {
  $cfg = $null
  if (Test-Path -LiteralPath $ConfigFile) {
    try { $cfg = ConvertFrom-Json ([System.IO.File]::ReadAllText($ConfigFile)) }
    catch { Write-Log "WARN scaling-config.json is invalid JSON; using built-in defaults" }
  } else {
    Write-Log "WARN scaling-config.json not found; using built-in defaults"
  }
  $result = @{
    IntervalDays = 30
    AgentHeadroom = 1.0
    BlocksRatio = 1.5
    RoutingFloor = 0.85
    ReuseCeiling = 0.25
    OutputDir = ''
  }
  if ($null -ne $cfg) {
    if ($null -ne $cfg.PSObject.Properties['evaluation_interval_days']) { $result.IntervalDays = [int]$cfg.evaluation_interval_days }
    if ($null -ne $cfg.PSObject.Properties['thresholds']) {
      $t = $cfg.thresholds
      if ($null -ne $t.PSObject.Properties['agent_count_headroom'])       { $result.AgentHeadroom = [double]$t.agent_count_headroom }
      if ($null -ne $t.PSObject.Properties['blocks_per_department_ratio']){ $result.BlocksRatio = [double]$t.blocks_per_department_ratio }
      if ($null -ne $t.PSObject.Properties['routing_accuracy_floor'])     { $result.RoutingFloor = [double]$t.routing_accuracy_floor }
      if ($null -ne $t.PSObject.Properties['error_code_reuse_ceiling'])   { $result.ReuseCeiling = [double]$t.error_code_reuse_ceiling }
    }
    if ($null -ne $cfg.PSObject.Properties['output_dir']) { $result.OutputDir = [string]$cfg.output_dir }
  }
  if ([string]::IsNullOrWhiteSpace($result.OutputDir)) { $result.OutputDir = '{WORKSPACE_ROOT}/.skill-upgrade' }
  return $result
}

# --------------------------------------------------------------------------------------
# State file handling (step 1 ; SCL_007 on corrupt / inconsistent)
# --------------------------------------------------------------------------------------

function Read-State {
  if (-not (Test-Path -LiteralPath $StateFile)) {
    Stop-WithCode 'SCL_007' "state file not found: $StateFile"
  }
  $state = $null
  try { $state = ConvertFrom-Json ([System.IO.File]::ReadAllText($StateFile)) }
  catch { Stop-WithCode 'SCL_007' "state file is not valid JSON: $StateFile" }
  foreach ($field in @('schema_version', 'current_tier', 'tier_history', 'pending_proposals', 'next_evaluation')) {
    if ($null -eq $state.PSObject.Properties[$field]) {
      Stop-WithCode 'SCL_007' "state file is missing required field '$field'"
    }
  }
  $validTiers = @('micro', 'small', 'medium', 'large', 'group')
  if ($validTiers -notcontains [string]$state.current_tier) {
    Stop-WithCode 'SCL_007' "state file current_tier has an illegal value: '$($state.current_tier)'"
  }
  # P41 : current_tier must agree with the SKILL.md frontmatter scale_tier.
  $fm = Get-FrontmatterText (Join-Path $SkillDir 'SKILL.md')
  if ($null -ne $fm) {
    $fmTier = $null
    $fmMatch = [regex]::Match($fm, '(?m)^\s*scale_tier\s*:\s*([a-z]+)\s*$')
    if ($fmMatch.Success) { $fmTier = $fmMatch.Groups[1].Value }
    if (($null -ne $fmTier) -and ($fmTier -ne [string]$state.current_tier)) {
      Stop-WithCode 'SCL_007' ("current_tier '{0}' does not match SKILL.md frontmatter scale_tier '{1}'" -f $state.current_tier, $fmTier)
    }
  }
  return $state
}

function Set-StateProperty {
  param($State, [string]$Name, $Value)
  if ($null -ne $State.PSObject.Properties[$Name]) { $State.$Name = $Value }
  else { $State | Add-Member -MemberType NoteProperty -Name $Name -Value $Value }
}

function Save-State {
  param($State)
  $json = ConvertTo-Json -InputObject $State -Depth 10
  Write-TextFileNoBom -Path $StateFile -Text ($json + "`n")
  Write-Log "state file updated: $StateFile"
}

# --------------------------------------------------------------------------------------
# Frontmatter helpers
# --------------------------------------------------------------------------------------

function Get-FrontmatterText {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return $null }
  $lines = [System.IO.File]::ReadAllLines($Path)
  if ($lines.Count -lt 2) { return $null }
  if ($lines[0].Trim() -ne '---') { return $null }
  for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Trim() -eq '---') {
      if ($i -le 1) { return '' }
      return ($lines[1..($i - 1)] -join "`n")
    }
  }
  return $null
}

function Get-FrontmatterSubBlock {
  # Returns the full YAML sub-block of a top-level key (the key line plus every
  # indented line that follows it), or $null when the key is absent.
  param([string]$FrontmatterText, [string]$Key)
  if ($null -eq $FrontmatterText) { return $null }
  $lines = $FrontmatterText -split "`n"
  $start = -1
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match ('^' + $Key + '\s*:\s*$')) { $start = $i; break }
  }
  if ($start -lt 0) { return $null }
  $out = New-Object System.Collections.Generic.List[string]
  $out.Add($lines[$start])
  for ($i = $start + 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\S') { break }
    $out.Add($lines[$i])
  }
  return ($out -join "`n")
}

function Get-DenyItems {
  # Extracts the items of the 'deny' list inside a permissions block. Supports
  # both the inline flow form  deny: ["a", "b", ...]  (README-FOR-AI.md sec 9.1 shape) and the
  # block list form  deny:\n  - a\n  - b .
  param([string]$PermissionsBlock)
  $items = @()
  if ($null -eq $PermissionsBlock) { return $items }
  foreach ($line in ($PermissionsBlock -split "`n")) {
    if ($line -match '^\s+deny\s*:\s*\[(.*)\]\s*$') {
      foreach ($m in [regex]::Matches($Matches[1], '"([^"]+)"')) { $items += $m.Groups[1].Value }
    }
  }
  if ($items.Count -eq 0) {
    $inDeny = $false
    foreach ($line in ($PermissionsBlock -split "`n")) {
      if ($line -match '^\s+deny\s*:\s*$') { $inDeny = $true; continue }
      if ($inDeny) {
        if ($line -match '^\s+-\s+(.+?)\s*$') { $items += $Matches[1].Trim('"') }
        elseif ($line -match '^\S') { break }
      }
    }
  }
  return $items
}

# --------------------------------------------------------------------------------------
# Metric collection (step 2)
# --------------------------------------------------------------------------------------

function Get-MaxBlocksPerDepartment {
  # Live count of '## FB-N:' headings across the current D2 pages (T2 data source).
  $max = 0
  if (-not (Test-Path -LiteralPath $DepartmentsDir)) { return $max }
  $files = @(Get-ChildItem -LiteralPath $DepartmentsDir -Filter '*.md' -File -ErrorAction SilentlyContinue)
  foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName)
    $count = ([regex]::Matches($text, '(?m)^##\s+FB-\d+\s*:')).Count
    if ($count -gt $max) { $max = $count }
  }
  return $max
}

function Get-CurrentMetrics {
  param($State)
  $m = @{ AgentCount = 0; RoutingAccuracy = 1.0; ReuseRatio = 0.0; MaxBlocks = 0 }
  if ($null -ne $State.PSObject.Properties['last_metrics']) {
    $lm = $State.last_metrics
    if ($null -ne $lm.PSObject.Properties['agent_count'])            { $m.AgentCount = [int]$lm.agent_count }
    if ($null -ne $lm.PSObject.Properties['routing_accuracy'])       { $m.RoutingAccuracy = [double]$lm.routing_accuracy }
    if ($null -ne $lm.PSObject.Properties['error_code_reuse_ratio']) { $m.ReuseRatio = [double]$lm.error_code_reuse_ratio }
    if ($null -ne $lm.PSObject.Properties['max_blocks_per_department']) { $m.MaxBlocks = [int]$lm.max_blocks_per_department }
  }
  $live = Get-MaxBlocksPerDepartment
  if ($live -gt 0) { $m.MaxBlocks = $live }
  return $m
}

# --------------------------------------------------------------------------------------
# Threshold evaluation (step 2, T1-T4)
# --------------------------------------------------------------------------------------

function Invoke-ThresholdEvaluation {
  param($State, $Metrics, $Config)
  $tier = [string]$State.current_tier
  $cap = $TierAgentCaps[$tier]
  $mean = $TierBlockMean[$tier]
  $triggers = @()

  # T1 - agent capacity overflow
  $t1Limit = [math]::Round($cap * $Config.AgentHeadroom, 3)
  Write-Log ("T1 agent capacity: agent_count = {0}, threshold > {1}" -f $Metrics.AgentCount, $t1Limit)
  if ($Metrics.AgentCount -gt $t1Limit) {
    $triggers += @{ Id = 'T1'; Name = 'Agent capacity overflow'; Metric = 'agent_count'; Value = $Metrics.AgentCount; Threshold = ('> ' + $t1Limit) }
  }

  # T2 - function-block overload in a single department
  $t2Limit = [math]::Round($mean * $Config.BlocksRatio, 3)
  Write-Log ("T2 function-block overload: max_blocks_per_department = {0}, threshold > {1}" -f $Metrics.MaxBlocks, $t2Limit)
  if ($Metrics.MaxBlocks -gt $t2Limit) {
    $triggers += @{ Id = 'T2'; Name = 'Function-block overload'; Metric = 'max_blocks_per_department'; Value = $Metrics.MaxBlocks; Threshold = ('> ' + $t2Limit) }
  }

  # T3 - routing accuracy below the floor on 3 consecutive evaluations
  $streak = 0
  if ($null -ne $State.PSObject.Properties['routing_miss_streak']) { $streak = [int]$State.routing_miss_streak }
  if ($Metrics.RoutingAccuracy -lt $Config.RoutingFloor) { $streak = $streak + 1 } else { $streak = 0 }
  Write-Log ("T3 routing accuracy: routing_accuracy = {0}, floor {1}, consecutive misses = {2}" -f $Metrics.RoutingAccuracy, $Config.RoutingFloor, $streak)
  if (($Metrics.RoutingAccuracy -lt $Config.RoutingFloor) -and ($streak -ge 3)) {
    $triggers += @{ Id = 'T3'; Name = 'Routing accuracy drop'; Metric = 'routing_accuracy'; Value = $Metrics.RoutingAccuracy; Threshold = ('< ' + $Config.RoutingFloor + ' for 3 consecutive evaluations') }
  }

  # T4 - error-code reuse above the ceiling
  Write-Log ("T4 error-code reuse: error_code_reuse_ratio = {0}, ceiling {1}" -f $Metrics.ReuseRatio, $Config.ReuseCeiling)
  if ($Metrics.ReuseRatio -gt $Config.ReuseCeiling) {
    $triggers += @{ Id = 'T4'; Name = 'Error-code reuse excess'; Metric = 'error_code_reuse_ratio'; Value = $Metrics.ReuseRatio; Threshold = ('> ' + $Config.ReuseCeiling) }
  }

  return @{ Triggers = $triggers; RoutingMissStreak = $streak }
}

# --------------------------------------------------------------------------------------
# Alias Map parsing / appending (steps 5g and gate G5)
# --------------------------------------------------------------------------------------

function Get-AliasRows {
  # Parses active alias rows from the '## Alias Map' table of a scaling.md file.
  # Rows inside fenced code blocks are ignored (they are illustrative, not active).
  param([string]$ScalingMdPath)
  $rows = @()
  if (-not (Test-Path -LiteralPath $ScalingMdPath)) { return $rows }
  $lines = [System.IO.File]::ReadAllLines($ScalingMdPath)
  $inSection = $false
  $inFence = $false
  foreach ($line in $lines) {
    if ($line -match '^\s*```') { $inFence = (-not $inFence); continue }
    if ($inFence) { continue }
    if ($line -match '^##\s+Alias Map') { $inSection = $true; continue }
    if ($inSection -and $line -match '^##\s') { break }
    if ($inSection -and $line -match '^\|\s*([a-z0-9][a-z0-9-]*)\s*\|\s*([a-z]+)\s*\|\s*([a-z0-9][a-z0-9-]*)\s*\|\s*(v[0-9.]+)\s*\|\s*$') {
      $rows += @{ Legacy = $Matches[1]; LegacyTier = $Matches[2]; Target = $Matches[3]; Since = $Matches[4] }
    }
  }
  return $rows
}

function Add-AliasRows {
  # Appends rows to the active table inside the '## Alias Map' section, after the
  # last existing table row of that section. History rows are never removed.
  param([string]$ScalingMdPath, [string[]]$NewRows)
  if (-not (Test-Path -LiteralPath $ScalingMdPath)) {
    Write-Log "WARN scaling.md not found at $ScalingMdPath; alias rows not appended"
    return
  }
  $lines = [System.IO.File]::ReadAllLines($ScalingMdPath)
  $headingIdx = -1
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^##\s+Alias Map') { $headingIdx = $i; break }
  }
  if ($headingIdx -lt 0) {
    Write-Log "WARN '## Alias Map' section not found; alias rows not appended"
    return
  }
  $sectionEnd = $lines.Count
  for ($i = $headingIdx + 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^##\s') { $sectionEnd = $i; break }
  }
  # Find the last active table row (pipe lines inside fenced code blocks are
  # illustrative and must not receive the appended rows).
  $insertAt = $sectionEnd
  $inFence = $false
  for ($i = $headingIdx + 1; $i -lt $sectionEnd; $i++) {
    if ($lines[$i] -match '^\s*```') { $inFence = (-not $inFence); continue }
    if ($inFence) { continue }
    if ($lines[$i] -match '^\|') { $insertAt = $i + 1 }
  }
  $out = New-Object System.Collections.Generic.List[string]
  for ($i = 0; $i -lt $insertAt; $i++) {
    # Drop the "_(none - initial micro tier, no upgrade has occurred)_" placeholder
    # row once real rows exist; it is a template placeholder, not a history row.
    if (($i -gt $headingIdx) -and ($i -lt $sectionEnd) -and ($lines[$i] -match '^\|\s*_\(none')) { continue }
    $out.Add($lines[$i])
  }
  foreach ($r in $NewRows) { $out.Add($r) }
  for ($i = $insertAt; $i -lt $lines.Count; $i++) { $out.Add($lines[$i]) }
  # E15 : keep the .md file at LF - explicit "`n" join with WriteAllText,
  # never WriteAllLines (which would emit platform CRLF).
  Write-TextFileNoBom -Path $ScalingMdPath -Text (($out -join "`n") + "`n")
}

# --------------------------------------------------------------------------------------
# Upgrade package generation (step 5)
# --------------------------------------------------------------------------------------

function New-UpgradePackage {
  param([string]$PkgDir)
  # Retired legacy D2 pages (replaced by their splits), as normalized relative paths.
  $retiredD2 = @('references/departments/governance-and-delivery.md', 'references/departments/engineering-and-safety.md')

  # 5h (basis) : copy the current package verbatim, except the retired legacy D2
  # pages (replaced by their splits), the operational state file (regenerated),
  # and build residues (E1 : __pycache__/ directories and *.pyc files are
  # git-ignored compilation leftovers - they must never reach the package nor
  # its file count or gate hashes).
  $allFiles = @(Get-ChildItem -LiteralPath $SkillDir -Recurse -File -Force)
  foreach ($f in $allFiles) {
    $rel = $f.FullName.Substring($SkillDir.Length + 1).Replace('\', '/')
    if ($rel -eq '.scaling-state.json') { continue }
    if ($retiredD2 -contains $rel) { continue }
    if ($rel -match '(^|/)__pycache__/') { continue }
    if ($rel -match '\.pyc$') { continue }
    $dest = Join-Path $PkgDir $rel
    $destDir = Split-Path -Parent $dest
    if (-not (Test-Path -LiteralPath $destDir)) {
      New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    Copy-Item -LiteralPath $f.FullName -Destination $dest -Force
  }
  Write-Log ("5h copied current package files to {0} (tests/ and self-scale.ps1 verbatim)" -f $PkgDir)

  # 5a + 5b : split the legacy D2 pages into the 5 target departments, in page
  # order, according to the merge tree block counts (conservation = 18, gate G4).
  $pkgDeptDir = Join-Path $PkgDir 'references\departments'
  if (-not (Test-Path -LiteralPath $pkgDeptDir)) {
    New-Item -ItemType Directory -Path $pkgDeptDir -Force | Out-Null
  }
  $sources = @('governance-and-delivery', 'engineering-and-safety')
  foreach ($src in $sources) {
    $srcPath = Join-Path $DepartmentsDir ($src + '.md')
    $targets = @($UpgradeEdge.Split | Where-Object { $_.Source -eq $src })
    if (-not (Test-Path -LiteralPath $srcPath)) {
      Write-Log "WARN legacy D2 page not found (split impossible, G4 will fail): $srcPath"
      continue
    }
    $text = [System.IO.File]::ReadAllText($srcPath)
    $fbMatches = [regex]::Matches($text, '(?m)^##\s+FB-\d+\s*:')
    if ($fbMatches.Count -eq 0) {
      Stop-WithCode 'SCL_010' ("legacy D2 page '{0}' contains no '## FB-N:' headings; the split cannot run" -f $srcPath)
    }
    # E5 : the section count must equal the merge-tree expectation exactly.
    # More sections (leftover) or fewer (shortage) both abort immediately -
    # function blocks are never silently dropped or padded.
    $expectedTotal = 0
    foreach ($t in $targets) { $expectedTotal += [int]$t.Blocks }
    if ($fbMatches.Count -ne $expectedTotal) {
      Stop-WithCode 'SCL_010' ("legacy D2 page '{0}' contains {1} '## FB-N:' section(s); the merge tree expects {2} (leftover and shortage both abort; nothing is silently dropped or padded)" -f $src, $fbMatches.Count, $expectedTotal)
    }
    $preamble = $text.Substring(0, $fbMatches[0].Index)
    $sections = @()
    for ($i = 0; $i -lt $fbMatches.Count; $i++) {
      $start = $fbMatches[$i].Index
      $end = $text.Length
      if ($i -lt $fbMatches.Count - 1) { $end = $fbMatches[$i + 1].Index }
      $sections += $text.Substring($start, $end - $start)
    }
    $cursor = 0
    foreach ($t in $targets) {
      $take = [int]$t.Blocks
      $body = ''
      for ($i = $cursor; $i -lt ($cursor + $take); $i++) { $body += $sections[$i] }
      $pre = $preamble.Replace($src, [string]$t.Slug)
      $destPath = Join-Path $pkgDeptDir ([string]$t.Slug + '.md')
      Write-TextFileNoBom -Path $destPath -Text ($pre + $body)
      Write-Log ("5a/5b split {0} -> {1} ({2} function blocks)" -f $src, $t.Slug, $take)
      $cursor += $take
    }
    # $cursor now equals $sections.Count by construction (verified above);
    # there is no leftover path anymore (E5).
  }

  # 5a (S-tier third prompt) : generate prompts/03-test-cases.md, the small-tier
  # agent-invoked prompt (E1 : without it the clean-environment target file count
  # is unreachable and propose fails G6/SCL_006). First screen follows README-FOR-AI.md sec 11.4
  # (agent-invoked variant) and satisfies the A1-A5 constraints of README-FOR-AI.md sec 11.3 :
  # A1 paths as placeholders, A2 expected artifacts declared, A3 failure codes
  # declared, A4 harness level >= L3, A5 template anchors referenced, never
  # inlined (no code blocks at all).
  $pkgPromptsDir = Join-Path $PkgDir 'prompts'
  if (-not (Test-Path -LiteralPath $pkgPromptsDir)) {
    New-Item -ItemType Directory -Path $pkgPromptsDir -Force | Out-Null
  }
  $testCasesPrompt = @'
---
mode: agent-invoked
id: 03-test-cases
title: Generate Test Cases
output_language: user-specified
harness_level: L3
---

> **Mode**: agent-invoked (executed by the agent runtime; not pasted by a human)
> **Purpose**: Generate a boundary-aware test-case suite for one method that was
> implemented to this skill's shared standard, and write it into the workspace.
>
> **Expected artifact path**:
> - `{WORKSPACE_ROOT}/tests/<METHOD_NAME>_test.py` - the generated test file
>   (standard library only; the file is created, never overwritten without an
>   explicit user confirmation)
>
> **Failure error codes**:
> - `CTO_003` - the generated suite assesses below Harness L3 (error handling,
>   retry, or idempotency coverage missing)
> - `CTO_002` - the generated suite fails the quality gate (a case has no
>   assertion, requires network access, or imports a non-standard library)
> - `SCL_006` - the generated artifact fails package validation
>
> **Referenced template anchors** (link, never inline - the authoritative code
> lives in `references/method-patterns.md`):
> - `references/method-patterns.md#3-1-validate_input_schema`
> - `references/method-patterns.md#3-5-retry_with_backoff`
> - `references/method-patterns.md#3-9-mask_sensitive_data`
>
> **Output language**: follow the language the user is currently using.

## Prompt

Inputs (supplied by the invoking agent):

- `<METHOD_NAME>` - the method to generate test cases for
- `<SPEC_SUMMARY>` - the method's contract: parameters, return value, and
  documented failure modes
- `<TARGET_LEVEL>` - required harness level (default L3)

Task: produce a test suite for `<METHOD_NAME>` covering, at minimum:

1. Normal path - at least one case per documented behavior.
2. Input validation - invalid inputs are rejected before any processing
   (see `references/method-patterns.md#3-1-validate_input_schema`).
3. Retry behavior - transient failures are retried and the retry limit is
   enforced (see `references/method-patterns.md#3-5-retry_with_backoff`).
4. PII masking - outputs replace email addresses, IPv4 addresses, and
   11-digit phone numbers with their placeholders (see
   `references/method-patterns.md#3-9-mask_sensitive_data`).
5. Boundary conditions - empty input, single element, maximum size, and
   off-by-one cases.

Requirements: standard library only; no network access; every test asserts
exactly one behavior and carries a docstring naming the covered dimension.

## Expected Output

A single test file at `{WORKSPACE_ROOT}/tests/<METHOD_NAME>_test.py`, plus a
summary stating: the dimensions covered, the number of cases per dimension,
and any dimension that cannot be tested, with the reason.

## Self-Check Checklist

- [ ] The artifact lands at the expected path under `{WORKSPACE_ROOT}/tests/`.
- [ ] No case requires network access or non-standard libraries.
- [ ] Every dimension above has at least one case or a stated reason.
- [ ] Any generation failure is reported with the error codes listed above.
'@
  Write-TextFileNoBom -Path (Join-Path $pkgPromptsDir '03-test-cases.md') -Text $testCasesPrompt
  Write-Log '5a generated prompts/03-test-cases.md (agent-invoked, S-tier third prompt)'

  # 5d : rewrite the package frontmatter (tier fields, version, alias pointer,
  # interface department enum, and description - E2 : leaving the two retired
  # slugs in the enum would contradict department_count: 5 inside the same
  # frontmatter and make the new departments unreachable through the interface).
  # The permissions and language_policy blocks are never touched by the rewrite.
  $newEnum = '[auto, governance-and-operations, technology-and-platform, security-and-compliance, people-and-growth, quality-and-delivery]'
  $newDescription = 'Small-tier governance skill for growing AI agent organizations (3-10 agents). Distributes 18 enterprise function blocks across 5 departments - governance-and-operations, quality-and-delivery, technology-and-platform, security-and-compliance, and people-and-growth - covering strategy, operations, quality, delivery, architecture, security, compliance, and people growth. Ships ten harness code templates, three prompt frameworks, a full error-code catalog, and a scaling specification. Provides two self-contained human-paste prompts plus one agent-invoked prompt for test-case generation. Source files are authored in English; runtime output follows the user''s language per the language policy, with English fallback. Includes propose-only self-scaling that evaluates scaling thresholds and proposes tier upgrades up to group. Use when a growing team needs enterprise-grade governance, engineering harnesses, PII masking, AIGC disclosure, or tier-upgrade assessment for its agents.'
  $skPath = Join-Path $PkgDir 'SKILL.md'
  if (Test-Path -LiteralPath $skPath) {
    $lines = [System.IO.File]::ReadAllLines($skPath)
    $fmEnd = -1
    for ($i = 1; $i -lt $lines.Count; $i++) {
      if ($lines[$i].Trim() -eq '---') { $fmEnd = $i; break }
    }
    if (($lines.Count -ge 2) -and ($lines[0].Trim() -eq '---') -and ($fmEnd -gt 0)) {
      $inMetadata = $false
      $inInterface = $false
      $hasAliasPointer = $false
      $versionRewrites = 0       # E16 : every rewrite is counted and located
      $enumRewrites = 0
      $descriptionRewrites = 0
      for ($i = 1; $i -lt $fmEnd; $i++) {
        $line = $lines[$i]
        if ($line -match '^metadata\s*:\s*$') { $inMetadata = $true; continue }
        if ($line -match '^interface\s*:\s*$') { $inInterface = $true; continue }
        if ($line -match '^\S') { $inMetadata = $false; $inInterface = $false }
        if ($line -match '^(\s*)version\s*:\s*.*$') {
          $lines[$i] = "{0}version: {1}" -f $Matches[1], $UpgradeEdge.NewVersion
          $versionRewrites++
          Write-Log ("5d version rewritten at SKILL.md frontmatter line {0}: '{1}' -> '{2}'" -f ($i + 1), $UpgradeEdge.OldVersion, $UpgradeEdge.NewVersion)
          continue
        }
        if ($line -match '^(\s*)error_code_prefixes\s*:\s*.*$') {
          $lines[$i] = "{0}error_code_prefixes: [CEO_, CTO_, CISO_, CHO_, CQO_, SCL_]" -f $Matches[1]
          continue
        }
        # E2 : top-level description (the only unindented description: line).
        if ($line -match '^description\s*:\s*".*"\s*$') {
          $lines[$i] = 'description: "' + $newDescription + '"'
          $descriptionRewrites++
          continue
        }
        # E2 : the department enum inside the interface block (the only enum:
        # line, and it must list "auto" first).
        if ($inInterface -and ($line -match '^(\s*)enum\s*:\s*\[.*\]\s*$') -and ($line -match '\bauto\b')) {
          $lines[$i] = "{0}enum: {1}" -f $Matches[1], $newEnum
          $enumRewrites++
          continue
        }
        if ($line -match 'department_aliases') { $hasAliasPointer = $true }
        if ($inMetadata) {
          if ($line -match '^(\s*)scale_tier\s*:') {
            $lines[$i] = "{0}scale_tier: {1}" -f $Matches[1], $UpgradeEdge.To; continue
          }
          if ($line -match '^(\s*)department_count\s*:') {
            $lines[$i] = "{0}department_count: 5" -f $Matches[1]; continue
          }
          if ($line -match '^(\s*)function_block_count\s*:') {
            $lines[$i] = "{0}function_block_count: 18" -f $Matches[1]; continue
          }
        }
      }
      # E16 : verify each targeted rewrite actually happened (>= 1 occurrence).
      if ($versionRewrites -lt 1)     { Write-Log 'WARN 5d version line was not found in the package frontmatter (G6 version check will fail)' }
      if ($enumRewrites -lt 1)        { Write-Log 'WARN 5d interface.department.enum was not found in the package frontmatter (G6 enum check will fail)' }
      if ($descriptionRewrites -lt 1) { Write-Log 'WARN 5d top-level description was not found in the package frontmatter (stale micro-tier description left in place; flagged for human review)' }
      if (-not $hasAliasPointer) {
        $out = New-Object System.Collections.Generic.List[string]
        for ($i = 0; $i -lt $fmEnd; $i++) { $out.Add($lines[$i]) }
        $out.Add('department_aliases: references/scaling.md#alias-map')
        for ($i = $fmEnd; $i -lt $lines.Count; $i++) { $out.Add($lines[$i]) }
        $lines = $out.ToArray()
      }
      # E1 : list the new prompt in the SKILL.md Prompts index (zero-orphan,
      # README-FOR-AI.md sec 11.1) - inserted right after the 02-robustness-checks row.
      $promptRow = '| [03-test-cases.md](prompts/03-test-cases.md) | `agent-invoked` | Agent runtime generates a test-case suite for one method and writes it to {WORKSPACE_ROOT}/tests/ |'
      $promptRowAt = -1
      for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^\|\s*\[02-robustness-checks\.md\]') { $promptRowAt = $i + 1; break }
      }
      if ($promptRowAt -gt 0) {
        $out = New-Object System.Collections.Generic.List[string]
        for ($i = 0; $i -lt $promptRowAt; $i++) { $out.Add($lines[$i]) }
        $out.Add($promptRow)
        for ($i = $promptRowAt; $i -lt $lines.Count; $i++) { $out.Add($lines[$i]) }
        $lines = $out.ToArray()
        Write-Log '5d prompts index row added for 03-test-cases.md (zero-orphan)'
      } else {
        Write-Log 'WARN 5d Prompts index row for 02-robustness-checks.md not found; 03-test-cases.md row not added'
      }
      # E15 : keep the package SKILL.md at LF (explicit "`n", never WriteAllLines).
      Write-TextFileNoBom -Path $skPath -Text (($lines -join "`n") + "`n")
      Write-Log "5d package frontmatter rewritten (scale_tier=small, department_count=5, function_block_count=18, version=2.0.0, department_aliases pointer, enum + description updated for 5 departments)"
    } else {
      Write-Log 'WARN package SKILL.md has no parseable frontmatter; 5d skipped (G1/G6 will fail)'
    }
  } else {
    Write-Log 'WARN package SKILL.md not found; 5d skipped (G1/G3/G6 will fail)'
  }

  # 5e (deterministic part) : _meta.json version bump.
  $metaPath = Join-Path $PkgDir '_meta.json'
  if (Test-Path -LiteralPath $metaPath) {
    try {
      $meta = ConvertFrom-Json ([System.IO.File]::ReadAllText($metaPath))
      if ($null -ne $meta.PSObject.Properties['version']) { $meta.version = $UpgradeEdge.NewVersion }
      Write-TextFileNoBom -Path $metaPath -Text ((ConvertTo-Json -InputObject $meta -Depth 6) + "`n")
      Write-Log "5e _meta.json version bumped to $($UpgradeEdge.NewVersion)"
    } catch { Write-Log 'WARN _meta.json could not be updated (G6 version check will fail)' }
  }

  # 5e (E10, skeleton part) : append an error-code alias-table skeleton to the
  # package error-codes.md. The function-level merge lists are not
  # machine-derivable in this build, so every row is generated as an explicit
  # "requires human review" placeholder - the table makes the package
  # structurally complete; a human completes the mappings before installation.
  $pkgErrorCodes = Join-Path (Join-Path $PkgDir 'references') 'error-codes.md'
  if (Test-Path -LiteralPath $pkgErrorCodes) {
    $aliasHeader = @'

## Error-Code Alias Map (proposed - requires human review)

The micro -> small upgrade revives the `CISO_`, `CHO_`, and `CQO_` prefixes.
The function-level merge lists are not machine-derivable in this build, so the
legacy-to-new mapping below is a generated skeleton: every row requires human
review before installation (README-FOR-AI.md sec 12.4, step 5e). `CEO_` and `CTO_`
codes whose functions stay in the successor departments keep their codes.

| Legacy code | Resolves to | Status |
|---|---|---|
'@
    $aliasRowsText = ''
    foreach ($pfx in @('CEO_', 'CTO_')) {
      for ($n = 1; $n -le 12; $n++) {
        $code = '{0}{1:d3}' -f $pfx, $n
        $aliasRowsText += ("| {0} | <requires human review> | proposed |`n" -f $code)
      }
    }
    $oldErr = Read-TextFile -Path $pkgErrorCodes
    if ($null -ne $oldErr) {
      Write-TextFileNoBom -Path $pkgErrorCodes -Text ($oldErr.TrimEnd("`n") + $aliasHeader + "`n" + $aliasRowsText)
      Write-Log '5e error-code alias-table skeleton appended to references/error-codes.md (24 rows, all marked requires human review)'
    }
  } else {
    Write-Log 'WARN references/error-codes.md missing from the package; alias-table skeleton not generated'
  }

  # 5i (E16) : version strings in the README files - context-exact, counted
  # replacements only (never a blind whole-file string replace). Each target
  # context must occur at least once per applicable file; every replacement
  # location is logged. SKILL.md's version is handled by 5d and verified by G6.
  $zhVersionWord = [string][char]0x7248 + [string][char]0x672C   # the Chinese word for "version" (README.zh.md table row); built from code points so this script stays pure ASCII
  $readmeTargets = @(
    @{ Pattern = 'version-1\.0\.0-blue';     Replace = 'version-2.0.0-blue';  What = 'badge' },
    @{ Pattern = ('\| ' + $zhVersionWord + ' \| 1\.0\.0 \|'); Replace = ('| ' + $zhVersionWord + ' | 2.0.0 |'); What = 'at-a-glance version row (Chinese)' },
    @{ Pattern = '\| Version \| 1\.0\.0 \|'; Replace = '| Version | 2.0.0 |'; What = 'at-a-glance version row (English)' }
  )
  $replaceCounts = @{}
  foreach ($name in @('README.md', 'README.en.md', 'README.zh.md')) {
    $p = Join-Path $PkgDir $name
    if (-not (Test-Path -LiteralPath $p)) { continue }
    $t = Read-TextFile -Path $p
    if ($null -eq $t) { continue }
    foreach ($tgt in $readmeTargets) {
      $hits = [regex]::Matches($t, $tgt.Pattern)
      if ($hits.Count -eq 0) { continue }
      # Log every replacement location (line number) before touching anything.
      foreach ($h in $hits) {
        $lineNo = 1 + ([regex]::Matches($t.Substring(0, $h.Index), "`n")).Count
        Write-Log ("5i {0}: {1} rewritten at line {2} ('{3}' -> '{4}')" -f $name, $tgt.What, $lineNo, $UpgradeEdge.OldVersion, $UpgradeEdge.NewVersion)
      }
      $t = [regex]::Replace($t, $tgt.Pattern, $tgt.Replace)
      $replaceCounts[("{0}|{1}" -f $name, $tgt.What)] = $hits.Count
    }
    Write-TextFileNoBom -Path $p -Text $t
  }
  # E16 : post-replacement count verification. Every applicable target must
  # have been replaced at least once; a miss is logged as a warning (the badge
  # target is additionally enforced by gate G6).
  foreach ($name in @('README.md', 'README.en.md', 'README.zh.md')) {
    if (-not ($replaceCounts.ContainsKey("$name|badge")) -or ($replaceCounts["$name|badge"] -lt 1)) {
      Write-Log "WARN 5i $name : badge version context was not found / not replaced"
    }
  }
  foreach ($name in @('README.md', 'README.en.md')) {
    if (-not ($replaceCounts.ContainsKey("$name|at-a-glance version row (English)")) -or ($replaceCounts["$name|at-a-glance version row (English)"] -lt 1)) {
      Write-Log "WARN 5i $name : English version table row was not found / not replaced"
    }
  }
  if (-not ($replaceCounts.ContainsKey('README.zh.md|at-a-glance version row (Chinese)')) -or ($replaceCounts['README.zh.md|at-a-glance version row (Chinese)'] -lt 1)) {
    Write-Log 'WARN 5i README.zh.md : Chinese version table row was not found / not replaced'
  }

  # 5i (E10, skeleton part) : rewrite the README Project Structure tree to the
  # 29-file small-tier skeleton, marked as requiring human review. Without this
  # the package READMEs would still describe the 25-file micro layout.
  # The tree (which contains box-drawing characters) is stored base64-encoded
  # so this script stays pure ASCII: Windows PowerShell 5.1 reads BOM-less
  # UTF-8 scripts as ANSI, which would corrupt literal non-ASCII characters.
  # Decoded, $newTree is the 29-file small-tier layout: 15 root files
  # (incl. README-FOR-AI.md), prompts/ (3), references/ (3),
  # references/departments/ (5 new slugs), scripts/ (2), tests/ (1).
  $newTree = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('YWktY29tcGFueS1nb3Zlcm5hbmNlLwrilJzilIDilIAgLmVkaXRvcmNvbmZpZwrilJzilIDilIAgLmdpdGlnbm9yZQrilJzilIDilIAgLnNjYWxpbmctc3RhdGUuanNvbgrilJzilIDilIAgQUdFTlRTLm1kCuKUnOKUgOKUgCBDSEFOR0VMT0cubWQK4pSc4pSA4pSAIENPREVfT0ZfQ09ORFVDVC5tZArilJzilIDilIAgQ09OVFJJQlVUSU5HLm1kCuKUnOKUgOKUgCBMSUNFTlNFCuKUnOKUgOKUgCBSRUFETUUtRk9SLUFJLm1kCuKUnOKUgOKUgCBSRUFETUUuZW4ubWQK4pSc4pSA4pSAIFJFQURNRS5tZArilJzilIDilIAgUkVBRE1FLnpoLm1kCuKUnOKUgOKUgCBTRUNVUklUWS5tZArilJzilIDilIAgU0tJTEwubWQK4pSc4pSA4pSAIF9tZXRhLmpzb24K4pSc4pSA4pSAIHByb21wdHMvCuKUgiAgIOKUnOKUgOKUgCAwMS1pbXBsZW1lbnQtbWV0aG9kLm1kCuKUgiAgIOKUnOKUgOKUgCAwMi1yb2J1c3RuZXNzLWNoZWNrcy5tZArilIIgICDilJTilIDilIAgMDMtdGVzdC1jYXNlcy5tZArilJzilIDilIAgcmVmZXJlbmNlcy8K4pSCICAg4pSc4pSA4pSAIG1ldGhvZC1wYXR0ZXJucy5tZArilIIgICDilJzilIDilIAgZXJyb3ItY29kZXMubWQK4pSCICAg4pSc4pSA4pSAIHNjYWxpbmcubWQK4pSCICAg4pSU4pSA4pSAIGRlcGFydG1lbnRzLwrilIIgICAgICAg4pSc4pSA4pSAIGdvdmVybmFuY2UtYW5kLW9wZXJhdGlvbnMubWQK4pSCICAgICAgIOKUnOKUgOKUgCBxdWFsaXR5LWFuZC1kZWxpdmVyeS5tZArilIIgICAgICAg4pSc4pSA4pSAIHRlY2hub2xvZ3ktYW5kLXBsYXRmb3JtLm1kCuKUgiAgICAgICDilJzilIDilIAgc2VjdXJpdHktYW5kLWNvbXBsaWFuY2UubWQK4pSCICAgICAgIOKUlOKUgOKUgCBwZW9wbGUtYW5kLWdyb3d0aC5tZArilJzilIDilIAgc2NyaXB0cy8K4pSCICAg4pSc4pSA4pSAIHNlbGYtc2NhbGUucHMxCuKUgiAgIOKUlOKUgOKUgCBzY2FsaW5nLWNvbmZpZy5qc29uCuKUlOKUgOKUgCB0ZXN0cy8KICAgIOKUlOKUgOKUgCB0ZXN0LW1ldGhvZC1wYXR0ZXJucy5weQo='))
  $newTree = $newTree + "`n"
  $treeNoteEn = '> Structure tree rewritten to the 29-file small-tier skeleton by the'
  $treeNoteEn = $treeNoteEn + ' upgrade generator - requires human review before installation.'
  # README.zh.md carries a Chinese note. The text is stored base64-encoded so
  # this script stays pure ASCII (Windows PowerShell 5.1 reads BOM-less UTF-8
  # as ANSI, which would corrupt literal CJK characters). Decoded, it is the
  # Chinese translation of $treeNoteEn: "structure tree rewritten to the
  # 29-file small-tier skeleton by the upgrade generator - requires human
  # review before installation".
  $treeNoteZh = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('PiDnu5PmnoTmoJHlt7LnlLHljYfnuqfnlJ/miJDlmajmlLnlhpnkuLogMjkg5Liq5paH5Lu255qE5bCP5Z6L5qGj6aqo5p6277yIc21hbGzvvInigJTigJTlronoo4XliY3pnIDkurrlt6XlpI3moLjjgII='))
  foreach ($name in @('README.md', 'README.en.md', 'README.zh.md')) {
    $p = Join-Path $PkgDir $name
    if (-not (Test-Path -LiteralPath $p)) { continue }
    $t = Read-TextFile -Path $p
    if ($null -eq $t) { continue }
    $treeFence = '(?s)```text\r?\nai-company/.*?\r?\n```'
    if (-not ([regex]::IsMatch($t, $treeFence))) {
      Write-Log "WARN 5i Project Structure tree fence not found in $name; tree not rewritten"
      continue
    }
    $note = $treeNoteEn
    if ($name -eq 'README.zh.md') { $note = $treeNoteZh }
    $replacement = '```text' + "`n" + $newTree + '```' + "`n`n" + $note
    $treeRegex = New-Object System.Text.RegularExpressions.Regex($treeFence)
    $t2 = $treeRegex.Replace($t, $replacement.Replace('$', '$$'), 1)
    Write-TextFileNoBom -Path $p -Text $t2
    Write-Log "5i Project Structure tree rewritten to the 29-file skeleton in $name (marked requires human review)"
  }

  # 5i (E17) : CHANGELOG.md upgrade entry - inserted directly after the
  # '## [Unreleased]' heading (Keep a Changelog order: newest version first),
  # never appended at the end of the file.
  $changelogPath = Join-Path $PkgDir 'CHANGELOG.md'
  if (Test-Path -LiteralPath $changelogPath) {
    $entry = "## [$($UpgradeEdge.NewVersion)] - $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')) - tier upgrade proposal (micro -> small)`n`n" +
      "- Departments: 2 -> 5 (merge-tree split, function blocks conserved at 18)`n" +
      "- Revived error-code prefixes: CISO_, CHO_, CQO_ (alias-table skeleton appended to references/error-codes.md)`n" +
      "- New agent-invoked prompt: prompts/03-test-cases.md`n" +
      "- Slug aliases appended to references/scaling.md (Alias Map)`n" +
      "- PROPOSED ONLY - requires human approval and an external installer`n"
    $old = Read-TextFile -Path $changelogPath
    if ($null -ne $old) {
      $chLines = $old -split "`n"
      $unreleasedIdx = -1
      for ($i = 0; $i -lt $chLines.Count; $i++) {
        if ($chLines[$i] -match '^##\s*\[Unreleased\]') { $unreleasedIdx = $i; break }
      }
      if ($unreleasedIdx -ge 0) {
        # Insert after the [Unreleased] heading, skipping the blank lines that
        # follow it, so the new entry becomes the first version section.
        $insertAt = $unreleasedIdx + 1
        while (($insertAt -lt $chLines.Count) -and ([string]::IsNullOrWhiteSpace($chLines[$insertAt]))) { $insertAt++ }
        $out = New-Object System.Collections.Generic.List[string]
        for ($i = 0; $i -lt $insertAt; $i++) { $out.Add($chLines[$i]) }
        foreach ($l in ($entry -split "`n")) { $out.Add($l) }
        for ($i = $insertAt; $i -lt $chLines.Count; $i++) { $out.Add($chLines[$i]) }
        Write-TextFileNoBom -Path $changelogPath -Text ((($out -join "`n").TrimEnd("`r`n")) + "`n")
        Write-Log '5i CHANGELOG.md entry inserted after [Unreleased] (E17 order)'
      } else {
        # No [Unreleased] heading: fall back to inserting after the header
        # paragraph rather than appending at the end.
        $insertAfter = 0
        for ($i = 0; $i -lt $chLines.Count; $i++) {
          if ($chLines[$i] -match '^##\s') { $insertAfter = $i; break }
        }
        $out = New-Object System.Collections.Generic.List[string]
        for ($i = 0; $i -lt $insertAfter; $i++) { $out.Add($chLines[$i]) }
        foreach ($l in ($entry -split "`n")) { $out.Add($l) }
        for ($i = $insertAfter; $i -lt $chLines.Count; $i++) { $out.Add($chLines[$i]) }
        Write-TextFileNoBom -Path $changelogPath -Text ((($out -join "`n").TrimEnd("`r`n")) + "`n")
        Write-Log 'WARN 5i CHANGELOG.md has no [Unreleased] heading; entry inserted before the first version section'
      }
    }
  }

  # 5g : append the slug alias rows to the package's scaling.md Alias Map.
  $pkgScalingMd = Join-Path (Join-Path $PkgDir 'references') 'scaling.md'
  $aliasRows = @(
    '| governance-and-delivery | micro | governance-and-operations | v2.0.0 |',
    '| governance-and-delivery | micro | quality-and-delivery | v2.0.0 |',
    '| engineering-and-safety | micro | technology-and-platform | v2.0.0 |',
    '| engineering-and-safety | micro | security-and-compliance | v2.0.0 |',
    '| engineering-and-safety | micro | people-and-growth | v2.0.0 |'
  )
  Add-AliasRows -ScalingMdPath $pkgScalingMd -NewRows $aliasRows
  Write-Log '5g alias rows appended to the package Alias Map (history preserved)'

  # Package state file : initial state for the target tier. E7 : tier_history
  # is never reset to an empty array (README-FOR-AI.md sec 12.6 - append-only audit trail);
  # it carries a skeleton entry for THIS upgrade with approved_by / installed_at
  # empty (the external installer fills them in at install time) and
  # acceptance_passed false until the human reviewer completes README-FOR-AI.md sec 15
  # acceptance.
  $nowIso = Get-UtcNowIso
  $pkgState = [ordered]@{
    schema_version      = 1
    current_tier        = $UpgradeEdge.To
    tier_history        = @(
      [ordered]@{
        from          = $UpgradeEdge.From
        to            = $UpgradeEdge.To
        proposed_at   = $nowIso
        approved_by   = $null
        installed_at  = $null
        package_path  = $PkgDir
        validation    = [ordered]@{
          file_count        = $TargetFileCount[$UpgradeEdge.To]
          function_blocks   = 18
          gates_passed      = 6
          acceptance_passed = $false
        }
      }
    )
    pending_proposals   = @()
    next_evaluation     = (Get-Date).ToUniversalTime().AddDays(30).ToString('yyyy-MM-ddTHH:mm:ssZ')
    last_metrics        = [ordered]@{
      agent_count               = 0
      routing_accuracy          = 1.0
      max_blocks_per_department = 6
      error_code_reuse_ratio    = 0.0
    }
  }
  Write-TextFileNoBom -Path (Join-Path $PkgDir '.scaling-state.json') -Text ((ConvertTo-Json -InputObject $pkgState -Depth 10) + "`n")
  Write-Log "package state file initialized for tier '$($UpgradeEdge.To)' (tier_history carries the upgrade skeleton entry, append-only)"
}

# --------------------------------------------------------------------------------------
# Gate G1 - permission-unchanged gate (SCL_004)
# --------------------------------------------------------------------------------------

function Invoke-GateG1 {
  param([string]$PkgDir)
  Write-Log 'G1 permission-unchanged gate: comparing permissions block hash (current vs package)...'
  $curFm = Get-FrontmatterText (Join-Path $SkillDir 'SKILL.md')
  $pkgFm = Get-FrontmatterText (Join-Path $PkgDir 'SKILL.md')
  $curPerm = Get-FrontmatterSubBlock -FrontmatterText $curFm -Key 'permissions'
  $pkgPerm = Get-FrontmatterSubBlock -FrontmatterText $pkgFm -Key 'permissions'
  if (($null -eq $curPerm) -or ($null -eq $pkgPerm)) {
    return @{ Passed = $false; Detail = 'permissions block not found in the current or the package SKILL.md frontmatter' }
  }
  $curHash = Get-TextSha256 $curPerm
  $pkgHash = Get-TextSha256 $pkgPerm
  if ($curHash -ne $pkgHash) {
    return @{ Passed = $false; Detail = "permissions block hash mismatch: current=$curHash package=$pkgHash" }
  }
  return @{ Passed = $true; Detail = "permissions block hash identical ($curHash)" }
}

# --------------------------------------------------------------------------------------
# Gate G2 - tests-unchanged gate (SCL_005)
# --------------------------------------------------------------------------------------

function Get-TestsHashMap {
  param([string]$Root)
  $map = @{}
  $testsDir = Join-Path $Root 'tests'
  if (Test-Path -LiteralPath $testsDir) {
    $files = @(Get-ChildItem -LiteralPath $testsDir -Recurse -File -ErrorAction SilentlyContinue)
    foreach ($f in $files) {
      $rel = $f.FullName.Substring($testsDir.Length).TrimStart('\', '/').Replace('\', '/')
      # E1 : build residues are compared like-for-like - they are excluded on
      # both sides (the package copy already refuses them), so a leftover
      # __pycache__/ in the working tree can never fail (or pad) this gate.
      if ($rel -match '(^|/)__pycache__/') { continue }
      if ($rel -match '\.pyc$') { continue }
      $map[$rel] = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
    }
  }
  return $map
}

function Invoke-GateG2 {
  param([string]$PkgDir)
  Write-Log 'G2 tests-unchanged gate: verifying tests/** in the package is byte-identical to the current package...'
  $curMap = Get-TestsHashMap -Root $SkillDir
  $pkgMap = Get-TestsHashMap -Root $PkgDir
  $diffs = @()
  foreach ($k in $curMap.Keys) {
    if (-not $pkgMap.ContainsKey($k)) { $diffs += "missing in package: tests/$k" }
    elseif ($pkgMap[$k] -ne $curMap[$k]) { $diffs += "hash differs: tests/$k" }
  }
  foreach ($k in $pkgMap.Keys) {
    if (-not $curMap.ContainsKey($k)) { $diffs += "unexpected file in package: tests/$k" }
  }
  if ($diffs.Count -gt 0) {
    return @{ Passed = $false; Detail = ($diffs -join '; ') }
  }
  return @{ Passed = $true; Detail = ("{0} test file(s) verified byte-identical (SHA-256)" -f $curMap.Count) }
}

# --------------------------------------------------------------------------------------
# Gate G3 - deny-and-gate-unchanged gate (SCL_004)
# --------------------------------------------------------------------------------------

function Invoke-GateG3 {
  param([string]$PkgDir)
  Write-Log 'G3 deny-and-gate-unchanged gate: verifying the 5 deny items and the self-scale.ps1 hash...'
  $curPerm = Get-FrontmatterSubBlock -FrontmatterText (Get-FrontmatterText (Join-Path $SkillDir 'SKILL.md')) -Key 'permissions'
  $pkgPerm = Get-FrontmatterSubBlock -FrontmatterText (Get-FrontmatterText (Join-Path $PkgDir 'SKILL.md')) -Key 'permissions'
  if (($null -eq $curPerm) -or ($null -eq $pkgPerm)) {
    return @{ Passed = $false; Detail = 'permissions block not found; deny items cannot be verified' }
  }
  $curDeny = @(Get-DenyItems -PermissionsBlock $curPerm)
  $pkgDeny = @(Get-DenyItems -PermissionsBlock $pkgPerm)
  if (($curDeny.Count -ne 5) -or ($pkgDeny.Count -ne 5)) {
    return @{ Passed = $false; Detail = ("deny item count: current={0}, package={1} (expected 5)" -f $curDeny.Count, $pkgDeny.Count) }
  }
  if (($curDeny -join '|') -ne ($pkgDeny -join '|')) {
    return @{ Passed = $false; Detail = 'deny items differ between the current and the package SKILL.md' }
  }
  $curScript = Join-Path $PSScriptRoot 'self-scale.ps1'
  $pkgScript = Join-Path $PkgDir 'scripts\self-scale.ps1'
  if (-not (Test-Path -LiteralPath $pkgScript)) {
    return @{ Passed = $false; Detail = 'scripts/self-scale.ps1 missing from the package' }
  }
  $curHash = (Get-FileHash -LiteralPath $curScript -Algorithm SHA256).Hash
  $pkgHash = (Get-FileHash -LiteralPath $pkgScript -Algorithm SHA256).Hash
  if ($curHash -ne $pkgHash) {
    return @{ Passed = $false; Detail = "self-scale.ps1 hash mismatch: current=$curHash package=$pkgHash" }
  }
  return @{ Passed = $true; Detail = "5 deny items intact; self-scale.ps1 hash identical ($curHash)" }
}

# --------------------------------------------------------------------------------------
# Gate G4 - function-block conservation gate (SCL_010)
# --------------------------------------------------------------------------------------

function Invoke-GateG4 {
  param([string]$PkgDir)
  Write-Log "G4 function-block conservation gate: counting '## FB-N:' headings across the package D2 pages (total + per-department distribution)..."
  $pkgDeptDir = Join-Path $PkgDir 'references\departments'
  $actualPerDept = @{}
  $total = 0
  if (Test-Path -LiteralPath $pkgDeptDir) {
    $files = @(Get-ChildItem -LiteralPath $pkgDeptDir -Filter '*.md' -File -ErrorAction SilentlyContinue)
    foreach ($f in $files) {
      $text = [System.IO.File]::ReadAllText($f.FullName)
      $count = ([regex]::Matches($text, '(?m)^##\s+FB-\d+\s*:')).Count
      $actualPerDept[$f.BaseName] = $count
      $total += $count
    }
  }
  # E5 : the total alone can hide a wrong distribution (e.g. 7/1/3/3/4 still
  # sums to 18). Every department must match its merge-tree expectation
  # (small tier: 6/2/3/3/4), and no unexpected D2 page may exist.
  $problems = @()
  foreach ($t in $UpgradeEdge.Split) {
    $actual = 0
    if ($actualPerDept.ContainsKey([string]$t.Slug)) { $actual = $actualPerDept[[string]$t.Slug] }
    if ($actual -ne [int]$t.Blocks) {
      $problems += ("{0}: expected {1}, found {2}" -f $t.Slug, $t.Blocks, $actual)
    }
  }
  $expectedSlugs = @($UpgradeEdge.Split | ForEach-Object { [string]$_.Slug })
  foreach ($k in @($actualPerDept.Keys)) {
    if ($expectedSlugs -notcontains $k) {
      $problems += ("unexpected D2 page in the package: references/departments/{0}.md ({1} block(s))" -f $k, $actualPerDept[$k])
    }
  }
  if ($total -ne $UpgradeEdge.ExpectedBlocks) {
    $problems += ("total function blocks = {0}, expected {1}" -f $total, $UpgradeEdge.ExpectedBlocks)
  }
  if ($problems.Count -gt 0) {
    return @{ Passed = $false; Detail = ('function-block conservation violated: ' + ($problems -join '; ')) }
  }
  $dist = ($UpgradeEdge.Split | ForEach-Object { "{0}={1}" -f $_.Slug, $_.Blocks }) -join ', '
  return @{ Passed = $true; Detail = "total function blocks = $total (conserved, 18 -> 18); per-department distribution verified ($dist); no unexpected D2 pages" }
}

# --------------------------------------------------------------------------------------
# Gate G5 - alias completeness gate (SCL_003)
# --------------------------------------------------------------------------------------

function Invoke-GateG5 {
  param([string]$PkgDir)
  Write-Log 'G5 alias-completeness gate: checking legacy slug coverage and slug/alias conflicts...'
  $pkgScalingMd = Join-Path (Join-Path $PkgDir 'references') 'scaling.md'
  if (-not (Test-Path -LiteralPath $pkgScalingMd)) {
    return @{ Passed = $false; Detail = 'references/scaling.md missing from the package; Alias Map cannot be verified' }
  }
  $rows = @(Get-AliasRows -ScalingMdPath $pkgScalingMd)
  $legacySlugs = @($UpgradeEdge.Split | ForEach-Object { $_.Source } | Select-Object -Unique)
  $targetSlugs = @($UpgradeEdge.Split | ForEach-Object { $_.Slug })
  $problems = @()
  foreach ($legacy in $legacySlugs) {
    $hits = @($rows | Where-Object { $_.Legacy -eq $legacy })
    if ($hits.Count -eq 0) { $problems += "legacy slug '$legacy' has no alias row" }
  }
  foreach ($target in $targetSlugs) {
    $hits = @($rows | Where-Object { $_.Target -eq $target })
    if ($hits.Count -eq 0) { $problems += "target slug '$target' is not reachable through any alias row" }
  }
  foreach ($row in $rows) {
    if ($targetSlugs -contains $row.Legacy) {
      $problems += ("slug/alias conflict: new slug '{0}' equals a historical alias" -f $row.Legacy)
    }
  }
  if ($problems.Count -gt 0) {
    return @{ Passed = $false; Detail = ($problems -join '; ') }
  }
  return @{ Passed = $true; Detail = ("{0} active alias row(s), {1} conflict(s); all legacy and target slugs covered" -f $rows.Count, $problems.Count) }
}

# --------------------------------------------------------------------------------------
# Gate G6 - acceptance gate, machine-checkable subset (SCL_006)
# --------------------------------------------------------------------------------------

function Invoke-GateG6 {
  param([string]$PkgDir)
  Write-Log 'G6 acceptance gate: running the machine-checkable acceptance items on the package...'
  $fails = @()
  $expectedFiles = $TargetFileCount[$UpgradeEdge.To]

  # File count (skill files; the UPGRADE-PROPOSAL.md report artifact is excluded).
  $reportPath = Join-Path $PkgDir 'UPGRADE-PROPOSAL.md'
  $fileCount = @(Get-ChildItem -LiteralPath $PkgDir -Recurse -File -ErrorAction SilentlyContinue).Count
  if (Test-Path -LiteralPath $reportPath) { $fileCount = $fileCount - 1 }
  if ($fileCount -ne $expectedFiles) {
    $fails += "file_count: expected $expectedFiles, found $fileCount"
  }

  # Frontmatter triple consistency (H12) and version (H15, 4 locations).
  $fm = Get-FrontmatterText (Join-Path $PkgDir 'SKILL.md')
  if ($null -eq $fm) {
    $fails += 'SKILL.md frontmatter not found in the package'
  } else {
    if (-not ([regex]::IsMatch($fm, '(?m)^\s*scale_tier\s*:\s*small\s*$')))          { $fails += 'frontmatter scale_tier is not "small"' }
    if (-not ([regex]::IsMatch($fm, '(?m)^\s*department_count\s*:\s*5\s*$')))         { $fails += 'frontmatter department_count is not 5' }
    if (-not ([regex]::IsMatch($fm, '(?m)^\s*function_block_count\s*:\s*18\s*$')))    { $fails += 'frontmatter function_block_count is not 18' }
    if (-not ([regex]::IsMatch($fm, '(?m)^\s*version\s*:\s*2\.0\.0\s*$')))            { $fails += 'frontmatter version is not 2.0.0' }
    if (-not ([regex]::IsMatch($fm, 'department_aliases\s*:\s*references/scaling\.md#alias-map'))) { $fails += 'frontmatter department_aliases pointer missing' }
    $prefixLine = (($fm -split "`n") | Where-Object { $_ -match '^\s*error_code_prefixes\s*:' } | Select-Object -First 1)
    if ($null -eq $prefixLine) {
      $fails += 'frontmatter error_code_prefixes line missing'
    } else {
      foreach ($pfx in @('CEO_', 'CTO_', 'CISO_', 'CHO_', 'CQO_', 'SCL_')) {
        if ($prefixLine -notmatch [regex]::Escape($pfx)) { $fails += "error_code_prefixes is missing $pfx" }
      }
    }
    # E2 : interface.department.enum must list exactly 'auto' plus the 5
    # small-tier department slugs (item count = department_count + 1), with
    # no retired slug left behind - otherwise the frontmatter contradicts
    # itself and the new departments are unreachable through the interface.
    $enumLine = (($fm -split "`n") | Where-Object { $_ -match '^\s*enum\s*:\s*\[' } | Select-Object -First 1)
    if ($null -eq $enumLine) {
      $fails += 'frontmatter interface.department.enum line missing'
    } else {
      $enumMatch = [regex]::Match($enumLine, 'enum\s*:\s*\[([^\]]*)\]')
      $enumItems = @()
      if ($enumMatch.Success) {
        $enumItems = @($enumMatch.Groups[1].Value -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
      }
      $expectedEnum = @('auto') + @($UpgradeEdge.Split | ForEach-Object { [string]$_.Slug })
      if ($enumItems.Count -ne ($expectedEnum.Count)) {
        $fails += ("interface.department.enum has {0} item(s), expected {1} (auto + department_count)" -f $enumItems.Count, $expectedEnum.Count)
      }
      foreach ($item in $enumItems) {
        if ($expectedEnum -notcontains $item) {
          $fails += "interface.department.enum contains an item outside the small-tier department list: '$item'"
        }
      }
      foreach ($expected in $expectedEnum) {
        if ($enumItems -notcontains $expected) {
          $fails += "interface.department.enum is missing the required item '$expected'"
        }
      }
    }
  }

  # Version agreement in the four required locations (H15).
  $metaPath = Join-Path $PkgDir '_meta.json'
  if (-not (Test-Path -LiteralPath $metaPath)) {
    $fails += '_meta.json missing from the package'
  } else {
    try {
      $meta = ConvertFrom-Json ([System.IO.File]::ReadAllText($metaPath))
      if ([string]$meta.version -ne $UpgradeEdge.NewVersion) { $fails += "_meta.json version is '$($meta.version)', expected $($UpgradeEdge.NewVersion)" }
    } catch { $fails += '_meta.json is not valid JSON' }
  }
  $readmePath = Join-Path $PkgDir 'README.md'
  if (Test-Path -LiteralPath $readmePath) {
    $rText = Read-TextFile -Path $readmePath
    # E18 : the badge must match the concrete shields.io format, not just
    # contain the version string somewhere in the file.
    if (($null -eq $rText) -or (-not ([regex]::IsMatch($rText, 'version-2\.0\.0-blue')))) { $fails += 'README.md badge does not match the expected format version-2.0.0-blue' }
  } else {
    $fails += 'README.md missing from the package'
  }
  $pkgSk = Read-TextFile -Path (Join-Path $PkgDir 'SKILL.md')
  if (($null -eq $pkgSk) -or (-not $pkgSk.Contains($UpgradeEdge.NewVersion))) { $fails += 'SKILL.md body does not contain version 2.0.0 (title)' }

  # Target-tier department D2 files present.
  $pkgDeptDir = Join-Path $PkgDir 'references\departments'
  foreach ($t in $UpgradeEdge.Split) {
    $p = Join-Path $pkgDeptDir ([string]$t.Slug + '.md')
    if (-not (Test-Path -LiteralPath $p)) { $fails += "department D2 file missing: references/departments/$($t.Slug).md" }
  }

  # E1 : the small-tier third prompt must exist, be agent-invoked, and declare
  # a harness level >= L3 (README-FOR-AI.md sec 11.3 A4 / sec 11.1 S-tier prompt count).
  $thirdPromptPath = Join-Path $PkgDir 'prompts\03-test-cases.md'
  if (-not (Test-Path -LiteralPath $thirdPromptPath)) {
    $fails += 'prompts/03-test-cases.md missing from the package (S tier requires 3 prompts)'
  } else {
    $tp = Read-TextFile -Path $thirdPromptPath
    if ($null -eq $tp) {
      $fails += 'prompts/03-test-cases.md is not readable'
    } else {
      if (-not ([regex]::IsMatch($tp, '(?m)^mode\s*:\s*agent-invoked\s*$'))) { $fails += 'prompts/03-test-cases.md mode is not agent-invoked' }
      $harnessMatch = [regex]::Match($tp, '(?m)^harness_level\s*:\s*L(\d)\s*$')
      if (-not $harnessMatch.Success) {
        $fails += 'prompts/03-test-cases.md has no harness_level declaration'
      } elseif ([int]$harnessMatch.Groups[1].Value -lt 3) {
        $fails += 'prompts/03-test-cases.md harness_level is below L3'
      }
    }
  }

  if ($fails.Count -gt 0) {
    return @{ Passed = $false; Detail = ($fails -join '; ') ; FailedItems = $fails }
  }
  return @{ Passed = $true; Detail = "file_count=$fileCount; frontmatter triple consistent; version 2.0.0 agrees in all 4 locations (badge format verified); 5 D2 files present; prefixes complete; interface enum consistent (auto + 5 slugs); prompts/03-test-cases.md agent-invoked L3"; FailedItems = @() }
}

# --------------------------------------------------------------------------------------
# Proposal report (step 7, template README-FOR-AI.md sec 12)
# --------------------------------------------------------------------------------------

function New-ProposalReport {
  param([string]$PkgDir, [string]$PkgName, $Triggers, $GateResults, $Metrics)
  $now = Get-UtcNowIso
  # E1 : build residues (__pycache__/, *.pyc) are not package files and are
  # excluded from this count, exactly as the package copy excludes them.
  $curFileCount = @(Get-ChildItem -LiteralPath $SkillDir -Recurse -File -Force -ErrorAction SilentlyContinue |
    Where-Object { ($_.FullName.Substring($SkillDir.Length + 1).Replace('\', '/') -notmatch '(^|/)__pycache__/') -and ($_.Name -notmatch '\.pyc$') }).Count
  $triggerText = 'SCL_001: forced proposal; no threshold was met (invoked with -Force / propose)'
  if ($Triggers.Count -gt 0) {
    $parts = @()
    foreach ($t in $Triggers) {
      $parts += ("{0}: {1} = {2}, threshold {3}" -f $t.Id, $t.Metric, $t.Value, $t.Threshold)
    }
    $triggerText = $parts -join '; '
    $t3t4 = @($Triggers | Where-Object { ($_.Id -eq 'T3') -or ($_.Id -eq 'T4') })
    $t1 = @($Triggers | Where-Object { $_.Id -eq 'T1' })
    if (($t3t4.Count -gt 0) -and ($t1.Count -eq 0)) {
      $triggerText += ' | Note: capacity has not overflowed, but the structure no longer fits.'
    }
  }
  $permHash = Get-TextSha256 (Get-FrontmatterSubBlock -FrontmatterText (Get-FrontmatterText (Join-Path $SkillDir 'SKILL.md')) -Key 'permissions')
  $gateLines = @()
  foreach ($g in @('G1', 'G2', 'G3', 'G4', 'G5', 'G6')) {
    $r = $GateResults[$g]
    $mark = 'FAILED'
    if ($r.Passed) { $mark = 'PASSED' }
    $gateLines += ("| {0} | {1} | {2} |" -f $g, $mark, $r.Detail)
  }
  $report = @"
# Tier Upgrade Proposal: micro -> small

> Generated by scripts/self-scale.ps1 (propose-only). This proposal has NOT taken effect.

| Item | Value |
|---|---|
| Proposal time | $now |
| Current tier | micro (2 departments, 18 function blocks, $curFileCount files) |
| Target tier | small (5 departments, 18 function blocks, 29 files expected) |
| Trigger reason | $triggerText |
| Package path | {WORKSPACE_ROOT}/.skill-upgrade/$PkgName/ |
| Status | PENDING APPROVAL - NOT EFFECTIVE |

## Change list

| Type | Count | Notes |
|---|---|---|
| New department D2 files | 5 | governance-and-operations, quality-and-delivery, technology-and-platform, security-and-compliance, people-and-growth |
| Retired department D2 files | 2 | governance-and-delivery, engineering-and-safety (slugs preserved as aliases) |
| New department D3 files | 0 | Not applicable (target tier < large) |
| New prompts | 1 | prompts/03-test-cases.md (agent-invoked, harness level L3, listed in the SKILL.md Prompts index) |
| Frontmatter rewritten | 1 | scale_tier / department_count / function_block_count / version / error_code_prefixes / department_aliases pointer / interface.department.enum / description |
| Revived error-code prefixes | 3 | CISO_, CHO_, CQO_ |
| Error-code alias skeleton | 1 table | 24 legacy-code rows appended to references/error-codes.md, every row marked "requires human review" |
| Aliases added | 5 | See the Alias Map in references/scaling.md |
| Governance files updated | <=4 | CHANGELOG.md entry inserted after [Unreleased]; version strings bumped (counted, context-exact) and Project Structure tree rewritten to the 29-file skeleton in SKILL.md index / README*.md |

## Frontmatter diff note

The permissions block and the language_policy block are copied unchanged; the
permissions block hash is verified identical by gate G1 ($permHash). The
structural fields change exactly as listed above. A full unified diff is
produced by the human review tooling; the script deliberately does not
fabricate one.

## Human review items (cannot be machine-verified by this build)

1. Error-code remapping from CEO_ / CTO_ to the revived CISO_ / CHO_ / CQO_
   prefixes in references/error-codes.md. The alias-table skeleton (24 rows)
   has been generated; every "requires human review" cell must be completed
   with the real new code, and the file header counts updated (step 5e).
2. README Project Structure trees have been rewritten to the 29-file
   small-tier skeleton in README.md / README.en.md / README.zh.md; the
   remaining narrative claims (department names, block split, quick-start
   wording) still describe the micro layout and require human review (step 5i).
3. Department D2 pages produced by the deterministic split keep the legacy
   preamble wording; a human should confirm each page's non-FB narrative
   matches its new department scope.
4. Full acceptance (README-FOR-AI.md sec 15; content groups A-G, H, I, U) on
   the package. The pending proposal records acceptance_passed = false until
   this is done.

## Gate results

| Gate | Result | Detail |
|---|---|---|
$(($gateLines -join "`n"))

## Installation instructions (execute only after human approval)

The skill itself never installs. An external trusted installer must:

    Copy-Item the package to a temporary directory
    -> verify integrity (file count, hashes)
    -> atomically replace the skill directory
    -> only delete the old directory after confirming success.

Forbidden: Remove-Item -Path {SKILL_DIR} -Recurse -Force followed by a restore
(P23). Backup directories must be cross-platform: fall back from
`$env:USERPROFILE to `$HOME when the former is empty (P26).

## Rollback

If problems are found after installation, restore the pre-upgrade backup made
by the installer (see above). The pre-upgrade state is also recoverable from
the tier_history entry recorded in .scaling-state.json at install time.
"@
  $reportPath = Join-Path $PkgDir 'UPGRADE-PROPOSAL.md'
  Write-TextFileNoBom -Path $reportPath -Text $report
  Write-Log "7 upgrade report written: $reportPath"
}

# --------------------------------------------------------------------------------------
# Main flows
# --------------------------------------------------------------------------------------

function Show-Status {
  $state = Read-State
  $config = Load-Config
  $metrics = Get-CurrentMetrics -State $state
  Write-Output '=== self-scale status ==='
  Write-Output ("current_tier            : {0}" -f $state.current_tier)
  Write-Output ("next_evaluation         : {0}" -f $state.next_evaluation)
  Write-Output ("agent_count             : {0}" -f $metrics.AgentCount)
  Write-Output ("routing_accuracy        : {0}" -f $metrics.RoutingAccuracy)
  Write-Output ("max_blocks_per_dept     : {0}" -f $metrics.MaxBlocks)
  Write-Output ("error_code_reuse_ratio  : {0}" -f $metrics.ReuseRatio)
  Write-Output ("upgrade_policy          : {0}" -f 'propose-only')
  Write-Output ("tier_history entries    : {0}" -f @($state.tier_history).Count)
  Write-Output ("pending_proposals       : {0}" -f @($state.pending_proposals).Count)
  exit 0
}

function Show-Report {
  $state = Read-State
  $pending = @($state.pending_proposals)
  if ($pending.Count -eq 0) {
    Write-Output 'No pending proposals. Run -Action evaluate or -Action propose first.'
    exit 0
  }
  $latest = $pending[$pending.Count - 1]
  Write-Output ("Latest pending proposal: {0} -> {1} (proposed {2})" -f $latest.from_tier, $latest.to_tier, $latest.proposed_at)
  $reportPath = Join-Path $latest.package_path 'UPGRADE-PROPOSAL.md'
  if (Test-Path -LiteralPath $reportPath) {
    Write-Output '---'
    Write-Output (Read-TextFile -Path $reportPath)
  } else {
    Write-Output "Report file not found at: $reportPath"
  }
  exit 0
}

function Invoke-Proposal {
  param($State, $Metrics, $Triggers, $Config, [int]$RoutingMissStreak)

  # --- Step 4 : deterministic merge-tree lookup -------------------------------
  Write-Log '4 looking up the upgrade path in the merge tree (deterministic, no improvisation)...'
  if ([string]$State.current_tier -eq 'group') {
    Stop-WithCode 'SCL_009' 'already at the highest tier (group); no upgrade path exists'
  }
  if ([string]$State.current_tier -ne $UpgradeEdge.From) {
    Stop-WithCode 'SCL_002' ("no upgrade mapping defined for tier '{0}' in this build (only {1} -> {2})" -f $State.current_tier, $UpgradeEdge.From, $UpgradeEdge.To)
  }
  Write-Log ("4 upgrade path: {0} -> {1} (departments 2 -> 5, function blocks 18 -> 18, major {2} -> {3})" -f $UpgradeEdge.From, $UpgradeEdge.To, $UpgradeEdge.OldVersion, $UpgradeEdge.NewVersion)

  # --- Step 5 : generate the upgrade package -----------------------------------
  $pkgName = (Get-Date).ToString('yyyyMMdd-HHmmss')
  $outputRoot = $Config.OutputDir.Replace('{WORKSPACE_ROOT}', $WorkspaceRoot)
  $pkgDir = Join-Path $outputRoot $pkgName

  if ($DryRun) {
    Write-Log "DRY-RUN: would generate the upgrade package in $pkgDir"
    Write-Log 'DRY-RUN: 5h copy the package (excluding .scaling-state.json, retired D2, __pycache__/, *.pyc)'
    Write-Log 'DRY-RUN: 5a/5b split 2 legacy D2 pages into 5 departments (18 blocks conserved; leftover/shortage aborts with SCL_010)'
    Write-Log 'DRY-RUN: 5a generate prompts/03-test-cases.md (agent-invoked, L3)'
    Write-Log 'DRY-RUN: 5d rewrite frontmatter (scale_tier=small, department_count=5, version=2.0.0, enum + description)'
    Write-Log 'DRY-RUN: 5e bump _meta.json; append the error-code alias-table skeleton (requires human review)'
    Write-Log 'DRY-RUN: 5g append 5 alias rows to the package Alias Map'
    Write-Log 'DRY-RUN: 5i bump README versions (counted, context-exact); rewrite structure trees to the 29-file skeleton; insert the CHANGELOG entry after [Unreleased]'
    Write-Log 'DRY-RUN: package state file with tier_history skeleton entry (append-only)'
    Write-Log 'DRY-RUN: 6 run gates G1-G6 on the package'
    Write-Log 'DRY-RUN: 7 write UPGRADE-PROPOSAL.md; 8 stop (no install)'
    exit 0
  }

  if (-not (Test-Path -LiteralPath $outputRoot)) {
    New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
  }
  New-Item -ItemType Directory -Path $pkgDir -Force | Out-Null
  Write-Log ("5 generating upgrade package in {0}" -f $pkgDir)
  New-UpgradePackage -PkgDir $pkgDir

  # --- Step 6 : the six gates, one independent branch each (README-FOR-AI.md sec 12.3) ---
  Write-Log '6 running gates G1-G6 on the upgrade package...'
  $gateResults = @{}
  $failedGates = @()

  $g1 = Invoke-GateG1 -PkgDir $pkgDir
  $gateResults['G1'] = $g1
  if ($g1.Passed) { Write-Log 'G1 PASSED' } else { Write-Log 'G1 FAILED'; $failedGates += 'G1' }

  $g2 = Invoke-GateG2 -PkgDir $pkgDir
  $gateResults['G2'] = $g2
  if ($g2.Passed) { Write-Log 'G2 PASSED' } else { Write-Log 'G2 FAILED'; $failedGates += 'G2' }

  $g3 = Invoke-GateG3 -PkgDir $pkgDir
  $gateResults['G3'] = $g3
  if ($g3.Passed) { Write-Log 'G3 PASSED' } else { Write-Log 'G3 FAILED'; $failedGates += 'G3' }

  $g4 = Invoke-GateG4 -PkgDir $pkgDir
  $gateResults['G4'] = $g4
  if ($g4.Passed) { Write-Log 'G4 PASSED' } else { Write-Log 'G4 FAILED'; $failedGates += 'G4' }

  $g5 = Invoke-GateG5 -PkgDir $pkgDir
  $gateResults['G5'] = $g5
  if ($g5.Passed) { Write-Log 'G5 PASSED' } else { Write-Log 'G5 FAILED'; $failedGates += 'G5' }

  $g6 = Invoke-GateG6 -PkgDir $pkgDir
  $gateResults['G6'] = $g6
  if ($g6.Passed) { Write-Log 'G6 PASSED' } else { Write-Log 'G6 FAILED'; $failedGates += 'G6' }

  if ($failedGates.Count -gt 0) {
    $codeByGate = @{ 'G1' = 'SCL_004'; 'G2' = 'SCL_005'; 'G3' = 'SCL_004'; 'G4' = 'SCL_010'; 'G5' = 'SCL_003'; 'G6' = 'SCL_006' }
    $code = $codeByGate[$failedGates[0]]
    # Recoverable quarantine (P23): the package is moved aside, never destroyed.
    $rejectedRoot = Join-Path $outputRoot '_rejected'
    if (-not (Test-Path -LiteralPath $rejectedRoot)) {
      New-Item -ItemType Directory -Path $rejectedRoot -Force | Out-Null
    }
    $rejectedDir = Join-Path $rejectedRoot ($pkgName + '-' + $code)
    Move-Item -LiteralPath $pkgDir -Destination $rejectedDir
    Write-Log ("6 FATAL $code : gate(s) failed: {0}; package quarantined at {1}" -f ($failedGates -join ', '), $rejectedDir)
    # Failure record in the state file.
    Set-StateProperty -State $State -Name 'last_failure' -Value ([ordered]@{
      at = (Get-UtcNowIso)
      code = $code
      gates_failed = $failedGates
      package_path = $rejectedDir
    })
    Save-State -State $State
    exit 3
  }

  # --- Step 7 : upgrade report ---------------------------------------------------
  New-ProposalReport -PkgDir $pkgDir -PkgName $pkgName -Triggers $Triggers -GateResults $gateResults -Metrics $Metrics

  # --- Step 5j / step 8 : record the proposal, stop (no install) ------------------
  $proposal = [ordered]@{
    proposal_id = $pkgName
    from_tier = $UpgradeEdge.From
    to_tier = $UpgradeEdge.To
    proposed_at = (Get-UtcNowIso)
    trigger_reasons = @()
    package_path = $pkgDir
    status = 'pending'
    approved_by = $null
    installed_at = $null
    validation = [ordered]@{
      file_count = $TargetFileCount[$UpgradeEdge.To]
      function_blocks = 18
      gates_passed = 6
      # E6 : honest pending record. The machine-checkable gates passed, but the
      # full README-FOR-AI.md sec 15 acceptance (content groups A-G, H, I, U) has NOT been
      # performed by a human yet. The external installer sets this to true only
      # after the human acceptance is completed at install time.
      acceptance_passed = $false
    }
  }
  foreach ($t in $Triggers) {
    $proposal.trigger_reasons += ("{0}: {1} = {2} (threshold {3})" -f $t.Id, $t.Metric, $t.Value, $t.Threshold)
  }
  if ($Triggers.Count -eq 0) { $proposal.trigger_reasons += 'SCL_001: forced proposal, no threshold met' }
  Set-StateProperty -State $State -Name 'pending_proposals' -Value (@($State.pending_proposals) + $proposal)
  Set-StateProperty -State $State -Name 'last_metrics' -Value ([ordered]@{
    agent_count = $Metrics.AgentCount
    routing_accuracy = $Metrics.RoutingAccuracy
    max_blocks_per_department = $Metrics.MaxBlocks
    error_code_reuse_ratio = $Metrics.ReuseRatio
  })
  Set-StateProperty -State $State -Name 'routing_miss_streak' -Value $RoutingMissStreak
  Save-State -State $State

  Write-Log '8 STOP - proposal generated, NOT EFFECTIVE.'
  Write-Log '8 The proposal is pending in .scaling-state.json (approved_by / installed_at empty).'
  Write-Log '8 Human approval followed by an external installer is required before anything takes effect.'
  Write-Log '8 The skill directory content was not modified; no install was performed.'
  exit 0
}

function Invoke-EvaluateFlow {
  # --- Step 1 : read the state file ----------------------------------------------
  Write-Log '1 reading .scaling-state.json...'
  $state = Read-State
  Write-Log ("1 current_tier={0}, next_evaluation={1}, pending_proposals={2}" -f $state.current_tier, $state.next_evaluation, @($state.pending_proposals).Count)

  # --- Step 2 : collect metrics, evaluate T1-T4 ----------------------------------
  Write-Log '2 collecting the four scaling metrics and evaluating thresholds T1-T4...'
  $config = Load-Config
  $metrics = Get-CurrentMetrics -State $state
  $evaluation = Invoke-ThresholdEvaluation -State $state -Metrics $metrics -Config $config
  $triggers = $evaluation.Triggers

  # --- Step 3 : no trigger -> refresh the state and exit --------------------------
  if ($triggers.Count -eq 0) {
    if (-not $Force) {
      Write-Log '3 no threshold hit - updating next_evaluation and last_metrics, then exiting.'
      $next = (Get-Date).ToUniversalTime().AddDays($config.IntervalDays).ToString('yyyy-MM-ddTHH:mm:ssZ')
      Set-StateProperty -State $state -Name 'next_evaluation' -Value $next
      Set-StateProperty -State $state -Name 'last_metrics' -Value ([ordered]@{
        agent_count = $metrics.AgentCount
        routing_accuracy = $metrics.RoutingAccuracy
        max_blocks_per_department = $metrics.MaxBlocks
        error_code_reuse_ratio = $metrics.ReuseRatio
      })
      Set-StateProperty -State $state -Name 'routing_miss_streak' -Value $evaluation.RoutingMissStreak
      Save-State -State $state
      Write-Log '3 done. No proposal generated.'
      exit 0
    }
    Write-Log 'SCL_001 WARNING: forced invocation, but no threshold was hit; generating a proposal anyway.'
  } else {
    foreach ($t in $triggers) {
      Write-Log ("2 TRIGGERED {0} ({1}): {2} = {3}, threshold {4}" -f $t.Id, $t.Name, $t.Metric, $t.Value, $t.Threshold)
    }
  }

  # --- Steps 4-8 : generate the proposal ------------------------------------------
  Invoke-Proposal -State $state -Metrics $metrics -Triggers $triggers -Config $config -RoutingMissStreak $evaluation.RoutingMissStreak
}

function Invoke-ProposeFlow {
  Write-Log '1 reading .scaling-state.json...'
  $state = Read-State
  Write-Log '2 collecting metrics for the proposal report...'
  $config = Load-Config
  $metrics = Get-CurrentMetrics -State $state
  $evaluation = Invoke-ThresholdEvaluation -State $state -Metrics $metrics -Config $config
  $triggers = $evaluation.Triggers
  if ($triggers.Count -eq 0) {
    Write-Log 'SCL_001 WARNING: explicit propose action, but no threshold was hit; the report will carry the SCL_001 note.'
  }
  Invoke-Proposal -State $state -Metrics $metrics -Triggers $triggers -Config $config -RoutingMissStreak $evaluation.RoutingMissStreak
}

# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

switch ($Action) {
  'status'   { Show-Status }
  'report'   { Show-Report }
  'evaluate' { Invoke-EvaluateFlow }
  'propose'  { Invoke-ProposeFlow }
}
