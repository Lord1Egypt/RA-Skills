# Troubleshooting Guide for CPA Manager

## Common Issues and Solutions

### 1. Authentication Errors

**Symptom**: `401 Unauthorized` or `Invalid token` errors when running any command.

**Solutions**:
- Verify your management token in `config.json` matches the one in CPA's configuration
- Check that the base URL is correct and reachable from your environment
- Ensure the token has proper management permissions
- Test connectivity: `curl -H "Authorization: Bearer your-token" http://your-cpa-url/v0/management/auth-files`

### 2. Connection Timeouts

**Symptom**: Operations fail with timeout errors or hang indefinitely.

**Solutions**:
- Increase the `timeout` value in `config.json` (default: 15 seconds)
- Reduce `probe_workers` and `action_workers` to lower concurrency
- Check network connectivity between your machine and the CPA service
- Verify CPA service is running and responsive

### 3. Empty or Incomplete Scan Results

**Symptom**: Scan completes but shows no accounts or fewer accounts than expected.

**Solutions**:
- Verify the CPA auth directory contains valid `.json` authentication files
- Check that there are no backup, trash, or log subdirectories in the auth path
- Ensure CPA service can read the auth directory (file permissions)
- Restart CPA service after making changes to the auth directory
- Run a manual test: `curl -H "Authorization: Bearer your-token" http://your-cpa-url/v0/management/auth-files`

### 4. Unexpected Account Deletion

**Symptom**: More accounts deleted than expected during maintenance operations.

**Solutions**:
- Always run `scan` mode first and review output before maintenance
- Use `--no-delete-401` flag to preview maintenance impact
- Check if backup directories were accidentally included in auth path
- Verify quota detection thresholds in configuration
- Restore from backup if necessary

### 5. Database Lock Issues

**Symptom**: SQLite database errors like "database is locked" or corruption messages.

**Solutions**:
- Ensure only one instance of cpa-warden runs at a time
- Delete the `cpa_warden_state.sqlite3` file and restart (loses local state but safe)
- Check file permissions on the database file
- Consider using separate working directories for different operations

### 6. Memory or Resource Exhaustion

**Symptom**: Process crashes, high memory usage, or system becomes unresponsive.

**Solutions**:
- Reduce worker counts significantly (`probe_workers: 5`, `action_workers: 10`)
- Limit the number of accounts being processed simultaneously
- Monitor system resources during operation
- Consider processing accounts in smaller batches

### 7. False Positive 401 Detection

**Symptom**: Valid accounts marked as 401 and deleted incorrectly.

**Solutions**:
- Review the probe logic in `cpa_warden.py` to understand detection criteria
- Adjust retry settings (`retries: 5`) to handle temporary failures
- Manually verify account status before deletion
- Use the manual workflow: `scan -> review -> delete_401_only` instead of full maintain

### 8. Quota Account Misidentification

**Symptom**: Working accounts incorrectly identified as quota-limited.

**Solutions**:
- Understand that quota detection relies on `wham/usage` API responses
- Some providers may have different quota response formats
- Review the quota detection logic in the source code
- Manually verify account status before taking action

## Debugging Steps

### Step 1: Verify Basic Connectivity
```bash
# Test basic API access
curl -H "Authorization: Bearer your-token" http://your-cpa-url/v0/health
curl -H "Authorization: Bearer your-token" http://your-cpa-url/v0/management/auth-files
```

### Step 2: Run Verbose Scan
```bash
# Enable debug mode in config.json
# Set "debug": true
python3 cpa_warden.py --mode scan --config config.json
```

### Step 3: Check Individual Account
```bash
# Test a specific account manually
python3 scan_cpa.py --out-dir /tmp/debug-scan --single-account your-account-file.json
```

### Step 4: Review Logs
- Check `cpa_warden.log` for detailed error messages
- Look for patterns in failed requests
- Identify specific accounts causing issues

### Step 5: Isolate the Problem
- Test with a minimal auth directory (1-2 known good accounts)
- Gradually add more accounts to identify problematic ones
- Compare working vs non-working account structures

## Recovery Procedures

### Accidental Mass Deletion
1. Stop all CPA Manager operations immediately
2. Restore auth directory from backup
3. Restart CPA service
4. Run scan to verify restoration
5. Document the incident and update procedures

### Corrupted State Database
1. Backup current `cpa_warden_state.sqlite3` (if needed for analysis)
2. Delete the corrupted database file
3. Run a fresh scan to rebuild state
4. Proceed with caution on subsequent operations

### Configuration Issues
1. Start with `config.example.json` as a clean template
2. Add settings incrementally, testing each change
3. Keep a backup of working configurations
4. Document any custom settings for your environment

## Support Resources

- Official cpa-warden GitHub: https://github.com/fantasticjoe/cpa-warden
- CPA documentation: Check your CPA deployment documentation
- Community forums: [Add relevant community links for your deployment]
- Issue tracking: Report bugs with detailed reproduction steps

## When to Seek Help

Contact support or developers when:
- You encounter consistent authentication failures with verified credentials
- The tool produces unexpected results that can't be explained by configuration
- You experience crashes or data corruption
- You need clarification on detection logic or behavior