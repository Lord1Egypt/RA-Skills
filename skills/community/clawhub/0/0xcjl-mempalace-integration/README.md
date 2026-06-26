# mempalace-integration

> MemPalace memory system integration - AAAK compression + Hall classification + L0-L3 layering

[中文](./README_zh.md)

## Overview

Integrates MemPalace's core concepts into your AI agent system:
- **AAAK Compression**: 30x lossless compression
- **Hall Classification**: facts/events/discoveries/preferences/advice
- **L0-L3 Layering**: loading priority for memory

## Core Concepts

### AAAK Compression
30x lossless compression for AI memory.

**Format**: `KEY: VALUE | KEY2: VALUE2`

**Example** (30x compression):
```
Original: ~1000 tokens
Compressed: ~33 tokens
```

### Hall Classification

| Hall | Content |
|------|--------|
| hall_facts | Decisions, choices |
| hall_events | Sessions, milestones |
| hall_discoveries | New insights |
| hall_preferences | Habits, preferences |
| hall_advice | Recommendations |

### L0-L3 Layering

| Layer | Content | Loading |
|-------|--------|--------|
| L0 | Identity (~50) | Always |
| L1 | Key facts (~120) | Always |
| L2 | Recent sessions | On-demand |
| L3 | Deep search | On-demand |

## Retrieval Performance

- Wing + Room: **94.8%** (R@10)
- Wing + Hall: 84.8%
- Wing only: 73.1%

## Usage

1. Compress original content
2. Classify into Hall
3. Load by L0-L3 priority

## Installation

### Hermes Agent
```bash
# Clone to skills directory
git clone https://github.com/0xcjl/mempalace-integration.git ~/.hermes/skills/mempalace-integration
```

### Claude Code / OpenClaw
```bash
git clone https://github.com/0xcjl/mempalace-integration.git ~/.claude/skills/mempalace-integration
```

## Credits

- **Source**: [MemPalace](https://github.com/milla-jovovich/mempalace)
- **Integration**: [0xcjl](https://github.com/0xcjl)

## License

MIT
