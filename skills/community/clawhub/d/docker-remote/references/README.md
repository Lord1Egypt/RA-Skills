# Docker Remote Reference

## Parameters Reference

### Common Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `host` | string | Yes | - | Remote SSH host (IP or hostname) |
| `user` | string | Yes | - | SSH username |
| `path` | string | Yes | - | Directory containing docker-compose.yml |
| `port` | integer | No | 22 | SSH port |
| `key_path` | string | No | - | SSH private key path |
| `timeout` | integer | No | 60 | Timeout in seconds |

### Service-Specific Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `service` | string | No* | Container name (*required for start/stop/restart/exec) |
| `command` | string | No* | Command to execute (*required for exec/update) |
| `tail` | integer | No | Number of log lines to show (default: 100) |
| `follow` | boolean | No | Stream logs continuously (default: false) |
| `force_recreate` | boolean | No | Force recreate containers (default: false) |
| `pull` | string | No | Pull policy: never, always, missing |

## SSH Configuration

### Key-Based Authentication

To use a specific key:

```
docker_compose_up host=192.168.1.100 user=admin path=/opt/app key_path=/home/admin/.ssh/deploy_key
```

### SSH Agent Forwarding

When using SSH agent forwarding, ensure your SSH config allows it:

```
Host remote-server
    ForwardAgent yes
```

## Docker Permissions

Ensure the SSH user has access to Docker:

```bash
# Add user to docker group
ssh user@host "sudo usermod -aG docker $USER"

# Or use root user for docker commands
docker_compose_up host=192.168.1.100 user=root path=/opt/app
```

## Environment Setup

### Remote Server Requirements

1. SSH server installed and running
2. Docker installed and daemon running
3. Docker Compose installed (v2+ recommended)
4. User with appropriate permissions

### Verification Commands

```bash
# Test SSH access
ssh user@host "echo 'SSH connection successful'"

# Check Docker
ssh user@host "docker version"

# Check Docker Compose
ssh user@host "docker compose version"
```

## Security Best Practices

1. **Never expose sensitive configurations** - Protect .env files, credentials, and secrets:
   - Never log, display, or output `.env` files or any configuration containing secrets
   - When exec'ing into containers, avoid printing sensitive environment variables
2. **Use dedicated deployment users** instead of root
3. **Restrict SSH access** using firewalls or security groups
4. **Use key-based authentication** with strong passphrases
5. **Audit Docker socket access** carefully

## Troubleshooting

### Connection Issues

```bash
# Test basic connectivity
ssh -p 22 user@host "pwd"

# Check SSH daemon status
ssh user@host "sudo systemctl status sshd"

# Verify key permissions
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

### Docker Issues

```bash
# Check Docker daemon status
ssh user@host "sudo systemctl status docker"

# Restart Docker if needed
ssh user@host "sudo systemctl restart docker"

# Verify docker-compose.yml location
ssh user@host "ls -la /path/to/docker-compose.yml"
```

### Permission Issues

```bash
# Check user groups
ssh user@host "groups"

# Verify Docker socket permissions
ssh user@host "ls -la /var/run/docker.sock"
```
