# dxyz-cPanel Skill

[![cPanel Version](https://img.shields.io/badge/cPanel-134.0.11-blue.svg)](https://cpanel.net/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A PicoClaw/OpenClaw skill for managing cPanel/WHM hosting accounts via API. Designed for cPanel version 134.0.11 with backward compatibility for versions 130.x–133.x.

## Features

| Category | Capabilities |
|----------|-------------|
| **Account Management** | Create, suspend, unsuspend, terminate hosting accounts |
| **DNS Management** | List, add, modify, delete DNS records (A, AAAA, CNAME, MX, TXT, SRV) |
| **Email Management** | Create/delete email accounts, password changes, forwarders, autoresponders |
| **Database Management** | MySQL & PostgreSQL databases and users, privilege management |
| **SSL Certificates** | List, install, manage SSL certificates including Let's Encrypt |
| **File Operations** | List, upload, copy, move, delete files via File Manager API |
| **Backup Operations** | Create full account backups, restore from backup files |
| **Bandwidth Monitoring** | View bandwidth usage and statistics |

## Installation

### Via PicoClaw CLI
```bash
picoclaw skill install dxyz-cpanel
```

### Via ClawHub Registry
```bash
picoclaw skill install dxyz-cpanel --registry clawhub
```

### Manual Installation
```bash
git clone https://github.com/picodozbotdoz/dxyz-cpanel.git
cd dxyz-cpanel
cp -r . ~/.picoclaw/workspace-default/skills/dxyz-cpanel/
```

## Configuration

### Environment Variables (Recommended)
```bash
export CPANEL_HOST="https://your-server.com:2087"  # WHM port (2087) or cPanel port (2083)
export CPANEL_TOKEN="your-api-token"                # Generate in WHM → Development → Manage API Tokens
export CPANEL_USER="root"                           # WHM username (optional, defaults to root)
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

## Quick Start

### Test Connection
```bash
# Using PicoClaw exec tool
exec command="curl -s -H 'Authorization: whm $CPANEL_TOKEN' '$CPANEL_HOST/json-api/version' | jq ."
```

### List All Accounts
```bash
exec command="curl -s -H 'Authorization: whm $CPANEL_TOKEN' '$CPANEL_HOST/json-api/listaccts?api.version=1' | jq ."
```

### Create New Account
```bash
exec command='curl -s -H "Authorization: whm $CPANEL_TOKEN" "$CPANEL_HOST/json-api/createacct?api.version=1&username=newuser&domain=newdomain.com&password=secure123&plan=default" | jq .'
```

### Create Email Account
```bash
exec command='curl -s -H "Authorization: cpanel $CPANEL_TOKEN" "$CPANEL_HOST/execute/Email/add_pop?email=newuser&password=secure123&domain=example.com&quota=250" | jq .'
```

## API Reference

### Supported APIs

| API | Purpose | Endpoint Prefix | Auth Header |
|-----|---------|-----------------|-------------|
| **WHM API 1** | Server admin, account management | `/json-api/` | `Authorization: whm <token>` |
| **UAPI** | cPanel user operations | `/execute/` | `Authorization: cpanel <token>` |
| **cPanel API 2** | Legacy (deprecated) | `/json-api/cpanel2` | Not recommended |

### Common WHM API Endpoints

| Function | Endpoint |
|----------|----------|
| List accounts | `/json-api/listaccts?api.version=1` |
| Create account | `/json-api/createacct?api.version=1&username=...` |
| Suspend account | `/json-api/suspendacct?api.version=1&user=...` |
| Unsuspend account | `/json-api/unsuspendacct?api.version=1&user=...` |
| Terminate account | `/json-api/removeacct?api.version=1&user=...` |
| Account summary | `/json-api/accountsummary?api.version=1&user=...` |

### Common UAPI Endpoints

| Module | Function | Endpoint |
|--------|----------|----------|
| Email | add_pop | `/execute/Email/add_pop?email=...` |
| Email | list_pops | `/execute/Email/list_pops?domain=...` |
| DNS | add_zone_record | `/execute/DNS/add_zone_record?domain=...` |
| DNS | zone_records | `/execute/DNS/zone_records?domain=...` |
| Mysql | create_database | `/execute/Mysql/create_database?name=...` |
| SSL | list_certs | `/execute/SSL/list_certs` |

## Helper Scripts

The skill includes executable scripts for common operations:

```bash
# Generic API caller
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/cpanel_api.sh listaccts"

# Create hosting account
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/create_account.sh --user=myuser --domain=mydomain.com"

# Manage DNS records
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/manage_dns.sh add example.com www A 192.168.1.1"

# Manage email accounts
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/manage_email.sh create user@example.com password123"

# Manage databases
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/manage_database.sh create mydb"

# Backup operations
exec command="bash ~/.picoclaw/workspace-default/skills/dxyz-cpanel/scripts/backup_account.sh create username"
```

## Documentation

| File | Description |
|------|-------------|
| [SKILL.md](SKILL.md) | Full skill documentation with all operations |
| [references/api-reference.md](references/api-reference.md) | Complete API endpoint reference |
| [references/whm-api.md](references/whm-api.md) | WHM API 1 detailed documentation |
| [references/uapi.md](references/uapi.md) | UAPI module reference |
| [references/error-codes.md](references/error-codes.md) | Common errors and solutions |
| [references/version-134-changes.md](references/version-134-changes.md) | What's new in cPanel 134.0.11 |

## Version Compatibility

| Version | Status | Notes |
|---------|--------|-------|
| **134.0.11** | ✅ Primary Target | Fully tested |
| **134.x.x** | ✅ Supported | API stable |
| **130.x - 133.x** | ⚠️ Backward Compatible | Some features may differ |
| **< 130** | ❌ Not Supported | API differences |

## Security Best Practices

1. **Use API Tokens** - More secure than basic authentication
2. **HTTPS Only** - Always use port 2087 (WHM) or 2083 (cPanel)
3. **Limit Token Permissions** - Use ACL to restrict token capabilities
4. **Enable 2FA** - Two-factor authentication for WHM access
5. **Audit Tokens** - Regularly review and rotate API tokens
6. **Log API Calls** - Enable API logging in WHM for audit trail

## Rate Limits

- **WHM API**: 100 requests/minute
- **UAPI**: Varies by module (check cPanel documentation)

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Access denied` | Invalid token/permissions | Regenerate token, check ACL |
| `Account exists` | Duplicate username | Use different username |
| `Invalid domain` | Domain format/syntax | Check DNS, use FQDN |
| `Quota exceeded` | Disk limit reached | Increase quota or cleanup |
| `Rate limited` | Too many requests | Implement backoff/retry |

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Support

- **Issues**: [GitHub Issues](https://github.com/picodozbotdoz/dxyz-cpanel/issues)
- **cPanel API Docs**: [https://api.docs.cpanel.net/](https://api.docs.cpanel.net/)