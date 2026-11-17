# Commands, Severity Grades, and Findings

Detail split out of `SKILL.md` to keep it within the 100-line budget.

All examples assume the project-local pinned install described in `SKILL.md`:

```bash
npm install --save-dev ecc-agentshield@1.2.3
```

`npx --no-install` is used throughout so a command can never fetch a version
that is not already pinned in the project's lockfile. Drop `--no-install` only
if you deliberately want npx to fetch, and never run an unpinned `@latest` tag
against a config directory.

### Commands

```bash
# Basic scan of the current project
npx --no-install ecc-agentshield scan --path .claude

# Filter by severity
npx --no-install ecc-agentshield scan --path .claude --min-severity medium

# Output formats
npx --no-install ecc-agentshield scan --path .claude --format json
npx --no-install ecc-agentshield scan --path .claude --format markdown

# Deep analysis (requires ANTHROPIC_API_KEY) — uses a limited key
npx --no-install ecc-agentshield scan --path .claude --opus --stream

# AUTO-FIX: modifies your configuration. Run only after reviewing a plain
# scan, and only against a version-controlled or throwaway working tree
# so the changes are reviewable and reversible.
npx --no-install ecc-agentshield scan --path .claude --fix

# INITIALIZE: writes a starter configuration. Read what it would create
# before letting it write to your config directory.
npx --no-install ecc-agentshield init
```

---

## Severity Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Secure |
| B | 75-89 | Minor issues |
| C | 60-74 | Needs attention |
| D | 40-59 | Significant risks |
| F | 0-39 | Critical |

## Critical Findings (Fix Immediately)

- Hardcoded API keys in config
- `Bash(*)` unrestricted shell access
- Command injection via `${file}` interpolation
- Shell-running MCP servers

## High Findings (Fix Before Production)

- Auto-run instructions in CLAUDE.md
- Missing deny lists
- Unnecessary Bash access in agents
