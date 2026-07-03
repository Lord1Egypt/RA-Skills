# nssm Path Refresh

## When to Use

- When refreshing the path of a specific service detected as a shim by diagnose
- When the existing binary path no longer exists after choco upgrade because the version folder changed (stale path)

## Procedure

### 1. Check Refresh Command

```bash
node scripts/nssm-manager.js update-path <service-name>
```

JSON output:
```json
{
  "service": "syncthing",
  "current": "C:\\ProgramData\\chocolatey\\bin\\syncthing.exe",
  "actual": "C:\\ProgramData\\chocolatey\\lib\\syncthing\\tools\\syncthing-windows-amd64-v2.0.15\\syncthing.exe",
  "commands": [
    "nssm stop \"syncthing\"",
    "nssm set \"syncthing\" Application \"...actual path...\"",
    "nssm start \"syncthing\""
  ]
}
```

### 2. Run with Administrator Privileges

```bash
powershell -Command "Start-Process powershell -ArgumentList '-Command', 'nssm stop \"<svc>\"; nssm set \"<svc>\" Application \"<actual-path>\"; nssm start \"<svc>\"' -Verb RunAs -Wait"
```

### 3. Verify

```bash
nssm status <service>
nssm get <service> Application
```

## Path Selection Strategy

### Stable Shim Path (recommended)

`%ChocolateyInstall%\bin\<exe>` — Path remains unchanged after choco upgrade.

```bash
gsudo nssm set <service> Application "C:\ProgramData\chocolatey\bin\<exe>"
```

Use the version-specific actual path only when the shim conflicts with the service (immediate process termination → nssm misinterprets as crash).

### Version-Specific Actual Path (only when shim conflicts)

`chocolatey\lib\*\tools\*` — Stable, but **breaks on every upgrade**. Using this path requires a post-upgrade hook.

## Path Change Pattern During Version Upgrades

```
v1.27.x: chocolatey\lib\syncthing\tools\syncthing-windows-amd64-v1.27.x\syncthing.exe
v2.0.15: chocolatey\lib\syncthing\tools\syncthing-windows-amd64-v2.0.15\syncthing.exe
v2.0.16: chocolatey\lib\syncthing\tools\syncthing-windows-amd64-v2.0.16\syncthing.exe
```

Folder name changes with each version, requiring refresh every time.

### Real Case: syncthing v2.0.15 → v2.0.16 (2026-04-30)

- After `choco upgrade syncthing`, NSSM pointed to the v2.0.15 path → `SERVICE_STOPPED`
- Not a shim, but the **previous version's path of the actual binary** — undetectable by `isChocoShim()`
- Resolved by adding `isStaleChocoPath()`: if a path under `chocolatey\lib\` exists but the file does not, it is treated as stale
