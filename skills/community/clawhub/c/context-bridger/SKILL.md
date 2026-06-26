# Context Bridge

**The unified continuity system for OpenClaw.**

Ensures context persists across sessions, models, and time. Prevents "starting from zero" on every `/new`.

**Version:** 1.0  
**Created:** 2026-04-03

---

## Quick Start

### Installation

```bash
# 1. Install the skill
openclaw skills install https://github.com/loudmouthedmedia/context-bridge

# 2. Run setup to create registry files
cd ~/.openclaw/workspace/skills/context-bridge/scripts
./setup.sh

# 3. Update AGENTS.md (see below)
```

### Setup Script

The `setup.sh` script **auto-discovers and populates** all existing skills, crons, and agents:

1. Scans `~/.openclaw/workspace/skills/` for local skills
2. Scans `~/.openclaw/skills/` for system skills  
3. Checks `openclaw cron list` for active cron jobs
4. Checks `openclaw agents list` and `~/.openclaw/agents/` for agents
5. Creates and populates all registry files with actual data

---

## What It Does

**Before Context Bridge:**
```
You: /new
Model A: "Hello! How can I help?" [blank slate]
You: [re-explain everything]

You: /new  
Model B: "Hello! How can I help?" [blank slate again]
You: [re-explain everything again]
```

**After Context Bridge:**
```
You: /new
Model C: "📧 [email-skill] available, 📈 [analytics-skill] ready. 
          Working on [Your Project]. Previous model 
          (GPT-X) scheduled a meeting 30 min ago. 
          Ready to continue."
```

---

## Components

### 1. Registries (The "What Exists")

| Registry | File | Tracks |
|----------|------|--------|
| **Skills** | `~/.openclaw/skills-registry.json` | All installed skills |
| **Crons** | `~/.openclaw/cron-registry.json` | Active scheduled jobs |
| **Agents** | `~/.openclaw/agents/*/agent.md` | Agent configurations |
| **Discovery** | `~/.openclaw/skills-discovery.json` | Skill capabilities |

### 2. Handoff Memory (The "What Happened")

**File:** `~/.openclaw/model-agnostic-memory/model-handoff.md`

- Session-to-session context
- What previous models did
- Active projects
- Recent actions

### 3. SOPs (The "Rules")

**Documentation:** `~/.openclaw/workspace/notes/openclaw-reliability-issues.md` (Issue #9)

- File responsibility assignments
- Before-adding-content checklist
- Cross-reference comments

---

## Session Startup Protocol

**Required by AGENTS.md:**

```
1. Read SOUL.md
2. Read USER.md  
3. Read memory files
4. READ CONTEXT BRIDGE FILES:
   - ~/.openclaw/skills-discovery.json
   - ~/.openclaw/model-agnostic-memory/model-handoff.md
   - ~/.openclaw/cron-registry.json
   - ~/.openclaw/skills-registry.json
5. ACKNOWLEDGE context in first response
```

---

## File Responsibilities (SOP)

| File | Responsibility | Must NOT |
|------|----------------|----------|
| AGENTS.md | Session startup rules | Periodic checks |
| HEARTBEAT.md | Periodic health checks | Session setup |
| SOUL.md | Personality/vibe | Technical instructions |
| Context Bridge | Registries & discovery | Implementation |

---

## Usage

### Automatic
On `/new` or model switch: Registries auto-load via AGENTS.md

### Manual Fallback
If needed, say: `load context`

### Update Workflow
When adding skills/crons/agents:
1. Update appropriate registry
2. Update discovery (if new capabilities)
3. Update handoff (log the change)
4. Git commit

---

## Why "Context Bridge"?

- **Context** = What the model knows
- **Bridge** = Connection between isolated sessions/Models

Builds bridges across the memory gap.