# Persist (Knowledge Persistence)

Save session-discovered knowledge to appropriate long-term storage.

## When to Use

- `/claudify persist` — direct invocation
- `/cleanup run` Step 3 — automatic as part of session cleanup

## Workflow

### A. Documentation Recommendation

Suggest where to document new information discovered during conversation.

**Detection targets**: Troubleshooting solutions, project/infra structure, failed attempts, external service usage, environment setup.

**Location recommendations**:

| Information type | Recommended location |
|-----------------|---------------------|
| Project structure/config | Project `CLAUDE.md` or `README.md` |
| Infrastructure/server info | `pages/` or Logseq |
| Failed attempts | `pages/FAILED_ATTEMPTS.md` |
| External service integration | Project `docs/` |
| Personal workflow | `~/.claude/CLAUDE.md` (global) |
| Troubleshooting record | Logseq daily journal |

Exclude already-documented info and sensitive data (API keys, passwords).

### B. Infrastructure Documentation Check

**Skip condition**: No infrastructure work in session.

When infra work was performed, verify that discovered information (config file paths, port mappings, network routing, service connection structure) is documented in CLAUDE.md.

### C. Memory Save

Save session-learned project knowledge to persistent memory.

#### Pre-check: Storage Location Classification

| Information type | Storage | Example |
|-----------------|---------|---------|
| One-time environment fact | **Memory** | Server IP, resource usage, API key location |
| IaC/infra knowledge | **Skill** (`/skill-kit route`) | Terraform structure, ArgoCD procedures |
| Domain knowledge, procedures | **Skill** (`/skill-kit route`) | Deploy procedures, troubleshooting guides |
| Behavior rules, prohibitions | **Rules** | Mistake prevention (handled in improve topic) |

**Decision criteria**: Procedurally reusable → skill. Fits existing skill topic → skill. Reference-only → memory.

#### Storage Tool Priority

| Priority | Condition | Tool |
|----------|-----------|------|
| 1 | Serena MCP available | `activate_project` → `list_memories` → `read_memory` → `edit_memory` / `write_memory` |
| 2 | Serena unavailable (fallback) | Claude Code auto memory (`memory/MEMORY.md` + individual `.md` files) |

**Serena procedure**: `read_memory` to check existing topic → `edit_memory` if exists, `write_memory` if not. No overwrites.

**Claude Code fallback note**: In vibe-kanban worktrees, save to **main project path** only.

#### What to Save (Context Preservation Focus)

- **Decisions**: Why this approach was chosen (vs alternatives)
- **Deploy/infra state**: Current versions, deploy progress, pending work
- **Discovered patterns/rules**: Code conventions, project-specific quirks
- **In-progress work**: Work state to continue in next session

**Not saved here** (experience-logger domain): Hot Files, tool usage patterns.

## Ralph Mode

**Detection**: see SKILL.md — only when both `.ralph/` directory exists **and** environment variable `RALPH_LOOP=1` is set.

A-C: detect + record to `.ralph/improvements.md` only. No direct modifications/saves.

## Phase 2 Integration

This topic does NOT call AskUserQuestion directly. All findings are returned to the caller (cleanup run.md) for batch Phase 2 confirmation.

**Return format** (internal):
```
{
  docs: [{ label, description, location }],
  infra: [{ label, description }],
  memory: [{ label, description, storageType: "serena"|"claude-memory"|"skill" }]
}
```
