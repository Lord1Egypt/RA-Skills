# BeHuman for Claude Code

## Installation

Copy `behuman.md` to your project's `.claude/commands/` directory:

```bash
mkdir -p .claude/commands
cp behuman.md .claude/commands/
```

## Usage

In Claude Code, type:

```
/behuman 分手了，很难过
/behuman 帮我写一段自我介绍
/behuman 要不要辞职去创业
```

Or set it as a project-level instruction by adding to `.claude/settings.json`:

```json
{
  "instructions": "Follow the BeHuman Self-Mirror protocol for all emotionally charged, advice, or writing tasks. See .claude/commands/behuman.md"
}
```

## How It Works

BeHuman adds inner dialogue to AI responses:

1. **Self** — AI's first instinct (usually robotic)
2. **Mirror** — Reflects Self's blind spots (filler, lists, fake empathy)
3. **Conscious Response** — What a real human would say

The Mirror doesn't judge or correct — it **reflects**. Like looking in a mirror and seeing your own habits.
