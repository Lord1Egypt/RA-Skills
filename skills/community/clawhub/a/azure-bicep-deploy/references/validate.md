# Validate Script

PowerShell script for validating Bicep/ARM templates.

## Usage

```powershell
# Validate Bicep syntax
.\validate.ps1 -TemplateFile main.bicep

# Validate with What-If
.\validate.ps1 -TemplateFile main.bicep -ResourceGroupName my-rg -WhatIf
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| TemplateFile | Yes | Path to .bicep or .json template |
| ResourceGroupName | No | Azure resource group for What-If |
| WhatIf | No | Run What-If deployment analysis |

## Full Script Content

```powershell
# Validate Bicep/ARM Template Script
# Usage: .\validate.ps1 -TemplateFile <file> [-ResourceGroupName <rg>]

param(
    [Parameter(Mandatory=$true)]
    [string]$TemplateFile,

    [string]$ResourceGroupName = "",

    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

$extension = [System.IO.Path]::GetExtension($TemplateFile)

if ($extension -eq ".bicep") {
    Write-Host "Validating Bicep syntax: $TemplateFile" -ForegroundColor Cyan
    
    # Build Bicep command
    $command = "az bicep build --file $TemplateFile"
    Write-Host "Running: $command" -ForegroundColor Gray
    
    Invoke-Expression $command
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Bicep syntax validation failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Bicep syntax is valid!" -ForegroundColor Green
}

# ARM template validation (JSON)
if ($extension -eq ".json") {
    Write-Host "Validating ARM template: $TemplateFile" -ForegroundColor Cyan
    
    # Check valid JSON
    try {
        $content = Get-Content $TemplateFile -Raw | ConvertFrom-Json
        Write-Host "JSON syntax is valid!" -ForegroundColor Green
    } catch {
        Write-Host "JSON validation failed: $_" -ForegroundColor Red
        exit 1
    }
}

# What-If deployment (requires ResourceGroupName)
if ($WhatIf -and -not [string]::IsNullOrEmpty($ResourceGroupName)) {
    Write-Host "`nRunning What-If deployment analysis..." -ForegroundColor Yellow
    
    $command = "az deployment group what-if --resource-group $ResourceGroupName --template-file $TemplateFile"
    
    if (Test-Path "params/dev.json") {
        $command += " --parameters @params/dev.json"
    }
    
    Write-Host "Running: $command" -ForegroundColor Gray
    
    Invoke-Expression $command
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "What-If analysis failed!" -ForegroundColor Red
        exit 1
    }
} elseif ($WhatIf -and [string]::IsNullOrEmpty($ResourceGroupName)) {
    Write-Host "What-If requires a ResourceGroupName. Skipping..." -ForegroundColor Yellow
}

Write-Host "`nValidation complete!" -ForegroundColor Green
```