# APEX STACK for Claude Code ⚡🧠⚙

**Three skills. One install. Complete autonomous developer agent.**

```bash
clawhub install apex-stack-claude-code
```

---

## What this bundles

| Skill | Layer | What it does |
|---|---|---|
| **apex-agent** | Cognition | Better thinking, 5 modes, 7 anti-patterns eliminated |
| **agent-memoria** | Memory | Persistent project context across every session |
| **agent-architect** | Execution | Autonomous goal pursuit, self-correcting task execution |

All three, adapted specifically for Claude Code workflows.

---

## Install in 2 steps

```bash
# 1. Install the skill
clawhub install apex-stack-claude-code

# 2. Add to your project
cat ~/.openclaw/skills/apex-stack-claude-code/SKILL.md >> CLAUDE.md
```

Or globally (all Claude Code sessions):
```bash
cat ~/.openclaw/skills/apex-stack-claude-code/SKILL.md >> ~/.claude/CLAUDE.md
```

---

## What changes immediately

**Session start:**
```
⚡🧠⚙ APEX STACK active.
🧠 [Project] context loaded. FastAPI · Docker · Working on pagination. Ready.
```

**Bug fix request:**
```
Developer: "Fix the 500 error on /api/users"

Without APEX STACK: "Can you share the error message and your code?"
With APEX STACK:    Reads the file, finds the N+1 query causing the timeout,
                    fixes it, checks for the same pattern elsewhere, done.
```

**Goal-oriented request:**
```
Developer: "Add authentication to this API"

Without APEX STACK: "Here are 5 approaches to authentication..."
With APEX STACK:    ⚙ Executing: READ → PLAN → IMPLEMENT → TEST → VERIFY
                    JWT auth added, middleware configured, endpoints protected,
                    tests written, docs updated. One response.
```

---

## For solo founders and indie developers

If you build alone, context is everything. Every session you re-explain:
- What the project does
- What stack you're using  
- What you decided last week
- What you're trying to achieve today

APEX STACK ends that. One `CLAUDE.md` file holds everything.
Every session starts where the last one ended.

---

## Requirements

- Claude Code (any version)
- A `CLAUDE.md` file in your project (or create one)
- Nothing else

No API keys. No configuration. No external services.

---

*APEX STACK for Claude Code v1.0.0 by contrario*
*Part of the APEX ecosystem on ClawHub*
