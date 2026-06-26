# Error Codes Reference

## ⚠️ Security Reminders

- **Always use `--dry-run`** before mutation operations
- **Never commit credentials** to version control
- **Use least-privilege OAuth scopes** for your app
- **Test in sandbox enterprise** before production

## Authentication Errors

### INVALID_TOKEN

**Code:** `AUTH_001`

**Message:** `Invalid or expired token`

**Cause:**
- Token has expired
- Credentials have been revoked
- First-time use without authentication

**Solution:**
```bash
# Re-authenticate
dws auth login --client-id <app-key> --client-secret <app-secret>
```

### PERMISSION_DENIED

**Code:** `AUTH_002`

**Message:** `Permission denied`

**Cause:**
- App lacks required permissions
- User not in whitelist
- Enterprise admin hasn't approved

**Solution:**
1. Check app permissions in DingTalk Open Platform Console
2. Contact enterprise admin for approval
3. Join DingTalk DWS co-creation group for whitelist setup

## Resource Errors

### RESOURCE_NOT_FOUND

**Code:** `RES_001`

**Message:** `Resource not found`

**Cause:**
- Invalid ID (base-id, table-id, user-id, etc.)
- Resource has been deleted
- Typo in ID

**Solution:**
```bash
# Verify ID with schema introspection
dws schema aitable.query_records --jq '.tool.parameters'

# List available resources
dws aitable base list --jq '.result[] | .baseId'
```

### INVALID_PARAMETER

**Code:** `RES_002`

**Message:** `Invalid parameter value`

**Cause:**
- Wrong date format (should be ISO 8601)
- Invalid enum value
- Missing required field

**Solution:**
```bash
# Check parameter schema
dws schema <product>.<operation> --jq '.tool.parameters'

# Use correct date format
# Wrong: "2024/03/29"
# Right: "2024-03-29T14:00:00Z"
```

## Rate Limiting

### RATE_LIMITED

**Code:** `RATE_001`

**Message:** `Rate limit exceeded`

**Cause:**
- Too many requests in short time
- Enterprise API quota exceeded

**Solution:**
```bash
# Wait and retry with exponential backoff
sleep 5
dws <command>

# Reduce request frequency
# Use --jq to reduce response size
```

## Network Errors

### NETWORK_TIMEOUT

**Code:** `NET_001`

**Message:** `Request timeout`

**Cause:**
- Network connectivity issue
- Server overload
- Large response

**Solution:**
```bash
# Increase timeout
dws <command> --timeout 60

# Reduce response size
dws <command> --jq '.result[] | {id: .id}'

# Retry
dws <command>
```

### NETWORK_ERROR

**Code:** `NET_002`

**Message:** `Network error`

**Cause:**
- No internet connection
- DNS resolution failure
- Firewall blocking

**Solution:**
```bash
# Check connectivity
curl https://oapi.dingtalk.com

# Check DWS_TRUSTED_DOMAINS
echo $DWS_TRUSTED_DOMAINS
```

## Operation Errors

### OPERATION_FAILED

**Code:** `OP_001`

**Message:** `Operation failed`

**Cause:**
- Business logic validation failed
- Conflicting operation
- Resource in use

**Solution:**
```bash
# Check operation details with --dry-run
dws <command> --dry-run

# Review error message for details
# Retry with corrected parameters
```

### CONFLICT

**Code:** `OP_002`

**Message:** `Resource conflict`

**Cause:**
- Duplicate resource
- Concurrent modification
- State mismatch

**Solution:**
```bash
# Check existing resources
dws <resource> list

# Retry with different parameters
```

## Recovery Workflow

When encountering errors, follow this workflow:

### Step 1: Identify Error Type

```bash
# Enable debug mode
export DWS_DEBUG=1
dws <command>
```

### Step 2: Check Error Code

Look for error code in response:
- `AUTH_*`: Authentication issue → Re-authenticate
- `RES_*`: Resource issue → Verify IDs
- `RATE_*`: Rate limit → Wait and retry
- `NET_*`: Network issue → Check connectivity
- `OP_*`: Operation issue → Review parameters

### Step 3: Apply Fix

Based on error type, apply the corresponding solution above.

### Step 4: Recovery Event

If you receive a `RECOVERY_EVENT_ID`:

```bash
dws --recovery <RECOVERY_EVENT_ID>
```

This will replay the operation with corrected parameters.

## Debugging Tips

### Enable Verbose Logging

```bash
export DWS_DEBUG=1
dws <command>
```

### Use Dry-Run

```bash
# Preview before executing
dws <mutation-command> --dry-run
```

### Check Schema

```bash
# Verify parameter names and types
dws schema <product>.<operation>
```

### Test with Minimal Input

```bash
# Start with required fields only
dws <command> --required-field <value>

# Add optional fields one by one
```

### Use jq for Focused Output

```bash
# Extract error details
dws <command> --jq '.error'
```
