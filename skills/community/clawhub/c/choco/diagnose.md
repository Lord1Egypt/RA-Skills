# nssm Service Diagnosis

## When to Use

- nssm service is in `SERVICE_PAUSED` or `SERVICE_STOPPED` state
- Service behavior anomalies after choco upgrade
- When a specific service won't start

## Diagnosis Procedure

### 1. Run the Script

```bash
node scripts/nssm-manager.js diagnose
```

Output content:
- List of all nssm services
- Status of each service (RUNNING/STOPPED/PAUSED)
- Shim status (chocolatey\bin path = shim)
- Actual binary location (inside choco lib)
- List of commands required for fixes

### 2. Manual Diagnosis (if script fails)

```bash
# Service status
nssm status <service>

# Registered path
nssm get <service> Application

# Actual binary location
ls "C:/ProgramData/chocolatey/lib/<package>/tools/"
```

### 3. Shim Identification Criteria

| Path | Type | Service Behavior |
|------|------|------------------|
| `chocolatey\bin\*.exe` | shim (wrapper) | High failure likelihood |
| `chocolatey\lib\*\tools\*\*.exe` | actual binary | Normal |
| Other paths | direct install | Normal |

## Output Interpretation

- `Shim: YES` → Path refresh required via update-path topic
- `Shim: NO` → Investigate other causes (check logs, port conflicts, etc.)
- `Actual binary: not found` → Package was removed or structure changed
