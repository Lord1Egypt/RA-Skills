$ErrorActionPreference = 'Stop'

# ============================================================
# Restore PORTATIL do OpenClaw a partir do repositorio restic
# no Cloudflare R2. Funciona em QUALQUER PC.
#
# Coloque nesta mesma pasta:
#   restic\restic.exe   (binario do restic)
#   .env                (credenciais R2 + RESTIC_REPOSITORY)
#   .restic-pass        (senha do repositorio)
#
# O script: baixa o backup mais recente do R2, extrai e
# instala em %USERPROFILE%\.openclaw, preservando a pasta
# atual como .openclaw.backup-<data> antes de sobrescrever.
# ============================================================

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ResticExe = Join-Path $Root 'restic\restic.exe'
$EnvFile = Join-Path $Root '.env'
$PassFile = Join-Path $Root '.restic-pass'

if (!(Test-Path $ResticExe)) { throw "Missing: $ResticExe" }
if (!(Test-Path $EnvFile)) { throw "Missing: $EnvFile" }
if (!(Test-Path $PassFile)) { throw "Missing: $PassFile" }

Get-Content $EnvFile | ForEach-Object {
  $line = $_.Trim()
  if (!$line -or $line.StartsWith('#')) { return }
  $n,$v = $line.split('=',2)
  if ($n) { Set-Item -Path "env:$($n.Trim())" -Value $v.Trim() }
}
$env:RESTIC_PASSWORD_FILE = $PassFile

if ($env:RESTIC_REPOSITORY -and -not ($env:RESTIC_REPOSITORY -match '^s3:')) {
  if ($env:RESTIC_REPOSITORY -match '^https?://') {
    $env:RESTIC_REPOSITORY = 's3:' + $env:RESTIC_REPOSITORY.TrimEnd('/')
  }
}

$Dest = Join-Path $env:USERPROFILE '.openclaw'

# ============================================================
# AVISO: operacao DESTRUTIVA.
# Este script SUBSTITUI o seu .openclaw ATIVO pelo conteudo do
# backup mais recente do R2. Qualquer alteracao feita DEPOIS do
# ultimo backup (agentes, credenciais, config) sera perdida.
# A pasta atual e movida para .openclaw.backup-<data> antes de
# sobrescrever, mas se essa pasta estiver com arquivos travados
# (gateway aberto, por ex.) o backup local pode falhar e a
# sobrescrita acontece "in place".
# ============================================================
if (Test-Path $Dest) {
  Write-Host ""
  Write-Host "ATENCAO: ja existe um OpenClaw instalado em:" -ForegroundColor Yellow
  Write-Host "  $Dest" -ForegroundColor Yellow
  Write-Host "Continuar VAI SUBSTITUIR essa instalacao pelo backup do R2." -ForegroundColor Red
  Write-Host "Sua pasta atual sera preservada como .openclaw.backup-<data> (se nao estiver travada)." -ForegroundColor Yellow
  Write-Host ""
  if (-not $env:OPENCLAW_RESTORE_YES) {
    $answer = Read-Host "Digite EXATAMENTE 'RESTAURAR' para confirmar (qualquer outra coisa cancela)"
    if ($answer -ne 'RESTAURAR') {
      Write-Host "Cancelado pelo usuario. Nada foi alterado." -ForegroundColor Cyan
      exit 1
    }
  } else {
    Write-Host "OPENCLAW_RESTORE_YES definido: pulando confirmacao (modo nao-interativo)." -ForegroundColor Yellow
  }
}

# para o gateway se o openclaw estiver instalado (reduz lock)
if (Get-Command openclaw -ErrorAction SilentlyContinue) {
  try { & openclaw gateway stop | Out-Null } catch {}
}

$DesktopRestoreRoot = Join-Path ([Environment]::GetFolderPath('Desktop')) 'OpenClaw-restore'
$TmpRestoreRoot = Join-Path $DesktopRestoreRoot 'tmp-restore'
$runId = (Get-Date -Format 'yyyyMMdd-HHmmss')
$RestoreDir = Join-Path $TmpRestoreRoot ('restore-' + $runId)
$UnpackedDir = Join-Path $TmpRestoreRoot ('unpacked-' + $runId)
New-Item -ItemType Directory -Path $RestoreDir -Force | Out-Null
New-Item -ItemType Directory -Path $UnpackedDir -Force | Out-Null

Write-Host "Restic check..." -ForegroundColor Cyan
& $ResticExe check

Write-Host "Restic restore latest (tag openclaw)..." -ForegroundColor Cyan
& $ResticExe restore latest --tag openclaw --target $RestoreDir

$tar = Get-ChildItem $RestoreDir -Recurse -Filter '*-openclaw-backup.tar.gz' | Select-Object -First 1
if (-not $tar) { throw "Could not find *-openclaw-backup.tar.gz under $RestoreDir" }
Write-Host "Tar found: $($tar.FullName)" -ForegroundColor Green

Write-Host "Extracting tar..." -ForegroundColor Cyan
$oldEAP = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
& tar -xzf $tar.FullName -C $UnpackedDir 2>&1 | Out-Null
$ErrorActionPreference = $oldEAP

$found = Get-ChildItem -Path $UnpackedDir -Directory -Filter '.openclaw' -Recurse | Select-Object -First 1
if (-not $found) { throw "Could not find restored .openclaw under $UnpackedDir" }
Write-Host "Restored .openclaw at: $($found.FullName)" -ForegroundColor Green

if (Test-Path $Dest) {
  $BackupDest = $Dest + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
  Write-Host "Destination exists. Moving current to: $BackupDest" -ForegroundColor Yellow
  try { Move-Item -Path $Dest -Destination $BackupDest -Force } catch { Write-Host "Move failed (locked). Will overwrite in place." -ForegroundColor Yellow }
}

Write-Host "Copying to: $Dest" -ForegroundColor Cyan
try { Copy-Item -Path $found.FullName -Destination $Dest -Recurse -Force }
catch { Write-Host "Copy failed: $($_.Exception.Message)" -ForegroundColor Red; throw }

if (Get-Command openclaw -ErrorAction SilentlyContinue) {
  & openclaw config validate | Out-Null
  & openclaw status | Out-Null
  Write-Host "OK: openclaw looks healthy." -ForegroundColor Green
} else {
  Write-Host "Done: OpenClaw nao instalado neste PC; pulei a validacao." -ForegroundColor Yellow
}

Write-Host "Restore completed successfully." -ForegroundColor Green
