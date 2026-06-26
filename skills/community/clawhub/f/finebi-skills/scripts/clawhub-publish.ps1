$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$packageDir = Resolve-Path (Join-Path $scriptDir "..")

Set-Location $packageDir

if ($args -contains "--dry-run") {
  Write-Error "ClawHub CLI does not support --dry-run for skill publish."
}

$pkg = Get-Content -Path "package.json" -Raw | ConvertFrom-Json

Remove-Item Env:npm_config_dir -ErrorAction SilentlyContinue
Remove-Item Env:npm_config_workspace_dir -ErrorAction SilentlyContinue
Remove-Item Env:npm_config_prefix -ErrorAction SilentlyContinue
Remove-Item Env:npm_config_userconfig -ErrorAction SilentlyContinue
Remove-Item Env:npm_config_local_prefix -ErrorAction SilentlyContinue

& npx clawhub `
  --workdir . `
  --dir . `
  skill publish . `
  --slug finebi-skills `
  --name "FineBI Skills" `
  --version $pkg.version `
  --tags latest

exit $LASTEXITCODE
