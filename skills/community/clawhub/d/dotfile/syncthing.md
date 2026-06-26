# Syncthing Integration

Syncs chezmoi source directory via Syncthing to share dotfiles across multiple machines.

## Register Folder via API

Auto-register chezmoi folder using Syncthing REST API:

```bash
# API key (macOS - uses xmllint, grep -oP is GNU-only and doesn't work on macOS)
API_KEY=$(xmllint --xpath '//configuration/gui/apikey/text()' ~/Library/Application\ Support/Syncthing/config.xml)

# Add folder
curl -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8384/rest/config/folders \
  -d '{
    "id": ".local/share/chezmoi",
    "label": ".local/share/chezmoi",
    "path": "~/.local/share/chezmoi",
    "type": "sendreceive",
    "versioning": {
      "type": "staggered",
      "params": {"maxAge": "31536000"}
    }
  }'
```

## Auto Ignore Setup

Creates `.stignore` during chezmoi initialization:

```bash
# ~/.local/share/chezmoi/.stignore
.git
(?d).DS_Store
*.bak
```

### `(?d)` Prefix Guide

When a parent directory is deleted on a remote, deletion is blocked if ignored files remain locally:

```
syncing: delete dir: directory has been deleted on a remote device
but contains ignored files (see ignore documentation for (?d) prefix)
```

**`(?d)` prefix**: Allows parent directory deletion even if ignored files exist.

### `(?d)` Application Rules

| Apply | Pattern | Reason |
|-------|---------|--------|
| **Prohibited** | `.bak` | Backup files -- must be preserved locally even on remote deletion |
| **Prohibited** | `.git` | Repository data -- must be preserved locally |
| **Prohibited** | `.env*` | Environment variables/secrets -- must be preserved locally |
| Apply | `.DS_Store` | Volatile metadata |
| Apply | `.ansible`, `.terraform`, `.venv`, `venv`, `node_modules` | Reinstallable runtime/dependencies |
| Apply | `build`, `cache`, `defined`, `dist`, `out`, `target` | Regenerable build artifacts |

### `.claude/.stignore` Current Patterns

```bash
# Backups/secrets -- (?d) prohibited, preserve locally on remote deletion
.bak
.env*
.git
# Regenerable -- (?d) applied, cleaned up together on remote deletion
(?d).ansible
(?d).DS_Store
(?d).terraform
(?d).venv
(?d)build
(?d)cache
(?d)defined
(?d)dist
(?d)node_modules
(?d)out
(?d)target
(?d)venv
# Whitelist
!commands
!hooks
!plugins/marketplaces
!projects
!scripts
*
```

> **Strictly prohibited**: Adding `(?d)` to `.bak`, `.git`, `.env*` -- backup/secret loss on remote deletion

## Directory Structure

```
~/.local/share/chezmoi/
├── .chezmoitemplates/     # Shared data (JSON, etc.)
│   └── mcp-servers.json
├── .chezmoi-lib/          # Shared scripts (executables)
│   ├── executable_*.sh
│   └── ...
├── .stignore              # Syncthing ignore patterns
└── ...
```

## New Machine Setup

```bash
# 1. After syncing chezmoi source via Syncthing
# 2. Initialize chezmoi (keep source directory)
chezmoi init --source ~/.local/share/chezmoi

# 3. Apply
chezmoi apply
```

## Managing Syncthing Default Config with chezmoi

Manage Syncthing defaults via chezmoi modify:

```
~/.local/share/chezmoi/private_Library/private_Application Support/private_Syncthing/
└── modify_private_config.xml.tmpl
```

**Managed items:**
- `defaults/folder`: minDiskFree 1GB, versioning staggered 1 year
- `defaults/ignores`: Global ignore patterns

**Behavior:** On chezmoi apply, settings are applied via Syncthing API -> config.xml auto-updated

## Sync Diagnostics

### Get API Key

**macOS:**
```bash
API_KEY=$(xmllint --xpath '//configuration/gui/apikey/text()' ~/Library/Application\ Support/Syncthing/config.xml)
```

**Linux:**
```bash
API_KEY=$(xmllint --xpath '//configuration/gui/apikey/text()' ~/.config/syncthing/config.xml)
```

**Windows (PowerShell):**
```powershell
$configPath = "$env:LOCALAPPDATA\Syncthing\config.xml"
[xml]$xml = Get-Content $configPath
$API_KEY = $xml.configuration.gui.apikey
```

### Check Folder Status

```bash
# Full folder sync status (state, globalFiles, localFiles, needFiles)
curl -s -H "X-API-Key: $API_KEY" "http://localhost:8384/rest/db/status?folder=<FOLDER_ID>"
```

| Field | Meaning |
|-------|---------|
| `state` | `idle` normal, `scanning` scanning, `sync-waiting` waiting to sync |
| `globalFiles` | Total file count across all devices |
| `localFiles` | File count on this device |
| `needFiles` | Files still to be received |

**global > local && needFiles=0**: Files only on other devices (`.stignore` whitelist differences). Normal.

### Check Incomplete Items

```bash
# List of files not yet synced
curl -s -H "X-API-Key: $API_KEY" "http://localhost:8384/rest/db/need?folder=<FOLDER_ID>"

# Completion from a specific device to this device
curl -s -H "X-API-Key: $API_KEY" "http://localhost:8384/rest/db/completion?folder=<FOLDER_ID>&device=<DEVICE_ID>"
```

### Connection Status

```bash
# Check connected/disconnected devices
curl -s -H "X-API-Key: $API_KEY" http://localhost:8384/rest/system/connections

# Check device names
curl -s -H "X-API-Key: $API_KEY" http://localhost:8384/rest/config/devices
```

### Rescan (Index Refresh)

```bash
# Rescan specific folder -- effective for resolving stale states like sync-waiting
curl -s -X POST -H "X-API-Key: $API_KEY" "http://localhost:8384/rest/db/scan?folder=<FOLDER_ID>"
```

### DB Reset (Full Index Reset)

Used when stale entries from offline devices remain or when encountering persistent transfer queue freezes. Settings/keys are preserved; only the index is rebuilt.

> **Note**: `syncthing --reset-database` was removed in v2.0. Replaced by deleting the `index-v2` directory.

**macOS / Linux:**
```bash
# 1. Stop Syncthing
brew services stop syncthing

# 2. Back up and delete index
mv ~/Library/Application\ Support/Syncthing/index-v2 \
   ~/Library/Application\ Support/Syncthing/index-v2.bak

# 3. Restart (index auto-rebuilt)
brew services start syncthing

# 4. Remove backup after verification
rm -rf ~/Library/Application\ Support/Syncthing/index-v2.bak
```

**Windows (PowerShell - Run as Admin if service-managed):**
```powershell
# 1. Stop Syncthing service
Stop-Service syncthing
# Force kill processes if locked
Get-Process | Where-Object { $_.Name -like "*syncthing*" } | Stop-Process -Force

# 2. Back up and delete index
$dbPath = "$env:LOCALAPPDATA\Syncthing\index-v2"
$backupPath = "$env:LOCALAPPDATA\Syncthing\index-v2.bak"
if (Test-Path $backupPath) { Remove-Item $backupPath -Recurse -Force }
Move-Item $dbPath $backupPath -Force

# 3. Start service (index auto-rebuilt)
Start-Service syncthing

# 4. After verifying Syncthing is healthy, manually delete the backup
# (left intentionally commented — confirm sync works first, then run this)
# Remove-Item $backupPath -Recurse -Force
```

**Check index path**: `syncthing paths` or `syncthing.exe paths` -> "Database location" entry

### Windows Service Account: User vs LocalSystem (HARD STOP)

**Recommended**: Run Syncthing as a Windows service under the **user account**, not `LocalSystem`. User-account service can expand `~` paths in `config.xml` and avoids the `.git/` corruption pattern seen with `LocalSystem`.

| Aspect | `LocalSystem` (avoid) | User account (recommended) |
|--------|----------------------|---------------------------|
| `~` path expansion | ❌ Fails — needs absolute path conversion | ✅ Native `~` resolution |
| User profile access | ❌ Different `$HOME` (`C:\Windows\System32\config\systemprofile`) | ✅ Matches `C:\Users\<user>` |
| `.git/` corruption | ⚠️ Higher risk (no user lock context) | Lower risk |
| Starts at boot (no login) | ✅ Yes | Service: ✅ Yes (Automatic start). **Task Scheduler (AtLogOn): ❌ No — waits for first user login** |
| Requires user login | ❌ No | Service: ❌ No. **Task Scheduler (AtLogOn): ✅ Yes (fires once at logon)** |

#### Migrate LocalSystem → User Account (Task Scheduler with hidden VBS launcher)

**Recommended approach**: Task Scheduler at user logon + VBS launcher for hidden execution. No password storage required. Run admin steps via `gsudo` (a Windows `sudo`-equivalent — installs via `winget install gerardog.gsudo`; if `gsudo` is unavailable, run an elevated PowerShell prompt manually for the `Register-ScheduledTask` step below).

##### Step 1: Create VBS hidden launcher

`syncthing.exe` is a console app — running it directly from Task Scheduler shows a console window that, **when closed, terminates the process**. Wrap it in VBS to launch hidden.

```vbs
' ~/.local/bin/syncthing-hidden.vbs
Set objShell = CreateObject("WScript.Shell")
objShell.Run """C:\ProgramData\chocolatey\bin\syncthing.exe"" --no-browser --home=""C:\Users\<USERNAME>\AppData\Local\Syncthing""", 0, False
```

The `0` argument = `vbHidden` (no window). The `False` = don't wait for completion (VBS exits, child syncthing.exe keeps running).

##### Step 2: Migration script

`~/.local/share/syncthing-migrate-to-user.ps1`:

```powershell
# Stop and delete existing LocalSystem service
Stop-Service syncthing -Force -ErrorAction SilentlyContinue
sc.exe delete syncthing

# Register Task Scheduler entry
$user = "$env:USERDOMAIN\$env:USERNAME"
$vbs = "$env:USERPROFILE\.local\bin\syncthing-hidden.vbs"

$action = New-ScheduledTaskAction `
    -Execute "wscript.exe" `
    -Argument "`"$vbs`"" `
    -WorkingDirectory $env:USERPROFILE
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $user
$principal = New-ScheduledTaskPrincipal `
    -UserId $user `
    -LogonType Interactive `
    -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Days 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -Hidden

Register-ScheduledTask `
    -TaskName "Syncthing" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings
Start-ScheduledTask -TaskName "Syncthing"
```

##### Step 3: Run via gsudo

```powershell
gsudo powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.local\share\syncthing-migrate-to-user.ps1"
```

##### Step 4: Verify

```powershell
Get-Process syncthing | ForEach-Object {
    # Get-CimInstance is the PowerShell 7+ replacement for the deprecated Get-WmiObject
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)"
    $owner = Invoke-CimMethod -InputObject $proc -MethodName GetOwner
    $hidden = if ([string]::IsNullOrEmpty($_.MainWindowTitle)) { "hidden" } else { "visible" }
    Write-Host "PID $($_.Id) owner=$($owner.Domain)\$($owner.User) $hidden"
}
# Expected: owner=<DOMAIN>\<USER>, hidden
```

#### Alternative: Windows Service (user account) — requires password

If you need Syncthing to start before user logon, register as a Windows Service under the user account. Service Control Manager will encrypt and store the password. This trade-off (password storage) is rarely worth it on personal machines — prefer Task Scheduler unless multi-user / server context.

```powershell
# Run as Admin (or via gsudo). Define the variables this command references before invoking sc.exe.
$shawl    = "$env:USERPROFILE\.local\bin\shawl.exe"     # path to a shawl.exe wrapper (https://github.com/mtkennerly/shawl)
$syncthing = "$env:USERPROFILE\.local\bin\syncthing.exe" # path to syncthing.exe
$home     = "$env:USERPROFILE\.local\share\syncthing"    # Syncthing --home directory
$user     = "$env:USERDOMAIN\$env:USERNAME"              # account to run the service as

sc.exe create syncthing binPath= "`"$shawl`" run --name syncthing -- `"$syncthing`" --no-browser --home=`"$home`"" start= auto obj= $user password= "<USER_PASSWORD>"
# Plus: grant "Log on as a service" right via secpol.msc or ntrights.exe
```

#### After Migration: Use `~` Paths

Once running under user account, `config.xml` folder paths can use `~`:

```xml
<folder id="..." path="~/.claude" ... />
```

Syncthing will resolve `~` to `C:\Users\<USERNAME>` natively.

### Troubleshooting: Garbage `encryptionPassword` (Antigravity / Gemini re-registration)

**Symptom**: All folders report `Failed to verify encryption consistency` against connected devices, message:
`remote expects to exchange plain data, but local data is encrypted (folder-type receive-encrypted)`.

Folder type is `sendreceive` on both ends, yet Syncthing treats one side as `receive-encrypted`.

**Cause**: When Antigravity (Gemini) re-registers Syncthing folders during config sync, it writes non-empty whitespace strings (commonly `&#xA;` followed by 6 spaces — LF + 6 spaces) into every `<encryptionPassword>` element under each `<folder>/<device>` block and the `<defaults>/<folder>/<device>` template. Syncthing treats any non-empty string as a valid password and switches the folder into encryption mode, which then mismatches the remote's `sendreceive` configuration.

The corrupted password is **invisible to the Web UI password field** (renders as empty) and to PowerShell `[xml]` access (auto-trimmed) — diagnosis requires reading the raw XML.

#### Diagnosis (raw XML hex inspection)

```powershell
$cfg = "$env:LOCALAPPDATA\Syncthing\config.xml"
$content = Get-Content $cfg -Raw
$pattern = '<encryptionPassword>([^<]*)</encryptionPassword>'
$mtchs = [regex]::Matches($content, $pattern)
$empty = 0; $nonempty = 0
foreach ($m in $mtchs) {
    $pwd = $m.Groups[1].Value
    if ($pwd.Length -eq 0) { $empty++ } else {
        $nonempty++
        $hex = ($pwd.ToCharArray() | ForEach-Object { "{0:X2}" -f [int]$_ }) -join " "
        Write-Host "  hex='$hex' (len=$($pwd.Length))"
    }
}
Write-Host "empty=$empty, non-empty=$nonempty"
```

A typical garbage value `hex='26 23 78 41 3B 20 20 20 20 20 20'` decodes to `&#xA;` followed by 6 spaces (LF + 6 spaces). If `non-empty > 0`, the bug is present.

#### Fix (API PUT — clears folders + defaults)

```powershell
$cfg = "$env:LOCALAPPDATA\Syncthing\config.xml"
[xml]$xml = Get-Content $cfg
$API_KEY = $xml.configuration.gui.apikey

# 1. Clear all folder/device encryption passwords
$folders = Invoke-RestMethod -Uri "http://localhost:8384/rest/config/folders" -Headers @{"X-API-Key"=$API_KEY}
foreach ($f in $folders) {
    foreach ($d in $f.devices) {
        if ($d.encryptionPassword -and $d.encryptionPassword.Length -gt 0) { $d.encryptionPassword = "" }
    }
}
$body = $folders | ConvertTo-Json -Depth 10 -Compress
Invoke-RestMethod -Method Put -Uri "http://localhost:8384/rest/config/folders" `
    -Headers @{"X-API-Key"=$API_KEY; "Content-Type"="application/json"} -Body $body | Out-Null

# 2. Clear defaults/folder template (prevents recurrence on new folders)
$defaults = Invoke-RestMethod -Uri "http://localhost:8384/rest/config/defaults/folder" -Headers @{"X-API-Key"=$API_KEY}
foreach ($d in $defaults.devices) {
    if ($d.encryptionPassword -and $d.encryptionPassword.Length -gt 0) { $d.encryptionPassword = "" }
}
$dbody = $defaults | ConvertTo-Json -Depth 10 -Compress
Invoke-RestMethod -Method Put -Uri "http://localhost:8384/rest/config/defaults/folder" `
    -Headers @{"X-API-Key"=$API_KEY; "Content-Type"="application/json"} -Body $dbody | Out-Null
```

No Syncthing restart required — the API PUT writes through to config.xml and the running daemon picks up the change. Encryption errors stop within seconds.

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Trust the Web UI password field appearing empty | Read raw config.xml + hex-dump every `<encryptionPassword>` |
| 2 | Restart / unpause / re-add folders to fix the symptom | The garbage password persists across all those operations — clear via API PUT |
| 3 | Clear only folders, skip `<defaults>` | New folders will inherit the garbage password again — clear both |
| 4 | Use PowerShell `[xml]` parsing to compare passwords | `[xml]` auto-trims whitespace, hiding the garbage. Use regex on raw text |
| 5 | Assume "remote device has wrong type" and ask the user to reconfigure the peer | The peer is correct; the local non-empty password is what flips local-side to encrypted mode |

#### Verification

After the fix:
```powershell
$log = Invoke-RestMethod -Uri "http://localhost:8384/rest/system/log" -Headers @{"X-API-Key"=$API_KEY}
$recent = $log.messages | Where-Object {
    ($_.message -match "encryption") -and ([DateTime]$_.when -gt (Get-Date).AddMinutes(-2))
}
Write-Host "Encryption errors in last 2min: $($recent.Count)"  # expected: 0
```

### Legacy: "Folder Path Missing" Workaround (LocalSystem only)

**Use only if migrating to user account is not feasible.** Converts `~` to absolute paths in `config.xml`:

```powershell
$configPath = "$env:LOCALAPPDATA\Syncthing\config.xml"
[xml]$xml = Get-Content $configPath
$userHome = $env:USERPROFILE
$changed = 0
foreach ($folder in $xml.configuration.folder) {
    $oldPath = $folder.path
    if ($oldPath -match '^~[/\\]') {
        $newPath = $oldPath -replace '^~[/\\]', "$userHome\"
        $newPath = $newPath -replace '/', '\'
        $folder.path = $newPath
        $changed++
    }
}
if ($changed -gt 0) {
    $xml.Save($configPath)
    Write-Host "Paths converted successfully."
}
```

## Conflict Prevention

- Add temporary file patterns to `.stignore`
- Use chezmoi template conditionals for machine-specific config:

```go
{{ if eq .chezmoi.hostname "macbook" }}
// macbook-specific config
{{ end }}
```
