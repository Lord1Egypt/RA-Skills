# AMLClaw 🦅

AI-powered crypto AML compliance skill for coding agents.

Screen blockchain addresses, generate compliance rules, create policy documents — out of the box.

## Install

**OpenClaw:**
```bash
clawhub install amlclaw
```

**Claude Code:**
```bash
git clone https://github.com/amlclaw/amlclaw.git .claude/skills/amlclaw
```

**Any agent framework:**
```bash
git clone https://github.com/amlclaw/amlclaw.git ./skills/amlclaw
pip install -r skills/amlclaw/requirements.txt
```

One skill. Three capabilities. Zero configuration required.

## What's Included

| Asset | Path | Description |
|-------|------|-------------|
| Skill Definition | `SKILL.md` | Agent instructions — screen, generate rules, create policies |
| Rulesets (3) | `defaults/rulesets/` | Singapore MAS, Hong Kong SFC, Dubai VARA |
| Policies (3) | `defaults/policies/` | Pre-built compliance policy documents |
| Regulations (40+) | `references/` | FATF, MAS, SFC, VARA, OFAC, UN Sanctions |
| Tag Taxonomy | `references/trustin-labels.md` | TrustIn label categories for rule authoring |
| Scripts | `scripts/` | Python screening pipeline |
| Schemas | `schema/` | JSON schemas for rules and reports |

## API

Blockchain data via TrustIn KYA API. **No API key required** — works out of the box with desensitized data.

For full unmasked data: get a free key at [trustin.info](https://trustin.info) and set `TRUSTIN_API_KEY` in `.env`.

## Open Source Ecosystem

| Project | Description |
|---------|-------------|
| **[AMLClaw Skill](https://github.com/amlclaw/amlclaw)** | This repo — AI agent skill, CLI-based, lightweight |
| **[AMLClaw Dashboard](https://github.com/amlclaw/amlclaw.com)** | Full web UI — visual flow graphs, screening history, 24/7 monitoring |

## License

MIT
