---
name: skill-maker
description: Creates production-ready SKILL.md files for OpenClaw AI agents. Takes a skill concept and outputs a complete, publishable SKILL.md with metadata, instructions, and examples.
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins:
        - python3
        - markdown
    always: false
---

# Skill Maker

Creates complete, production-ready `SKILL.md` files for OpenClaw agents. Perfect for publishing on ClawHub or ugig.net.

## Usage

```bash
python3 skill_maker.py --name "my-skill" --desc "Does X" --output ./my-skill/
```

## What it generates

- `SKILL.md` — full skill file with frontmatter, instructions, examples
- `references/` — reference docs if applicable
- `README.md` — quick start guide

## Input options

| Flag | Description |
|------|-------------|
| `--name` | Skill name (lowercase, URL-safe) |
| `--desc` | Short description (<50 chars) |
| `--output` | Output directory |
| `--category` | Category: productivity/trading/research/automation |
| `--emoji` | Emoji icon |

## Output structure

```
{skill-name}/
├── SKILL.md          # Main skill file
├── references/       # Supporting docs
│   └── overview.md   # Feature breakdown
└── README.md         # Quick start
```

## Example

```bash
python3 skill_maker.py \
  --name "market-brief" \
  --desc "Generates hourly market briefings" \
  --category trading \
  --emoji "📊" \
  --output ./market-brief/
```

## Notes

- All metadata (env/bins) must match actual code references
- No obfuscated shell commands allowed
- Single bundle ≤ 50MB
- MIT-0 license by default
