# nssm → shawl Migration

## Background

NSSM is flagged as malware by some security solutions, so starting from syncthing v2 the official Windows Setup transitioned to **shawl**. During major upgrades (v1→v2), the existing nssm registration causes the following problems:

| Symptom | Cause |
|---------|-------|
| `service-specific error 3` (path not found) | LocalSystem/user context difference makes `%LOCALAPPDATA%\Syncthing` inaccessible |
| `service-specific error 3547` | nssm service times out during syncthing v2's SQLite migration |
| Dies immediately on start, no entry in syncthing log | nssm lacks LOAD_USER_PROFILE → cannot find home directory |
| v2.0.4+ migration re-runs on every restart | issue [#10340](https://github.com/syncthing/syncthing/issues/10340) |

## Applicable Cases

- nssm service start failure after syncthing v1.x → v2.x major upgrade
- Environments where NSSM is blocked as malware
- Other chocolatey packages with similar service model changes (same compatibility pattern)

## Prerequisites

Verify the shawl binary (`~/.local/bin/shawl.exe`) is available:

```bash
~/.local/bin/shawl.exe --version
```

If not installed → download from GitHub releases and place in `~/.local/bin/`:

```bash
mkdir -p ~/.local/bin && cd /tmp
curl -sL https://github.com/mtkennerly/shawl/releases/latest/download/shawl-v1.9.0-win64.zip -o shawl.zip
unzip -o shawl.zip
mv shawl.exe ~/.local/bin/
rm shawl.zip
```

(Based on v1.9.0. Query latest version via `https://api.github.com/repos/mtkennerly/shawl/releases/latest`)

## Migration Procedure

### 1. Diagnosis — Extract All Existing Service Settings (HARD STOP)

Before migration, extract all settings of the existing service to **preserve them as-is during shawl re-registration**. Applies the `common.md` "user-specified value change prohibition" rule.

```bash
sc query <service>             # Check SERVICE_STOPPED + error code
nssm get <service> Application # Current path
nssm get <service> AppParameters
nssm get <service> ObjectName  # ⚠️ Execution account — preservation target
nssm get <service> AppDirectory
nssm get <service> AppStdout   # Preserve log path
nssm get <service> AppStderr
sc qc <service>                # ObjectName fallback (admin required)
tasklist | grep <service>      # Lingering processes
netstat -ano | grep ":<port>"  # Port occupation
```

**Record extracted values (required)**: Preserve each value as a variable for use in the next step. Especially if `ObjectName` is not `LocalSystem`, specify the user account explicitly. Even if it is `LocalSystem`, services synchronizing user data like syncthing are recommended to use a user account (see "3. Determining Execution Account" below).

Run directly in the console to verify the syncthing binary itself is healthy:

```bash
"<app-path>" --no-console --no-browser
```

Console runs fine + service fails → this topic applies.

### 2. Migration Script (PowerShell, Administrator)

```powershell
$ErrorActionPreference = "Continue"

$serviceName = "syncthing"
$shawlExe = "$env:USERPROFILE\.local\bin\shawl.exe"
$appExe = "C:\ProgramData\chocolatey\bin\syncthing.exe"
$homePath = "$env:USERPROFILE\AppData\Local\Syncthing"

# ⚠️ Values extracted in diagnosis step — must be filled in by the user
$objectName = ".\<USERNAME>"        # Same as the existing nssm ObjectName. If LocalSystem, replace with a user account for user-data services like syncthing
$objectPassword = "<USER_PASSWORD>" # User's Windows password (don't hardcode plaintext in scripts — use SecureString or prompt for input)

# 1. Stop and remove existing nssm service
sc.exe stop $serviceName
Start-Sleep -Seconds 2
nssm.exe remove $serviceName confirm

# 2. Re-register with shawl (specify --home: access user config)
& $shawlExe add --name $serviceName -- $appExe --no-browser --home=$homePath

# 3. Configure ObjectName + LOAD_USER_PROFILE (preserve user account)
if ($objectName -ne "LocalSystem") {
    sc.exe config $serviceName obj= "$objectName" password= "$objectPassword"
    sc.exe privs $serviceName SeBackupPrivilege/SeRestorePrivilege/SeAssignPrimaryTokenPrivilege  # if needed
}

# 4. Start
sc.exe start $serviceName
Start-Sleep -Seconds 8

# 5. Verify (validate StartName preservation)
sc.exe query $serviceName
Get-CimInstance Win32_Service -Filter "Name='$serviceName'" | Format-List Name,State,StartName,PathName
netstat -an | Select-String "8384"
```

Save the script to `C:\Users\<user>\migrate-<service>-to-shawl.ps1`, then:

```bash
# Bash tool breaks -File argument due to backslash escape issues → use PowerShell tool directly
# In PowerShell tool:
gsudo powershell -ExecutionPolicy Bypass -File "C:\Users\<user>\migrate-<service>-to-shawl.ps1"
```

### 3. Determining Execution Account (HARD STOP — preserving existing ObjectName is the top priority)

**Default principle**: Preserve the `ObjectName` extracted in the diagnosis step as-is. Changes only on explicit user instruction.

| Service Type | Recommended Account | Reason |
|--------------|---------------------|--------|
| **User data sync/consume** (Syncthing, Dropbox, Resilio Sync, OneDrive, etc.) | `.\<USERNAME>` | The owner/permission of synced files is the user. Running as LocalSystem risks owner mismatch, permission denied, and file hash changes |
| **System daemon** (DB, web server, monitoring agent, etc.) | `LocalSystem` or `NT SERVICE\<name>` | Independent of user context. No password management needed |
| **GUI-dependent tools** | User account + `Interactive` (not recommended) | Requires user logon session — prefer daemon mode if possible |

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Leave shawl re-registration at LocalSystem (default) when existing nssm `ObjectName=.\USERNAME` | Specify the extracted value (`.\USERNAME`) explicitly via `sc.exe config obj=` |
| 2 | Assume "LocalSystem + `--home` specification" can serve as a workaround | `--home` only resolves config path — ownership/ACL problems of synced files are separate. User account execution is the proper fix |
| 3 | Hardcode plaintext password in script | Use `Read-Host -AsSecureString` or Group Managed Service Account (gMSA). If you must hardcode plaintext, apply `chmod 600` or `.gitignore` + remove immediately |
| 4 | Fail to update credentials when user password changes → service fails to start | Immediately update via `sc.exe config <svc> password= <new_pw>`. Be aware of Windows password rotation policy |

#### Verification After User Account Registration

```powershell
Get-CimInstance Win32_Service -Filter "Name='syncthing'" | Select-Object Name,State,StartName
# StartName should display as .\<USERNAME>. If LocalSystem, registration failed
```

After the service runs, verify in the syncthing GUI (`http://localhost:8384`) that sync folders scan correctly + new files created have the user account as owner.

## Don't / Do Table

| # | Don't | Do |
|---|-------|-----|
| 1 | Keep using nssm after v1→v2 major upgrade | Migrate to shawl (especially syncthing v2+) |
| 2 | LocalSystem account + omit `--home` | Specify `--home="C:\Users\<u>\AppData\Local\Syncthing"` |
| 2b | Skip extracting existing ObjectName before migration | Mandatory `nssm get <svc> ObjectName` in diagnosis step + use that value for shawl re-registration |
| 2c | Register user data sync services as LocalSystem | Specify the `.\USERNAME` user account. Preserve owner/permission |
| 3 | Attempt to install shawl via scoop/choco | No scoop manifest, no choco package. Download directly from GitHub releases |
| 4 | Call `gsudo powershell -File C:\...` directly from Bash | Bash escape breaks backslashes. Use PowerShell tool or `/c/Users/...` path |
| 5 | Forget to escape arguments in shawl add | Pass execution command as-is after the `--` separator. shawl preserves raw args |

## Applying to Other Packages

The same pattern (major upgrade + service model change) can occur in other chocolatey packages and use the same procedure:

- syncthing (case above, v1→v2)
- Other packages that changed service models (add to this section when cases are found)

## Follow-up Case — choco upgrade also Removes shawl Service (HARD STOP)

**Phenomenon**: With syncthing service registered via shawl, running `choco upgrade syncthing` → after the new version installs, the service disappears. `sc query syncthing` returns `service does not exist`.

**Cause**: The chocolatey syncthing package's `chocolateyBeforeModify.ps1` assumes nssm when a Windows service named "syncthing" exists, and calls stop/remove. Removal happens by name match, regardless of the registration tool (nssm vs shawl).

**Mitigation — always check service existence after choco upgrade**:

```bash
sc query syncthing 2>&1 | grep -E "SERVICE_NAME|STATE"
# Empty result → re-registration needed
```

One-time re-registration script (skip only the nssm remove step in shawl-migration.md "2. Migration Script"):

```powershell
$shawlExe = "$env:USERPROFILE\.local\bin\shawl.exe"
$appExe = "C:\ProgramData\chocolatey\bin\syncthing.exe"
$homePath = "$env:USERPROFILE\AppData\Local\Syncthing"

& $shawlExe add --name syncthing -- $appExe --no-browser --home=$homePath
sc.exe start syncthing
```

**Root solution (TODO)**: When registering with shawl, rename the service (e.g., `syncthing-shawl`) to avoid conflict with chocolateyBeforeModify's nssm assumption. However, GUI environment variables and existing automation may depend on the `syncthing` name, so compatibility review is required.

## Violation Cases

**2026-05-21 (1st occurrence)**: On a Windows machine, syncthing 2.1.0 nssm service immediately failed with service-specific error 3. Console syncthing.exe started normally (PID 28208, 8384 LISTENING). Initially suspected nssm shim path / user password, but the actual cause was v1→v2 major compatibility. Resolved via shawl migration:
- nssm remove syncthing confirm
- shawl add --name syncthing -- syncthing.exe --no-browser --home=...AppData\Local\Syncthing
- Service RUNNING + 8384 LISTENING recovery complete.

**2026-05-21 (2nd occurrence)**: Immediately after the 1st migration in the same session, `choco upgrade` or auto-upgrade transitioned syncthing 2.1.0 → 2.1.1. The shawl service was automatically removed by chocolateyBeforeModify. `sc query` showed service does not exist. Recovered via re-registration. → Created the "Follow-up Case" section in this topic.

**2026-05-21 (3rd occurrence)**: During 1st/2nd shawl re-registration, the existing nssm `ObjectName=.\<USERNAME>` was not extracted/preserved and was registered with the default LocalSystem. Risk of owner/permission mismatch for services like syncthing that sync user data. User pointed out "registered with the wrong user". Reinforced by adding ObjectName extraction in the diagnosis step + `sc.exe config obj=` step in the migration script + restructuring the execution account decision table.

## References

- [Syncthing v2.0 release notes](https://github.com/syncthing/syncthing/releases/tag/v2.0.0)
- [Syncthing v2 forum migration thread](https://forum.syncthing.net/t/syncthing-2-0-august-2025/24758)
- [shawl GitHub](https://github.com/mtkennerly/shawl)
- [issue #10340 — re-migrate every start](https://github.com/syncthing/syncthing/issues/10340)
