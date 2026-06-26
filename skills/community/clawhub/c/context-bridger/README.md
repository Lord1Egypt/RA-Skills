# Context Bridge

**The unified continuity system for OpenClaw.**

Ensures context persists across sessions, models, and time. Prevents "starting from zero" on every `/new`.

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/version-1.0-green)](https://github.com/loudmouthedmedia/context-bridge)

## Problem It Solves

**Before Context Bridge:**
```
You: /new
Model A: "Hello! How can I help?" [blank slate - no memory of previous work]
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

## What It Does

Context Bridge provides four core components:

### 1. Registries (The "What Exists")

Track all system resources in JSON files:

| Registry | File | Tracks |
|----------|------|--------|
| **Skills** | `~/.openclaw/skills-registry.json` | All installed skills |
| **Crons** | `~/.openclaw/cron-registry.json` | Active scheduled jobs |
| **Agents** | `~/.openclaw/agents/*/agent.md` | Agent configurations |

### 2. Discovery (The "How To Use")

**File:** `~/.openclaw/skills-discovery.json`

- Skill capabilities with examples
- Commands and triggers
- Last used by which model

### 3. Handoff Memory (The "What Happened")

**File:** `~/.openclaw/model-agnostic-memory/model-handoff.md`

- Session-to-session context
- What previous models did
- Active projects
- Recent actions

### 4. SOPs (The "Rules")

**Documentation:** Included in reliability issues

- File responsibility assignments
- Before-adding-content checklist
- Cross-reference comments

## Installation

### Method 1: Direct Install (Recommended)

```bash
openclaw skills install https://github.com/openclaw/context-bridge
```

### Method 2: Manual Setup

1. Clone this repository:
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw/context-bridge.git
```

2. Update AGENTS.md to load Context Bridge on session start:
```markdown
## Session Startup

Before doing anything else:

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

3. Create initial registries:
```bash
mkdir -p ~/.openclaw/model-agnostic-memory
mkdir -p ~/.openclaw/agents/defaults
```

## File Structure

```
~/.openclaw/
├── skills-registry.json          # Track all skills
├── cron-registry.json            # Track all crons
├── skills-discovery.json         # Skill capabilities
├── model-agnostic-memory/
│   └── model-handoff.md          # Cross-model context
├── agents/
│   └── defaults/
│       └── session-start-hook.md # Session startup rules
└── workspace/
    └── skills/
        └── context-bridge/
            ├── SKILL.md          # This skill
            └── README.md         # This file
```

## Usage

### Automatic
On `/new` or model switch: Registries auto-load via AGENTS.md

### Manual Fallback
If context missing, say: `load context`

### Update Workflow
When adding skills/crons/agents:
1. Update appropriate registry
2. Update discovery (if new capabilities)
3. Update handoff (log the change)
4. Git commit

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

## Why "Context Bridge"?

- **Context** = What the model knows
- **Bridge** = Connection between isolated sessions/models

Builds bridges across the memory gap.

## Compatibility

- OpenClaw >= 2026.4.x
- Works with any model provider (Ollama, OpenAI, Anthropic, etc.)
- Cross-platform (Linux, macOS, Windows)

## License

MIT - See LICENSE file

## Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## Related Skills

- [marketing-mode](https://clawhub.ai/thesethrose/marketing-mode) - Marketing strategy
- [systems-engineer](https://openclaw.ai/skills/systems-engineer) - System health
- [self-improving](https://openclaw.ai/skills/self-improving) - Learning & memory

## Support

- GitHub Issues: https://github.com/openclaw/context-bridge/issues
- OpenClaw Discord: https://discord.com/invite/clawd
- Documentation: https://docs.openclaw.ai

---

**Version:** 1.0  
**Created:** 2026-04-03  
**Maintained by:** OpenClaw Community

## Download Archives

### For Manual Installation

**TAR.GZ:**
```bash
curl -L https://github.com/loudmouthedmedia/context-bridge/releases/download/v1.0.0/context-bridge-1.0.0.tar.gz | tar -xzf -
```

**ZIP:**
```bash
curl -L https://github.com/loudmouthedmedia/context-bridge/releases/download/v1.0.0/context-bridge-1.0.0.zip -o context-bridge.zip
unzip context-bridge.zip
```

### For ClawHub Submission

Submit the GitHub repository URL:
```
https://github.com/loudmouthedmedia/context-bridge
```