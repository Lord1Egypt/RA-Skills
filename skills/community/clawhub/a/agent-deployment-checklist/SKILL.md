---
name: agent-deployment-checklist
description: 'Production deployment checklist for AI agent infrastructure. Covers Mac Mini and server deployment with 5-layer stack (base install, IAM config, client software, security hardening, onboarding), 5-file memory system pre-scaffolding, security baselines, starter crons, and day-1 onboarding. Use when deploying agents for clients or setting up new infrastructure. NOT for cloud/serverless deployments or containerized agents.'
license: MIT
metadata:
  openclaw:
    emoji: '🚀'
---

# Agent Deployment Checklist

Production deployment framework for AI agent infrastructure on dedicated hardware (Mac Mini, Linux servers). Every deployment follows the same 5-layer stack, every time, no shortcuts.

---

## The 5-Layer Deployment Stack

Every agent deployment is five layers applied in order. No layer is optional. Each layer has a binary pass/fail gate before moving to the next.

### Layer 1: Base OS + OpenClaw Install (Scripted)

**Goal:** Clean machine with OpenClaw runtime ready.

**Checklist:**

- [ ] Fresh OS install or verified clean state
- [ ] OS updates applied to latest stable
- [ ] Xcode Command Line Tools installed (macOS)
- [ ] Homebrew installed and updated (macOS)
- [ ] Node.js LTS installed via nvm
- [ ] Python 3.11+ installed
- [ ] Git configured with deploy key
- [ ] OpenClaw CLI installed and verified
- [ ] Claude Code installed and licensed
- [ ] Working directory created at `~/.openclaw/workspace`
- [ ] SSH key pair generated for this machine

**Script template:**

```bash
#!/bin/bash
# layer-1-base-install.sh
set -euo pipefail

echo "=== Layer 1: Base Install ==="

# macOS-specific
xcode-select --install 2>/dev/null || true
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update && brew upgrade

# Runtime
brew install nvm python@3.11 git jq
nvm install --lts
nvm use --lts

# OpenClaw workspace
mkdir -p ~/.openclaw/workspace
cd ~/.openclaw/workspace
git init

echo "Layer 1 complete. Verify: node --version && python3 --version && git --version"
```

**Gate:** `node --version` returns LTS, `python3 --version` returns 3.11+, `git status` works in workspace directory.

---

### Layer 2: IAM Config (White-Glove)

**Goal:** Identity, access, and API keys configured for this specific client/deployment.

This layer is always done manually — never scripted — because every client's access pattern is different.

**Checklist:**

- [ ] API keys provisioned (Anthropic, OpenAI if needed)
- [ ] API keys stored in environment variables (never in files)
- [ ] `.env` file created with proper permissions (`chmod 600`)
- [ ] Client-specific service accounts created
- [ ] MCP server credentials configured
- [ ] GitHub/GitLab access tokens scoped to client repos only
- [ ] Email/calendar integrations authorized (OAuth tokens)
- [ ] QuickBooks / accounting integrations connected (if applicable)
- [ ] All credentials tested with a live API call
- [ ] Credential rotation schedule documented

**Key principle:** Client pays for their own API keys and licenses. We never share keys across clients.

```bash
# Verify all credentials work
echo "Testing Anthropic API..."
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":10,"messages":[{"role":"user","content":"ping"}]}' \
  | jq '.content[0].text'

echo "Testing GitHub access..."
gh auth status
```

**Gate:** Every configured API key returns a valid response. No 401s, no 403s.

---

### Layer 3: Client-Specific Software (Varies)

**Goal:** Install and configure whatever tools this specific client needs.

This layer varies per deployment. Common patterns:

**For accounting/bookkeeping clients:**
- [ ] QuickBooks MCP server configured (read-only by default)
- [ ] Financial reporting templates deployed
- [ ] Tax calendar crons scheduled

**For marketing/content clients:**
- [ ] CMS integrations connected
- [ ] Social media API access configured
- [ ] Analytics dashboards linked

**For development team clients:**
- [ ] CI/CD pipeline access configured
- [ ] Code review automation set up
- [ ] Deployment notification channels connected

**For legal/compliance clients:**
- [ ] Document management system access
- [ ] Compliance calendar configured
- [ ] Audit trail logging enabled

**Gate:** Client-specific test suite passes. Each integration returns expected data.

---

### Layer 4: Security Hardening (Every Deployment)

**Goal:** Lock down the machine to production security standards.

**Checklist:**

- [ ] Firewall enabled and configured (only required ports open)
- [ ] SSH hardening applied:
  - [ ] Password authentication disabled
  - [ ] Root login disabled
  - [ ] Key-only authentication enforced
  - [ ] Non-standard SSH port configured
- [ ] Disk encryption enabled (FileVault on macOS, LUKS on Linux)
- [ ] Automatic security updates enabled
- [ ] Fail2ban or equivalent installed and configured
- [ ] Log rotation configured
- [ ] File integrity monitoring enabled
- [ ] `.env` and credential files have `600` permissions
- [ ] No credentials in git history (verified with `git log --all -p | grep -i "api_key\|secret\|password"`)
- [ ] SOUL, IDENTITY, USER, AGENTS files marked as sacred (never leave the environment)
- [ ] Outbound network allowlist configured (only known API endpoints)

**macOS firewall script:**

```bash
#!/bin/bash
# layer-4-firewall.sh
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setblockall on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsigned on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on
echo "Firewall configured. Verify: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate"
```

**Gate:** Security audit script returns grade A or B. No grade C or below passes.

---

### Layer 5: Onboarding — Day 1

**Goal:** Client can interact with their agent and sees value immediately.

**Checklist:**

- [ ] 5-file memory system scaffolded (see below)
- [ ] Starter crons installed and verified
- [ ] Health check running and reporting
- [ ] Client walkthrough completed (30-min live session)
- [ ] Client can ask agent a question and get a response
- [ ] First real task completed with client watching
- [ ] Emergency contact and escalation path documented
- [ ] Client has link to support channel
- [ ] Week-1 check-in scheduled

**The Day-1 demo:** Always do one real task live. Not a demo. Not a rehearsed script. Pick something from their actual workflow and do it. This is how you build trust.

**Gate:** Client has independently asked the agent a question and received a useful answer without help.

---

## Pre-Scaffolded 5-File Memory System

Every deployment starts with the same five files. They are empty templates, not boilerplate — the agent fills them in during operation.

### SOUL.md Template

```markdown
# SOUL

## Identity
You are [CLIENT_NAME]'s AI operations agent, deployed by IAM Solutions.

## Core Values
- Accuracy over speed
- Ask before assuming
- Protect client data absolutely
- Learn and improve continuously

## Boundaries
- Never share client data outside this environment
- Never execute financial transactions without explicit approval
- Never modify production systems without confirmation
- Escalate to human when uncertain

## Communication Style
[To be calibrated during onboarding based on client preference]
```

### IDENTITY.md Template

```markdown
# IDENTITY

## Deployment
- Deployed: [DATE]
- Hardware: [MACHINE_SPEC]
- Location: [PHYSICAL_OR_CLOUD_LOCATION]
- Managed by: IAM Solutions

## Capabilities
[Populated during Layer 3 based on installed integrations]

## Limitations
[Documented during onboarding based on what's explicitly out of scope]
```

### USER.md Template

```markdown
# USER

## Primary User
- Name: [CLIENT_NAME]
- Role: [CLIENT_ROLE]
- Communication preference: [EMAIL/SLACK/SMS]

## Access Pattern
[How and when the client typically interacts — populated after first week]

## Domain Knowledge
[What the client knows well vs. where they need more explanation — populated over time]
```

### AGENTS.md Template

```markdown
# AGENTS

## Active Agents
[List of running agents, their roles, and their schedules — populated during Layer 3]

## Agent Communication
[How agents coordinate, share memory, escalate — configured during deployment]
```

### MEMORY.md Template

```markdown
# MEMORY

Memory index for [CLIENT_NAME] deployment.
Created: [DATE]

## Memories
[Index populated as agent creates memories during operation]
```

---

## Starter Cron Templates

Every deployment gets these three crons minimum.

### Health Check (Every 4 Hours)

```bash
# health-check.cron
# Runs every 4 hours, reports system health
0 */4 * * * /path/to/health-check.sh >> /var/log/openclaw/health.log 2>&1
```

```bash
#!/bin/bash
# health-check.sh
GRADE="A"
ISSUES=""

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 90 ]; then GRADE="F"; ISSUES+="Disk >90%. ";
elif [ "$DISK_USAGE" -gt 80 ]; then GRADE="C"; ISSUES+="Disk >80%. "; fi

# Check memory
# Check API connectivity
# Check cron jobs running
# Check log file sizes

echo "$(date): Health Grade: $GRADE ${ISSUES:-No issues}"
```

### Memory Maintenance (Daily at 2 AM)

```bash
# memory-maintenance.cron
0 2 * * * /path/to/memory-maintenance.sh >> /var/log/openclaw/memory.log 2>&1
```

```bash
#!/bin/bash
# memory-maintenance.sh
# Compress old session logs
# Archive memories older than 30 days
# Verify MEMORY.md index matches actual files
# Report memory file count and total size

MEMORY_DIR="$HOME/.openclaw/workspace/memory"
FILE_COUNT=$(find "$MEMORY_DIR" -name "*.md" | wc -l)
TOTAL_SIZE=$(du -sh "$MEMORY_DIR" | awk '{print $1}')
echo "$(date): Memory files: $FILE_COUNT, Total size: $TOTAL_SIZE"
```

### Backup (Daily at 3 AM)

```bash
# backup.cron
0 3 * * * /path/to/backup.sh >> /var/log/openclaw/backup.log 2>&1
```

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/openclaw/$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

# Back up workspace (excluding node_modules, .git objects)
rsync -a --exclude='node_modules' --exclude='.git/objects' \
  "$HOME/.openclaw/workspace/" "$BACKUP_DIR/workspace/"

# Back up cron definitions
crontab -l > "$BACKUP_DIR/crontab.bak"

# Keep last 30 days of backups
find /backups/openclaw -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;

echo "$(date): Backup complete to $BACKUP_DIR"
```

---

## Hardware Requirements

### Minimum (Single-Agent Deployment)

| Component | Spec |
|-----------|------|
| CPU | Apple M1 or equivalent |
| RAM | 16 GB |
| Storage | 256 GB SSD |
| Network | Stable broadband, static IP preferred |
| UPS | Recommended for always-on deployments |

### Recommended (Multi-Agent Deployment)

| Component | Spec |
|-----------|------|
| CPU | Apple M2 Pro / M4 or equivalent |
| RAM | 32 GB |
| Storage | 512 GB SSD |
| Network | Business-grade with failover |
| UPS | Required |

---

## Network Configuration

```
Outbound allowlist (minimum):
- api.anthropic.com (Anthropic API)
- api.openai.com (if using OpenAI models)
- github.com (code repos)
- api.github.com (GitHub API)
- smtp.gmail.com (email, if applicable)
- quickbooks.api.intuit.com (QBO, if applicable)

Inbound:
- SSH on non-standard port (key-only)
- No other inbound ports required for typical deployments
```

---

## Post-Deployment Monitoring

### Week 1: Daily Check-ins
- Is the agent responding correctly?
- Are crons running on schedule?
- Any errors in logs?
- Client satisfaction?

### Weeks 2-4: Twice-Weekly
- Memory system growing appropriately?
- Performance stable?
- Any new integration needs?

### Month 2+: Weekly
- Health grade trend
- Backup verification
- Security update status
- Client feature requests

---

## Deployment Anti-Patterns

**Don't do these:**

- **Sharing API keys across clients.** Every client pays for their own. No exceptions.
- **Skipping Layer 4.** "It's just a test deployment" is how breaches start.
- **Copying another client's SOUL.md.** Every deployment gets a fresh identity calibrated to the client.
- **Enabling write access on day 1.** Start read-only. Earn write access through demonstrated reliability.
- **Deploying without a health check cron.** If you can't monitor it, don't deploy it.
- **Promising specific features before Layer 3.** Scope the deployment, then promise.
