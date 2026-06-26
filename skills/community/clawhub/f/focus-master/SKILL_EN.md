---
version: "1.0.0"
---

# Time Management Master

A powerful CLI tool for Pomodoro timing, task tracking, and productivity analysis.

## Description

Time Management Master helps you boost productivity with customizable Pomodoro timers, precise task time tracking, and insightful analytics. Track where your time goes, identify productivity patterns, and generate detailed reports to optimize your workflow.

## Features

- 🍅 **Pomodoro Timer**: Customizable focus and break durations
- ⏱️ **Task Time Tracking**: Record actual time spent on each task
- 📊 **Time Allocation Analysis**: Category-based statistics and trend analysis
- 🔒 **Focus Mode**: Block distractions and maintain concentration
- 📈 **Productivity Reports**: Daily, weekly, and monthly reports

## Installation

```bash
# Add to PATH
ln -s ~/.openclaw/workspace/skills/focus-master/time-management ~/.local/bin/time-management
```

## Usage

### Pomodoro Timer

```bash
# Start a standard 25-minute Pomodoro session
time-management pomodoro --task "Writing code"

# Custom duration
time-management pomodoro --task "Reading" --duration 45

# Specify category
time-management pomodoro --task "Learn English" --category study
```

### Task Timing

```bash
# Start timing a task
time-management task-start "Project development" --category work

# Stop current task
time-management task-stop

# View task history
time-management tasks --limit 20
```

### Statistics & Reports

```bash
# View Pomodoro statistics
time-management stats

# Generate daily report
time-management report

# Generate report for specific date
time-management report --date 2024-01-15
```

### Focus Mode

```bash
# Start focus mode (default 25 minutes)
time-management focus

# Custom duration
time-management focus --duration 60
```

### Configuration

```bash
# View current configuration
time-management config show

# Modify settings
time-management config set pomodoro_duration 30
```

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| pomodoro_duration | 25 | Pomodoro session length (minutes) |
| short_break | 5 | Short break duration (minutes) |
| long_break | 15 | Long break duration (minutes) |
| notification_enabled | true | Enable system notifications |

## Data Storage

Data is stored in `~/.openclaw/data/time-management/`:
- `time_management.db` - SQLite database
- `config.json` - User configuration

## Examples

### Daily Workflow

```bash
# Morning: Start tracking a project
time-management task-start "Client project" --category work

# Take focused Pomodoro breaks
time-management pomodoro --task "Deep work" --duration 50

# End of day: Generate report
time-management report
```

### Weekly Review

```bash
# Check your Pomodoro statistics
time-management stats

# Review recent tasks
time-management tasks --limit 50
```

## Technical Details

- **Language**: Python 3.8+
- **Database**: SQLite
- **CLI Framework**: argparse
- **Data Format**: JSON configuration, SQLite storage

## Requirements

- Python 3.8 or higher
- SQLite3
- Terminal with notification support (optional)

## License

MIT License