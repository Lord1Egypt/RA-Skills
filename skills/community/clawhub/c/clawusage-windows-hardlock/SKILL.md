---
name: clawusage
description: Run local clawusage monitoring commands from chat (Telegram/Feishu). Use when user types `/clawusage ...` or asks to check Codex usage, enable/disable auto idle alerts, set idle reminder threshold, or switch language with `lang english|chinese`.
user-invocable: false
disable-model-invocation: true
---

# ClawUsage Chat Command

Run bundled local scripts and return command output directly.

Command source:

- `scripts/clawusage.ps1` bundled inside this skill package

Supported arguments:

- `now`
- `usage`
- `status`
- `help`
- `lang`
- `lang english`
- `lang chinese`
- `auto on [minutes]`
- `auto off`
- `auto set <minutes>`
- `auto status`
- `doctor`
- `-help`

Execution rules:

1. Parse user input after `/clawusage`.
2. If no argument is provided, default to `usage`.
3. Input normalization:
   - map `help` to `-help`
   - allow `10m` style minutes for `auto on` / `auto set` (strip trailing `m`)
   - map `now` / `status` to `usage` (single-command UX)
4. Resolve skill script directory in this order:
   - `$env:USERPROFILE\\.openclaw\\workspace\\skills\\clawusage\\scripts`
   - `$env:USERPROFILE\\.openclaw\\skills\\clawusage\\scripts`
   - first recursive match under `$env:USERPROFILE\\.openclaw\\` ending with `\\clawusage\\scripts`
5. Prefer text-packaged script files (ClawHub-safe):
   - `clawusage.ps1.txt`
   - `openclaw-usage-monitor.ps1.txt`
   - `clawusage-auto-worker.ps1.txt`
   Fallback to direct `.ps1` files only for local dev installs.
6. Materialize runtime files under:
   - `$env:USERPROFILE\\.clawusage\\skill-runtime`
   - write `clawusage.ps1`, `openclaw-usage-monitor.ps1`, `clawusage-auto-worker.ps1`
7. Run exactly one local command:
   - `& powershell -NoProfile -ExecutionPolicy Bypass -File "<runtime_root>\\clawusage.ps1" <args>`
8. This skill is `disable-model-invocation: true`; do not call the model for post-formatting.
9. Return stdout directly. Do not rewrite, summarize, or translate command output.
10. Do not run unrelated commands.
11. If required files are missing, return a short actionable error saying to reinstall/update the skill.

Path-resolution snippet (PowerShell):

```powershell
$scriptDirs = @(
  "$env:USERPROFILE\.openclaw\workspace\skills\clawusage\scripts",
  "$env:USERPROFILE\.openclaw\skills\clawusage\scripts"
)
$dir = $scriptDirs | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $dir) {
  $dir = Get-ChildItem -Path "$env:USERPROFILE\.openclaw" -Recurse -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -match "[\\/]clawusage[\\/]scripts$" } |
    Select-Object -First 1 -ExpandProperty FullName
}
if (-not $dir) { throw "clawusage skill scripts folder not found. Reinstall clawusage skill." }

$runtimeRoot = Join-Path $env:USERPROFILE ".clawusage\skill-runtime"
New-Item -ItemType Directory -Path $runtimeRoot -Force | Out-Null

$pairs = @(
  @{ target = "clawusage.ps1"; srcTxt = "clawusage.ps1.txt"; srcPs1 = "clawusage.ps1" },
  @{ target = "openclaw-usage-monitor.ps1"; srcTxt = "openclaw-usage-monitor.ps1.txt"; srcPs1 = "openclaw-usage-monitor.ps1" },
  @{ target = "clawusage-auto-worker.ps1"; srcTxt = "clawusage-auto-worker.ps1.txt"; srcPs1 = "clawusage-auto-worker.ps1" }
)
foreach ($p in $pairs) {
  $srcTxt = Join-Path $dir $p.srcTxt
  $srcPs1 = Join-Path $dir $p.srcPs1
  $dst = Join-Path $runtimeRoot $p.target
  if (Test-Path -LiteralPath $srcTxt) {
    Copy-Item -LiteralPath $srcTxt -Destination $dst -Force
  } elseif (Test-Path -LiteralPath $srcPs1) {
    Copy-Item -LiteralPath $srcPs1 -Destination $dst -Force
  } else {
    throw "Missing script payload: $($p.srcTxt) (or $($p.srcPs1)). Reinstall clawusage skill."
  }
}

& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $runtimeRoot "clawusage.ps1") @args
```


