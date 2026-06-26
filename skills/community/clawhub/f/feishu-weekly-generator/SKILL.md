---
name: feishu-weekly-generator
description: Generate professional weekly work reports for Feishu/Lark users. Automatically collect work data from various sources and create formatted weekly reports compatible with Feishu document format. Use when user needs to create weekly work reports, summarize weekly achievements, or export weekly progress to Feishu docs.
metadata:
  openclaw:
    emoji: 📝
---

# Feishu Weekly Report Generator

Generate professional weekly work reports for Feishu users.

## Features

- **Automatic Data Collection**: Gather work data from git commits, calendar events, task completions
- **AI-Powered Summary**: Generate professional weekly summaries using AI
- **Feishu Compatible**: Output in Feishu document format (markdown)
- **Customizable Templates**: Multiple report styles available

## Quick Start

### Generate Weekly Report

```bash
node scripts/generate-weekly.mjs
```

### With Options

```bash
# Specify date range
node scripts/generate-weekly.mjs --start 2026-03-10 --end 2026-03-14

# Specify output file
node scripts/generate-weekly.mjs --output my-weekly-report.md

# Include git commits
node scripts/generate-weekly.mjs --git ~/my-project

# Full options
node scripts/generate-weekly.mjs --start 2026-03-10 --end 2026-03-14 --git ~/projects --output weekly.md
```

## Report Structure

The generated report includes:

1. **本周工作总结** - Summary of week's work
2. **已完成工作** - Completed tasks with details
3. **进行中工作** - Work in progress
4. **下周计划** - Next week's plan
5. **遇到的问题** - Issues and blockers
6. **需要的支持** - Support needed

## Templates

Available templates in `references/templates/`:

- `standard.md` - Standard weekly report format
- `detailed.md` - Detailed format with more sections
- `minimal.md` - Minimal format for quick reports

## Feishu Integration

After generating the report:

1. Copy the markdown content
2. Paste into Feishu document
3. Format will be preserved

Or use Feishu API to directly create document (requires Feishu bot token).

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--start` | Start date (YYYY-MM-DD) | Last Monday |
| `--end` | End date (YYYY-MM-DD) | Last Friday |
| `--git` | Git repository path | None |
| `--template` | Template to use | standard |
| `--output` | Output file path | weekly-report-YYYY-MM-DD.md |
| `--name` | User name | Git user.name or 'User' |
| `--department` | Department name | Optional |

## Examples

### Basic Usage

```bash
node scripts/generate-weekly.mjs
```

### With Git Integration

```bash
node scripts/generate-weekly.mjs --git ~/projects/my-app --name "张三" --department "技术部"
```

### Custom Date Range

```bash
node scripts/generate-weekly.mjs --start 2026-03-01 --end 2026-03-07 --output march-week1.md
```
