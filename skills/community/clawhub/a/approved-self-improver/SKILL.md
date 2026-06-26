---
name: approved-self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement with user-approved skill updates. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task, (7) User asks 'what skill improvements do you recommend?' or 'show me pending skill updates' or similar, (8) A skill failure matches an existing improvement proposal. Also review learnings and pending improvement proposals before major tasks. IMPORTANT: Never modify any skill without explicit user approval unless the user has authorized auto-update for that specific skill."
metadata:
---

# Approved-Self-Improvement Skill

Log learnings and errors to markdown files for continuous improvement. Coding agents can later process these into fixes, and important learnings get promoted to project memory. **All skill modifications require explicit user approval** — improvement proposals are documented and presented to the user before any changes are applied. See [Approval-Gated Skill Improvement](#approval-gated-skill-improvement) for the full workflow.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings/pending-improvements
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n\nCorrections, insights, and knowledge gaps captured during development.\n\n**Categories**: correction | insight | knowledge_gap | best_practice\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/ERRORS.md ] || printf "# Errors\n\nCommand failures and integration errors.\n\n---\n" > .learnings/ERRORS.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nCapabilities requested by the user.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
[ -f .learnings/AUTO_UPDATE_AUTHORIZATIONS.md ] || printf "# Auto-Update Authorizations\n\nSkills authorized for automatic self-improvement without user approval.\nBy default, NO skills are authorized. Users must explicitly grant per-skill.\n\n---\n" > .learnings/AUTO_UPDATE_AUTHORIZATIONS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log secrets, tokens, private keys, environment variables, or full source/config files unless the user explicitly asks for that level of detail. Prefer short summaries or redacted excerpts over raw command output or full transcripts.

If you want automatic reminders or setup assistance, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| User corrects you | Log to `.learnings/LEARNINGS.md` with category `correction` |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` |
| API/external tool fails | Log to `.learnings/ERRORS.md` with integration details |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` with category `knowledge_gap` |
| Found better approach | Log to `.learnings/LEARNINGS.md` with category `best_practice` |
| Skill failure identified with fix | Create proposal in `.learnings/pending-improvements/` — **do NOT modify the skill** |
| Recurring failure matches existing proposal | Log recurrence in proposal, notify user and recommend applying it |
| User asks for recommended improvements | List all pending proposals from `.learnings/pending-improvements/` |
| User approves an improvement proposal | Apply changes, update proposal status to `applied` |
| User authorizes auto-update for a skill | Record in `.learnings/AUTO_UPDATE_AUTHORIZATIONS.md` |
| Skill failure + skill is auto-update authorized | Apply fix directly, log what changed |
| Simplify/Harden recurring patterns | Log/update `.learnings/LEARNINGS.md` with `Source: simplify-and-harden` and a stable `Pattern-Key` |
| Similar to existing entry | Link with `**See Also**`, consider priority bump |
| Broadly applicable learning | Promote to `CLAUDE.md`, `AGENTS.md`, and/or `.github/copilot-instructions.md` |
| Workflow improvements | Promote to `AGENTS.md` (OpenClaw workspace) |
| Tool gotchas | Promote to `TOOLS.md` (OpenClaw workspace) |
| Behavioral patterns | Promote to `SOUL.md` (OpenClaw workspace) |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-agent
```

**Manual:**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

Remade for openclaw from original repo : https://github.com/pskoett/pskoett-ai-skills - https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, delegation patterns
├── SOUL.md            # Behavioral guidelines, personality, principles
├── TOOLS.md           # Tool capabilities, integration gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── ERRORS.md
    ├── FEATURE_REQUESTS.md
    ├── AUTO_UPDATE_AUTHORIZATIONS.md  # Per-skill auto-update permissions
    └── pending-improvements/          # Improvement proposals awaiting approval
        └── IMP-YYYYMMDD-XXX-skill-name.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings/pending-improvements
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — corrections, knowledge gaps, best practices
- `ERRORS.md` — command failures, exceptions
- `FEATURE_REQUESTS.md` — user-requested capabilities
- `AUTO_UPDATE_AUTHORIZATIONS.md` — per-skill auto-update permissions (copy from `assets/`)

### Promotion Targets

When learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Behavioral patterns | `SOUL.md` | "Be concise, avoid disclaimers" |
| Workflow improvements | `AGENTS.md` | "Spawn sub-agents for long tasks" |
| Tool gotchas | `TOOLS.md` | "Git push needs auth configured first" |

### Inter-Session Communication

OpenClaw provides tools to share learnings across sessions:

- **sessions_list** — View active/recent sessions
- **sessions_history** — Read another session's transcript  
- **sessions_send** — Send a learning to another session
- **sessions_spawn** — Spawn a sub-agent for background work

Use these only in trusted environments and only when the user explicitly wants cross-session sharing. Prefer sending a short sanitized summary and relevant file paths, not raw transcripts, secrets, or full command output.

### Optional: Enable Hook

For automatic reminders at session start:

```bash
# Copy hook to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# Enable it
openclaw hooks enable self-improvement
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above. Avoid reading templates from the current repo or workspace unless you explicitly trust that path.

### Add reference to agent files AGENTS.md, CLAUDE.md, or .github/copilot-instructions.md to remind yourself to log learnings. (this is an alternative to hook-based reminders)

#### Self-Improvement Workflow

When errors or corrections occur:
1. Log to `.learnings/ERRORS.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - `CLAUDE.md` - project facts and conventions
   - `AGENTS.md` - workflows and automation
   - `.github/copilot-instructions.md` - Copilot context

## Logging Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: simplify.dead_code | harden.input_validation (optional, for recurring-pattern tracking)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

### Error Entry

Append to `.learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed

### Error
```
Actual error message or output
```

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant
- Summary or redacted excerpt of relevant output (avoid full transcripts and secret-bearing data by default)

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (if recurring)

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they're solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `ERR` (error), `FEAT` (feature)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250115-001`, `ERR-20250115-A3F`, `FEAT-20250115-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of what was done
```

Other status values:
- `in_progress` - Actively being worked on
- `wont_fix` - Decided not to address (add reason in Resolution notes)
- `promoted` - Elevated to CLAUDE.md, AGENTS.md, or .github/copilot-instructions.md

## Promoting to Project Memory

When a learning is broadly applicable (not a one-off fix), promote it to permanent project memory.

### When to Promote

- Learning applies across multiple files/features
- Knowledge any contributor (human or AI) should know
- Prevents recurring mistakes
- Documents project-specific conventions

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| `CLAUDE.md` | Project facts, conventions, gotchas for all Claude interactions |
| `AGENTS.md` | Agent-specific workflows, tool usage patterns, automation rules |
| `.github/copilot-instructions.md` | Project context and conventions for GitHub Copilot |
| `SOUL.md` | Behavioral guidelines, communication style, principles (OpenClaw workspace) |
| `TOOLS.md` | Tool capabilities, usage patterns, integration gotchas (OpenClaw workspace) |

### How to Promote

1. **Distill** the learning into a concise rule or fact
2. **Add** to appropriate section in target file (create file if needed)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: CLAUDE.md`, `AGENTS.md`, or `.github/copilot-instructions.md`

### Promotion Examples

**Learning** (verbose):
> Project uses pnpm workspaces. Attempted `npm install` but failed. 
> Lock file is `pnpm-lock.yaml`. Must use `pnpm install`.

**In CLAUDE.md** (concise):
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**Learning** (verbose):
> When modifying API endpoints, must regenerate TypeScript client.
> Forgetting this causes type mismatches at runtime.

**In AGENTS.md** (actionable):
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: ERR-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring issues often indicate:
   - Missing documentation (→ promote to CLAUDE.md or .github/copilot-instructions.md)
   - Missing automation (→ add to AGENTS.md)
   - Architectural problem (→ create tech debt ticket)

## Simplify & Harden Feed

Use this workflow to ingest recurring patterns from the `simplify-and-harden`
skill and turn them into durable prompt guidance.

### Ingestion Workflow

1. Read `simplify_and_harden.learning_loop.candidates` from the task summary.
2. For each candidate, use `pattern_key` as the stable dedupe key.
3. Search `.learnings/LEARNINGS.md` for an existing entry with that key:
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. If found:
   - Increment `Recurrence-Count`
   - Update `Last-Seen`
   - Add `See Also` links to related entries/tasks
5. If not found:
   - Create a new `LRN-...` entry
   - Set `Source: simplify-and-harden`
   - Set `Pattern-Key`, `Recurrence-Count: 1`, and `First-Seen`/`Last-Seen`

### Promotion Rule (System Prompt Feedback)

Promote recurring patterns into agent context/system prompt files when all are true:

- `Recurrence-Count >= 3`
- Seen across at least 2 distinct tasks
- Occurred within a 30-day window

Promotion targets:
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md` for OpenClaw workspace-level guidance when applicable

Write promoted rules as short prevention rules (what to do before/while coding),
not long incident write-ups.

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before starting a new major task
- After completing a feature
- When working in an area with past learnings
- Weekly during active development

### Quick Status Check
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: backend" .learnings/*.md
```

### Review Actions
- Resolve fixed items
- Promote applicable learnings
- Link related entries
- Escalate recurring issues

## Detection Triggers

Automatically log when you notice:

**Corrections** (→ learning with `correction` category):
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's outdated..."

**Feature Requests** (→ feature request):
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."
- "Why can't you..."

**Knowledge Gaps** (→ learning with `knowledge_gap` category):
- User provides information you didn't know
- Documentation you referenced is outdated
- API behavior differs from your understanding

**Errors** (→ error entry):
- Command returns non-zero exit code
- Exception or stack trace
- Unexpected output or behavior
- Timeout or connection failure

**Skill Improvement Needed** (→ improvement proposal in `.learnings/pending-improvements/`):
- Skill produced wrong output or used wrong approach
- Skill instructions are outdated or incomplete
- Skill failed to handle an edge case
- User manually corrected a skill's output
- Multiple errors logged against the same skill
- **NEVER modify the skill directly** — create a proposal instead

**Improvement Review Requested** (→ list pending proposals):
- "What skill improvements do you recommend?"
- "Show me pending skill updates"
- "Any skill fixes waiting?"
- "What needs updating?"

**Auto-Update Authorization** (→ update `AUTO_UPDATE_AUTHORIZATIONS.md`):
- "Allow auto-updates for [skill-name]"
- "Let [skill-name] self-improve"
- "Stop auto-updating [skill-name]"
- "Require approval for [skill-name]"

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| `critical` | Blocks core functionality, data loss risk, security issue |
| `high` | Significant impact, affects common workflows, recurring issue |
| `medium` | Moderate impact, workaround exists |
| `low` | Minor inconvenience, edge case, nice-to-have |

## Area Tags

Use to filter learnings by codebase region:

| Area | Scope |
|------|-------|
| `frontend` | UI, components, client-side code |
| `backend` | API, services, server-side code |
| `infra` | CI/CD, deployment, Docker, cloud |
| `tests` | Test files, testing utilities, coverage |
| `docs` | Documentation, comments, READMEs |
| `config` | Configuration files, environment, settings |

## Best Practices

1. **Log immediately** - context is freshest right after the issue
2. **Be specific** - future agents need to understand quickly
3. **Include reproduction steps** - especially for errors
4. **Link related files** - makes fixes easier
5. **Suggest concrete fixes** - not just "investigate"
6. **Use consistent categories** - enables filtering
7. **Promote aggressively** - if in doubt, add to CLAUDE.md or .github/copilot-instructions.md
8. **Review regularly** - stale learnings lose value

## Gitignore Options

**Keep learnings local** (per-developer):
```gitignore
.learnings/
```

This repo uses that default to avoid committing sensitive or noisy local logs by accident.

**Track learnings in repo** (team-wide):
Don't add to .gitignore - learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in** - you must explicitly configure hooks.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}
```

This is optional. The recommended default is activator-only setup; enable `PostToolUse` only if you are comfortable with hook scripts inspecting command output for error patterns.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on command errors |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Approval-Gated Skill Improvement

**CRITICAL RULE: Never modify any skill file without explicit user approval.** When a skill fails or could be improved, document the proposed changes as an improvement proposal. The user decides whether to apply them.

### Core Principles

1. **No silent updates**: AI must never edit a skill's SKILL.md, scripts, or references without the user saying yes
2. **Document first, change never (unless approved)**: Every proposed fix goes into a proposal file in `.learnings/pending-improvements/`
3. **Proactive notification on recurrence**: If a failure matches an existing proposal, tell the user immediately and recommend applying it
4. **Per-skill auto-update opt-in**: Users can authorize specific skills for automatic updates — but the default is always **approval required**

### When a Skill Fails — What To Do

When a skill produces an error, wrong output, or suboptimal result:

1. **Log the error** to `.learnings/ERRORS.md` as usual
2. **Check for existing proposal**: `ls .learnings/pending-improvements/*-<skill-name>.md 2>/dev/null`
3. **If a proposal already exists for this skill**:
   - Add the new occurrence to the proposal's **Recurrence Log** table
   - **Notify the user immediately**: _"I've encountered this issue with the [skill-name] skill again. We already have a documented fix (IMP-XXXXXXXX-XXX). Would you like me to apply the proposed changes?"_
   - Present a summary of what the proposal would change
   - Wait for explicit approval before touching anything
4. **If no proposal exists yet**:
   - Analyze the failure and determine what skill changes would fix it
   - Create a new proposal file: `.learnings/pending-improvements/IMP-YYYYMMDD-XXX-skill-name.md`
   - Inform the user: _"I've documented a proposed improvement to the [skill-name] skill. You can review it anytime by asking 'what skill improvements do you recommend?'"_
   - Do NOT apply the changes
5. **Check auto-update authorization**: Before creating a proposal, check `.learnings/AUTO_UPDATE_AUTHORIZATIONS.md`. If this specific skill is listed as authorized for auto-update, apply the fix directly, then inform the user what was changed. Otherwise, follow steps 3-4.

### Improvement Proposal Format

Save each proposal as its own file in `.learnings/pending-improvements/` named `IMP-YYYYMMDD-XXX-skill-name.md`:

```markdown
# Improvement Proposal: IMP-YYYYMMDD-XXX

**Skill**: skill-name
**Skill Path**: path/to/skill/SKILL.md
**Created**: ISO-8601 timestamp
**Status**: pending | approved | rejected | applied
**Priority**: low | medium | high | critical
**Triggered By**: error | user_feedback | recurring_pattern | knowledge_gap

## Problem

What went wrong. Reference error IDs (e.g., ERR-YYYYMMDD-XXX) if applicable.

## Root Cause

Why the skill failed or produced suboptimal results.

## Proposed Changes

### Change 1: [add | modify | remove] — [brief label]

**Section**: Which section of the SKILL.md is affected
**Current Content** (if modifying/removing):
\```
Existing text or instruction that needs changing
\```
**Proposed Content** (if adding/modifying):
\```
New or updated text or instruction
\```
**Rationale**: Why this change fixes the problem

### Change 2: [add | modify | remove] — [brief label]
(repeat as needed)

## Expected Impact

What will improve after applying these changes.

## Recurrence Log

| Date | Error/Context | Notes |
|------|--------------|-------|
| YYYY-MM-DD | ERR-YYYYMMDD-XXX | First occurrence |

---
```

### User-Triggered Review of Pending Improvements

The user can ask for a review of all pending improvement proposals at any time. Trigger phrases include:

- "What skill improvements do you recommend?"
- "Show me pending skill updates"
- "Any skill fixes waiting?"
- "What skills need updating?"
- "Review skill improvement proposals"

When triggered:

1. **List all files** in `.learnings/pending-improvements/` with status `pending`
2. **For each proposal**, present a clear summary:
   - Which skill it affects
   - What the problem is (one sentence)
   - What changes are proposed (bullet list of add/modify/remove)
   - How many times the issue has recurred
   - Priority level
3. **Ask the user** which proposals they want to approve, reject, or defer
4. **On approval**: Apply the changes to the skill, update proposal status to `applied`, add resolution timestamp
5. **On rejection**: Update proposal status to `rejected`, add user's reason if given
6. **On defer**: Leave as `pending`, no changes

### Applying Approved Changes

When the user approves a proposal:

1. Read the full proposal file
2. For each proposed change:
   - If `add`: Insert the new content at the specified section
   - If `modify`: Replace the current content with the proposed content
   - If `remove`: Delete the specified content
3. Update the proposal file:
   - Set `**Status**: applied`
   - Add `**Applied**: ISO-8601 timestamp` after Status
   - Add `**Applied By**: user-approved` after Applied
4. Log a learning entry in `.learnings/LEARNINGS.md` noting the skill improvement was applied
5. Confirm to the user exactly what was changed

### Auto-Update Authorization

By default, **no skill is authorized for auto-update**. The user must explicitly grant permission on a per-skill basis.

**How to authorize a skill for auto-update:**

The user says something like:
- "Allow auto-updates for the [skill-name] skill"
- "The [skill-name] skill can self-improve without asking me"
- "Auto-approve improvements to [skill-name]"

When authorized:

1. Add an entry to `.learnings/AUTO_UPDATE_AUTHORIZATIONS.md`:

```markdown
## [skill-name]
**Authorized**: ISO-8601 timestamp
**Authorized By**: user
**Scope**: full
**Notes**: User authorized auto-update in conversation

---
```

2. Confirm to the user: _"I've authorized auto-updates for [skill-name]. Future improvements to this skill will be applied automatically and I'll inform you what changed. You can revoke this anytime."_

**How to revoke auto-update:**

The user says something like:
- "Stop auto-updating [skill-name]"
- "Require approval for [skill-name] again"
- "Revoke auto-update for [skill-name]"

When revoked: Remove the entry from `AUTO_UPDATE_AUTHORIZATIONS.md` and confirm.

**Checking authorization before applying changes:**

```bash
grep -l "## skill-name-here" .learnings/AUTO_UPDATE_AUTHORIZATIONS.md 2>/dev/null
```

If the skill is listed AND its entry is present (not just the file header), it is authorized. Otherwise, require user approval.

### Auto-Update Behavior

When a skill IS authorized for auto-update and a failure is detected:

1. Analyze the failure and determine the fix
2. Check if a pending proposal already exists — if so, apply it
3. If no proposal exists, create one with status `applied` (for the record) and apply the fix
4. **Always inform the user** what was changed: _"I auto-applied an improvement to [skill-name]: [one-line summary of change]. This skill is authorized for auto-update. Details logged in IMP-XXXXXXXX-XXX."_
5. Log the change in `.learnings/LEARNINGS.md`

### Detection Triggers for Skill Improvements

Watch for these signals that a skill needs an improvement proposal:

**During skill execution:**
- Skill produces an error or unexpected output
- Skill's instructions lead to a wrong approach
- Skill is missing a step that was needed
- Skill references outdated tools, APIs, or syntax
- User has to manually correct the skill's output

**From error logs:**
- Multiple errors logged against the same skill (check `See Also` links)
- Error with `Reproducible: yes` tied to a skill

**From user feedback:**
- "This skill keeps getting X wrong"
- "The skill should also handle Y"
- "That's not how you do X anymore"

## Automatic Skill Extraction

When a learning is valuable enough to become a reusable skill, extract it using the provided helper.

### Skill Extraction Criteria

A learning qualifies for skill extraction when ANY of these apply:

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Has `See Also` links to 2+ similar issues |
| **Verified** | Status is `resolved` with working fix |
| **Non-obvious** | Required actual debugging/investigation to discover |
| **Broadly applicable** | Not project-specific; useful across codebases |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with learning content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Manual Extraction

If you prefer manual creation:

1. Create `skills/<skill-name>/SKILL.md`
2. Use template from `assets/SKILL-TEMPLATE.md`
3. Follow [Agent Skills spec](https://agentskills.io/specification):
   - YAML frontmatter with `name` and `description`
   - Name must match folder name
   - No README.md inside skill folder

### Extraction Detection Triggers

Watch for these signals that a learning should become a skill:

**In conversation:**
- "Save this as a skill"
- "I keep running into this"
- "This would be useful for other projects"
- "Remember this pattern"

**In learning entries:**
- Multiple `See Also` links (recurring issue)
- High priority + resolved status
- Category: `best_practice` with broad applicability
- User feedback praising the solution

### Skill Quality Gates

Before extraction, verify:

- [ ] Solution is tested and working
- [ ] Description is clear without original context
- [ ] Code examples are self-contained
- [ ] No project-specific hardcoded values
- [ ] Follows skill naming conventions (lowercase, hyphens)

## Multi-Agent Support

This skill works across different AI coding agents with agent-specific activation.

### Claude Code

**Activation**: Hooks (UserPromptSubmit, PostToolUse)
**Setup**: `.claude/settings.json` with hook configuration
**Detection**: Automatic via hook scripts

### Codex CLI

**Activation**: Hooks (same pattern as Claude Code)
**Setup**: `.codex/settings.json` with hook configuration
**Detection**: Automatic via hook scripts

### GitHub Copilot

**Activation**: Manual (no hook support)
**Setup**: Add to `.github/copilot-instructions.md`:

```markdown
## Self-Improvement

After solving non-obvious issues, consider logging to `.learnings/`:
1. Use format from self-improvement skill
2. Link related entries with See Also
3. Promote high-value learnings to skills

Ask in chat: "Should I log this as a learning?"
```

**Detection**: Manual review at session end
