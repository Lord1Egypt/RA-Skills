---
name: log-analyzer
description: Analyze log files to extract insights, errors, and patterns. Use when user needs to debug application errors, find patterns in server logs, analyze access logs, extract metrics from log files, or create log summaries.
---

# Log Analyzer

Analyze log files to extract insights, errors, and patterns.

## Quick Start

```bash
# Analyze a log file
python scripts/analyze.py /var/log/app.log

# Find errors
python scripts/analyze.py /var/log/app.log --errors

# Generate summary
python scripts/analyze.py /var/log/app.log --summary
```

## Usage

```bash
python scripts/analyze.py LOG_FILE [OPTIONS]

Options:
  --errors         Show only error lines
  --warnings       Show warning lines
  --pattern REGEX  Search for pattern
  --summary        Show summary statistics
  --json           Output as JSON
  --lines NUM      Number of lines to show
```

## Examples

```bash
# Find all errors
python scripts/analyze.py app.log --errors

# Search for specific pattern
python scripts/analyze.py app.log --pattern "user_id=.*"

# Get summary
python scripts/analyze.py access.log --summary

# Output JSON
python scripts/analyze.py app.log --json --output analysis.json
```

## Log Formats Supported

- Apache/Nginx access logs
- Application logs (timestamp + level + message)
- JSON logs
- Syslog format

## Features

- Error/warning extraction
- Pattern matching with regex
- Statistical summaries
- JSON output
- Timestamp parsing
