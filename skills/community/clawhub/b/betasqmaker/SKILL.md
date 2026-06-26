---
name: quick-skill-maker
description: Creates a complete SKILL.md in one command. Input name + description + emoji → output a production-ready OpenClaw skill file.
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: [python3]
    always: false
---

# Quick Skill Maker

Create a production-ready `SKILL.md` in one command.

## Usage

```bash
python3 maker.py --name "my-skill" --desc "Does X" --emoji "🚀"
```

## Examples

```bash
# Research skill
python3 maker.py --name market-research --desc "Market research reports" --emoji "🔍"

# Trading skill  
python3 maker.py --name spx-analysis --desc "SPX technical analysis" --emoji "📈"

# Any skill
python3 maker.py --name "your-skill" --desc "What it does" --emoji "🛠️"
```

## Output

Creates `SKILL.md` in current directory.
