# Safety Guidelines for CPA Manager

## ⚠️ Critical Safety Warnings

### 1. Never Commit Credentials
- **NEVER** commit actual tokens, API keys, or credentials to version control
- Always use `config.example.json` as a template and create local `config.json` with real credentials
- Ensure `.gitignore` includes `config.json`, `*.log`, `*.sqlite3`, and JSON output files

### 2. Test Before Destructive Operations
- Always run `scan` mode first to understand the current state
- Review the output files (`cpa_401_accounts.json`, `cpa_quota_accounts.json`) before running `maintain`
- Use `--no-delete-401` flag to preview what would be affected

### 3. Backup Strategy
- Backup your auth directory **outside** the CPA auth directory structure
- Never place backup directories inside `/path/to/cpa/auth/` as they will be scanned by CPA
- Keep backups in a separate location like `/path/to/backups/cpa-auth/`

### 4. Directory Structure Safety
- Only valid authentication files should be in the CPA auth directory
- Remove any `backup-*`, `trash-*`, `logs`, or other subdirectories from auth directory
- CPA recursively scans all subdirectories, treating all `.json` files as potential accounts

### 5. Production Environment Precautions
- Run CPA Manager in a controlled environment with proper access controls
- Limit who can execute maintenance operations
- Monitor logs and output files regularly
- Set appropriate worker counts to avoid overwhelming the CPA service

## Safe Usage Patterns

### Read-Only Operations (Safe)
```bash
# These operations only read data, never modify
python3 cpa_warden.py --mode scan --config config.json
python3 scan_cpa.py --out-dir /tmp/scan-results
```

### Controlled Write Operations (Use with Caution)
```bash
# These operations modify CPA state - always test first
python3 delete_401_only.py --input /tmp/scan-results/cpa_401_accounts.json
python3 cpa_warden.py --mode maintain --config config.json --yes
```

### Recovery Operations (Emergency Use)
```bash
# Use only when quota accounts were accidentally disabled
python3 reenable_quota.py --input /tmp/scan-results/cpa_quota_accounts.json
```

## Environment Variables vs Config Files

Prefer environment variables for sensitive data in production:
- `CPA_BASE_URL` instead of hardcoding in config
- `CPA_TOKEN` instead of storing in config files

For development and testing, use `config.json` but ensure it's in `.gitignore`.

## Rate Limiting Considerations

- Start with lower worker counts (`probe_workers: 10`, `action_workers: 20`)
- Monitor CPA service performance during scans
- Increase workers gradually based on service capacity
- Use appropriate timeout and retry settings

## Audit Trail

Always maintain an audit trail:
- Keep scan output files with timestamps
- Log all maintenance operations
- Document any manual interventions
- Track changes to the auth directory structure