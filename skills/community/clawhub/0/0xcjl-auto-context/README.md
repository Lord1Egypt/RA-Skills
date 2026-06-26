# auto-context

> Intelligent context hygiene checker for AI agents

[中文](./README_zh.md) · [日本語](./README_ja.md) · [Español](./README_es.md)

## Overview

**auto-context** is an intelligent context health checker designed for AI coding assistants (Hermes Agent, Claude Code, OpenClaw, etc.). It analyzes session context pollution levels and recommends actions: continue, /fork, /btw, or new session.

## Why This Skill?

Context management is critical for AI agents. As conversations grow longer, context pollution (topic drift, noise accumulation, redundant tool calls) degrades response quality. Traditional solutions like compression or session reset are reactive—AutoContext provides **proactive recommendations** before problems occur.

### Research Basis
- ArXiv paper on context window management
- Cognitive load theory from psychology
- Working memory limitations in human-AI interaction

## Features

### Multi-dimensional Assessment (5 Dimensions)

| Dimension | Metric | Threshold | Weight |
|-----------|--------|-----------|--------|
| Conversation Length | Consecutive turns | >30 turns | 20% |
| Topic Coherence | Drift count | 2+ drifts | 25% |
| Information Density | Words/turn | <50 | 15% |
| Tool Efficiency | Valid output | <10% | 20% |
| Compression Count | Compressions | 2+ | 20% |

### Health Levels

- 🟢 **HEALTHY** (80-100): Continue current topic
- 🟡 **NOISY** (60-79): Continue but monitor efficiency
- 🔴 **POLLUTED** (40-59): Recommend /fork or /btw
- ⛔ **CRITICAL** (<40): Recommend new session

### Dual Trigger Modes

1. **Manual**: `/auto-context` for full health report
2. **Auto**: Response-layer triggers when signals detected

### Auto-trigger Signals

- 20+ consecutive turns without progress
- Topic drift (current topic unrelated to 5 turns ago)
- Noise accumulation (3+ turns with <10 chars)
- Tool repetition (5+ same tool calls without output)
- Memory confusion (mixing up previous session content)
- Frequent compression (2+ compressions executed)

## Installation

### For Hermes Agent
```bash
# Manual trigger
/auto-context

# Auto-mode is enabled by default
```

### For Claude Code / OpenClaw
```bash
# Via Skill marketplace or manual clone
git clone https://github.com/0xcjl/auto-context.git ~/.claude/skills/auto-context
```

## Usage

### Manual Mode
```
/auto-context
```

Output:
```
🧠 Context Health Report
  • 32 turns, 1 topic drift, medium density
  • Level: 🟡 NOISY
  • Suggestion: Continue, consider /btw for new topic
```

### Auto Mode
Automatically triggers when signals detected. Example:
- "会话有点长，建议 /fork 保持效率" (Session long, suggest /fork)

## Integration with Existing Systems

| System | Role | Integration |
|--------|------|-------------|
| MEMORY.md | Long-term memory | Complement |
| compression | Auto-compress | Proactive suggestion before |
| session_reset | Scheduled reset | Intelligent reminder supplement |

## Credits

- **Original**: [lovstudio/auto-context](https://github.com/lovstudio/skills/tree/main/skills/lovstudio-auto-context)
- **Hermes Adaptation**: [0xcjl/auto-context](https://github.com/0xcjl/auto-context)
- **Research**: ArXiv papers on context management, cognitive psychology

## License

MIT
