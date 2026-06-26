---
name: neon
description: "Manage Neon Serverless Postgres via CLI - projects, branches, databases, roles, endpoints, connection strings. Use when user mentions 'neon', 'neonctl', 'serverless postgres', or wants to manage Neon databases."
category: devtools
install_command: "npm i -g neonctl"
---

# neon

## Setup

```bash
npm i -g neonctl
```

Verify installation:
```bash
neonctl --version
```

Always use `--output json` flag when calling commands programmatically.

## Authentication

```bash
neonctl auth
```

## Resources

### Projects

| Command | Description |
|---------|-------------|
| `neonctl projects list` | List all projects |
| `neonctl projects create --name <name>` | Create a new project |
| `neonctl projects delete <id>` | Delete a project |
| `neonctl projects get <id>` | Get project details |

### Branches

| Command | Description |
|---------|-------------|
| `neonctl branches list --project-id <id>` | List all branches |
| `neonctl branches create --project-id <id> --name <name>` | Create a branch |
| `neonctl branches delete <branch-id> --project-id <id>` | Delete a branch |
| `neonctl branches get <branch-id> --project-id <id>` | Get branch details |
| `neonctl branches reset <branch-id> --project-id <id> --parent` | Reset branch to parent |

### Databases

| Command | Description |
|---------|-------------|
| `neonctl databases list --project-id <id> --branch-id <id>` | List databases |
| `neonctl databases create --project-id <id> --branch-id <id> --name <name>` | Create a database |
| `neonctl databases delete <name> --project-id <id> --branch-id <id>` | Delete a database |

### Roles

| Command | Description |
|---------|-------------|
| `neonctl roles list --project-id <id>` | List all roles |
| `neonctl roles create --project-id <id> --branch-id <id> --name <name>` | Create a role |
| `neonctl roles delete <name> --project-id <id> --branch-id <id>` | Delete a role |

### Endpoints

| Command | Description |
|---------|-------------|
| `neonctl endpoints list --project-id <id>` | List all endpoints |

### Connection Strings

| Command | Description |
|---------|-------------|
| `neonctl connection-string --project-id <id>` | Get default connection string |
| `neonctl connection-string --project-id <id> --branch-id <id>` | Get connection string for a branch |
| `neonctl connection-string --project-id <id> --branch-id <id> --database-name <db> --role-name <role>` | Get connection string with specific db and role |

### Context

| Command | Description |
|---------|-------------|
| `neonctl set-context --project-id <id>` | Set project context to avoid passing --project-id |

## Global Flags

| Flag | Description |
|------|-------------|
| `--output json` | Output result as JSON |
| `--project-id <id>` | Specify project ID |
| `--api-key <key>` | Use API key for authentication |
| `--no-color` | Disable colored output |
