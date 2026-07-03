# choco upgrade Post-Processing

## When to Use

- After running `choco upgrade all`
- After upgrading specific packages, to check services

## Procedure

### 1. Run Full Check

```bash
node scripts/nssm-manager.js post-upgrade
```

Output:
- One-line summary of shim status for all nssm services
- List of services requiring updates
- Administrator PowerShell commands (bulk/individual)

### 2. Run Update Commands

Execute the commands output by the script with administrator privileges:

```bash
# Bulk execution (the "Administrator PowerShell commands" section from script output)
powershell -Command "Start-Process powershell -ArgumentList '-Command', '<commands>' -Verb RunAs -Wait"
```

### 3. Check Service Status

```bash
nssm status <service>
```

## Check Targets

The script automatically finds nssm-managed services in `Win32_Service` and checks them:
- All services where `BINARY_PATH_NAME` contains `nssm`
- Verifies whether each service's Application path is a shim
- If shim, searches choco lib for the actual binary

## Notes

- Administrator privileges required (UAC prompt)
- If services are already healthy right after upgrade, refresh is unnecessary
- Binary location may differ per package (within tools/ subfolders)
