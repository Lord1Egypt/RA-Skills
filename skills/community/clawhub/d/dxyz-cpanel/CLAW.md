# dxyz-cpanel

Manage cPanel hosting accounts via API for version 134.0.11 and compatible versions.

## Installation

```bash
picoclaw skill install dxyz-cpanel
```

## Features

- **Account Management**: Create, suspend, unsuspend, delete accounts
- **DNS Management**: List, add, delete DNS records (A, AAAA, CNAME, MX, TXT)
- **Email Management**: Create, delete, password change, forwarders
- **Database Management**: MySQL & PostgreSQL databases and users
- **SSL Certificates**: List, install, manage certificates
- **File Operations**: List, upload, copy files
- **Backup Operations**: Create, restore, download backups

## API Support

| API Type | Purpose |
|----------|---------|
| WHM API 1 | Server administration |
| UAPI | cPanel user operations |
| cPanel API 2 | Legacy (deprecated) |

## Configuration

Set environment variables:
```bash
export CPANEL_HOST="https://your-server.com:2087"
export CPANEL_TOKEN="your-api-token"
```

## Version

- Primary: cPanel 134.0.11
- Compatible: All 134.x versions
- Backward: 130.x - 133.x