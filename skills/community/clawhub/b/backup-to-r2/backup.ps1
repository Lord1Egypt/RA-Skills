$ErrorActionPreference = 'Stop'

# ============================================================
# OpenClaw Backup -> Cloudflare R2 (via restic)
# Gera o tar.gz nativo do OpenClaw, envia pro R2 criptografado
# e deduplicado pelo restic, e aplica retencao automatica.
#
# Requisitos (mesma pasta deste script):
#   .env          -> credenciais R2 + RESTIC_REPOSITORY (veja .env.example)
#   .restic-pass  -> senha de criptografia do repositorio restic
# E o restic instalado (no PATH ou em .\restic\restic.exe)
# ============================================================

$BaseDir   = $PSScriptRoot
$TempDir   = Join-Path $BaseDir 'temp'
$LogDir    = Join-Path $BaseDir 'logs'
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogFile   = Join-Path $LogDir ("backup-" + (Get-Date -Format 'yyyyMMdd') + '.log')

function Log([string]$m) {
  $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
  Add-Content -Path $LogFile -Value $line
  Write-Host $line
}

# --- localiza restic (PATH ou .\restic\restic.exe) ---
$ResticExe = (Get-Command restic -ErrorAction SilentlyContinue).Source
if (-not $ResticExe) { $ResticExe = Join-Path $BaseDir 'restic\restic.exe' }
if (-not (Test-Path $ResticExe)) { throw "restic nao encontrado. Instale-o ou coloque em .\restic\restic.exe" }

# --- localiza openclaw (PATH ou openclaw.cmd no npm global) ---
$OpenClaw = (Get-Command openclaw -ErrorAction SilentlyContinue).Source
if (-not $OpenClaw) { $OpenClaw = Join-Path $env:APPDATA 'npm\openclaw.cmd' }
if (-not (Test-Path $OpenClaw)) { throw "openclaw nao encontrado. Instale o OpenClaw primeiro." }

# --- carrega credenciais R2 do .env ---
$EnvFile = Join-Path $BaseDir '.env'
if (-not (Test-Path $EnvFile)) { throw "Faltando .env (copie de .env.example e preencha)." }
Get-Content $EnvFile | ForEach-Object {
  $line = $_.Trim()
  if (-not $line -or $line.StartsWith('#')) { return }
  $name, $value = $line.split('=', 2)
  if ($name) { Set-Item -Path "env:$($name.Trim())" -Value $value.Trim() }
}
$PassFile = Join-Path $BaseDir '.restic-pass'
if (-not (Test-Path $PassFile)) { throw "Faltando .restic-pass (senha do repositorio restic)." }
Set-Item -Path 'env:RESTIC_PASSWORD_FILE' -Value $PassFile

# --- normaliza RESTIC_REPOSITORY pro formato S3 do restic ---
if ($env:RESTIC_REPOSITORY -and -not ($env:RESTIC_REPOSITORY -match '^s3:')) {
  if ($env:RESTIC_REPOSITORY -match '^https?://') {
    $env:RESTIC_REPOSITORY = 's3:' + $env:RESTIC_REPOSITORY.TrimEnd('/')
  }
}

New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
New-Item -ItemType Directory -Path $LogDir  -Force | Out-Null

Log "=== Backup iniciado ($Timestamp) ==="

$tarPath = $null
try {
  # 1) tar.gz nativo do OpenClaw + verify
  Log '[1/4] openclaw backup create --verify'
  & $OpenClaw backup create --verify --output $TempDir 2>&1 | Tee-Object -FilePath $LogFile -Append | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "openclaw backup falhou (exit $LASTEXITCODE)" }

  $new = Get-ChildItem $TempDir -Filter '*-openclaw-backup.tar.gz' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if (-not $new) { throw "Nao encontrei o .tar.gz gerado em $TempDir" }
  $tarPath = $new.FullName
  Log "Tar gerado: $tarPath ($([math]::Round($new.Length/1MB,2)) MB)"

  # 2) restic backup (dedupe + criptografia client-side)
  Log '[2/4] restic backup -> R2'
  & $ResticExe backup $tarPath --tag openclaw --tag "host:$env:COMPUTERNAME" --tag "date:$Timestamp" 2>&1 | Tee-Object -FilePath $LogFile -Append | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "restic backup falhou (exit $LASTEXITCODE)" }

  # 3) retencao: 7 diarios, 4 semanais, 6 mensais
  Log '[3/4] restic forget --prune'
  & $ResticExe forget --prune --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --tag openclaw 2>&1 | Tee-Object -FilePath $LogFile -Append | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "restic forget falhou (exit $LASTEXITCODE)" }

  # 4) limpa tar local (ja esta no R2 criptografado)
  Log '[4/4] Limpando tar.gz local'
  Remove-Item $tarPath -Force

  Log '=== Backup concluido com sucesso ==='
}
catch {
  Log ("ERRO: " + $_.Exception.Message)
  if ($_.ScriptStackTrace) { Log ("Stack: " + $_.ScriptStackTrace) }
  exit 1
}
