# Analyze Json Data

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-blue)](SKILL.md)

> Analyze JSON data and generate a structured API design document or OpenAPI specification

## What Problem This Solves

Brief paragraph explaining the specific engineering problem this skill solves.
When triggered: [trigger condition].

## Features

- Transforms analyze json data input into structured output
- Handles analyze json data and generate a structured api design do...
- Preserves data integrity — no silent drops or fabrication

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install Analyze Json Data

# Or manually
cp -r Analyze Json Data ~/.openclaw/skills/
```

### Usage

```bash
# Mode 1
clawhub run Analyze Json Data --mode read

# Mode 2
clawhub run Analyze Json Data --mode write --input ./data.json
```

## Directory Structure

```
Analyze Json Data/
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