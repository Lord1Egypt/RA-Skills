# cPanel Version 134.0.11 Changes

## Overview

cPanel & WHM version 134.0.11 is a stable release in the 134 LTS (Long Term Support) branch.

## Version Compatibility

| Version Range | Support Status |
|---------------|----------------|
| 134.0.x | Current LTS |
| 134.1.x | Current LTS |
| 130.x - 133.x | Previous LTS (deprecated) |
| 128.x and older | End of Life |

## Key Features in 134.x

### Security Enhancements

1. **Improved API Token ACL**
   - Granular permissions for API tokens
   - Token expiration dates
   - IP restrictions per token

2. **Two-Factor Authentication**
   - TOTP support for WHM login
   - Backup codes
   - Recovery options

3. **SSL Improvements**
   - AutoSSL improvements for Let's Encrypt
   - ECC certificate support
   - Improved certificate validation

### API Changes

#### New UAPI Modules

- `Market` - cPanel Market integration
- `WordPressBackup` - WordPress backup management
- `SitePublisher` - Site Publisher templates

#### Deprecated Functions

| API | Function | Replacement |
|-----|----------|-------------|
| cPanel API 2 | `Email::listpopswithdisk` | `UAPI Email::list_pops` |
| cPanel API 2 | `MysqlFE::listdbs` | `UAPI Mysql::list_databases` |
| cPanel API 2 | `Fileman::listfiles` | `UAPI Fileman::list_files` |

#### New WHM API Functions

- `backup_config` - Configure backup settings
- `restore_backup_config` - Restore backup configuration
- `list_ssl_capable_domains` - List domains that can have SSL

### Performance Improvements

1. **Faster API Responses**
   - Optimized JSON serialization
   - Reduced memory usage
   - Connection pooling

2. **Database Optimization**
   - Improved MySQL query performance
   - Connection caching
   - Query batching

### Breaking Changes

#### 1. API Response Format

All WHM API calls now require `api.version=1`:

```bash
# Old (deprecated)
curl -H "Authorization: whm $TOKEN" "$HOST/json-api/listaccts"

# New (required)
curl -H "Authorization: whm $TOKEN" "$HOST/json-api/listaccts?api.version=1"
```

#### 2. Default Theme

- Default theme changed from `paper_lantern` to `jupiter`
- `paper_lantern` is deprecated

#### 3. PHP Version

- Minimum PHP version: 8.1
- PHP 7.x support removed

#### 4. MySQL Version

- Minimum MySQL version: 5.7
- MariaDB 10.3+ recommended

## Migration from 130.x/132.x

### Pre-Upgrade Checklist

1. **Backup Everything**
   ```bash
   /scripts/pkgacct --backup --all
   ```

2. **Check Compatibility**
   ```bash
   /scripts/check_cpanel_versions
   ```

3. **Update API Calls**
   - Add `api.version=1` to all WHM API calls
   - Replace deprecated cPanel API 2 calls with UAPI

### Post-Upgrade Tasks

1. **Verify Services**
   ```bash
   /scripts/restartsrv_httpd
   /scripts/restartsrv_mysql
   ```

2. **Update API Tokens**
   - Regenerate tokens with appropriate ACL
   - Remove unused tokens

3. **Test API Access**
   ```bash
   curl -H "Authorization: whm $TOKEN" "$HOST/json-api/version"
   ```

## Known Issues in 134.0.11

1. **DNS Cluster Sync**
   - May require manual sync after upgrade
   - Use `/scripts/dnscluster syncall`

2. **SSL Certificate Renewal**
   - AutoSSL may need reconfiguration
   - Check `/var/cpanel/autossl` logs

3. **Email Quota Calculation**
   - May show incorrect values initially
   - Runs `/scripts/generate_maildirsize` to fix

## Version-Specific API Parameters

### 134.0.11 Specific

```bash
# Account creation with new parameters
curl -H "Authorization: whm $TOKEN" \
  "$HOST/json-api/createacct?api.version=1&username=user1&domain=example.com&password=secret&plan=default&contactemail=admin@example.com&language=en"
```

### New in 134.x

| Parameter | Function | Description |
|-----------|----------|-------------|
| language | createacct | Set account language |
| locale | createacct | Set account locale |
| max_email_per_hour | createacct | Email rate limit |
| max_defer_fail_percentage | createacct | Deferred email limit |

## Deprecation Timeline

| Version | Deprecation Date | End of Life |
|---------|-----------------|-------------|
| 130.x | 2024-Q4 | 2025-Q2 |
| 132.x | 2025-Q2 | 2025-Q4 |
| 134.x | 2026-Q2 | 2026-Q4 |

## Resources

- [cPanel 134 Release Notes](https://docs.cpanel.net/release-notes/134-release-notes/)
- [API Documentation](https://api.docs.cpanel.net/)
- [Migration Guide](https://docs.cpanel.net/installation-guide/upgrade-to-cpanel-whm-134/)