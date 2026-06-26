# Troubleshooting Guide

This guide provides step-by-step solutions for common OpenClaw sandbox issues.

## Quick Diagnostics

Start with these commands to diagnose any issue:

```bash
# 1. Check OpenClaw status
openclaw status

# 2. List containers
openclaw sandbox list

# 3. Check policy
openclaw sandbox explain

# 4. Check Docker
docker ps -a | grep openclaw
docker images | grep openclaw
```

---

## Common Issues

### Container Won't Start

**Symptoms:**
- `openclaw sandbox list` shows containers as "Exited" or doesn't show them at all
- Agent fails with "container not found" or "failed to start"
- Docker commands timeout

**Solutions:**

**1. Check Docker daemon**

```bash
# Verify Docker is running
docker info

# If Docker is not running, start it
sudo systemctl start docker
# or
sudo service docker start

# Check Docker status
sudo systemctl status docker
```

**2. Check Docker images**

```bash
# List OpenClaw images
docker images | grep openclaw

# If images are missing, pull them
docker pull openclaw/agent:latest
docker pull openclaw/browser:latest
docker pull openclaw/session:latest

# Or use OpenClaw CLI
openclaw update
```

**3. Check container logs**

```bash
# Get container name
openclaw sandbox list

# View logs
docker logs <container-name>

# View last 50 lines
docker logs --tail 50 <container-name>

# Follow logs in real-time
docker logs -f <container-name>
```

**4. Force recreation**

```bash
# Recreate specific container
openclaw sandbox recreate --session main
openclaw sandbox recreate --agent mybot

# Recreate all containers
openclaw sandbox recreate --all
```

---

### Permission Denied Errors

**Symptoms:**
- Agent gets "Permission denied" when running commands
- "Access denied" errors when accessing files
- "Operation not permitted" for system operations

**Solutions:**

**1. Check policy**

```bash
# Review current policy
openclaw sandbox explain

# Look for denied tools
openclaw sandbox explain | grep -A 10 "Denied Tools"
```

**2. Verify Docker permissions**

```bash
# Check if user is in docker group
groups | grep docker

# If not, add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker
```

**3. Check workspace permissions**

```bash
# List workspace directories
ls -la ~/.openclaw/workspaces/

# Fix permissions if needed
sudo chown -R $USER:$USER ~/.openclaw/workspaces/
chmod -R 755 ~/.openclaw/workspaces/
```

**4. Adjust policy**

```bash
# If tool is denied, check policy
openclaw sandbox explain | grep -A 5 "exec"

# Allow tool if needed (temporary)
openclaw config set sandbox.policies.standard.allowed "exec:bash,python,node,sh"

# Recreate container to apply
openclaw sandbox recreate --session main
```

---

### Config Changes Not Applied

**Symptoms:**
- Updated `~/.openclaw/openclaw.json` but changes don't take effect
- New settings not reflected in agent behavior
- Old policies still active

**Solutions:**

**1. Verify config syntax**

```bash
# Check JSON is valid
cat ~/.openclaw/openclaw.json | jq empty

# If error, fix JSON syntax
cat ~/.openclaw/openclaw.json | jq . > /tmp/openclaw.json
cp /tmp/openclaw.json ~/.openclaw/openclaw.json
```

**2. Restart containers**

```bash
# Recreate containers to pick up new config
openclaw sandbox recreate --all

# Or recreate specific session/agent
openclaw sandbox recreate --session main
```

**3. Check effective policy**

```bash
# Verify policy changed
openclaw sandbox explain

# Compare with config
cat ~/.openclaw/openclaw.json | jq .sandbox
```

**4. Restart OpenClaw (if needed)**

```bash
# Restart gateway
openclaw gateway restart

# Or stop and start
openclaw gateway stop
openclaw gateway start
```

---

### Agent Behavior Changes After Update

**Symptoms:**
- Agent acts differently after OpenClaw or Docker update
- New restrictions or permissions appear
- Performance changes

**Solutions:**

**1. Check versions**

```bash
# OpenClaw version
openclaw --version

# Docker version
docker --version

# Container image version
docker images | grep openclaw
```

**2. Review changelogs**

```bash
# Check OpenClaw docs
openclaw docs --changelog

# View Docker image history
docker history openclaw/agent:latest
```

**3. Recreate with current config**

```bash
# Force recreation with current config
openclaw sandbox recreate --all

# If issues persist, try reverting image
docker pull openclaw/agent:<previous-version>
openclaw config set agent.image openclaw/agent:<previous-version>
openclaw sandbox recreate --all
```

---

### Disk Space Issues

**Symptoms:**
- "No space left on device" errors
- Containers fail to start
- Performance degradation

**Solutions:**

**1. Check disk usage**

```bash
# Docker system usage
docker system df

# Overall disk usage
df -h

# Workspace size
du -sh ~/.openclaw/workspaces/
```

**2. Clean up Docker**

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean everything
docker system prune -a --volumes
```

**3. Clean up workspaces**

```bash
# List workspace sizes
du -sh ~/.openclaw/workspaces/* | sort -hr

# Remove old sessions (backup first!)
trash ~/.openclaw/workspaces/sessions/old-session
```

**4. Increase disk limits**

```bash
# Edit config to increase limits
cat ~/.openclaw/openclaw.json | jq '.sandbox.policies.standard.restrictions.diskGB = 20'

# Recreate containers
openclaw sandbox recreate --all
```

---

### Network Issues

**Symptoms:**
- Agent can't access internet
- External APIs fail
- "Network unreachable" errors

**Solutions:**

**1. Test connectivity**

```bash
# From host
curl -I https://example.com

# From container
docker exec openclaw-agent-mybot curl -I https://example.com

# Check DNS
docker exec openclaw-agent-mybot nslookup example.com
```

**2. Check network policy**

```bash
# Review network policy
openclaw sandbox explain | grep -A 5 "network"

# If network is denied, allow it
openclaw config set sandbox.policies.standard.allowed "exec:...,network:http,https"

# Recreate container
openclaw sandbox recreate --session main
```

**3. Check Docker network**

```bash
# List Docker networks
docker network ls

# Check OpenClaw network
docker network inspect openclaw-sandbox

# Restart Docker networking
sudo systemctl restart docker
```

**4. Check firewall/proxy**

```bash
# Check if firewall is blocking
sudo ufw status

# Check proxy settings
env | grep -i proxy

# Test bypass proxy
docker exec openclaw-agent-mybot env | grep -i proxy
```

---

### Container Exits Immediately

**Symptoms:**
- Container starts then exits within seconds
- `openclaw sandbox list` shows "Exited" status
- Agent fails to initialize

**Solutions:**

**1. Check exit code**

```bash
# Check container status
docker ps -a | grep openclaw

# View exit code
docker inspect <container-name> | grep ExitCode

# Exit codes:
# 0 = Success
# 1 = General error
# 125 = Docker daemon error
# 126 = Container command not found
# 127 = Command not found
# 137 = Killed (SIGKILL)
```

**2. Check logs**

```bash
# View container logs
docker logs <container-name>

# Look for errors
docker logs <container-name> 2>&1 | grep -i error
```

**3. Check entrypoint/command**

```bash
# Inspect container
docker inspect <container-name> | jq '.[0].Config.Cmd'
docker inspect <container-name> | jq '.[0].Config.Entrypoint'
```

**4. Verify workspace**

```bash
# Check workspace exists
ls -la ~/.openclaw/workspaces/

# Create if missing
mkdir -p ~/.openclaw/workspaces/sessions/main
mkdir -p ~/.openclaw/workspaces/agents/mybot
```

---

### Performance Issues

**Symptoms:**
- Slow agent responses
- High CPU/memory usage
- Agent hangs or times out

**Solutions:**

**1. Check resource usage**

```bash
# Docker stats
docker stats --no-stream

# Container-specific stats
docker stats <container-name>

# System resources
top
htop
```

**2. Check limits**

```bash
# Review policy limits
openclaw sandbox explain | grep -A 10 "Restrictions"

# Increase limits if needed
cat ~/.openclaw/openclaw.json | \
  jq '.sandbox.policies.standard.restrictions.cpuCores = 4' \
  | jq '.sandbox.policies.standard.restrictions.memoryMB = 4096'
```

**3. Check for resource leaks**

```bash
# Find large files in workspace
find ~/.openclaw/workspaces/ -type f -size +100M -exec ls -lh {} \;

# Clean up large files
trash ~/.openclaw/workspaces/*/large-file.log
```

**4. Optimize policy**

```bash
# Reduce allowed tools (faster startup)
openclaw config set sandbox.policies.standard.allowed "exec:python,sh,filesystem:read,write"

# Recreate container
openclaw sandbox recreate --session main
```

---

## Diagnostic Commands

### Full Diagnostic

```bash
#!/bin/bash

echo "=== OpenClaw Status ==="
openclaw status

echo -e "\n=== Container List ==="
openclaw sandbox list

echo -e "\n=== Docker Containers ==="
docker ps -a | grep openclaw

echo -e "\n=== Docker Images ==="
docker images | grep openclaw

echo -e "\n=== Disk Usage ==="
df -h
docker system df

echo -e "\n=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo -e "\n=== Policy ==="
openclaw sandbox explain
```

Save as `diagnostic.sh` and run: `bash diagnostic.sh`

---

## Getting Help

If you've tried all solutions and still have issues:

1. **Gather logs:**
   ```bash
   openclaw logs > openclaw-logs.txt
   docker logs openclaw-agent-$(openclaw sandbox list | head -1) > docker-logs.txt 2>&1
   ```

2. **Run diagnostic:**
   ```bash
   bash diagnostic.sh > diagnostic.txt
   ```

3. **Check documentation:**
   - [OpenClaw Docs](https://docs.openclaw.ai)
   - [GitHub Issues](https://github.com/openclaw/openclaw/issues)

4. **Ask for help:**
   - OpenClaw Discord: https://discord.gg/openclaw
   - GitHub Discussions

---

**For architecture details, see [sandbox-architecture.md](./sandbox-architecture.md).**  
**For policy details, see [policies.md](./policies.md).**
