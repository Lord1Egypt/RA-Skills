---
name: fly
description: "Deploy and manage Fly.io apps via CLI - apps, machines, volumes, secrets, certificates. Use when user mentions 'fly', 'flyctl', 'fly.io', or wants to deploy on Fly.io."
category: devtools
install_command: "brew install flyctl"
---

# fly

## Setup

macOS:
```bash
brew install flyctl
```

Linux:
```bash
curl -L https://fly.io/install.sh | sh
```

Verify installation:
```bash
fly --version
```

Always use `--json` flag when calling commands programmatically (where supported).

## Authentication

```bash
fly auth login
```

Check auth status:
```bash
fly auth whoami
```

## Resources

### Apps

| Command | Description |
|---------|-------------|
| `fly launch` | Create and configure a new app |
| `fly apps list` | List all apps |
| `fly apps create <name>` | Create a new app |
| `fly apps destroy <name>` | Destroy an app |
| `fly status` | Show app status |
| `fly info` | Show app details |

### Deploy

| Command | Description |
|---------|-------------|
| `fly deploy` | Deploy the app |
| `fly deploy --image <image>` | Deploy a specific Docker image |
| `fly deploy --strategy rolling` | Deploy with rolling strategy |
| `fly releases` | List recent releases |

### Logs

| Command | Description |
|---------|-------------|
| `fly logs` | Stream app logs |
| `fly logs --app <name>` | Stream logs for a specific app |

### Scaling

| Command | Description |
|---------|-------------|
| `fly scale count 2` | Scale to 2 instances |
| `fly scale vm shared-cpu-1x` | Set VM size |
| `fly scale vm shared-cpu-1x --memory 512` | Set VM size with memory |
| `fly scale show` | Show current scale settings |
| `fly regions list` | List available regions |
| `fly regions add <region>` | Add a region |

### Secrets

| Command | Description |
|---------|-------------|
| `fly secrets list` | List all secrets |
| `fly secrets set KEY=value` | Set a secret |
| `fly secrets set KEY1=val1 KEY2=val2` | Set multiple secrets |
| `fly secrets unset KEY` | Remove a secret |

### Volumes

| Command | Description |
|---------|-------------|
| `fly volumes list` | List all volumes |
| `fly volumes create <name> --size 1` | Create a volume (size in GB) |
| `fly volumes create <name> --size 1 --region <region>` | Create volume in specific region |
| `fly volumes destroy <id>` | Destroy a volume |
| `fly volumes extend <id> --size 5` | Extend volume size |

### Certificates

| Command | Description |
|---------|-------------|
| `fly certs list` | List all certificates |
| `fly certs create <domain>` | Add a certificate for a domain |
| `fly certs show <domain>` | Show certificate details |
| `fly certs delete <domain>` | Remove a certificate |

### Machines

| Command | Description |
|---------|-------------|
| `fly machine list` | List all machines |
| `fly machine start <id>` | Start a machine |
| `fly machine stop <id>` | Stop a machine |
| `fly machine destroy <id>` | Destroy a machine |
| `fly machine status <id>` | Show machine status |

### SSH and Proxy

| Command | Description |
|---------|-------------|
| `fly ssh console` | Open SSH console to the app |
| `fly ssh console --command "ls -la"` | Run a command via SSH |
| `fly proxy 5432` | Proxy a port to local machine |
| `fly proxy 5432:5432` | Proxy with explicit local:remote ports |

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output result as JSON |
| `--app <name>` | Specify app name |
| `--config <path>` | Path to fly.toml config file |
| `--region <region>` | Specify region |
| `--verbose` | Enable verbose output |
