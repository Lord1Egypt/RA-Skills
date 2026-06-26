---
name: doppler
description: "Manage secrets and environment variables via Doppler CLI - secrets, projects, configs, environments. Use when user mentions 'doppler', 'secrets management', 'env variables', or wants to manage secrets with Doppler."
category: devtools
install_command: "brew install dopplerhq/cli/doppler"
---

# doppler

## Setup

macOS:
```bash
brew install dopplerhq/cli/doppler
```

Or install from https://docs.doppler.com/docs/install-cli for other platforms.

Verify installation:
```bash
doppler --version
```

Always use `--json` flag when calling commands programmatically.

## Authentication

```bash
doppler login
```

## Resources

### Setup

| Command | Description |
|---------|-------------|
| `doppler setup` | Configure Doppler for current directory |
| `doppler setup --project <name> --config <config>` | Configure with specific project and config |

### Secrets

| Command | Description |
|---------|-------------|
| `doppler secrets` | List all secrets in current config |
| `doppler secrets get KEY` | Get a specific secret value |
| `doppler secrets get KEY --plain` | Get plain text value (no formatting) |
| `doppler secrets set KEY=value` | Set a secret |
| `doppler secrets set KEY1=val1 KEY2=val2` | Set multiple secrets |
| `doppler secrets delete KEY` | Delete a secret |
| `doppler secrets download --no-file --format env` | Download secrets as .env format |
| `doppler secrets download --no-file --format json` | Download secrets as JSON |

### Run

| Command | Description |
|---------|-------------|
| `doppler run -- <command>` | Run a command with secrets injected as env vars |
| `doppler run -- npm start` | Run npm start with secrets injected |
| `doppler run --command "echo \$KEY"` | Run shell command with secrets |

### Projects

| Command | Description |
|---------|-------------|
| `doppler projects` | List all projects |
| `doppler projects create <name>` | Create a new project |
| `doppler projects delete <name>` | Delete a project |
| `doppler projects get <name>` | Get project details |

### Configs

| Command | Description |
|---------|-------------|
| `doppler configs` | List all configs in current project |
| `doppler configs create --name <name> --environment <env>` | Create a new config |
| `doppler configs delete --config <name> --yes` | Delete a config |
| `doppler configs clone --config <source> --name <target>` | Clone a config |

### Environments

| Command | Description |
|---------|-------------|
| `doppler environments` | List all environments |
| `doppler environments create --name <name> --slug <slug>` | Create an environment |
| `doppler environments delete <slug>` | Delete an environment |

### Activity

| Command | Description |
|---------|-------------|
| `doppler activity` | View recent activity log |
| `doppler activity --number 20` | View last 20 activity entries |

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output result as JSON |
| `--project <name>` | Specify project |
| `--config <name>` | Specify config |
| `--token <token>` | Use service token for auth |
| `--no-color` | Disable colored output |
