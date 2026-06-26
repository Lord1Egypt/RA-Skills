# actual CLI Skill (OpenClaw variant)

A feature-complete AI companion for the [actual CLI](https://cli.actual.ai),
an ADR-powered CLAUDE.md/AGENTS.md generator.

This is the **OpenClaw/ClawdHub variant** of the skill. It includes an
ADR Pre-Check section that nudges agents to check for existing ADR context
before creating new skills or components.

For the standard variant (Claude Code marketplace, Codex, manual installs),
see [actual-software/actual-skill](https://github.com/actual-software/actual-skill).

## What it does

- Runs and troubleshoots `actual adr-bot` with pre-flight → dry-run → execute → diagnose → retry
- Covers all 5 runners (claude-cli, anthropic-api, openai-api, codex-cli, cursor-cli)
- Covers all 3 output formats (claude-md, agents-md, cursor-rules)
- Includes error catalog, config reference, runner guide, and diagnostic script
- ADR Pre-Check: checks for ADR context before creating new work (OpenClaw-specific)

## Install

### ClawdHub (recommended)

```bash
clawhub install actual
```

### Manual

Clone and copy the SKILL.md + supporting files into your skills directory:

```bash
git clone https://github.com/actual-software/actual-skill-openclaw.git ~/.local/share/actual-skill-openclaw

# Copy to your agent's skills directory
cp -r ~/.local/share/actual-skill-openclaw ~/.claude/skills/actual
```

## Requirements

- The [actual CLI](https://cli.actual.ai) installed
  (`npm install -g @actualai/actual` or `brew install actual-software/actual/actual`)
- At least one runner configured (see `actual runners`)

## License

MIT-0
