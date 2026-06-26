# founderclaw development

## Commands

```bash
bun install              # install dependencies
bun test                 # run free tests
bun run build            # gen docs + compile binaries
bun run gen:skill-docs   # regenerate SKILL.md files from templates
bun run skill:check      # health dashboard for all skills
bun run dev:skill        # watch mode: auto-regen + validate on change
```

## Install

```bash
# Symlink skills to OpenClaw
cd founderclaw
for d in */; do
  [ -f "$d/SKILL.md" ] && ln -sf "$(pwd)/${d%/}" ~/.agents/skills/"${d%/}"
done

# Build browse binary
cd browse && bun install && bun build src/cli.ts --compile --outfile dist/browse
```

## Testing

```bash
bun test             # run before every commit — free, <2s
```

## Architecture

```
founderclaw/
├── ceo/                    ← CEO agent (SOUL.md, AGENTS.md, etc.)
├── projects/               ← shared project workspace
├── strategy-dept/          ← department desks
├── shipping-dept/
├── testing-dept/
├── security-dept/
├── history-dept/
├── company/                ← shared config
├── skills/                 ← 29 founderclaw skills
├── bin/                    ← CLI tools
├── scripts/                ← build scripts
├── lib/                    ← shared libraries
├── extension/              ← Chrome extension
├── docs/                   ← design docs
├── ETHOS.md                ← builder philosophy
├── AGENTS.md               ← master instructions
├── ARCHITECTURE.md         ← system design
├── DESIGN.md               ← design system reference
├── CONTRIBUTING.md         ← how to contribute
├── TODOS.md                ← project TODOs
├── VERSION                 ← version
└── package.json            ← dependencies
```

## Skill Generation

Skills use templates (`SKILL.md.tmpl`). To regenerate:

```bash
bun run gen:skill-docs
```

This reads each skill's `SKILL.md.tmpl` and generates `SKILL.md` with the
correct frontmatter, voice section, and preamble.

## Models

FounderClaw uses 3 model tiers (user picks at install):

| Tier | Use | Example |
|---|---|---|
| Fast | Quick tasks, mechanical work | haiku, gpt-4o-mini |
| Best | Strategy, deep thinking | claude-opus, gpt-4 |
| Vision | Image analysis | mimo-v2-omni, gpt-4o |

## Tool Policy

Each department has different tool access. See `docs/founderclaw-design.md` for
the full tool policy matrix.
