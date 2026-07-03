---
name: choco
metadata:
  author: es6kr
  version: "0.0.0"
description: |
  Chocolatey operations integration — post-processing after choco upgrade, nssm service path refresh, NSSM → shawl migration (syncthing v2 etc.), resync on UniGetUI/choco metadata update failures. diagnose [diagnose.md], metadata-fix [metadata-fix.md], post-upgrade [post-upgrade.md], shawl-migration [shawl-migration.md], update-path [update-path.md].
  Use when: "choco", "chocolatey", "choco upgrade", "choco outdated", "vcredist", "nssm", "nssm recovery", "nssm path", "service path refresh", "after choco upgrade", "service failure", "SERVICE_STOPPED", "shim issue", "syncthing nssm", "syncthing v2", "shawl migration", "nssm deprecation", "service-specific error", "UniGetUI", "metadata update failure", "metadata stale", ".nuspec stale", "choco metadata".
---

# Choco

Chocolatey operations integration skill. Pre- and post-processing for choco upgrade, nssm service compatibility management, and metadata update failure recovery.

## Core Problems

| Area | Problem | Resolution Topic |
|------|---------|------------------|
| Package path | After choco upgrade, the nssm Application path becomes stale due to version-specific folders | [update-path.md](./update-path.md) |
| Service compatibility | After major upgrade (e.g., syncthing v1→v2), NSSM fails with service-specific error | [shawl-migration.md](./shawl-migration.md) |
| Metadata | Runtime install succeeds + chocolatey `.nuspec` is stale (UniGetUI shows repeated upgrades) | [metadata-fix.md](./metadata-fix.md) |
| Diagnosis | Identify which service has issues / which package is stale | [diagnose.md](./diagnose.md) |
| Bulk post-processing | Automatically check affected services after choco upgrade | [post-upgrade.md](./post-upgrade.md) |

## Path Strategy (HARD STOP — required decision before nssm set Application)

| Strategy | Example Path | Pros | Cons |
|----------|--------------|------|------|
| **Stable shim path (recommended)** | `%ChocolateyInstall%\bin\syncthing.exe` | Path remains unchanged after choco upgrade | Without `--shimgen-waitforexit`, nssm may misinterpret shim exit as a crash |
| Version-specific actual path | `%ChocolateyInstall%\lib\syncthing\tools\...-v2.1.0\syncthing.exe` | No shim issues | **Path breaks on every upgrade** — this is why this skill exists |

**Default choice: stable shim path.** Use version-specific path + post-upgrade hook combination only for services where shim issues occur. When NSSM compatibility itself breaks (like syncthing v2), apply [shawl-migration](./shawl-migration.md).

### Using environment variable paths in nssm

nssm supports `REG_EXPAND_SZ` but `nssm set` defaults to `REG_SZ`. Set registry directly via PowerShell:

```powershell
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\<service>\Parameters"
Set-ItemProperty -Path $regPath -Name "Application" -Value '%ChocolateyInstall%\bin\<exe>' -Type ExpandString
```

Or use an expanded literal path:

```bash
gsudo nssm set <service> Application "C:\ProgramData\chocolatey\bin\<exe>"
```

## Topics

| Topic | File | Description |
|-------|------|-------------|
| diagnose | [diagnose.md](./diagnose.md) | nssm service diagnosis procedure |
| metadata-fix | [metadata-fix.md](./metadata-fix.md) | Recovery for UniGetUI/choco metadata (.nuspec) update failures |
| post-upgrade | [post-upgrade.md](./post-upgrade.md) | Post-processing after choco upgrade |
| shawl-migration | [shawl-migration.md](./shawl-migration.md) | NSSM → shawl migration (major upgrades like syncthing v2) |
| update-path | [update-path.md](./update-path.md) | nssm path refresh |

## Scripts

| Mode | Command | Description |
|------|---------|-------------|
| diagnose | `node <skill-dir>/scripts/nssm-manager.js diagnose` | Check all nssm services |
| update-path | `node <skill-dir>/scripts/nssm-manager.js update-path <service>` | Output path refresh command for a specific service |
| post-upgrade | `node <skill-dir>/scripts/nssm-manager.js post-upgrade` | Full post-processing check |

`<skill-dir>` = `~/.claude/skills/choco`

**Note**: `node` may not be on PATH in bash. In an fnm environment, use the full path:

```bash
"$APPDATA/fnm/node-versions/v20.20.0/installation/node.exe" <skill-dir>/scripts/nssm-manager.js <mode>
```

## Administrator Privileges

`nssm set/stop/start` and `choco upgrade` commands require administrator privileges. Per the Windows rule, **using `gsudo` is the default**:

```bash
gsudo choco upgrade <pkg> -y
gsudo nssm set <service> Application "<path>"
```

Or invoke via the PowerShell tool:

```powershell
gsudo powershell -ExecutionPolicy Bypass -File "<script.ps1>"
```

## Topic Dependencies

```text
choco (main workflow)
  ├─→ diagnose (step 1 diagnosis)
  ├─→ metadata-fix (recover stale choco/UniGetUI metadata)
  ├─→ post-upgrade (bulk check after choco upgrade)
  ├─→ update-path (nssm path refresh)
  └─→ shawl-migration (NSSM → shawl migration)
        └─→ shawl binary (~/.local/bin/shawl.exe, downloaded from GitHub releases)
```

- Simple path refresh → `update-path`
- Major upgrade requiring nssm deprecation → `shawl-migration`
- Runtime OK + only chocolatey metadata stale → `metadata-fix`
- Multiple services in bulk → `diagnose` + `post-upgrade`

## Self-heal

This skill is subject to self-improvement after execution.
If malfunction is detected, improve it via `/skill-kit upgrade choco`.

Checklist:
1. Are the trigger keywords in description sufficient?
2. Was the topic selection accurate? (e.g., misrouting metadata stale to update-path)
3. Was the procedure complete? (Was no manual correction needed?)
4. Were there no omissions in the deliverables?

## References

- Previous skill: `choco-nssm` (absorbed into this skill, moved to `~/.claude/.bak/`)
- [Chocolatey docs](https://docs.chocolatey.org/)
- [UniGetUI repo](https://github.com/Devolutions/UniGetUI)
- [shawl repo](https://github.com/mtkennerly/shawl)
