# COM PNG export template (1920x1080) -- safe version
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File export_png_template.ps1 -PptxPath <ascii path to .pptx> [-OutDir <dir>]
# Safety rules (ClawHub T09 remediation):
#   1. NEVER deletes existing files. Output goes to a run-specific directory.
#   2. Default OutDir = <pptx folder>\png_<yyyyMMdd_HHmmss> (unique per run).
#   3. COM objects are cleaned up in finally, independent of export success.
param(
    [Parameter(Mandatory = $true)][string]$PptxPath,
    [string]$OutDir = ""
)
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $PptxPath)) { throw "PptxPath not found: $PptxPath" }

if ($OutDir -eq "") {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $OutDir = Join-Path (Split-Path -Parent (Resolve-Path -LiteralPath $PptxPath).Path) ("png_" + $stamp)
}
$OutDir = [System.IO.Path]::GetFullPath($OutDir)
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

$app = $null
$pres = $null
$count = 0
try {
    $app = New-Object -ComObject PowerPoint.Application
    $pres = $app.Presentations.Open((Resolve-Path -LiteralPath $PptxPath).Path, $true, $false, $false)
    $i = 0
    foreach ($slide in $pres.Slides) {
        $i++
        $png = Join-Path $OutDir ("slide_" + $i + ".png")
        $slide.Export($png, 'PNG', 1920, 1080)
        Write-Output ("exported " + $png)
    }
    $count = $i
}
finally {
    if ($null -ne $pres) { $pres.Close() }
    if ($null -ne $app) { $app.Quit() }
}
Write-Output ("slides=" + $count)
