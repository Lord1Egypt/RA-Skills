# Bicep Build Script

PowerShell script for building Bicep files to ARM JSON templates.

## Usage

```powershell
# Build Bicep to ARM JSON
.\bicep-build.ps1 -BicepFile main.bicep

# Specify output file
.\bicep-build.ps1 -BicepFile main.bicep -OutputFile arm-template.json
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| BicepFile | Yes | Path to .bicep file |
| OutputFile | No | Output ARM JSON path (default: same name, .json extension) |

## Full Script Content

```powershell
# Build Bicep to ARM Template
# Usage: .\bicep-build.ps1 -BicepFile <file> [-OutputFile <arm.json>]

param(
    [Parameter(Mandatory=$true)]
    [string]$BicepFile,

    [string]$OutputFile = ""
)

$ErrorActionPreference = "Stop"

# Check Bicep
if (-not (Get-Command bicep -ErrorAction SilentlyContinue)) {
    Write-Error "Bicep CLI not found. Install with: az bicep install"
    exit 1
}

# Default output path
if ([string]::IsNullOrEmpty($OutputFile)) {
    $OutputFile = [System.IO.Path]::ChangeExtension($BicepFile, ".json")
}

Write-Host "Building Bicep file: $BicepFile" -ForegroundColor Cyan
Write-Host "Output ARM template: $OutputFile" -ForegroundColor Cyan

$command = "az bicep build --file $BicepFile --outfile $OutputFile"
Write-Host "Running: $command" -ForegroundColor Gray

Invoke-Expression $command

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nBuild successful! ARM template written to: $OutputFile" -ForegroundColor Green
```