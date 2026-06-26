# Multi-Agent Support

`coding-pipeline` works across different AI coding agents with agent-specific activation. Read the section for the platform you're using.

## Claude Code

**Activation**: Skill description match + optional `UserPromptSubmit` hook
**Setup**: `.claude/settings.json` (see `hooks-setup.md`)
**Detection**: Automatic when a task matches the skill description, reinforced by the optional hook

The skill activates whenever Claude Code sees a task description that matches the frontmatter (bug, feature, refactor, error investigation). The optional hook adds a reminder at every prompt start.

**Recommended Claude Code workflow:**

1. Install: copy the skill folder to `~/.claude/skills/coding-pipeline/`
2. Optional: enable the hook via `~/.claude/settings.json`
3. Start a task — Claude Code should invoke the skill automatically based on the description

## Codex CLI

**Activation**: Skill description match + optional `UserPromptSubmit` hook
**Setup**: `.codex/settings.json` (same shape as Claude Code)
**Detection**: Automatic via the skill description

Codex supports the same hook events and skill loading as Claude Code. Point the same activator script at both.

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/coding-pipeline/scripts/activator.sh"
      }]
    }]
  }
}
```

## OpenClaw

**Activation**: Workspace injection at session start
**Setup**: See `openclaw-integration.md` for full details
**Detection**: Automatic — the skill content is loaded at workspace start

OpenClaw is the primary home for this skill. Workspace injection means the 4-phase structure is always in context, no hooks required.

## GitHub Copilot

**Activation**: Manual — Copilot has no hook support
**Setup**: Add a reminder block to `.github/copilot-instructions.md`:

```markdown
## Coding Pipeline

For non-trivial tasks (bug fixes, features, refactors, error investigations), follow a 4-phase discipline:

1. **Phase 1 — Planner**: Write a one-sentence hypothesis before touching code. Define scope and success criteria.
2. **Phase 2 — Coder**: Apply exactly one focused change. Full files, no speculative refactors.
3. **Phase 3 — Validator**: Verify root cause, not just symptom. Build check + types + focused test + scope check.
4. **Phase 4 — Debugger**: Max 3 attempts, each with a new hypothesis, all documented. Escalate after 3.

Skip the pipeline only for typos, formatting, and one-line config changes.
```

**Copilot Chat prompts:**

- "Apply the coding-pipeline discipline to this task — start at Phase 1"
- "Write the hypothesis for Phase 1 before suggesting any code"
- "Is this Phase 2 or Phase 3?" (useful mid-task)

**Detection**: Manual — Copilot won't auto-invoke the pipeline. Reference it explicitly in prompts.

## Cursor

**Activation**: Manual — similar to Copilot
**Setup**: Add the 4-phase discipline to `.cursor/rules` or equivalent

Cursor respects project-level rule files; the content should mirror the Copilot section above.

## Agent-Agnostic Guidance

Regardless of platform, apply the pipeline when:

1. **A bug is reported** — don't jump to Phase 2
2. **A feature is requested** — scope and success criteria first
3. **A refactor is planned** — multi-cycle by default
4. **An error is unclear** — Phase 1 forces you to articulate what you don't know
5. **A test is failing** — the failing test is your Phase 3 verification

The 4 phases are text, not tooling. Any agent that reads markdown can follow them.

## Platform Comparison

| Platform | Auto-invocation | Hook support | Token overhead | Best for |
|----------|-----------------|---------------|----------------|----------|
| Claude Code | ✅ (description) | ✅ | ~80/prompt with hook | Single-project discipline |
| Codex CLI | ✅ (description) | ✅ | ~80/prompt with hook | Same as Claude Code |
| OpenClaw | ✅ (injection) | ❌ (not needed) | Baseline injection | Multi-project consistency |
| GitHub Copilot | ❌ (manual) | ❌ | 0 | Teams already using Copilot |
| Cursor | ❌ (manual) | ❌ | 0 | Cursor users who want structure |

## Recommendation

If you use **more than one** of these platforms, install via ClawdHub in OpenClaw (zero overhead, automatic) and configure the hook in Claude Code / Codex. Copilot and Cursor users get the manual version via rule files.
