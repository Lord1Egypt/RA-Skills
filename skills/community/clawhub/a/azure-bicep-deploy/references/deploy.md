# Deploy Script

PowerShell script for deploying Bicep/ARM templates.

## Usage

```powershell
# Deploy dev environment
.\deploy.ps1 -ResourceGroupName my-rg -TemplateFile main.bicep -Environment dev

# Deploy staging with what-if
.\deploy.ps1 -ResourceGroupName my-rg -TemplateFile main.bicep -Environment staging -WhatIf

# Deploy prod
.\deploy.ps1 -ResourceGroupName my-rg -TemplateFile main.bicep -Environment prod
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| ResourceGroupName | Yes | Azure resource group name |
| TemplateFile | Yes | Path to .bicep or .json template |
| Environment | No | dev/staging/prod (default: dev) |
| ParametersFile | No | Custom parameters file path |
| WhatIf | No | Run what-if analysis before deploying |

## Environment Parameters

Place parameter files in `params/` folder:
- `params/dev.json`
- `params/staging.json`
- `params/prod.json`

## Full Script Content

```powershell
# Azure Bicep Deployment Script
# Usage: .\deploy.ps1 -ResourceGroupName <rg> -TemplateFile <bicep> [-Environment dev|staging|prod] [-ParametersFile <path>]

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,

    [Parameter(Mandatory=$true)]
    [string]$TemplateFile,

    [string]$Environment = "dev",

    [string]$ParametersFile = "",

    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

# Check Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Error "Azure CLI not found. Install from https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
}

# Check Bicep
if (-not (Get-Command bicep -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Bicep CLI..."
    az bicep install
}

# Build parameters file path if not provided
$envFile = "params/$Environment.json"
if ([string]::IsNullOrEmpty($ParametersFile) -and (Test-Path $envFile)) {
    $ParametersFile = $envFile
}

# Build the deployment command
$deploymentName = "bicep-deploy-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$command = "az deployment group create --resource-group $ResourceGroupName --name $deploymentName --template-file $TemplateFile"

if (-not [string]::IsNullOrEmpty($ParametersFile)) {
    $command += " --parameters @$ParametersFile"
}

Write-Host "Environment: $Environment" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Cyan
Write-Host "Template: $TemplateFile" -ForegroundColor Cyan
Write-Host ""

if ($WhatIf) {
    Write-Host "Running What-If analysis..." -ForegroundColor Yellow
    $command = $command -replace "deployment group create", "deployment group what-if"
}

Write-Host "Executing: $command" -ForegroundColor Gray
Write-Host ""

# Execute
Invoke-Expression $command

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDeployment completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nDeployment failed!" -ForegroundColor Red
    exit 1
}
```