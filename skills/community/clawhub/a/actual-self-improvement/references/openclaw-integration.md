# OpenClaw integration

OpenClaw can make this skill more powerful because it already has workspace-level memory files and optional hooks.

## Suggested workspace layout

```text
~/.openclaw/
├── workspace/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── MEMORY.md
│   └── .learnings/
│       ├── LEARNINGS.md
│       ├── ERRORS.md
│       └── FEATURE_REQUESTS.md
├── skills/
│   └── self-improvement/
└── hooks/
    └── self-improvement/
```

## Recommended split

- keep incident details in `.learnings/`
- promote stable workflow rules to `AGENTS.md`
- promote behavioural rules to `SOUL.md`
- promote tool gotchas to `TOOLS.md`

## Why this works well

OpenClaw already distinguishes between transient task work and durable context. This skill adds a disciplined loop for deciding what should graduate from one-off troubleshooting into shared memory.

## Hook bundle

The optional OpenClaw hook lives in `hooks/openclaw/`.

Suggested use:
1. install the skill in your OpenClaw skills directory
2. copy `hooks/openclaw/` into your OpenClaw hooks directory if desired
3. enable the hook in OpenClaw
4. keep `.learnings/` in the workspace root, not the skill directory

## Promotion examples

### To `TOOLS.md`

```markdown
## GitHub CLI
- Check `gh auth status` before assuming push or PR automation will work.
```

### To `AGENTS.md`

```markdown
## After OpenAPI changes
1. Regenerate the API client
2. Run type-checking
3. Re-run contract-sensitive tests
```

### To `SOUL.md`

```markdown
## Correction behaviour
- Admit wrong assumptions quickly and replace them with the corrected fact.
```
