---
name: docker-remote
description: Remotely manage Docker Compose instances via SSH. Execute docker compose commands, view logs, update images, and exec into containers on remote servers. Use when deploying, monitoring, or debugging containerized applications.
license: MIT
compatibility: Requires SSH access and Docker Compose installed on the remote server.
metadata: {"clawdbot":{"emoji":"🐬"}}
---

# Docker Remote Skill

Remotely manage Docker Compose instances through SSH connections.

## Overview

This skill provides a complete set of actions for Docker Compose lifecycle management on remote servers. All operations are performed via SSH, requiring only standard SSH and Docker tools on both client and server.

## Quick Start

```bash
# Start services
docker_compose_up host=192.168.1.100 user=root path=/opt/myapp

# Check status
docker_compose_ps host=192.168.1.100 user=root path=/opt/myapp

# View logs
docker_compose_logs host=192.168.1.100 user=root path=/opt/myapp tail=50

# Update and restart
docker_compose_update host=192.168.1.100 user=root path=/opt/myapp pull=always
```

## Actions

### docker_compose_up

Start Docker Compose services in detached mode.

**Parameters:**
- `host` (required): Remote SSH host (IP or hostname)
- `user` (required): SSH username
- `path` (required): Directory containing docker-compose.yml
- `port` (optional, default: 22): SSH port
- `key_path` (optional): SSH private key path
- `timeout` (optional, default: 60): Operation timeout in seconds

**Example:**
```
docker_compose_up host=192.168.1.100 user=admin path=/opt/app port=2222
```

### docker_compose_down

Stop and remove containers, networks, and volumes defined in docker-compose.yml.

**Parameters:** Same as `up`

**Example:**
```
docker_compose_down host=192.168.1.100 user=admin path=/opt/app
```

### docker_compose_start

Start specific stopped services.

**Parameters:**
- All `up` parameters
- `service` (optional): Service name to start (starts all if not specified)

**Example:**
```
docker_compose_start host=192.168.1.100 user=admin path=/opt/app service=web
```

### docker_compose_stop

Stop running services without removing them.

**Parameters:**
- All `up` parameters
- `service` (optional): Service name to stop (stops all if not specified)

**Example:**
```
docker_compose_stop host=192.168.1.100 user=admin path=/opt/app service=worker
```

### docker_compose_restart

Restart services.

**Parameters:**
- All `up` parameters
- `service` (optional): Service name to restart

**Example:**
```
docker_compose_restart host=192.168.1.100 user=admin path=/opt/app service=api
```

### docker_compose_ps

List all containers with their status.

**Parameters:** Same as `up`

**Example:**
```
docker_compose_ps host=192.168.1.100 user=admin path=/opt/app
```

### docker_compose_logs

Fetch and display logs from services.

**Parameters:**
- All `up` parameters
- `service` (optional): Filter logs to specific service
- `tail` (optional, default: 100): Number of lines to show
- `follow` (optional, default: false): Stream logs continuously

**Example:**
```
docker_compose_logs host=192.168.1.100 user=admin path=/opt/app tail=50 follow=true
```

### docker_compose_update

Pull the latest images and restart services.

**Parameters:**
- All `up` parameters
- `force_recreate` (optional, default: false): Force recreate containers
- `pull` (optional): Image pull policy (never, always, missing)
- `command` (optional): Custom command to execute instead of default "pull && up"

**Example:**
```
# Default behavior
docker_compose_update host=192.168.1.100 user=admin path=/opt/app pull=always

# Custom command
docker_compose_update host=192.168.1.100 user=admin path=/opt/app command="sh ./upgrade.sh"
```

### docker_compose_exec

Execute a command in a running container.

**Parameters:**
- All `up` parameters
- `service` (required): Container name to execute in
- `command` (required): Command to execute
- `timeout` (optional, default: 60): Command execution timeout

**Example:**
```
docker_compose_exec host=192.168.1.100 user=admin path=/opt/app service=web command="ls -la /app"
```

## Implementation Notes

- SSH connections use key-based authentication by default
- Always change to the correct directory before running docker compose commands
- Use `-d` flag for detached mode when starting services
- Handle SSH connection timeouts and authentication failures gracefully
- Return structured output with success/failure status and relevant logs
- Include error context when operations fail

## Error Handling

Common errors and handling:

1. **SSH connection refused**: Verify host, port, and network access
2. **Authentication failed**: Check SSH key path and permissions
3. **Path not found**: Ensure docker-compose.yml exists at specified path
4. **Docker not running**: Verify Docker daemon is accessible on remote host
5. **Permission denied**: Check user has access to Docker socket

## Deployment Configuration

This skill supports a `deploy-apps.json` configuration file that maps your remote hosts and applications. The Agent automatically reads this configuration to resolve host aliases, app names, SSH credentials, and file paths.

### Configuration File

The structure of the `deploy-apps.json` file should be as follows:

```json
{
    "hosts": {
        "<host-alias>": {
            "host": "remote.server.com",
            "description": "Server description",
            "base-dir": "/path/to/docker",
            "user": "ssh-user",
            "apps": {
                "<app-name>": {
                    "description": "Application description",
                    "update-command": "Custom command to execute update"
                }
            }
        }
    }
}
```

### How It Works

When you reference a host alias or app name, the Agent:

1. Reads `deploy-apps.json` to find the matching configuration
2. Resolves `host` to the actual SSH hostname/IP
3. Constructs `path` from `<base-dir>/<app-name>`
4. Uses the configured `user` for SSH authentication

### Configuration Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hosts.<alias>.host` | string | Yes | Remote SSH hostname or IP |
| `hosts.<alias>.base-dir` | string | Yes | Base directory containing app folders |
| `hosts.<alias>.user` | string | Yes | SSH username |
| `hosts.<alias>.description` | string | No | Human-readable description |
| `hosts.<alias>.apps.<name>.description` | string | Yes* | App description |
| `hosts.<alias>.apps.<name>.update-command` | string | Yes* | Custom command to execute update |

### Path Resolution Example

With:
- `base-dir`: `/data/docker`
- `app-name`: `mysql`

The resolved path would be: `/data/docker/mysql`

## See Also

- [Usage Reference](references/README.md) - Detailed parameter documentation
- [Examples](examples/docker-remote.json) - Command examples
- [Deployment Configuration](examples/deploy-apps.json) - Example configuration file
