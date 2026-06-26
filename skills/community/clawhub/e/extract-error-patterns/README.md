# Extract Error Patterns

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-blue)](SKILL.md)

> Extract error patterns from server logs and generate actionable alert rules

## What Problem This Solves

Brief paragraph explaining the specific engineering problem this skill solves.
When triggered: [trigger condition].

## Features

- Transforms extract error patterns input into structured output
- Handles extract error patterns from server logs and generate acti...
- Preserves data integrity — no silent drops or fabrication

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install Extract Error Patterns

# Or manually
cp -r Extract Error Patterns ~/.openclaw/skills/
```

### Usage

```bash
# Mode 1
clawhub run Extract Error Patterns --mode read

# Mode 2
clawhub run Extract Error Patterns --mode write --input ./data.json
```

## Directory Structure

```
Extract Error Patterns/
├── SKILL.md          # Entry point
├── LICENSE           # MIT
├── README.md         # This file
├── README_zh.md      # Chinese version
├── CONTRIBUTING.md    # Contribution guide
├── .gitignore
├── references/       # Templates and schemas
│   └── ...
└── scripts/          # Helper scripts (if any)
    └── ...
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | Yes | API key for the service |

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

Powered by [MiniMax](https://minimax.io).