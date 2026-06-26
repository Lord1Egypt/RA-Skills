# Automation Decision Guide

## Automation Types Comparison

| Type | Location | Purpose | Trigger | Complexity |
|------|----------|---------|---------|------------|
| **Skill** | `.claude/skills/` | Specialized capability with instructions | Automatic (description match) | Low-Medium |
| **Agent** | `.claude/agents/` | Task delegation with specific tools | `Task` tool with `subagent_type` | Medium-High |
| **Rules** | `.claude/rules/` | AI behavior constraints, conventions | Automatic (session start) | Low |
| **Slash Command** | `.claude/commands/` | Quick prompt templates | User types `/command` | Low |
| **Hook** | `.claude/settings.json` | Lifecycle event automation | Tool use / Session events | Low-Medium |

## Decision Guide

### Choose **Skill** when

- Providing specialized instructions for a domain (PDF, Excel, API design)
- Need automatic activation based on context
- Want to guide Claude's behavior for specific file types
- Single capability that enhances Claude's responses
- **Existing shell scripts/functions** - Skill guides execution, lighter and faster than Agent

**Examples**: code-reviewer, excel-analyzer, pdf-processor

### Choose **Agent** when

- Task requires autonomous multi-step execution
- Need specific tool restrictions or permissions
- Want to delegate complex tasks to a subprocess
- Requires parallel execution or background processing

**Examples**: gitlab-cicd-manager, weekly-report-manager, macos-cleanup

### Choose **Rules** when

- Define project-wide coding conventions
- Set AI behavior constraints and guardrails
- Enforce security policies (forbidden commands, backup requirements)
- Establish documentation standards
- Need passive guidance that applies to all interactions

**Examples**: code-style.md, git-workflow.md, security-constraints.md

### Choose **Slash Command** when

- Simple prompt template or shortcut
- User-initiated action (not automatic)
- Quick access to common operations
- No complex logic needed

**Examples**: /review-pr, /summarize, /translate

### Choose **Hook** when

- React to tool use events (before/after Edit, Write, Bash, etc.)
- Automate actions on session lifecycle (start, end)
- Run shell commands in response to Claude's actions
- Need validation or side effects without user interaction

**Examples**: auto-build after file changes, lint on save, cleanup on session end

**Hook Events**: PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop, SessionStart, SessionEnd, Notification, PreCompact

**HARD STOP — every hook must have an owning skill**:
- Hook scripts must be installed from some skill's `resources/` directory (orphan hooks forbidden)
- Domain hooks (openclaw, semaphore, ralph, etc.) → store at `resources/<hook>.sh` in the matching domain skill, install via the skill's install procedure
- Shared/system hooks (Bash guards, session handling, etc.) → **the `hook` skill is the default installer** (`~/.claude/skills/hook/resources/`)
- Never create a hook in isolation — decide its owning skill at the same time it is added (see `~/.agents/rules/automation.md`)

### Choose **Distribution Level**

| Level | Location | Target | Characteristics |
|-------|----------|--------|-----------------|
| **Open Source** | claudemarketplaces.com | All users | Universal, documentation required |
| **Team/Project** | `.claude/` (project) | Dev team | Git commit, project-specific |
| **Personal** | `~/.claude/` (global) | Self only | Experimental, personal workflow |

### Distribution Decision

| Question | Open Source | Team | Personal |
|----------|-------------|------|----------|
| Useful to other developers? | ✅ | ⚠️ | ❌ |
| Team members need this? | ⚠️ | ✅ | ❌ |
| Project-specific? | ❌ | ✅ | ⚠️ |
| Personal workflow? | ❌ | ❌ | ✅ |

## Combination Patterns

### Choose **Combination** when

Consider separation when functionality includes multiple concerns or reusable parts.

**Skill + Skill** (separation of concerns)

- Each can activate independently
- Example: `pdf-reader` + `pdf-form-filler` (read vs write)
- Example: `api-designer` + `api-validator` (design vs validation)

**Agent + Skill** (execution + guidance separation)

- Agent: Autonomous execution, tool use, background tasks
- Skill: Domain knowledge/guidelines for agent reference
- Example: `deploy-agent` (execution) + `deploy-checklist` (validation criteria)
- Example: `code-reviewer-agent` (execution) + `code-style-guide` (style rules)

**Agent + Agent** (parallel processing)

- Independent tasks that can run in parallel
- Example: `test-runner` + `lint-checker` (simultaneous execution)

### Separation Criteria Checklist

- [ ] Is each part independently useful?
- [ ] Can one change without affecting the other?
- [ ] Can it be reused in other features?
- [ ] Does separation reduce complexity?

If one is sufficient, don't separate. Over-separation increases complexity.

## Quick Reference

### File Locations

| Type | Global | Project |
|------|--------|---------|
| Skill | `~/.claude/skills/name/SKILL.md` | `.claude/skills/name/SKILL.md` |
| Agent | `~/.claude/agents/name.md` | `.claude/agents/name.md` |
| Rules | `~/.claude/rules/name.md` | `.claude/rules/name.md` |
| Command | `~/.claude/commands/name.md` | `.claude/commands/name.md` |
| Hook | `~/.claude/settings.json` | `.claude/settings.json` |

### Answer → Type Mapping

| Answer Combination | Recommended Type |
|--------------------|------------------|
| Automatic + instruction-focused | Skill |
| Automatic + tool execution | Agent |
| Automatic + constraints/conventions | Rules |
| Manual + simple | Slash Command |
| Event reaction | Hook |
| Complex requirements | Combination |
