---
name: feishu-candy
description: Convert ICS (iCalendar) files to JSON for Feishu calendar integration. Use when user needs to import calendar events from ICS format, export Feishu calendar to JSON, or process calendar files for Feishu calendar apps. Triggers on: ICS to JSON conversion, calendar file parsing, Feishu calendar data transformation.
---

# Feishu Calendar Candy

Convert ICS calendar files to JSON format for Feishu calendar integration.

## requirement

install vdirsyncer and setup calendar sync

## Quick Start

Run the conversion script:

```bash
python scripts/ics2json.py <input_directory> [-o output.json] [--split]
```

## Arguments

- `input_dir` - Directory containing .ics files (required)
- `-o, --output` - Output JSON file (default: output.json)
- `--split` - Output one JSON per ICS file instead of merging

## Examples

**Merge all ICS files into one JSON:**
```bash
python scripts/ics2json.py ./calendars -o events.json
```

**Split each ICS into separate JSON:**
```bash
python scripts/ics2json.py ./calendars --split
```

## Output Format

Each event contains:
- `uid` - Unique event identifier
- `summary` - Event title
- `status` - Event status
- `organizer` - Organizer info
- `start` - Start time (ISO format)
- `end` - End time (ISO format)
- `alarms` - List of reminders/triggers
