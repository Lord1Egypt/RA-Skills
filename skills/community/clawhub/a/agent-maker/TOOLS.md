# TOOLS.md - Agent Maker Local Notes

## Available Tools

### 1. create-agent.sh
**Purpose:** Create a new Agent with complete configuration

**Usage:**
```bash
./tools/create-agent.sh --name=agent-name --role="Role description" [--workspace=/path] [--template=default]
```

**Example:**
```bash
./tools/create-agent.sh --name=content-writer --role="Content creation and writing specialist"
```

**What it creates:**
- `～/.openclaw/agents/[name]/` - Config files
- `～/[name]-workspace/` - Work directory
- All standard files: IDENTITY.md, SYSTEM.md, SOUL.md, etc.

---

### 2. list-agents.sh
**Purpose:** List all configured Agents

**Usage:**
```bash
./tools/list-agents.sh
```

**Output:**
- Agent name
- Config location
- Role description
- Workspace path

---

### 3. validate-agent.sh
**Purpose:** Validate Agent configuration completeness

**Usage:**
```bash
./tools/validate-agent.sh --name=agent-name
```

**Checks:**
- Required files present
- Optional files present
- Basic content structure
- Workspace definition

---

## Installation

### Install to OpenClaw
```bash
 

# Verify installation
ls -la ~/.openclaw/skills/agent-maker/
```

### Test Tools
```bash
# List current agents
~/.openclaw/skills/agent-maker/tools/list-agents.sh

# Validate existing agent
~/.openclaw/skills/agent-maker/tools/validate-agent.sh --name=frontend-dev
```

---

## Workflow

### Creating a New Agent

1. **Run create-agent.sh**
   ```bash
   ./tools/create-agent.sh --name=my-agent --role="My agent role"
   ```

2. **Review generated files**
   ```bash
   ls -la ~/.openclaw/agents/my-agent/
   ```

3. **Customize as needed**
   - Edit IDENTITY.md for personality
   - Edit SYSTEM.md for specific rules
   - Edit SOUL.md for philosophy

4. **Validate configuration**
   ```bash
   ./tools/validate-agent.sh --name=my-agent
   ```

5. **Start using the agent**
   - Agent is ready to use immediately
   - Files are in standard OpenClaw format

---

## Common Templates

### Developer Template
```bash
./tools/create-agent.sh \
  --name=backend-dev \
  --role="Backend development specialist" \
  --workspace=/home/openclaw/backend
```

### Operations Template
```bash
./tools/create-agent.sh \
  --name=devops \
  --role="DevOps and deployment specialist" \
  --workspace=/home/openclaw/devops
```

### Creative Template
```bash
./tools/create-agent.sh \
  --name=content-creator \
  --role="Content creation and social media" \
  --workspace=/home/openclaw/content
```

---

## Troubleshooting
 
### Missing Files
```bash
# Re-run validation
./tools/validate-agent.sh --name=agent-name

# Check what's missing
ls -la ～/.openclaw/agents/agent-name/
```

---

_last_updated: 2026-03-17_
