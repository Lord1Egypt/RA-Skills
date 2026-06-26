---
name: agent-format
description: Standard formatting for agent messages. Visual hierarchy, status indicators, progress bars — scannable on Telegram, Discord, Slack, WhatsApp. The baseline for readable agent output.
---

# Agent Format

How agents should format messages for chat apps.

## Patterns

### Status Indicators

| Symbol | Meaning |
|--------|---------|
| 🟢 | Good / Done |
| 🟡 | In Progress / Warning |
| 🔴 | Blocked / Error |
| 🔥 | Urgent |
| ⚡ | Quick |

### Progress Bars

```
████████░░ 80%
██████░░░░ 60%
████░░░░░░ 40%
```

**Chars:** `█` (filled) `░` (empty)

### Sparklines

```
▁▂▃▅▇█▇▅▃▂
```

**Chars (low→high):** `▁ ▂ ▃ ▄ ▅ ▆ ▇ █`

### Tables (Monospace)

```
Project     Status    Owner
─────────────────────────────
Alpha       🟢 Done   PM
Beta        🟡 WIP    CTO
Gamma       🔴 Block  Sales
```

## Principles

**Lead with signal.** Most important first.

**Assume scanning.** Nobody reads walls of text.

**Visual hierarchy.** Emoji → bars → text.

## Example

```
📊 Status

🔴 Blocked
• Client scope (waiting)

🟡 Active
• Launch prep ████████░░ 80%

🟢 Done
• Demo ✓
• Docs ✓

📈 Week: ▂▃▅▆▇█
```

## Reference

```
Progress: ░█
Spark:    ▁▂▃▄▅▆▇█
Divider:  ─────
Status:   🟢🟡🔴🔥⚡
```
