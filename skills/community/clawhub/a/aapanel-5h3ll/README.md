# aaPanel / BT-Panel — OpenClaw Skill

![aaPanel OpenClaw Skill](icon/bt.png)

[![clawhub](https://img.shields.io/badge/ClawHub-aapanel--5h3ll-ff6b35?style=flat-square)](https://clawhub.ai/skills/aapanel-5h3ll)
[![GitHub](https://img.shields.io/badge/GitHub-social5h3ll/aapanel--openclaw--skill-24292f?style=flat-square)](https://github.com/social5h3ll/aapanel-openclaw-skill)
[![Version](https://img.shields.io/badge/Version-1.0.7-3b82f6?style=flat-square)](#)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square)](#)
[![aaPanel](https://img.shields.io/badge/aaPanel-≥9.0.0-e34f26?style=flat-square)](#)

![X](icon/x-logo.png [@social5h3ll](https://x.com/social5h3ll))

**Version:** 1.0.7  
**Author:** [5H3LL / social5h3ll](https://github.com/social5h3ll) · [:bird: @social5h3ll](https://x.com/social5h3ll)  
**License:** MIT  
**Repository:** [github.com/social5h3ll/aapanel-openclaw-skill](https://github.com/social5h3ll/aapanel-openclaw-skill)  
**ClawHub:** [clawhub.ai/skills/aapanel-5h3ll](https://clawhub.ai/skills/aapanel-5h3ll)

---

A fully-featured [OpenClaw](https://github.com/openclaw/openclaw) skill for managing and monitoring **aaPanel/BT-Panel** servers. Connect one or more aaPanel instances and manage sites, SSL certificates, databases, firewall rules, FTP accounts, PHP versions, and more — directly from OpenClaw.

Built for homelab enthusiasts, sysadmins, and developers who run aaPanel as their server management panel.

---

## Install

```bash
# One command — ClawHub handles everything
clawhub install aapanel-5h3ll

# Update to latest version
clawhub update aapanel-5h3ll
```

**Requirements:** Python 3.10+, `requests`, `pyyaml`, `rich`

```bash
pip install requests pyyaml rich
```

---

## Features

### 🔍 Server Monitoring
- **System resources** — CPU usage, RAM, disk (per partition), network throughput, load averages
- **Site status** — All sites/projects with running/stopped state, SSL certificate expiry tracking
- **Service status** — Nginx, Apache, MySQL, Redis, Memcached, PHP (multi-version), PostgreSQL
- **Log reading** — Nginx, Apache, MySQL error/slow logs, Redis, PostgreSQL
- **SSH audit** — Failed/successful login attempts with IP geolocation, firewall status, Fail2Ban state
- **Cron job inspection** — Backup tasks, shell scripts, sync jobs, log rotation

### 🔒 SSL Certificates
- List all site SSL certificates with expiry dates and issuer info
- Provision Let's Encrypt certificates automatically
- Renew expiring certificates
- Revoke certificates

### 🌐 Site Management
- Create and delete websites
- Add and remove domain bindings
- Switch PHP versions per site
- Full project type support: PHP, Java, Node.js, Go, Python, .NET, Proxy, Static HTML

### 🗄️ Database Management
- List all databases
- Create and delete databases
- Create database users with password
- Grant and revoke user privileges

### 🔥 Firewall / IP Management
- List firewall rules and current status
- Add IP addresses to whitelist
- Add IP addresses to blacklist
- Remove IPs from firewall

### 📂 FTP Account Management
- List all FTP accounts
- Create and delete FTP users
- Set FTP user passwords

### 📁 File Operations
- Browse remote directories with pagination
- Read files (full content or last N lines)
- Edit files with concurrency protection
- Create files and directories
- Delete to aaPanel recycle bin
- chmod/chown with recursive directory support

### ⚙️ Multi-Server Management
- Add, list, and remove multiple aaPanel servers via config tool
- Per-server health checks with configurable alert thresholds
- Global threshold configuration in `~/.openclaw/bt-skills.yaml`

---

## Quick Start

### 1. Add a Server

```bash
python3 scripts/bt-config.py add \
  -n my-server \
  -H https://panel.example.com:8888 \
  -t YOUR_API_TOKEN
```

> **Self-signed certificate?** Add `--verify-ssl false` to the add command.

**Getting an API token:**
1. Log in to your aaPanel web UI
2. Go to **Panel Settings → API Interface**
3. Click **Get API Token**
4. Ensure your calling server's IP is whitelisted in the aaPanel IP whitelist

### 2. Run a Health Check

```bash
python3 scripts/monitor.py --server my-server --format table
python3 scripts/sites.py --server my-server
python3 scripts/services.py --server my-server
```

### 3. Manage SSL Certificates

```bash
python3 scripts/ssl_certs.py --server my-server --list          # List all certs
python3 scripts/ssl_certs.py --server my-server --issue mysite.com  # Provision Let's Encrypt
python3 scripts/ssl_certs.py --server my-server --renew mysite.com  # Renew certificate
python3 scripts/ssl_certs.py --server my-server --revoke mysite.com # Revoke certificate
```

### 4. Create a Site

```bash
python3 scripts/sites_mgmt.py --server my-server --create \
  --name mysite.com --path /www/wwwroot/mysite.com --php 82
```

### 5. Manage Databases

```bash
python3 scripts/databases.py --server my-server --list            # List databases
python3 scripts/databases.py --server my-server --create-db mydb    # Create database
python3 scripts/databases.py --server my-server --create-user myuser --password secret --db mydb  # Create user
python3 scripts/databases.py --server my-server --grant myuser mydb --privileges ALL  # Grant privileges
```

### 6. Manage Firewall

```bash
python3 scripts/firewall.py --server my-server --list           # List rules
python3 scripts/firewall.py --server my-server --add-whitelist 1.2.3.4   # Add IP to whitelist
python3 scripts/firewall.py --server my-server --add-blacklist 5.6.7.8   # Add IP to blacklist
python3 scripts/firewall.py --server my-server --remove-ip 5.6.7.8       # Remove IP
```

### 7. Switch PHP Version

```bash
python3 scripts/php.py --server my-server --site mysite.com --version 82
```

---

## CLI Reference

### Monitoring

| Command | Description |
|---------|-------------|
| `python3 scripts/monitor.py` | System resources for all servers (JSON) |
| `python3 scripts/monitor.py --server s1 --format table` | Single server, table output |
| `python3 scripts/sites.py --filter ssl-warning` | Sites with SSL expiring within 30 days |
| `python3 scripts/sites.py --filter stopped` | Sites that are stopped |
| `python3 scripts/services.py` | All services across all servers |
| `python3 scripts/services.py --service nginx --service redis` | Specific services |
| `python3 scripts/ssh.py --logs --filter failed` | Failed SSH login attempts |
| `python3 scripts/ssh.py --status` | SSH service status |
| `python3 scripts/logs.py --service nginx --lines 100` | Last 100 lines of Nginx error log |
| `python3 scripts/logs.py --service mysql --log-type slow` | MySQL slow query log |
| `python3 scripts/crontab.py --backup-only` | All scheduled backup tasks |

### Site Management

| Command | Description |
|---------|-------------|
| `python3 scripts/sites_mgmt.py --server s1 --list` | List all sites |
| `python3 scripts/sites_mgmt.py --server s1 --create --name site.com --path /www/wwwroot/site --php 82` | Create site |
| `python3 scripts/sites_mgmt.py --server s1 --delete --site-id 5` | Delete site |
| `python3 scripts/sites_mgmt.py --server s1 --add-domain --site site.com --domain api.site.com` | Add domain |
| `python3 scripts/sites_mgmt.py --server s1 --remove-domain --site site.com --domain api.site.com` | Remove domain |

### SSL Certificates

| Command | Description |
|---------|-------------|
| `python3 scripts/ssl_certs.py --server s1 --list` | List all SSL certificates |
| `python3 scripts/ssl_certs.py --server s1 --issue mysite.com` | Provision Let's Encrypt cert |
| `python3 scripts/ssl_certs.py --server s1 --renew mysite.com` | Renew certificate |
| `python3 scripts/ssl_certs.py --server s1 --revoke mysite.com` | Revoke certificate |

### Database Management

| Command | Description |
|---------|-------------|
| `python3 scripts/databases.py --server s1 --list` | List all databases |
| `python3 scripts/databases.py --server s1 --create-db mydb` | Create database |
| `python3 scripts/databases.py --server s1 --delete-db mydb` | Delete database |
| `python3 scripts/databases.py --server s1 --create-user user --password pass --db mydb` | Create DB user |
| `python3 scripts/databases.py --server s1 --delete-user user` | Delete DB user |
| `python3 scripts/databases.py --server s1 --grant user mydb --privileges ALL` | Grant privileges |

### Firewall

| Command | Description |
|---------|-------------|
| `python3 scripts/firewall.py --server s1 --list` | List firewall rules |
| `python3 scripts/firewall.py --server s1 --status` | Firewall on/off status |
| `python3 scripts/firewall.py --server s1 --add-whitelist 1.2.3.4` | Add IP to whitelist |
| `python3 scripts/firewall.py --server s1 --add-blacklist 5.6.7.8` | Add IP to blacklist |
| `python3 scripts/firewall.py --server s1 --remove-ip 5.6.7.8` | Remove IP from firewall |

### FTP Account Management

| Command | Description |
|---------|-------------|
| `python3 scripts/ftp.py --server s1 --list` | List FTP accounts |
| `python3 scripts/ftp.py --server s1 --create --user ftpuser --password secret --path /www/ftp` | Create FTP user |
| `python3 scripts/ftp.py --server s1 --delete --user-id 3` | Delete FTP user |
| `python3 scripts/ftp.py --server s1 --set-password --user-id 2 --password newpass` | Set FTP password |

### PHP Version Switching

| Command | Description |
|---------|-------------|
| `python3 scripts/php.py --server s1 --list-versions` | List installed PHP versions |
| `python3 scripts/php.py --server s1 --site mysite.com --version 82` | Switch PHP version |

### File Operations

| Command | Description |
|---------|-------------|
| `python3 scripts/files.py ls /www` | List directory contents |
| `python3 scripts/files.py cat /path/to/file` | Read file content |
| `python3 scripts/files.py cat /path/to/file -n 50` | Last 50 lines |
| `python3 scripts/files.py edit /path/to/file "content"` | Edit / overwrite file |
| `python3 scripts/files.py mkdir /www/newdir` | Create directory |
| `python3 scripts/files.py touch /www/test.txt` | Create empty file |
| `python3 scripts/files.py rm /www/old.txt` | Delete file (to recycle bin) |
| `python3 scripts/files.py chmod 755 /www/file.txt` | Change permissions |
| `python3 scripts/files.py chmod 755 /www/dir -R` | Recursive chmod |
| `python3 scripts/files.py stat /www/file.txt` | View file permissions |
| `python3 scripts/download.py --url "https://..."` | Download file to server |
| `python3 scripts/unzip.py /www/archive.zip` | Extract ZIP on server |

### Config Management

| Command | Description |
|---------|-------------|
| `python3 scripts/bt-config.py list` | List all configured servers |
| `python3 scripts/bt-config.py add -n s1 -H https://... -t TOKEN` | Add a server |
| `python3 scripts/bt-config.py remove my-server` | Remove a server |
| `python3 scripts/bt-config.py threshold --cpu 75 --memory 80` | Set alert thresholds |

---

## Alert Thresholds

Edit `~/.openclaw/bt-skills.yaml` to configure global alert thresholds:

```yaml
global:
  thresholds:
    cpu: 80      # CPU usage alert threshold (%)
    memory: 85   # Memory usage alert threshold (%)
    disk: 90     # Disk usage alert threshold (%)
```

### SSL Certificate Alerts

| Condition | Level |
|-----------|-------|
| Certificate expired | 🔴 Critical |
| ≤ 7 days until expiry | 🔴 Critical |
| ≤ 30 days until expiry | 🟡 Warning |

---

## Config File

Server configurations and API tokens are stored in:

```
~/.openclaw/bt-skills.yaml
```

This file is local to your machine — it is never committed to the repository.

---

## aaPanel

This skill is an independent open source project — it is not affiliated with, sponsored by, or endorsed by [aaPanel](https://github.com/aaPanel) or BT-Security.

- **aaPanel GitHub:** https://github.com/aaPanel
- **aaPanel Website:** https://www.aapanel.com

---

## Troubleshooting

```bash
# Verify Python environment
python3 scripts/check_env.py

# Test server connection
python3 scripts/monitor.py --server my-server

# Check configured servers
python3 scripts/bt-config.py list
```

### Common Issues

**"Config file not found"** — Run `bt-config.py add` to add your server first.

**"Connection refused"** — Ensure aaPanel API is enabled and your IP is whitelisted in **Panel Settings → API Interface**.

**"SSL verify failed"** — If using a self-signed certificate, add `--verify-ssl false` when adding the server.

---

## Contributing

Issues, feature requests, and pull requests are welcome. If you find bugs or want to add features, open an issue first to discuss.

---

## Changelog

### v1.0.7 (2026-05-01)
- **Fix:** Renamed `ssl.py` → `ssl_certs.py` to avoid conflicting with Python's standard library `ssl` module
- **Fix:** Added missing `BtClient` imports to `databases.py`, `ftp.py`, `firewall.py`, `php.py`, `sites_mgmt.py`
- **Improved:** All scripts now work correctly when deployed to remote servers without Python path issues

### v1.0.5 (2026-04-11)
- **Translated:** All Chinese text in Python scripts fully translated to English
  - All comments, docstrings, and user-facing output strings now in English
  - No Chinese characters remain in any code, scripts, or documentation files
- **Chore:** Updated ClawHub skill name to `aaPanel-Server-Skill`

### v0.2.0 (2026-04-10)
- **New:** SSL certificate management — list, provision Let's Encrypt, renew, revoke
- **New:** Site management — create/delete sites, domain binding
- **New:** Database management — create/delete databases, user management, privilege grants
- **New:** Firewall — IP whitelist, blacklist, rule management
- **New:** FTP account management — create/delete users, password changes
- **New:** PHP version switching per site
- **Improved:** 15+ new API methods in bt_client.py

### v0.1.0-beta (2026-04-10)
- Initial combined release — monitoring + file management
