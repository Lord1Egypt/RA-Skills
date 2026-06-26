# Host Tool Mapping

This skill is intentionally tool-agnostic.

Map the instruction layer to the host tool you already use.

## Common mappings

### Claude Code

- Instruction layer: `CLAUDE.md` or `CLAUDE.local.md`
- Durable layer: repo-local memory directory such as `.agent-memory/`
- Session layer: `.agent-memory/session/summary.md`

### Codex

- Instruction layer: `AGENTS.md`, project instructions, or repo-local guidance file
- Durable layer: `.agent-memory/`
- Session layer: `.agent-memory/session/summary.md`

### GitHub Copilot

- Instruction layer: `.github/copilot-instructions.md`
- Durable layer: `.agent-memory/`
- Session layer: `.agent-memory/session/summary.md`

### Cursor or Windsurf

- Instruction layer: the tool's repo rules file
- Durable layer: `.agent-memory/`
- Session layer: `.agent-memory/session/summary.md`

## Recommended defaults

If your tool does not have a durable instruction file, create one and keep it small.

Recommended repo-local layout:

```text
.agent-memory/
├── MEMORY.md
├── user/
├── style/
├── project/
├── references/
└── session/
    └── summary.md
```

This keeps the durable layer explicit and portable across tools.
