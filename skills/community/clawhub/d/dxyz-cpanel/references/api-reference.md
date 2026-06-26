# cPanel API Reference

## Table of Contents
1. [API Types Overview](#api-types-overview)
2. [WHM API 1](#whm-api-1)
3. [UAPI](#uapi)
4. [cPanel API 2 (Legacy)](#cpanel-api-2-legacy)
5. [Authentication](#authentication)
6. [Response Format](#response-format)
7. [Rate Limiting](#rate-limiting)

---

## API Types Overview

| API | Purpose | Access Level | Endpoint Prefix |
|-----|---------|--------------|-----------------|
| **WHM API 1** | Server administration | root/reseller | `/json-api/` |
| **UAPI** | cPanel user functions | cPanel user | `/execute/` |
| **cPanel API 2** | Legacy operations | cPanel user | `/json-api/cpanel2` |

### When to Use Each API

**WHM API 1:**
- Account creation/deletion
- Server configuration
- DNS clustering
- Backups and restores
- Package management
- Reseller management

**UAPI:**
- Email management
- Database operations
- File operations
- SSL certificates
- DNS zone records (per domain)
- Cron jobs

**cPanel API 2 (Avoid):**
- Legacy applications only
- Being phased out
- Use UAPI instead

---

## WHM API 1

### Account Management

#### createacct
Create a new cPanel account.

**Endpoint:** `/json-api/createacct`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | Account username (max 16 chars) |
| domain | string | Yes | Primary domain |
| password | string | Yes | Account password |
| plan | string | No | Package name |
| email | string | No | Contact email |
| quota | integer | No | Disk quota in MB |
| bwlimit | integer | No | Bandwidth limit in MB |
| hasshell | boolean | No | Enable shell access |
| cpmod | string | No | cPanel theme (default: paper_lantern) |

**Example:**
```bash
curl -H "Authorization: whm $TOKEN" \
  "$HOST/json-api/createacct?api.version=1&username=user1&domain=example.com&password=secret&plan=default"
```

#### listaccts
List all cPanel accounts.

**Endpoint:** `/json-api/listaccts`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| search | string | No | Search pattern |
| searchtype | string | No | Search field (user, domain, owner) |
| want | string | No | Fields to return |

**Example:**
```bash
curl -H "Authorization: whm $TOKEN" \
  "$HOST/json-api/listaccts?api.version=1"
```

#### suspendacct / unsuspendacct
Suspend or unsuspend an account.

**Endpoint:** `/json-api/suspendacct`, `/json-api/unsuspendacct`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user | string | Yes | Account username |
| reason | string | No | Suspension reason |

#### removeacct
Delete an account.

**Endpoint:** `/json-api/removeacct`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user | string | Yes | Account username |
| keepdns | boolean | No | Keep DNS zones |

### Server Information

#### version
Get cPanel version.

```bash
curl -H "Authorization: whm $TOKEN" "$HOST/json-api/version"
```

#### loadavg
Get server load average.

```bash
curl -H "Authorization: whm $TOKEN" "$HOST/json-api/loadavg"
```

#### servicestatus
Check service status.

```bash
curl -H "Authorization: whm $TOKEN" "$HOST/json-api/servicestatus?service=httpd"
```

### DNS Management

#### dumpzone
Export DNS zone.

```bash
curl -H "Authorization: whm $TOKEN" "$HOST/json-api/dumpzone?domain=example.com"
```

#### addzonerecord
Add DNS record to zone.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Zone domain |
| name | string | Yes | Record name |
| type | string | Yes | Record type (A, AAAA, CNAME, etc.) |
| address | string | Yes | Record value |
| ttl | integer | No | TTL in seconds |

---

## UAPI

### Email Module

#### Email::list_pops
List email accounts.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Email/list_pops?domain=example.com"
```

#### Email::add_pop
Create email account.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | Email username |
| password | string | Yes | Password |
| domain | string | Yes | Domain |
| quota | integer | No | Quota in MB |

#### Email::delete_pop
Delete email account.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Email/delete_pop?email=user&domain=example.com"
```

#### Email::add_forwarder
Add email forwarder.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Domain |
| email | string | Yes | Source email |
| fwdopt | string | Yes | Forward type (fwd, pipe, fail) |
| fwdemail | string | Yes | Destination email |

### MySQL Module

#### Mysql::create_database
Create MySQL database.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Mysql/create_database?name=mydb"
```

#### Mysql::create_user
Create MySQL user.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Mysql/create_user?name=myuser&password=secret"
```

#### Mysql::set_privileges_on_database
Grant privileges.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Mysql/set_privileges_on_database?user=myuser&database=mydb&privileges=ALL%20PRIVILEGES"
```

### SSL Module

#### SSL::list_certs
List SSL certificates.

```bash
curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/SSL/list_certs"
```

#### SSL::install_ssl
Install SSL certificate.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Domain name |
| cert | string | Yes | Certificate content |
| key | string | Yes | Private key content |
| cabundle | string | No | CA bundle |

### Fileman Module

#### Fileman::list_files
List directory contents.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Fileman/list_files?dir=public_html"
```

#### Fileman::upload_files
Upload files.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Fileman/upload_files?dir=public_html" \
  -F "file-1=@localfile.txt"
```

#### Fileman::file_copy
Copy files.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/Fileman/file_copy?source=/home/user/public_html/file.txt&dest=/home/user/backup/"
```

### DNS Module

#### DNS::zone_records
List DNS records.

```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/execute/DNS/zone_records?domain=example.com"
```

#### DNS::add_zone_record
Add DNS record.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| domain | string | Yes | Zone domain |
| name | string | Yes | Record name |
| type | string | Yes | Record type |
| address | string | Yes | Record value |
| ttl | integer | No | TTL in seconds |
| preference | integer | No | MX preference |

---

## cPanel API 2 (Legacy)

> ⚠️ **Warning:** cPanel API 2 is deprecated. Use UAPI instead.

Only use cPanel API 2 if UAPI doesn't have the required function.

**Endpoint:** `/json-api/cpanel2`

**Example:**
```bash
curl -H "Authorization: cpanel $TOKEN" \
  "$HOST/json-api/cpanel2?cpanel_jsonapi_module=Email&cpanel_jsonapi_func=listpopswithdisk&cpanel_jsonapi_apiversion=2"
```

---

## Authentication

### API Token (Recommended)

1. **Generate Token:**
   - WHM → Development → Manage API Tokens
   - Click "Generate Token"
   - Set appropriate ACL permissions
   - Copy and store securely

2. **Use Token:**
```bash
# WHM API
curl -H "Authorization: whm YOUR_TOKEN" "$HOST/json-api/version"

# UAPI (cPanel user context)
curl -H "Authorization: cpanel YOUR_TOKEN" "$HOST/execute/Email/list_pops"
```

### Basic Authentication (Not Recommended)

```bash
curl -u 'username:password' "$HOST/json-api/version"
```

### ACL Permissions

| Permission | Description |
|------------|-------------|
| all | Full access |
| create-acct | Create accounts |
| list-accts | List accounts |
| suspend-acct | Suspend accounts |
| kill-acct | Delete accounts |
| edit-acct | Modify accounts |
| passwd | Change passwords |

---

## Response Format

### WHM API 1 Response

```json
{
  "metadata": {
    "result": 1,
    "reason": "OK",
    "version": 1,
    "command": "listaccts"
  },
  "data": {
    "acct": [...]
  }
}
```

### UAPI Response

```json
{
  "apiversion": 3,
  "module": "Email",
  "func": "list_pops",
  "result": {
    "status": 1,
    "messages": null,
    "errors": null,
    "data": [...]
  }
}
```

### Error Response

```json
{
  "metadata": {
    "result": 0,
    "reason": "Account does not exist",
    "version": 1
  }
}
```

---

## Rate Limiting

| API | Limit | Window |
|-----|-------|--------|
| WHM API | 100 requests | per minute |
| UAPI | 200 requests | per minute |

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1620000000
```

### Best Practices

1. Implement exponential backoff on 429 errors
2. Batch operations when possible
3. Cache frequently accessed data
4. Use webhooks for notifications instead of polling