# cPanel Error Codes Reference

## Common Errors

### Authentication Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| 401 | Access denied | Invalid API token | Regenerate token in WHM |
| 403 | Permission denied | Insufficient ACL | Update token permissions |
| 401 | Invalid credentials | Wrong username/password | Check credentials |
| 403 | IP blocked | IP not in whitelist | Add IP to allow list |

### Account Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| -1 | Account exists | Username already taken | Use different username |
| -1 | Domain exists | Domain already assigned | Check domain ownership |
| -1 | Invalid username | Username format invalid | Use 8 chars, alphanumeric |
| -1 | Invalid domain | Domain format invalid | Use valid FQDN |
| -1 | Invalid password | Password too weak | Use stronger password |
| -1 | Package not found | Plan doesn't exist | Create package first |
| -1 | Quota exceeded | Server disk full | Free up disk space |

### DNS Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| -1 | Zone not found | DNS zone doesn't exist | Create zone first |
| -1 | Record exists | Duplicate DNS record | Use different name |
| -1 | Invalid record | Invalid DNS record | Check record format |
| -1 | Zone locked | Zone being modified | Wait and retry |

### Email Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| -1 | Email exists | Account already exists | Use different email |
| -1 | Invalid email | Email format invalid | Check email format |
| -1 | Quota exceeded | Disk quota reached | Increase quota |
| -1 | Password too weak | Password policy violation | Use stronger password |

### Database Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| -1 | Database exists | DB already exists | Use different name |
| -1 | User exists | DB user already exists | Use different username |
| -1 | Access denied | User lacks privileges | Grant privileges |
| 1045 | Access denied | MySQL auth failed | Check credentials |
| 1007 | Can't create database | DB exists | Check if DB exists |
| 1396 | Operation failed | User doesn't exist | Create user first |

### SSL Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| -1 | Invalid certificate | Cert format invalid | Check PEM format |
| -1 | Invalid key | Key format invalid | Check private key |
| -1 | Key mismatch | Cert/key don't match | Verify key pair |
| -1 | Domain mismatch | Cert domain doesn't match | Use correct cert |

### File Errors

| Code | Error | Cause | Solution |
|------|-------|-------|----------|
| -1 | File not found | File doesn't exist | Check path |
| -1 | Permission denied | Insufficient permissions | Check file permissions |
| -1 | Directory not found | Directory doesn't exist | Create directory |
| -1 | Disk quota exceeded | Account disk full | Free up space |

## HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Server error |
| 503 | Service Unavailable | Service down |

## Error Response Format

### WHM API Error

```json
{
  "metadata": {
    "result": 0,
    "reason": "Account does not exist",
    "version": 1,
    "command": "suspendacct"
  }
}
```

### UAPI Error

```json
{
  "apiversion": 3,
  "module": "Email",
  "func": "add_pop",
  "result": {
    "status": 0,
    "messages": null,
    "errors": ["The email account already exists."],
    "data": null
  }
}
```

## Troubleshooting Guide

### 1. Authentication Fails

**Symptoms:**
- 401 Unauthorized
- "Access denied" error

**Steps:**
1. Verify API token is valid
2. Check token ACL permissions
3. Verify IP whitelist
4. Check token hasn't expired

```bash
# Test authentication
curl -v -H "Authorization: whm $TOKEN" "$HOST/json-api/version"
```

### 2. Account Creation Fails

**Symptoms:**
- "Account exists" error
- "Invalid username" error

**Steps:**
1. Check if username exists:
   ```bash
   curl -H "Authorization: whm $TOKEN" "$HOST/json-api/listaccts?api.version=1&search=username"
   ```
2. Verify username format (8 chars, alphanumeric, lowercase)
3. Check domain availability
4. Verify package exists

### 3. DNS Record Not Added

**Symptoms:**
- "Zone not found" error
- Record not appearing

**Steps:**
1. Verify zone exists:
   ```bash
   curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/DNS/zone_records?domain=example.com"
   ```
2. Check record format
3. Verify TTL is valid (300-86400)
4. Check for duplicate records

### 4. Email Account Creation Fails

**Symptoms:**
- "Email exists" error
- "Quota exceeded" error

**Steps:**
1. Check if email exists:
   ```bash
   curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Email/list_pops?domain=example.com"
   ```
2. Verify disk quota available
3. Check password strength
4. Verify email format

### 5. Database Connection Fails

**Symptoms:**
- "Access denied" error
- Connection timeout

**Steps:**
1. Verify database exists
2. Check user privileges
3. Verify password
4. Check MySQL service status:
   ```bash
   curl -H "Authorization: whm $TOKEN" "$HOST/json-api/servicestatus?service=mysql"
   ```

## Debug Mode

Enable verbose output for debugging:

```bash
# WHM API with debug
curl -v -H "Authorization: whm $TOKEN" "$HOST/json-api/listaccts?api.version=1"

# Check cPanel error logs
tail -f /usr/local/cpanel/logs/error_log

# Check API access logs
tail -f /usr/local/cpanel/logs/access_log
```

## Support Resources

- [cPanel Documentation](https://docs.cpanel.net/)
- [cPanel Forums](https://forums.cpanel.net/)
- [API Documentation](https://api.docs.cpanel.net/)
- [Error Code Reference](https://api.docs.cpanel.net/cpanel/error-codes/)