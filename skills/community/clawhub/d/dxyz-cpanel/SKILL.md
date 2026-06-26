---
name: dxyz-cpanel
description: Manage cPanel hosting accounts via API for version 134.0.11 and compatible versions. Supports account management, DNS zones, email accounts, databases (MySQL/PostgreSQL), file operations, SSL certificates, backups, and bandwidth monitoring. Use when managing cPanel/WHM servers, creating accounts, configuring domains, managing email, or performing server administration tasks. Integrates with UAPI, WHM API, and cPanel API 2. Uses exec, read_file, write_file tools for API calls and configuration.
---

# dxyz-cPanel Skill

Manage cPanel hosting accounts via API (version 134.0.11 compatible).

## Quick Start

### Connect to cPanel API
```bash
# Using API token (recommended)
export CPANEL_HOST="https://your-server.com:2087"
export CPANEL_TOKEN="your-api-token"

# Test connection
exec command="curl -s -H 'Authorization: whm $CPANEL_TOKEN' '$CPANEL_HOST/json-api/version' | jq ."
```

### Common Operations

**List Accounts:**
```bash
exec command="curl -s -H 'Authorization: whm $CPANEL_TOKEN' '$CPANEL_HOST/json-api/listaccts?api.version=1' | jq ."
```

**Create Email Account:**
```bash
exec command="curl -s -H 'Authorization: cpanel $CPANEL_TOKEN' '$CPANEL_HOST/execute/Email/add_pop?email=user&password=secure123&domain=example.com' | jq ."
```

## API Types

| API | Purpose | Endpoint Prefix |
|-----|---------|-----------------|
| **WHM API** | Server admin, account management | `/json-api/` |
| **UAPI** | cPanel user operations | `/execute/` |
| **cPanel API 2** | Legacy (deprecated) | `/json-api/cpanel2` |

## Authentication

### API Token (Recommended)
1. Generate in WHM → Development → Manage API Tokens
2. Use header: `Authorization: whm <token>` (WHM) or `Authorization: cpanel <token>` (UAPI)

### Basic Auth (Less Secure)
```bash
curl -u 'username:password' 'https://server:2087/json-api/...'
```

## Core Operations

### Account Management (WHM API)

**Create Account:**
```bash
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/createacct?api.version=1&username=newuser&domain=newdomain.com&password=secure123&plan=default" | jq .'
```

**Suspend/Unsuspend:**
```bash
# Suspend
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/suspendacct?api.version=1&user=username&reason=non-payment" | jq .'

# Unsuspend
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/unsuspendacct?api.version=1&user=username" | jq .'
```

**Terminate Account:**
```bash
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/removeacct?api.version=1&user=username" | jq .'
```

### DNS Management (UAPI)

**List DNS Zones:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/DNS/zone_records?domain=example.com" | jq .'
```

**Add DNS Record:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/DNS/add_zone_record?domain=example.com&name=www&type=A&address=192.168.1.1&ttl=3600" | jq .'
```

### Email Management (UAPI)

**List Email Accounts:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Email/list_pops?domain=example.com" | jq .'
```

**Create Email Account:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Email/add_pop?email=newuser&password=secure123&domain=example.com&quota=250" | jq .'
```

**Set Email Forwarder:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Email/add_forwarder?domain=example.com&email=user&fwdopt=fwd&fwdemail=dest@example.org" | jq .'
```

### Database Management (UAPI)

**Create MySQL Database:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Mysql/create_database?name=mydb" | jq .'
```

**Create MySQL User:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Mysql/create_user?name=myuser&password=secure123" | jq .'
```

**Grant Privileges:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Mysql/set_privileges_on_database?user=myuser&database=mydb&privileges=ALL%20PRIVILEGES" | jq .'
```

### SSL Certificates (UAPI)

**List SSL Certificates:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/SSL/list_certs" | jq .'
```

**Install Let's Encrypt:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/SSL/install_ssl?domain=example.com&cert=$(cat cert.pem | jq -sR .)&key=$(cat key.pem | jq -sR .)" | jq .'
```

### File Operations (UAPI)

**List Files:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Fileman/list_files?dir=public_html" | jq .'
```

**Upload File:**
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Fileman/upload_files?dir=public_html&file-1=@localfile.txt" | jq .'
```

### Backup Operations (WHM API)

**Create Account Backup:**
```bash
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/backupacct?api.version=1&user=username" | jq .'
```

**Restore Account:**
```bash
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/restoreacct?api.version=1&user=username" | jq .'
```

## Scripts

The skill includes helper scripts:

- `scripts/cpanel_api.sh` - Generic API caller with error handling
- `scripts/create_account.sh` - Create hosting account
- `scripts/manage_dns.sh` - DNS zone management
- `scripts/manage_email.sh` - Email account operations
- `scripts/manage_database.sh` - MySQL/PostgreSQL operations
- `scripts/backup_account.sh` - Backup/restore operations

Execute scripts using `exec` tool:
```bash
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/cpanel_api.sh listaccts"
```

## References

Load reference files using `read_file` tool when needed:

- **API Reference**: [references/api-reference.md](references/api-reference.md) - Complete API endpoint reference
- **WHM API**: [references/whm-api.md](references/whm-api.md) - WHM API 1 documentation
- **UAPI**: [references/uapi.md](references/uapi.md) - UAPI module reference
- **Error Codes**: [references/error-codes.md](references/error-codes.md) - Common errors and solutions
- **Version 134 Changes**: [references/version-134-changes.md](references/version-134-changes.md) - What's new in 134.0.11

## Configuration

### Environment Variables
```bash
CPANEL_HOST="https://your-server.com:2087"  # WHM port
CPANEL_TOKEN="your-api-token"                # API token
CPANEL_USER="root"                           # WHM username
```

### Config File
Create `~/.cpanel/config.json`:
```json
{
  "host": "https://your-server.com:2087",
  "token": "your-api-token",
  "default_plan": "default",
  "default_quota": 1000,
  "default_bwlimit": 10000
}
```

## Version Compatibility

This skill supports:
- **cPanel 134.0.11** (primary target)
- **cPanel 134.x.x** (all 134 minor versions)
- **cPanel 130.x - 133.x** (backward compatible, some features may differ)

### Version-Specific Notes

- **134.0.11**: Current target version
- **134.0.x**: API stable, minor bug fixes
- **134.1.x**: Feature additions, API backward compatible
- **Pre-134**: Some UAPI modules may differ

## Best Practices

1. **Use API Tokens**: More secure than basic auth
2. **Rate Limiting**: Max 100 requests/minute for WHM API
3. **Error Handling**: Check `metadata.result` for status
4. **Idempotency**: Use `api.version=1` for consistent responses
5. **Logging**: Enable API logs in WHM for audit trail
6. **Backups**: Always backup before destructive operations

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Access denied` | Invalid token/permissions | Regenerate token, check ACL |
| `Account exists` | Duplicate username | Use different username |
| `Invalid domain` | Domain format/syntax | Check DNS, use FQDN |
| `Quota exceeded` | Disk limit reached | Increase quota or cleanup |

## Security Notes

- Store API tokens securely (use environment variables or encrypted config)
- Use HTTPS (port 2087 for WHM, 2083 for cPanel)
- Limit API token permissions via ACL
- Enable two-factor authentication for WHM access
- Audit API token usage regularly