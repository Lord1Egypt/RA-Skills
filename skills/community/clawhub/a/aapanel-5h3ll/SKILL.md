---
name: aaPanel-Server-Skill
description: aaPanel/BT-Panel server monitoring and file management skill — system resources, site status, service status, SSH logs, cron jobs, log reading, and remote file operations
user-invocable: true
disable-model-invocation: false
icon: icon/bt.png
metadata:
  openclaw:
    requires:
      bins:
        - python3
    keywords:
      - aaPanel
      - BT-Panel
      - panel
      - server monitoring
      - system resources
      - CPU monitoring
      - memory monitoring
      - disk monitoring
      - site status
      - SSL certificates
      - service status
      - log reading
      - SSH
      - crontab
      - backup tasks
      - file management
      - file operations
      - directory browsing
      - file editing
      - database management
      - firewall
      - FTP accounts
      - PHP version
---

# aaPanel / BT-Panel — Monitoring & File Management

Combined server monitoring and file operations toolkit for aaPanel/BT-Panel. Supports multi-server management, resource monitoring, site status checks, service status, SSH security audits, cron job management, log reading, and remote file/directory operations.

![aaPanel](icon/bt-logo.svg)

**Skill version:** 1.0.7  
**aaPanel dependency:** >= 9.0.0 | Python >= 3.10

---

## aaPanel Skills Ecosystem

This is a combined skill containing both monitoring and file management:

| Capability | Description |
|-----------|-------------|
| **Monitoring** | CPU, memory, disk, network, site status, SSL certs, services, SSH logs, cron jobs |
| **File Operations** | Browse, read, edit, create, delete, chmod files and directories |

**Official aaPanel:** https://github.com/aaPanel

---

## Quick Start

### 1. Add a Server

```bash
python3 scripts/bt-config.py add -n my-server -H https://panel.example.com:8888 -t YOUR_TOKEN
```

**Getting an API Token:**
1. Log in to aaPanel → **Panel Settings → API Interface** → Get API Token
2. If using a self-signed certificate, add `--verify-ssl false`

### 2. Run a Health Check

```bash
python3 scripts/monitor.py --server my-server
python3 scripts/sites.py --server my-server
python3 scripts/services.py --server my-server
```

### 3. Browse Server Files

```bash
python3 scripts/files.py ls /www
python3 scripts/files.py cat /www/server/nginx/conf/nginx.conf
```

---

## CLI Commands

### Monitoring

```bash
python3 scripts/monitor.py                          # All servers, JSON
python3 scripts/monitor.py --server my-server       # Specific server
python3 scripts/monitor.py --format table          # Table output

python3 scripts/sites.py --filter ssl-warning       # SSL expiring soon
python3 scripts/sites.py --filter stopped          # Stopped sites

python3 scripts/services.py                         # Service status
python3 scripts/services.py --service nginx         # Specific service

python3 scripts/ssh.py --logs --filter failed      # Failed SSH logins
python3 scripts/ssh.py --status                     # SSH service status

python3 scripts/logs.py --service nginx --lines 100  # Nginx error log
python3 scripts/logs.py --service mysql            # MySQL log

python3 scripts/crontab.py --backup-only           # Backup cron jobs
```

### File Operations

```bash
python3 scripts/files.py ls /www                   # Browse directory
python3 scripts/files.py cat /www/config.php       # Read file
python3 scripts/files.py edit /www/config.php "new content"  # Edit file
python3 scripts/files.py mkdir /www/newdir         # Create directory
python3 scripts/files.py touch /www/test.txt       # Create file
python3 scripts/files.py rm /www/old.txt           # Delete file
python3 scripts/files.py chmod 755 /www/file.txt   # Change permissions
python3 scripts/files.py stat /www/file.txt        # View permissions

python3 scripts/download.py --url "https://..."    # Download file to server
python3 scripts/unzip.py /www/archive.zip          # Extract ZIP on server
```

### Config Management

```bash
python3 scripts/bt-config.py list                   # List servers
python3 scripts/bt-config.py add -n s1 -H https://... -t TOKEN  # Add server
python3 scripts/bt-config.py remove my-server     # Remove server
python3 scripts/bt-config.py threshold --cpu 80    # Set alert thresholds
```

### SSL Certificate Management

```bash
python3 scripts/ssl_certs.py list --server my-server           # List SSL certificates
python3 scripts/ssl_certs.py info --server my-server --site example.com  # Get site SSL info
python3 scripts/ssl_certs.py provision --server my-server --site example.com  # Let's Encrypt
python3 scripts/ssl_certs.py renew --server my-server --site example.com    # Renew certificate
python3 scripts/ssl_certs.py revoke --server my-server --site example.com   # Revoke/disable SSL
```

### Site Management

```bash
python3 scripts/sites_mgmt.py list --server my-server            # List all sites
python3 scripts/sites_mgmt.py create --server my-server --name example.com --path /www/wwwroot/example.com --php 83  # Create site
python3 scripts/sites_mgmt.py delete --server my-server --name example.com  # Delete site
python3 scripts/sites_mgmt.py add-domain --server my-server --site example.com --domain www.example.com  # Add domain
python3 scripts/sites_mgmt.py remove-domain --server my-server --site example.com --domain www.example.com  # Remove domain
python3 scripts/sites_mgmt.py domains --server my-server --site example.com  # List site domains
```

### Database Management

```bash
python3 scripts/databases.py list --server my-server                # List databases
python3 scripts/databases.py create --server my-server --name mydb --user dbuser --password Secret123  # Create database
python3 scripts/databases.py delete --server my-server --name mydb  # Delete database
python3 scripts/databases.py create-user --server my-server --user newuser --password Secret123  # Create user
python3 scripts/databases.py grant --server my-server --user dbuser --db mydb  # Grant privileges
```

### Firewall Management

```bash
python3 scripts/firewall.py list --server my-server          # List firewall rules
python3 scripts/firewall.py status --server my-server        # Get firewall status
python3 scripts/firewall.py allow --server my-server --ip 192.168.1.100  # Whitelist IP
python3 scripts/firewall.py deny --server my-server --ip 10.0.0.50      # Blacklist IP
python3 scripts/firewall.py remove --server my-server --ip 10.0.0.50    # Remove IP from list
```

### FTP Account Management

```bash
python3 scripts/ftp.py list --server my-server                    # List FTP accounts
python3 scripts/ftp.py create --server my-server --user ftpuser --password Secret123 --path /www/wwwroot  # Create FTP account
python3 scripts/ftp.py delete --server my-server --id 1           # Delete FTP account
python3 scripts/ftp.py set-password --server my-server --id 1 --password NewSecret123  # Set password
```

### PHP Version Management

```bash
python3 scripts/php.py list --server my-server              # List installed PHP versions
python3 scripts/php.py set --server my-server --site example.com --version 83  # Set PHP version
python3 scripts/php.py get --server my-server --site example.com  # Get current PHP version

---

## Alert Configuration

Edit `~/.openclaw/bt-skills.yaml` to set alert thresholds:

```yaml
global:
  thresholds:
    cpu: 80      # CPU usage alert threshold (%)
    memory: 85   # Memory usage alert threshold (%)
    disk: 90     # Disk usage alert threshold (%)
```

### SSL Certificate Alert Levels

| Days Remaining | Level |
|---------------|-------|
| Expired | critical |
| ≤ 7 days | critical |
| ≤ 30 days | warning |

---

## Config File

**Location:** `~/.openclaw/bt-skills.yaml`  
**Contains:** Server configs, API tokens, alert thresholds  
Server configs and tokens are stored locally in `~/.openclaw/bt-skills.yaml`.

---

## Monitoring Metrics

### System Resources
CPU usage, cores, model • Memory total/used/free • Disk usage per partition • Network speed/traffic • Load averages • System info (hostname, OS, uptime, panel version)

### Site Status Checks
PHP, Java, Node.js, Go, Python, .NET, Proxy, Static HTML — running/stopped/starting, SSL status, process info (PID, memory, CPU), backend health for proxies

### Service Status
Nginx, Apache, MySQL, Redis, Memcached, Pure-FTPD, PHP (multi-version), PostgreSQL — with error/slow logs where applicable

### File Operations
Browse • Read (with tail) • Edit (with concurrency protection) • Create files/dirs • Delete to recycle bin • chmod/chown with recursive support

---

## Troubleshooting

```bash
# Check config
python3 scripts/bt-config.py list

# Test connection
python3 scripts/monitor.py --server my-server

# Check Python environment
python3 scripts/check_env.py
```
