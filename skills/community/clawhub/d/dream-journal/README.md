# dream-journal

An OpenClaw skill for recording and interpreting dreams in Chinese.

## Features

- **Record dreams** — Describe a dream and have it structured, tagged, and saved locally
- **Interpret dreams** — Analyze dream symbols, emotional tone, and potential connections to waking life
- **Query history** — Search past dreams by date range or keyword

## Install

Place the `dream-journal/` folder inside your OpenClaw workspace `skills/` directory:

```
~/.openclaw/workspace/skills/dream-journal/
```

OpenClaw will automatically detect and load the skill.

## Usage

Trigger phrases (Chinese):
- `/记录梦` or describe a dream → records and structures the dream
- `/解梦` or "帮我解析这个梦" → interprets the dream
- "我最近梦过什么" / "查梦境记录" → lists recent dreams

## Storage

Dreams are saved to `~/.openclaw/memory/dreams/` as Markdown files:

```
2026-03-14-001.md
2026-03-14-002.md
...
```

Each file contains frontmatter (date, title, tags) plus the raw and structured dream narrative.

## Requirements

- Python 3.8+
- OpenClaw

## License

MIT
