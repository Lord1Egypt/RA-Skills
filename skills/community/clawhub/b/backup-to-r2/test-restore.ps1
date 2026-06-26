$ErrorActionPreference = 'Stop'

# ============================================================
# Testa o restore SEM tocar na sua instalacao do OpenClaw.
# Baixa o backup mais recente do R2, extrai e valida com
# "openclaw backup verify". A pasta restaurada fica intacta
# pra voce inspecionar.
# ============================================================

$BaseDir = $PSScriptRoot

$ResticExe = (Get-Command restic -ErrorAction SilentlyContinue).Source
if (-not $ResticExe) { $ResticExe = Join-Path $BaseDir 'restic\restic.exe' }
if (-not (Test-Path $ResticExe)) { throw "restic nao encontrado." }

$OpenClaw = (Get-Command openclaw -ErrorAction SilentlyContinue).Source
if (-not $OpenClaw) { $OpenClaw = Join-Path $env:APPDATA 'npm\openclaw.cmd' }

# valida arquivos obrigatorios antes de comecar
$EnvFile = Join-Path $BaseDir '.env'
$PassFile = Join-Path $BaseDir '.restic-pass'
if (-not (Test-Path $EnvFile)) { throw "Arquivo nao encontrado: $EnvFile (copie .env.example para .env e preencha)." }
if (-not (Test-Path $PassFile)) { throw "Arquivo nao encontrado: $PassFile (crie com a senha do repositorio restic)." }

# carrega credenciais R2
Get-Content $EnvFile | ForEach-Object {
  $line = $_.Trim()
  if (-not $line -or $line.StartsWith('#')) { return }
  $name, $value = $line.split('=', 2)
  if ($name) { Set-Item -Path "env:$($name.Trim())" -Value $value.Trim() }
}
Set-Item -Path 'env:RESTIC_PASSWORD_FILE' -Value $PassFile
if ($env:RESTIC_REPOSITORY -and -not ($env:RESTIC_REPOSITORY -match '^s3:')) {
  if ($env:RESTIC_REPOSITORY -match '^https?://') {
    $env:RESTIC_REPOSITORY = 's3:' + $env:RESTIC_REPOSITORY.TrimEnd('/')
  }
}

$RestoreDir = Join-Path $BaseDir ('restore-test-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $RestoreDir -Force | Out-Null

Write-Host "`n=== 1) restic check ===" -ForegroundColor Cyan
& $ResticExe check
if ($LASTEXITCODE -ne 0) { throw "restic check falhou (exit $LASTEXITCODE) - repositorio inacessivel ou credenciais erradas." }

Write-Host "`n=== 2) snapshots (preview) ===" -ForegroundColor Cyan
& $ResticExe snapshots --tag openclaw
if ($LASTEXITCODE -ne 0) { throw "restic snapshots falhou (exit $LASTEXITCODE)." }

# mesma selecao do restore real (restore-portable.ps1): latest com tag openclaw
Write-Host "`n=== 3) restore latest (tag openclaw) ===" -ForegroundColor Cyan
& $ResticExe restore latest --tag openclaw --target $RestoreDir
if ($LASTEXITCODE -ne 0) { throw "restic restore falhou (exit $LASTEXITCODE)." }

$restoredTar = Get-ChildItem $RestoreDir -Recurse -Filter '*-openclaw-backup.tar.gz' | Select-Object -First 1
if (-not $restoredTar) { Write-Host 'Nao encontrei tar.gz restaurado!' -ForegroundColor Red; exit 1 }
Write-Host "Tar restaurado: $($restoredTar.FullName)" -ForegroundColor Green

Write-Host "`n=== 4) openclaw backup verify (PROVA REAL) ===" -ForegroundColor Cyan
& $OpenClaw backup verify $restoredTar.FullName

if ($LASTEXITCODE -eq 0) {
  Write-Host "`n[OK] RESTORE TESTADO E VALIDADO pelo OPENCLAW" -ForegroundColor Green
  Write-Host "Pasta de teste: $RestoreDir" -ForegroundColor Yellow
  Write-Host "ATENCAO: ela contem seus dados DESCRIPTOGRAFADOS (credenciais em texto puro). Apague-a quando terminar de inspecionar." -ForegroundColor Yellow
} else {
  Write-Host "`n[FALHA] verify retornou erro - investigar!" -ForegroundColor Red
  exit 1
}
