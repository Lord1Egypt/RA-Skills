# Windows PowerShell & Command Prompt Equivalents

> **Prefer the PowerShell functions over the `.bat` equivalents.** The batch
> files interpolate `%DAYS%` into a `powershell -Command` string, which is a
> command-injection vector if that value is ever attacker-controlled. This
> reference no longer ships the `.bat` templates for that reason. If you keep
> them, validate `DAYS` as a positive integer first and quote every variable.

## Safety helper (required)

Every command below calls `ft_guard` first. It does three things:

1. **Targets one project explicitly.** `docker-compose` without `-p` acts on
   whatever project happens to be in the current directory. `ft_guard` resolves
   a single project name and passes it to every `docker-compose` call, so a
   command can never start or stop an unrelated container set.
2. **Detects the trading mode.** It reads `dry_run` from the Freqtrade config
   and refuses to run live-control commands against a live bot unless you
   confirm.
3. **Confirms destructive actions.** `--erase` deletes cached market data and
   `ftstop`/`ftrestart` interrupt a running bot. Both require confirmation.

Set `$env:FT_PROJECT` to your Freqtrade project name (it defaults to
`freqtrade`). Set `$env:FT_CONFIRM = "yes"` to skip the interactive prompts in
non-interactive shells where you have already confirmed the action yourself.

```powershell
# The compose project name. Override with $env:FT_PROJECT if yours differs.
if (-not $env:FT_PROJECT) { $env:FT_PROJECT = "freqtrade" }

# Resolve the Freqtrade config that holds dry_run.
if (-not $env:FT_CONFIG) { $env:FT_CONFIG = "user_data/config.json" }

# Read dry_run out of the config. Returns $true, $false, or $null (unknown).
function Get-FtDryRun {
  if (-not (Test-Path $env:FT_CONFIG)) { return $null }
  try {
    $cfg = Get-Content $env:FT_CONFIG -Raw | ConvertFrom-Json
    return [bool]$cfg.dry_run
  } catch {
    return $null
  }
}

# Guard for bot-control commands. Requires an explicit target and, against a
# live bot, an explicit confirmation.
function Invoke-FtGuard {
  param([string]$Action = "safe")

  $dry = Get-FtDryRun

  if ($null -eq $dry) {
    Write-Host "REFUSING: could not read dry_run from $env:FT_CONFIG."
    Write-Host "Check the config path (override with FT_CONFIG) and confirm the bot is in dry-run."
    return $false
  }

  if (-not $dry) {
    Write-Host "REFUSING: $($env:FT_PROJECT) is configured with dry_run: false (LIVE trading)."
    Write-Host "Confirm the target project and mode, then set FT_CONFIRM=yes to proceed."
    return $false
  }

  if ($Action -eq "destructive" -and $env:FT_CONFIRM -ne "yes") {
    Write-Host "CONFIRM REQUIRED: this command affects a running bot or deletes cached data."
    Write-Host "Re-run with FT_CONFIRM=yes once you have confirmed the target: $($env:FT_PROJECT)"
    return $false
  }
  return $true
}
```

## PowerShell Functions

Add these to your PowerShell profile (`$PROFILE`) or dot-source this file.

### ftdata — Download Data

```powershell
function ftdata {
  param(
    [string]$Pair = "BTC/USDT",
    [int]$Days = 30,
    [string]$Timeframe = "5m",
    [string]$Erase = ""
  )

  # Validate Pair (alphanumeric + / only)
  if ($Pair -notmatch '^[A-Za-z0-9/]+$') {
    Write-Host "Error: invalid pair format. Use alphanumeric and / only (e.g., BTC/USDT)"
    return
  }

  # Validate Timeframe (digits + m/h/d)
  if ($Timeframe -notmatch '^\d+(m|h|d)$') {
    Write-Host "Error: invalid timeframe format. Use format like 5m, 1h, 1d"
    return
  }

  # Validate Days (positive integer) — it is interpolated into a command line
  if ($Days -lt 1) {
    Write-Host "Error: invalid days. Use a positive integer (e.g., 30)"
    return
  }

  # Handle --erase flag safely — deletes cached data, so it needs confirmation
  $EraseFlag = ""
  if ($Erase -eq "--erase") {
    if (-not (Invoke-FtGuard -Action "destructive")) { return }
    $EraseFlag = "--erase"
  }

  $StartDate = (Get-Date).AddDays(-$Days).ToString("yyyyMMdd")
  docker-compose -p $env:FT_PROJECT run --rm freqtrade download-data `
    --exchange kraken `
    --pairs "$Pair" `
    --timerange "${StartDate}-" `
    --timeframe "$Timeframe" `
    $EraseFlag
}
```

**Usage Examples:**
```powershell
ftdata "BTC/USDT" 90 5m           # Download 90 days of 5-min BTC/USDT data
ftdata "ETH/USDT" 30 1h           # 30 days of 1-hour ETH/USDT
ftdata "SOL/USDT"                 # Use defaults: 30 days, 5-min
ftdata "XRP/USDT" 365 5m "--erase" # Download 1 year, erase old data first
```

**Critical Notes:**
- Call with ONE pair at a time. Multiple pairs cause errors.
- Use `--erase` when extending your data range backward in time.
- Set `$env:FT_PROJECT` if your compose project is not named `freqtrade`.

### ftback — Run Backtest

```powershell
function ftback {
  param(
    [string]$Strategy = "SampleStrategy",
    [int]$Days = 30,
    [string]$Timeframe = "5m",
    [string]$Pairs = ""
  )

  # Validate Strategy (alphanumeric, underscore, hyphen only)
  if ($Strategy -notmatch '^[A-Za-z0-9_-]+$') {
    Write-Host "Error: invalid strategy name. Use alphanumeric, underscore, or hyphen only"
    return
  }

  # Validate Timeframe (digits + m/h/d)
  if ($Timeframe -notmatch '^\d+(m|h|d)$') {
    Write-Host "Error: invalid timeframe format. Use format like 5m, 1h, 1d"
    return
  }

  # Validate Days (positive integer) — it is interpolated into a command line
  if ($Days -lt 1) {
    Write-Host "Error: invalid days. Use a positive integer (e.g., 30)"
    return
  }

  # Validate Pairs if provided (alphanumeric + / and comma)
  if (-not [string]::IsNullOrEmpty($Pairs) -and $Pairs -notmatch '^[A-Za-z0-9/,]+$') {
    Write-Host "Error: invalid pairs format. Use alphanumeric, /, and comma only"
    return
  }

  $StartDate = (Get-Date).AddDays(-$Days).ToString("yyyyMMdd")
  if ([string]::IsNullOrEmpty($Pairs)) {
    docker-compose -p $env:FT_PROJECT run --rm freqtrade backtesting `
      --strategy "$Strategy" `
      --timerange "${StartDate}-" `
      --timeframe "$Timeframe" `
      --breakdown day
  } else {
    docker-compose -p $env:FT_PROJECT run --rm freqtrade backtesting `
      --strategy "$Strategy" `
      --timerange "${StartDate}-" `
      --timeframe "$Timeframe" `
      --pairs "$Pairs" `
      --breakdown day
  }
}
```

**Usage Examples:**
```powershell
ftback "MyStrategy" 60 5m                      # Test MyStrategy for 60 days
ftback "MyStrategy" 90 1h "BTC/USDT"          # Test on specific pair
ftback                                         # Use defaults: SampleStrategy, 30 days, 5m
```

### Bot Control

These act on a running bot. Each one targets exactly one project and refuses
to run against a live (`dry_run: false`) bot unless `$env:FT_CONFIRM` is `yes`.

```powershell
function ftstop    { if (Invoke-FtGuard -Action "destructive") { docker-compose -p $env:FT_PROJECT stop } }
function ftstart   { if (Invoke-FtGuard -Action "destructive") { docker-compose -p $env:FT_PROJECT start } }
function ftrestart { if (Invoke-FtGuard -Action "destructive") { docker-compose -p $env:FT_PROJECT restart } }
function ftlogs    { docker-compose -p $env:FT_PROJECT logs -f freqtrade }
function ftstatus  {
  docker-compose -p $env:FT_PROJECT ps
  docker-compose -p $env:FT_PROJECT logs --tail=20 freqtrade
}
function ftlist    {
  if (Test-Path user_data/data/kraken/) {
    Get-ChildItem -Path user_data/data/kraken/ -Recurse | `
      Format-Table FullName, Length
  } else {
    Write-Host "No data. Run ftdata first."
  }
}
function ftui      { Start-Process "http://localhost:8080" }
```

`ftlogs`, `ftstatus`, `ftlist`, and `ftui` are read-only and need no
confirmation. `ftstop`, `ftstart`, and `ftrestart` do.

---

## Command Prompt (cmd.exe)

Prefer the PowerShell functions above from `cmd.exe` too — you can call them
from `cmd` via `powershell -NoProfile -Command ftstatus`. If you need native
cmd-only macros, use `doskey` with the project pinned and the guard applied
through the PowerShell helper rather than raw `docker-compose`:

```batch
REM Save to freqtrade-macros.bat and reference it from your cmd session.
REM These delegate to the PowerShell functions, which apply the guard.
doskey ftstop=powershell -NoProfile -Command ftstop
doskey ftstart=powershell -NoProfile -Command ftstart
doskey ftrestart=powershell -NoProfile -Command ftrestart
doskey ftlogs=powershell -NoProfile -Command ftlogs
doskey ftstatus=powershell -NoProfile -Command ftstatus
doskey ftui=powershell -NoProfile -Command ftui
```

**Installation:** Add `call C:\path\to\freqtrade-macros.bat` to your cmd
startup, or run it in each session.
