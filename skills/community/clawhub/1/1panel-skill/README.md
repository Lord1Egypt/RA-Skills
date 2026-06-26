# 1Panel Skill

[![npm version](https://img.shields.io/npm/v/1panel-skill.svg)](https://www.npmjs.com/package/1panel-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive TypeScript skill for managing 1Panel servers through AI agents.

## Features

- **TypeScript** - Type-safe implementation
- **Modular Design** - 38 organized API modules
- **Promise-based** - Modern async/await API
- **Full API Coverage** - 580+ 1Panel API endpoints
- **XPack Support** - Professional version features included

## Installation

```bash
npm install 1panel-skill
```

## Quick Start

```typescript
import { OnePanelClient } from '1panel-skill';

const client = new OnePanelClient({
  host: 'localhost',
  port: 8080,
  apiKey: 'your-api-key',
  protocol: 'http'
});

// List containers
const containers = await client.container.list();

// Create website
const website = await client.website.create({
  primaryDomain: 'example.com',
  type: 'deployment'
});
```

## Configuration

### Environment Variables

```bash
ONEPANEL_HOST=localhost      # 1Panel host
ONEPANEL_PORT=8080           # 1Panel port
ONEPANEL_API_KEY=xxx         # API key (required)
ONEPANEL_PROTOCOL=http       # http or https
```

### Getting API Key

1. Login to 1Panel web interface
2. Go to Profile → API
3. Generate or copy your API key

## API Modules

### Container & Docker

```typescript
// List containers
const containers = await client.container.list();

// Create container
const container = await client.container.create({
  name: 'my-app',
  image: 'nginx:latest'
});

// Start/Stop/Restart
await client.container.start(container.id);
await client.container.stop(container.id);
await client.container.restart(container.id);

// Get logs
const logs = await client.container.getLogs(container.id, 100);

// Docker Compose
const composes = await client.compose.list();
await client.compose.create('my-app', dockerComposeContent);

// Images
const images = await client.image.list();
await client.image.pull('nginx:latest');

// Networks
const networks = await client.network.list();
await client.network.create('my-network');

// Volumes
const volumes = await client.volume.list();
await client.volume.create('my-volume');
```

### Website Management

```typescript
// List websites
const websites = await client.website.list();

// Create website
const website = await client.website.create({
  primaryDomain: 'example.com',
  type: 'deployment'
});

// Manage domains
await client.websiteDomain.create({
  websiteId: website.id,
  domain: 'www.example.com'
});

// SSL certificates
await client.websiteSSL.create({
  websiteId: website.id,
  type: 'auto'
});

// Renew SSL
await client.websiteSSL.renew(sslId);
```

### Database Management

```typescript
// MySQL
const databases = await client.databaseMysql.list();
await client.databaseMysql.create({
  name: 'mydb',
  username: 'dbuser',
  password: 'secure-password'
});

// PostgreSQL
await client.database.create('postgresql', {
  name: 'mydb',
  username: 'dbuser'
});

// Redis
const conf = await client.databaseRedis.getConf(redisId);
await client.databaseRedis.changePassword(redisId, 'new-password');
```

### File Operations

```typescript
// List files
const files = await client.file.list('/opt');

// Get file content
const content = await client.file.getContent('/opt/config.json');

// Save file
await client.file.save('/opt/config.json', fileContent);

// Compress
await client.file.compress({
  files: ['/opt/app1', '/opt/app2'],
  dst: '/opt/backups',
  name: 'backup.tar.gz',
  type: 'tar.gz'
});

// Decompress
await client.file.decompress({
  path: '/opt/backups/backup.tar.gz',
  dst: '/opt/restore',
  type: 'tar.gz'
});

// File permissions
await client.file.chmod({ path: '/opt/app', mode: '755' });
await client.file.chown({ path: '/opt/app', user: 'root', group: 'root' });
```

### System Management

```typescript
// System info
const info = await client.system.getInfo();

// Dashboard
const baseInfo = await client.dashboard.getBaseInfo();
const currentInfo = await client.dashboard.getCurrentInfo();

// Settings
const settings = await client.settings.getAll();
await client.settings.update({ key: 'value' });

// Monitor
const monitorData = await client.monitor.getData();
await client.monitor.updateStatus(true);

// Device
const deviceInfo = await client.device.getInfo();
await client.device.updateHostname('new-hostname');
```

### Security

```typescript
// Firewall
const rules = await client.firewall.listRules();
await client.firewall.createRule({
  protocol: 'tcp',
  port: '8080',
  strategy: 'accept'
});

// Fail2Ban
const status = await client.fail2ban.getStatus();
await client.fail2ban.updateStatus(true);
const bannedIPs = await client.fail2ban.getBannedIPs();

// SSH
const sshInfo = await client.ssh.getInfo();
await client.ssh.updateStatus(true);
```

### Backup & Recovery

```typescript
// Backups
const backups = await client.backup.list();
await client.backup.create({ name: 'daily-backup' });
await client.backup.restore(backupId);

// Snapshots
const snapshots = await client.snapshot.list();
await client.snapshot.create({ name: 'system-snapshot' });

// Recycle Bin
const items = await client.recycleBin.list();
await client.recycleBin.restore(itemId);
```

### Applications

```typescript
// App Store
const apps = await client.app.listStore();
const installed = await client.app.listInstalled();

// Install app
await client.app.install({
  key: 'wordpress',
  name: 'my-wordpress'
});

// Runtimes
const runtimes = await client.runtime.list();
await client.php.create({ version: '8.2' });
await client.node.create({ version: '18' });
```

### XPack Features (Professional)

```typescript
// OpenResty
const status = await client.openresty.getStatus();
await client.openresty.reload();

// GPU
const gpuInfo = await client.gpu.getInfo();

// AI Agent
const agents = await client.ai.list();
await client.ai.create({ name: 'my-agent' });

// MCP Server
const servers = await client.ai.listMCPServers();

// Ollama
const models = await client.ollama.listModels();
await client.ollama.pullModel('llama2');
```

## Available Modules

### Core Modules (38 total)

| Module | Description |
|--------|-------------|
| `client.container` | Docker container management |
| `client.image` | Docker image management |
| `client.network` | Docker network management |
| `client.volume` | Docker volume management |
| `client.compose` | Docker Compose management |
| `client.app` | App Store management |
| `client.runtime` | Runtime environments |
| `client.php` | PHP management |
| `client.node` | Node.js management |
| `client.website` | Website management |
| `client.websiteDomain` | Domain management |
| `client.websiteSSL` | SSL certificate management |
| `client.database` | Generic database operations |
| `client.databaseMysql` | MySQL specific |
| `client.databaseRedis` | Redis specific |
| `client.file` | File system operations |
| `client.recycleBin` | Recycle bin |
| `client.system` | System information |
| `client.systemSetting` | System settings |
| `client.dashboard` | Dashboard data |
| `client.settings` | Global settings |
| `client.logs` | System logs |
| `client.monitor` | System monitor |
| `client.device` | Device management |
| `client.backup` | Backup operations |
| `client.backupAccount` | Backup account management |
| `client.snapshot` | System snapshots |
| `client.firewall` | Firewall management |
| `client.fail2ban` | Fail2Ban management |
| `client.ssh` | SSH management |
| `client.cronjob` | Cronjob management |
| `client.process` | Process management |
| `client.terminal` | Terminal sessions |
| `client.task` | Task management |
| `client.disk` | Disk management |
| `client.ftp` | FTP management |
| `client.clam` | ClamAV antivirus |
| `client.host` | Remote host management |
| `client.sshKey` | SSH key management |
| `client.openresty` | OpenResty management |
| `client.gpu` | GPU management |
| `client.ai` | AI Agent management |
| `client.ollama` | Ollama management |

## Error Handling

```typescript
try {
  await client.container.create(config);
} catch (error) {
  if (error.message.includes('UNAUTHORIZED')) {
    console.error('Invalid API key');
  } else {
    console.error('API Error:', error.message);
  }
}
```

## TypeScript Support

All modules include full TypeScript type definitions:

```typescript
import { OnePanelClient, OnePanelConfig } from '1panel-skill';

const config: OnePanelConfig = {
  host: 'localhost',
  port: 8080,
  apiKey: 'your-api-key',
  protocol: 'http'
};

const client = new OnePanelClient(config);
```

## API Coverage

| Category | Modules | Endpoints |
|----------|---------|-----------|
| Container & Docker | 5 | ~80 |
| Applications | 4 | ~60 |
| Website | 3 | ~50 |
| Database | 3 | ~40 |
| File Management | 2 | ~30 |
| System | 7 | ~100 |
| Backup & Recovery | 3 | ~40 |
| Security | 3 | ~50 |
| Tools | 6 | ~80 |
| Host Management | 2 | ~30 |
| XPack Features | 4 | ~40 |
| **Total** | **38** | **~580+** |

## License

MIT

## Links

- [npm](https://www.npmjs.com/package/1panel-skill)
- [GitHub](https://github.com/EaveLuo/1panel-skill)
- [1Panel](https://1panel.cn/)
