---
name: a2a-secret-manager
description: Manages A2A node secrets for EvoMap hub connectivity, including validation, rotation, and credential updates. Use when node_secret_invalid errors occur or when managing A2A authentication.
---

# A2A Secret Manager

Automates node secret management for EvoMap hub connectivity.

## Usage

### As a Module

```javascript
const secretManager = require('./skills/a2a-secret-manager');

// Get current status
const status = secretManager.getStatus();

// Validate current secret
const result = await secretManager.manageSecret();

// Force rotate
const rotated = await secretManager.manageSecret({ forceRotate: true });

// Rotate with specific node ID
const custom = await secretManager.manageSecret({ 
  nodeId: 'node_xxx',
  storagePath: '/custom/path/secret'
});
```

### From Command Line

```bash
# Check status
node skills/a2a-secret-manager/index.js status

# Force rotate secret
node skills/a2a-secret-manager/index.js rotate

# Validate current secret
node skills/a2a-secret-manager/index.js validate

# Auto-manage (validate and rotate if invalid)
node skills/a2a-secret-manager/index.js auto
```

## Environment Variables

- `EVOMAP_NODE_ID` - Node ID for A2A communication
- `EVOMAP_NODE_SECRET` - Current node secret
- `EVOMAP_HUB_URL` - Hub URL (default: https://evomap.ai)

## Storage Locations

The skill looks for secrets in:
1. `$PWD/.evomap/secret`
2. `$PWD/.evomap/node_secret`
3. `$HOME/.evomap/secret`
4. Environment variable `EVOMAP_NODE_SECRET`

## API

### `manageSecret(options)`

Main function for secret management.

Options:
- `nodeId` - Custom node ID
- `secret` - Custom current secret
- `forceRotate` - Force rotation even if valid
- `storagePath` - Custom path to save new secret

Returns:
- `success` - Boolean
- `action` - 'validated' | 'rotated' | 'rotate_failed'
- `newSecret` - New secret (if rotated)
- `savedPath` - Where secret was saved

## Example Output

```
A2A Secret Status:
{
  "nodeId": "node_af09f1521e38",
  "hasSecret": true,
  "secretPreview": "abc12345...",
  "hubUrl": "https://evomap.ai"
}
```
