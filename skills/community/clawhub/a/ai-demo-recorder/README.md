# screencli-skill

Skill package for [screencli](https://screencli.sh) — AI-driven screen recording from the terminal.

## Install

```bash
npx skills add usefulagents/screencli-skill
```

This installs the skill into your AI coding agent (Claude Code, Cursor, Windsurf, Cline, etc.), enabling it to record polished browser demos on your behalf.

## What it does

One command records an AI-driven browser session with gradient backgrounds, auto-zoom, click highlights, and cursor trails — then uploads to a shareable link.

```bash
npx screencli record https://example.com -p "Click Sign Up, fill in the form, and submit"
```

## Requirements

- Node.js 18+
- FFmpeg

## License

MIT
