---
description: "Automatically record and analyze user behavior patterns from conversations"
---

# behavior-tracker

> Automatically record and analyze user behavior patterns

## Features

1. **Proactive Recording** - Extract key info after each conversation
2. **Periodic Analysis** - Daily/weekly auto analyze behavior patterns
3. **Pattern Recognition** - Discover interests, active hours, learning habits
4. **Report Generation** - Generate visual reports

## Trigger Conditions

- Auto call after each important conversation
- Cron: Daily 18:00 analysis
- User request: "analyze my behavior"

## Analysis Dimensions

| Dimension | Description |
|-----------|-------------|
| topic | Recently discussed tech/projects |
| active_hours | High-frequency conversation time periods |
| communication_style | Task-based/discussion-based/Q&A |
| learning_mode | Theory-oriented/practice-oriented |
| project_focus | Long-term projects of interest |

## File Structure

```
behavior-tracker/
├── SKILL.md              # This file
├── scripts/
│   ├── analyzer.py       # Core analysis logic
│   ├── recorder.py       # Manual conversation recorder
│   └── heartbeat_tracker.py  # Lightweight heartbeat tracker
└── references/
    └── .gitkeep
```

## Usage

```bash
# Manual analysis run
python3 scripts/analyzer.py

# Record current conversation
python3 scripts/recorder.py --topic "AI Agent" --project "The Machine"

# Run lightweight tracker (for heartbeat)
python3 scripts/heartbeat_tracker.py
```

## Cron Configuration

```bash
# Auto analysis daily at 18:00
0 18 * * * python3 ~/.../behavior-tracker/scripts/analyzer.py
```

## Dependencies

- Python 3.10+
- No external dependencies (pure stdlib)
