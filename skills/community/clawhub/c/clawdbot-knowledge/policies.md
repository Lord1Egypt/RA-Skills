# Sandbox Policies

OpenClaw uses a policy-based security model to control what tools and actions are available to agents in sandbox containers. This document explains how policies work, how to configure them, and how to understand their output.

## Overview

Sandbox policies define:
- **Allowed tools** - Which categories of tools can be used
- **Permissions** - Specific read/write/execute rights
- **Denylists** - Explicitly forbidden commands or tools
- **Restrictions** - Network access, filesystem scope, resource limits

Policies are applied per-container and can vary by:
- Agent type (autonomous vs. session-based)
- Session configuration
- User preferences

## Policy Structure

### Policy Levels

OpenClaw supports multiple policy levels:

| Level | Security | Flexibility | Use Case |
|-------|----------|-------------|----------|
| **Strict** | High | Low | Production, sensitive data, untrusted agents |
| **Standard** | Medium | Medium | Development, general purpose (default) |
| **Permissive** | Low | High | Trusted environments, local development |
| **YOLO** | None | Maximum | Dangerous, only for trusted users |

### Tool Categories

Tools are grouped into categories:

| Category | Description | Examples |
|----------|-------------|----------|
| **exec** | Execute commands | bash, python, node, sh |
| **filesystem** | File operations | read, write, delete, list |
| **network** | Network access | http, https, tcp, udp |
| **system** | System operations | reboot, shutdown, process management |
| **docker** | Docker operations | docker run, docker ps |
| **browser** | Browser automation | selenium, puppeteer |
| **database** | Database access | mysql, postgresql, redis |

## Default Policies

### Standard Policy (Default)

```
Allowed tools:
  - exec (bash, python, node, sh)
  - filesystem (read, write, delete, list)
  - network (http, https)

Denied tools:
  - docker
  - system (reboot, shutdown)

Restrictions:
  - No internet access to localhost
  - Filesystem limited to workspace
  - CPU: 2 cores, Memory: 2GB
```

### Strict Policy

```
Allowed tools:
  - exec (python, sh)
  - filesystem (read, list)

Denied tools:
  - docker
  - system
  - network
  - exec (bash, node)
  - filesystem (write, delete)

Restrictions:
  - Read-only filesystem
  - No network access
  - CPU: 1 core, Memory: 1GB
```

### Permissive Policy

```
Allowed tools:
  - exec (bash, python, node, sh)
  - filesystem (read, write, delete, list)
  - network (http, https, tcp, udp)
  - docker

Denied tools:
  - system (reboot, shutdown)

Restrictions:
  - Full filesystem access
  - Full network access
  - CPU: 4 cores, Memory: 4GB
```

## Viewing Policies

### Explain Current Policy

```bash
# Default (current session)
openclaw sandbox explain

# Specific session
openclaw sandbox explain --session main

# Specific agent
openclaw sandbox explain --agent mybot
```

### Example Output

```
Sandbox Policy for session: main

Policy Level: Standard

Allowed Tools:
  ✓ exec: bash, python, node, sh
  ✓ filesystem: read, write, delete, list
  ✓ network: http, https

Denied Tools:
  ✗ docker
  ✗ system: reboot, shutdown

Restrictions:
  - Workspace: /home/user/.openclaw/workspaces/sessions/main
  - CPU Limit: 2 cores
  - Memory Limit: 2GB
  - Disk Limit: 10GB
  - Network: HTTP/HTTPS only, no localhost access

Denylist:
  - rm -rf /
  - dd if=/dev/...
  - mkfs
```

## Configuring Policies

### via Configuration File

Edit `~/.openclaw/openclaw.json`:

```json
{
  "sandbox": {
    "defaultPolicy": "standard",
    "policies": {
      "strict": {
        "allowed": ["exec:python,sh", "filesystem:read,list"],
        "denied": ["docker", "system", "network"],
        "restrictions": {
          "cpuCores": 1,
          "memoryMB": 1024,
          "readOnlyFilesystem": true
        }
      },
      "my-agent-policy": {
        "allowed": ["exec:bash,python,node", "filesystem:read,write", "network:http,https"],
        "denied": ["docker", "system"],
        "restrictions": {
          "cpuCores": 4,
          "memoryMB": 4096
        }
      }
    },
    "agentPolicies": {
      "mybot": "my-agent-policy"
    },
    "sessionPolicies": {
      "main": "standard"
    }
  }
}
```

### via Environment Variables

```bash
# Set policy level
export OPENCLAW_SANDBOX_POLICY=strict
export OPENCLAW_SANDBOX_POLICY=permissive
export OPENCLAW_SANDBOX_POLICY=yolo

# Set custom policy file
export OPENCLAW_SANDBOX_POLICY_FILE=/path/to/policy.json
```

### via Command Flags

```bash
# Set policy for agent
openclaw agent --policy strict --to +15555550123

# Set policy for session
openclaw session --policy permissive
```

## Custom Policies

### Creating a Custom Policy

Create a JSON policy file:

```json
{
  "name": "dev-workstation",
  "allowed": [
    "exec:bash,python,node,sh,git,npm,make,cargo",
    "filesystem:read,write,delete,list",
    "network:http,https,tcp,udp",
    "docker"
  ],
  "denied": [
    "system:reboot,shutdown"
  ],
  "restrictions": {
    "cpuCores": 8,
    "memoryMB": 8192,
    "diskGB": 20,
    "network": {
      "allowed": ["*"],
      "denied": ["localhost:*", "127.0.0.1:*"]
    },
    "filesystem": {
      "scope": "workspace",
      "allowedPaths": [
        "/home/user/projects",
        "/tmp"
      ],
      "deniedPaths": [
        "/home/user/.ssh",
        "/home/user/.gnupg"
      ]
    }
  }
}
```

### Loading Custom Policy

```bash
# Save as ~/.openclaw/policies/dev-workstation.json

# Load in config
openclaw config set sandbox.policies.dev-workstation ~/.openclaw/policies/dev-workstation.json

# Apply to agent
openclaw sandbox recreate --agent mybot
```

## Policy Examples

### Web Scraping Agent

```json
{
  "name": "web-scraper",
  "allowed": [
    "exec:python,node",
    "filesystem:read,write",
    "network:http,https",
    "browser"
  ],
  "denied": [
    "docker",
    "system"
  ],
  "restrictions": {
    "cpuCores": 2,
    "memoryMB": 2048
  }
}
```

### Testing Agent

```json
{
  "name": "tester",
  "allowed": [
    "exec:bash,python,node,npm",
    "filesystem:read,write,list",
    "network:http,https"
  ],
  "denied": [
    "docker",
    "filesystem:delete"
  ],
  "restrictions": {
    "readOnlyFilesystem": false,
    "scope": "workspace"
  }
}
```

### Database Admin Agent

```json
{
  "name": "db-admin",
  "allowed": [
    "exec:bash,python",
    "filesystem:read,write",
    "network:tcp,udp",
    "database"
  ],
  "denied": [
    "docker",
    "system",
    "filesystem:delete"
  ],
  "restrictions": {
    "network": {
      "allowed": ["db.example.com:5432", "redis.example.com:6379"]
    }
  }
}
```

## Policy Evaluation

### How Policies Are Applied

1. **Load base policy** (strict, standard, permissive)
2. **Apply overrides** (agent-specific or session-specific)
3. **Merge restrictions** (most restrictive wins)
4. **Denylist evaluation** (explicit denies always block)
5. **Final policy** applied to container

### Evaluation Order

1. **Explicit deny** → Blocked immediately
2. **Agent policy** → If set, used instead of default
3. **Session policy** → Overrides agent if more restrictive
4. **Command flags** → Temporary override for current run
5. **Environment variables** → Global override

### Conflict Resolution

When policies conflict:
- **Deny > Allow** - Explicit denies always win
- **Most restrictive** - Lower resource limits applied
- **Narrower scope** - Fewer allowed tools/path

## Security Considerations

### Principle of Least Privilege

- Start with **strict** policy, only allow what's needed
- Use **session policies** for temporary elevated access
- **Audit logs** track all policy violations

### Audit Logging

Policy violations are logged:

```bash
# View audit logs
openclaw logs --session main | grep "POLICY_VIOLATION"

# Example log entry
[POLICY_VIOLATION] Agent "mybot" attempted to run denied tool: docker
[POLICY_VIOLATION] Session "main" attempted to access denied path: /root
```

### Monitoring

Monitor for policy violations:

```bash
# Watch for violations
tail -f ~/.openclaw/logs/sandbox.log | grep POLICY_VIOLATION

# Count violations by agent
grep POLICY_VIOLATION ~/.openclaw/logs/sandbox.log | \
  awk '{print $4}' | sort | uniq -c
```

## Troubleshooting Policies

### Agent Can't Access Tool

```bash
# Check current policy
openclaw sandbox explain --agent mybot

# Check if tool is denied
grep "denied" ~/.openclaw/openclaw.json

# Adjust policy
openclaw config set sandbox.policies.standard.allowed exec:bash,python,node,sh,git
openclaw sandbox recreate --agent mybot
```

### Permission Denied Errors

```bash
# Check filesystem permissions
openclaw sandbox explain | grep filesystem

# Verify workspace path
ls -la ~/.openclaw/workspaces/agents/mybot

# Check denylist
openclaw sandbox explain | grep -A 10 Denylist
```

### Network Access Blocked

```bash
# Check network policy
openclaw sandbox explain | grep network

# Test connectivity from container
docker exec openclaw-agent-mybot curl -I https://example.com

# Allow network if needed
openclaw config set sandbox.policies.standard.allowed "exec:...,network:http,https"
```

## Best Practices

1. **Start strict** - Begin with minimal permissions, add as needed
2. **Use session policies** - Temporary elevated access instead of permanent changes
3. **Audit regularly** - Review logs for unexpected violations
4. **Document exceptions** - Note why specific tools were allowed
5. **Test thoroughly** - Verify agents work with new policies before production

---

**For architecture details, see [sandbox-architecture.md](./sandbox-architecture.md).**  
**For troubleshooting, see [troubleshooting.md](./troubleshooting.md).**
