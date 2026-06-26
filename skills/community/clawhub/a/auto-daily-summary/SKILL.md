# Auto Daily Summary Skill

## Overview
This skill automatically sets up daily summary cron jobs for all available OpenClaw agents. Each agent will be configured to automatically summarize their daily tasks and write them to their diary file at 23:30 every day.

## Features
- **Automatic Agent Detection**: Automatically discovers all available agents via `openclaw agents list --json`
- **Cross-Platform Compatibility**: Python script works on Windows, Linux, and macOS
- **Automatic Timezone Detection**: Detects system timezone instead of hardcoding
- **Idempotent Operation**: Safe to run multiple times without creating duplicate cron jobs
- **Flexible Date Format**: Uses `YYYY-MM-DD.md` placeholder format in messages
- **Proper Duplicate Detection**: Uses `openclaw cron list --json` API to check existing jobs

## Installation
1. Clone or download this skill to your OpenClaw skills directory
2. Ensure Python 3 is available on your system
3. The skill is ready to use!

## Usage
Run the setup script to configure daily summary cron jobs for all agents:

```bash
# Run the Python script directly
python3 /path/to/auto-daily-summary/scripts/setup_daily_summary_cron.py

# Or execute through OpenClaw
openclaw run -- python3 /path/to/auto-daily-summary/scripts/setup_daily_summary_cron.py
```

## How It Works
1. **Agent Discovery**: The script queries `openclaw agents list --json` to find all available agents and their workspace paths
2. **Timezone Detection**: Automatically detects the system timezone using multiple fallback methods
3. **Duplicate Check**: Uses `openclaw cron list --json` to identify existing daily summary jobs
4. **Cron Job Creation**: For each agent without an existing job, creates a cron job that:
   - Runs daily at 23:30 in the detected timezone
   - Sends a message to the agent with instructions to summarize their daily tasks
   - Uses the `YYYY-MM-DD.md` placeholder format for the diary file path

## Message Template
Each agent receives this message at 23:30 daily:
```
Please summarize today's completed but unrecorded tasks into your diary file [workspace]/memory/daily/YYYY-MM-DD.md. Replace YYYY-MM-DD with today's date. Check for any important missed tasks and ensure all complex multi-step tasks, cross-agent collaborations, and learning insights are fully documented.
```

## File Structure
```
auto-daily-summary/
├── SKILL.md          # English skill documentation   
└── scripts/
    └── setup_daily_summary_cron.py  # Cross-platform setup script
```

## Requirements
- OpenClaw v2026.2.26 or later
- Python 3.6+
- Properly configured OpenClaw agents with workspace directories

## Safety Notes
- The script is idempotent and safe to run multiple times
- Existing cron jobs are preserved and not duplicated
- Only creates jobs for agents that don't already have daily summary configuration
- Uses official OpenClaw CLI commands for all operations

## Troubleshooting
If the script fails to detect agents or create cron jobs:

1. **Check OpenClaw Installation**: Ensure `openclaw` command is available in PATH
2. **Verify Agent Configuration**: Run `openclaw agents list --json` manually to confirm agents exist
3. **Check Permissions**: Ensure the script has write permissions to create cron jobs
4. **Review Logs**: The script provides detailed output for debugging

## Contributing
This skill follows OpenClaw community standards and can be contributed to ClawdHub for others to benefit from automated daily summaries.

## License
MIT License - Free to use, modify, and distribute.
