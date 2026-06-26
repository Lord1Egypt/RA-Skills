# Meeting Minutes

Automatically organize meeting records and archive them intelligently.

## Features

- **Auto Scan**: Identify newly added meeting record files for the day
- **Smart Merge**: Automatically merge related meetings based on time, topic, and participants
- **Info Extraction**: Automatically extract participants, core topics, key decisions, and action items
- **Categorized Archive**: Support custom categories and automatic archiving to corresponding directories

## Trigger

Type `/纪要` to trigger.

## First Time Use

On first launch, you will be asked whether to categorize meeting archives:
- **No Category**: All minutes go to `meetings/` root directory
- **Default Categories**: Project Meetings / Department Meetings / External Meetings / Others
- **Custom Categories**: Enter your own category names

## Supported Meeting Record Format

By default scans `.txt` files in `./会议记录/` or `~/Documents/会议记录/`:

```
MM-DD MeetingType_ MeetingTopic.txt
```

Examples:
```
03-16 InternalMeeting_ ProductPlanning.txt
03-16 ClientMeeting_ PartnershipDiscussion.txt
```

## Output Format

Generates standard Markdown format meeting minutes:

```markdown
# Meeting Minutes: Product Planning

## Basic Info
- **Date**: 2026-03-16
- **Time**: 14:00 - 15:30
- **Type**: Internal Meeting
- **Participants**: Alice, Bob, Charlie
...
```

## Archive Rules

File naming format: `YYYYMMDD_{category_abbr}_{topic}.md`

Category abbreviations:
- Project Meetings → `proj`
- Department Meetings → `dept`
- External Meetings → `ext`
- Others → `misc`

Archive paths:
- With category: `./memory/meetings/{category}/`
- Without category: `./memory/meetings/`

## Merge Rules

Multiple meeting records will be merged into one meeting minutes when all conditions are met:
1. File creation time difference < 15 minutes
2. File name similarity > 70%
3. Specific person names (excluding "Speaker 1/2/3") overlap > 2/3

## Installation

```bash
clawhub install meeting-minutes
```

## Requirements

- OpenClaw environment
- Meeting record text files exported from DingTalk or Feishu

## License

MIT
