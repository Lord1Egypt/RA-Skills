# collective-memory

> Broadcast a single memory note to multiple AI-agent workspaces in one shot —
> idempotent upsert into `MEMORY.md`, `AGENTS.md`, `TOOLS.md`, `USER.md`, or
> any Markdown file across all targets.

Works on **OpenClaw, Claude Code, Cursor**, and any agent runtime that stores
per-project memory as Markdown files in a workspace directory.

**Pure file-ops. Zero network. Zero LLM. Zero pip dependencies.**

## Why

Multi-agent setups suffer from memory drift: you teach `proj-a` an API key
path, then later wonder why `proj-b` doesn't know about it. This skill lets
the calling agent push one note to every workspace at once, idempotently —
re-running the same broadcast never duplicates a section.

## Install

### Via [clawhub](https://clawhub.com)
```bash
clawhub install collective-memory
```

### Via [skills.sh](https://skills.sh)
```bash
npx skills install collective-memory
```

### Manual
```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
cp -r better-agent-skills/skills/collective-memory ~/.claude/skills/
# or wherever your agent reads skills from
```

## Quick start

Just say to your agent: **"broadcast this to all my agents"** / **"广播这条
记忆到所有 agent"** — the skill will walk you through it.

Or invoke the script directly:

```bash
# Three explicit targets
python3 <skill-install-path>/scripts/update_memory.py \
  --target ~/code/proj-a:MEMORY.md \
  --target ~/code/proj-b:MEMORY.md \
  --target ~/code/proj-c:MEMORY.md \
  --key   "API key path" \
  --content "## API key path
stored in .secrets/api-keys.env (chmod 600)"

# Auto-discover all subdirs of two parents
python3 <skill-install-path>/scripts/update_memory.py \
  --discover-under ~/.claude/projects \
  --discover-under ~/.openclaw/agents \
  --file MEMORY.md \
  --key   "API key path" \
  --content "..."

# Preview without writing
python3 <skill-install-path>/scripts/update_memory.py \
  --target ~/code/proj-a:MEMORY.md \
  --key "..." --content "..." --dry-run
```

## Trigger phrases (English / 中文)

- "broadcast memory", "tell every agent", "remember this everywhere"
- "sync this to all agents", "make all my agents know"
- 「集体记忆」「广播这条记忆」「你们全都记住」「所有agent记住」
- 「大家都记一下」「让他们都记住」

## How matching works

1. **Tokenize the `key`** — English/digit runs (single-char allowed) +
   CJK 2-gram spans → OR-match against every `##` heading in the target file.
2. **Hit** → replace that section up to the next same-or-higher level heading.
3. **Miss** → append to the end of the file.

Both branches are **idempotent**: re-running never produces duplicates.

## CLI Reference

| Flag | Repeatable | Description |
|------|-----------|-------------|
| `--workspace <path>` | no | Single workspace (legacy mode). Requires `--file`. |
| `--target <ws>:<file>` | yes | Explicit `workspace:filename` pair |
| `--discover-under <parent>` | yes | Auto-find first-level subdirs. Requires `--file`. |
| `--file <name>` | no | Default file for `--workspace` / `--discover-under` |
| `--key <text>` | no | Required. Heading lookup key. |
| `--content <markdown>` | no | Required. Full block, must include `##` heading. |
| `--dry-run` | no | Preview; no files written. |
| `--json` | no | Machine-readable result. |

Exit code: `0` = all targets OK, `1` = at least one failure.

## Files

```
collective-memory/
├── SKILL.md                          # Skill manifest (read by agents)
├── README.md                         # This file
├── LICENSE                           # MIT
└── scripts/
    └── update_memory.py              # Upsert engine
```

## Requirements

- Python 3.8+ (standard library only)

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
