---
name: 1panel
version: 1.0.0
description: Comprehensive 1Panel server management skill for AI agents. Manage Linux servers, Docker containers, databases, websites, SSL certificates, and more through 580+ API endpoints.
homepage: https://github.com/EaveLuo/1panel-skill
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":["node"],"env":["ONEPANEL_API_KEY"]},"primaryEnv":"ONEPANEL_API_KEY"}}
---

# 1Panel Skill

Manage 1Panel servers through AI agents. Full access to 580+ API endpoints covering containers, databases, websites, SSL, file management, system monitoring, and more.

## Prerequisites

- 1Panel server (https://1panel.cn/)
- API key from 1Panel Dashboard → Profile → API

## Configuration

Set environment variables:

```bash
export ONEPANEL_API_KEY="your-api-key"
export ONEPANEL_HOST="localhost"      # optional, default: localhost
export ONEPANEL_PORT="8080"           # optional, default: 8080
export ONEPANEL_PROTOCOL="http"       # optional, default: http
```

## Quick Start

```bash
# List containers
node {baseDir}/scripts/1panel.mjs containers

# Get container info
node {baseDir}/scripts/1panel.mjs container <id>

# Start/Stop/Restart container
node {baseDir}/scripts/1panel.mjs start <id>
node {baseDir}/scripts/1panel.mjs stop <id>
node {baseDir}/scripts/1panel.mjs restart <id>

# List images
node {baseDir}/scripts/1panel.mjs images

# List websites
node {baseDir}/scripts/1panel.mjs websites

# List databases
node {baseDir}/scripts/1panel.mjs databases

# List files
node {baseDir}/scripts/1panel.mjs files /opt

# Get system info
node {baseDir}/scripts/1panel.mjs system

# Get dashboard info
node {baseDir}/scripts/1panel.mjs dashboard
```

## Available Commands

| Command | Description |
|---------|-------------|
| `containers` | List all Docker containers |
| `container <id>` | Get container details |
| `start <id>` | Start a container |
| `stop <id>` | Stop a container |
| `restart <id>` | Restart a container |
| `images` | List Docker images |
| `websites` | List websites |
| `databases` | List databases |
| `files <path>` | List files in directory |
| `system` | Get system information |
| `dashboard` | Get dashboard information |

## API Coverage

### Container & Docker (24 tools)
- Container lifecycle (create, start, stop, restart, pause, kill, remove)
- Image management (pull, push, build, tag, save, load)
- Network & Volume management
- Docker Compose operations

### Website Management (24 tools)
- Website creation and configuration
- Domain management
- SSL certificate (Let's Encrypt, manual upload)
- HTTPS configuration
- Nginx configuration
- OpenResty (XPack)

### Database (24 tools)
- MySQL (create, delete, bind user, change password)
- PostgreSQL
- Redis (config, password, status)

### File Operations (19 tools)
- List, upload, download
- Compress/Decompress (zip, tar, tar.gz)
- Move, rename, delete
- Permissions (chmod, chown)

### System & Security (20+ tools)
- System settings
- Firewall rules
- Fail2ban
- SSH management
- ClamAV antivirus
- FTP server

### Monitoring (8 tools)
- Dashboard
- System monitor
- Device info
- Disk management

### Backup & Recovery (13 tools)
- Backup operations
- Backup accounts (local, SFTP, OSS, S3)
- System snapshots
- Recycle bin

### XPack Features (47 tools)
- AI Agent management
- MCP Server
- Ollama models
- GPU monitoring
- OpenResty
- Node.js runtime

## Output Format

All commands output JSON:

```json
{
  "data": [...],
  "success": true
}
```

Or on error:

```json
{
  "error": true,
  "message": "Error description"
}
```

## Advanced Usage

For full API access, use as a library:

```typescript
import { OnePanelClient } from '1panel-skill';

const client = new OnePanelClient({
  host: 'localhost',
  port: 8080,
  apiKey: 'your-api-key',
  protocol: 'http'
});

// Full API access
const containers = await client.containers.list();
const websites = await client.websites.list();
```

## Links

- [GitHub](https://github.com/EaveLuo/1panel-skill)
- [npm](https://www.npmjs.com/package/1panel-skill)
- [1Panel](https://1panel.cn/)
