# cPanel Quick Reference Card

## Environment Setup

```bash
export CPANEL_HOST="https://your-server.com:2087"
export CPANEL_TOKEN="your-api-token"
```

## Account Management

| Task | Command |
|------|---------|
| List accounts | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/listaccts?api.version=1"` |
| Create account | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/createacct?api.version=1&username=USER&domain=DOMAIN&password=PASS&plan=PLAN"` |
| Suspend account | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/suspendacct?api.version=1&user=USER"` |
| Unsuspend account | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/unsuspendacct?api.version=1&user=USER"` |
| Delete account | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/removeacct?api.version=1&user=USER"` |

## Email Management

| Task | Command |
|------|---------|
| List emails | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Email/list_pops?domain=DOMAIN"` |
| Create email | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Email/add_pop?email=USER&password=PASS&domain=DOMAIN"` |
| Delete email | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Email/delete_pop?email=USER&domain=DOMAIN"` |
| Add forwarder | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Email/add_forwarder?domain=DOMAIN&email=USER&fwdopt=fwd&fwdemail=DEST"` |

## DNS Management

| Task | Command |
|------|---------|
| List records | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/DNS/zone_records?domain=DOMAIN"` |
| Add A record | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/DNS/add_zone_record?domain=DOMAIN&name=NAME&type=A&address=IP"` |
| Add CNAME | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/DNS/add_zone_record?domain=DOMAIN&name=NAME&type=CNAME&address=TARGET"` |
| Add MX record | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/DNS/add_zone_record?domain=DOMAIN&name=@&type=MX&exchange=MAIL&preference=10"` |

## Database Management

| Task | Command |
|------|---------|
| List databases | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Mysql/list_databases"` |
| Create database | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Mysql/create_database?name=DB"` |
| Create user | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Mysql/create_user?name=USER&password=PASS"` |
| Grant privileges | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Mysql/set_privileges_on_database?user=USER&database=DB&privileges=ALL%20PRIVILEGES"` |

## SSL Certificates

| Task | Command |
|------|---------|
| List certs | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/SSL/list_certs"` |
| Check coverage | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/SSL/can_ssl_redirect?domain=DOMAIN"` |

## File Operations

| Task | Command |
|------|---------|
| List files | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Fileman/list_files?dir=public_html"` |
| Get disk usage | `curl -H "Authorization: cpanel $TOKEN" "$HOST/execute/Fileman/get_disk_usage"` |

## Server Status

| Task | Command |
|------|---------|
| Get version | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/version"` |
| Server load | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/loadavg"` |
| Service status | `curl -H "Authorization: whm $TOKEN" "$HOST/json-api/servicestatus?service=httpd"` |

## Using Helper Scripts

```bash
# Generic API caller
./scripts/cpanel_api.sh whm listaccts "api.version=1"
./scripts/cpanel_api.sh uapi "Email/list_pops" "domain=example.com"

# Account management
./scripts/create_account.sh user1 example.com password123 default

# DNS management
./scripts/manage_dns.sh list example.com
./scripts/manage_dns.sh add example.com www A 192.168.1.1

# Email management
./scripts/manage_email.sh list example.com
./scripts/manage_email.sh create user@example.com password123

# Database management
./scripts/manage_database.sh list mysql
./scripts/manage_database.sh create_db mydb mysql

# Backup operations
./scripts/backup_account.sh list
./scripts/backup_account.sh create username
```

## Response Parsing with jq

```bash
# Get account list
curl -s -H "Authorization: whm $TOKEN" "$HOST/json-api/listaccts?api.version=1" | jq '.data.acct[].user'

# Get email list
curl -s -H "Authorization: cpanel $TOKEN" "$HOST/execute/Email/list_pops?domain=example.com" | jq '.data[].email'

# Check result status
curl -s -H "Authorization: whm $TOKEN" "$HOST/json-api/version" | jq '.metadata.result'
```

## Common Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| api.version | 1 | WHM API version (required) |
| username | string | Account username (max 16 chars) |
| domain | string | Domain name (FQDN) |
| password | string | Password (min 8 chars, complexity required) |
| plan | string | Package name |
| quota | integer | Disk quota in MB |
| bwlimit | integer | Bandwidth limit in MB |
| ttl | integer | DNS TTL (300-86400) |

## Ports

| Service | Port | Protocol |
|---------|------|----------|
| WHM | 2087 | HTTPS |
| cPanel | 2083 | HTTPS |
| Webmail | 2096 | HTTPS |
| HTTP | 80 | HTTP |
| HTTPS | 443 | HTTPS |