param(
    [Parameter(Mandatory = $false)]
    [string]$TargetPath = "C:\",
    [Parameter(Mandatory = $false)]
    [string]$OutputDir = "outputs\win_c_audit",
    [Parameter(Mandatory = $false)]
    [string]$ConfigPath = "config\defaults.json"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $repoRoot
try {
    python -m dirstat_skill.cli audit --path $TargetPath --output-dir $OutputDir --config $ConfigPath
}
finally {
    Pop-Location
}
