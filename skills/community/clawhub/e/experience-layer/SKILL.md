---
name: experience-layer
description: Skill Experience Layer - A failure-driven learning mechanism for OpenClaw agents that automatically accumulates lessons and best practices to avoid repeating mistakes.
author: jilanfang
license: MIT
tags: [experience, learning, memory, best-practices, failure]
version: 1.0.2
---

# Skill Experience Layer for OpenClaw

A **failure-driven learning mechanism** that systematically accumulates experience from tool calls, mistakes, and successes. Each tool/skill category has its own experience file with:

- Lessons learned from failures
- Common mistakes pattern matching
- Preventive best practices
- Statistics tracking (total executions, success/failure counts)

## Core Philosophy

> "The man who repeats the same mistake and expects different results is a fool." - This mechanism eliminates that.

**Every failure is a one-time tuition payment for permanent knowledge.**

## How It Works

### 1. Pre-execution Experience Loading
Before any tool call, the agent must:
1. Identify the experience category
2. Read the compact experience file
3. Apply learned best practices
4. Avoid known mistakes

### 2. Post-execution Experience Update
If the tool call **fails**:
1. Stop immediately and analyze root cause
2. Add/Update the experience entry
3. Record the mistake and prevention
4. Continue only after updating

If the tool call **succeeds**:
1. Optionally add high-value best practices
2. Keep experience lean and actionable

### 3. Weekly/Monthly Maintenance
- Weekly: Remove outdated experiences
- Monthly: Clean up duplicates, consolidate patterns

## Experience Category Structure

```json
{
  "type": "skill",
  "name": "tool-name",
  "lastUpdated": "ISO timestamp",
  "totalExecutions": N,
  "successCount": N,
  "failureCount": N,
  "experiences": [
    {
      "mistake": "Description of what went wrong",
      "when": "Context/scenario where it happens",
      "avoidance": "How to avoid this mistake",
      "count": 1
    }
  ],
  "patterns": {
    "commonMistakes": [
      "List of frequent mistakes"
    ],
    "bestPractices": [
      "List of proven best practices"
    ]
  }
}
```

## Built-in Categories

| Category | Description |
|----------|-------------|
| `read` | File reading, web fetching |
| `write` | File writing, editing |
| `edit` | Exact text replacement in files |
| `exec` | Shell command execution |
| `browser` | Browser automation |
| `message` | Message sending, media upload |
| `search` | Web search tools |
| `feishu` | All Feishu/Lark API tools |
| `feishu-*` | Fine-grained Feishu sub-skill experiences |
| `memory` | Memory search and retrieval |
| `skill` | Skill management operations |
| `cron` | Cron job scheduling and delivery modes |
| `video-frames` | Video frame extraction with ffmpeg |

## Installation

```bash
clawhub install experience-layer
```

Or manually:

```bash
mkdir -p ~/.openclaw/workspace/memory/experiences
# Copy the empty category template to start
cp templates/empty-category.json ~/.openclaw/workspace/memory/experiences/your-category.json
# Edit the JSON and add your first experience
```

## What's Included

- `SKILL.md` - Complete documentation
- `templates/empty-category.json` - Starter template for new categories
- `templates/example.json` - Real-world example from production usage
- `examples/` - Full production-ready experience files:
  - `examples/edit.json` - Experience for file editing
  - `examples/exec.json` - Experience for shell command execution
  - `examples/feishu.json` - Experience for Feishu/Lark API
  - `examples/message.json` - Experience for message sending
  - `examples/cron.json` - Experience for cron job scheduling

## Usage in OpenClaw Workflow

1. **Before calling a tool**:
```javascript
read memory/experiences/{category}.json
apply the best practices and avoid the common mistakes
```

2. **After failure**:
```javascript
analyze root cause
update the corresponding experience file
record the lesson learned
then retry
```

## Benefits

- **No repeated mistakes** - Same mistake only pays tuition once
- **Progressive improvement** - System gets better over time
- **Compact and searchable** - JSON format for easy semantic search
- **Low overhead** - Small files, quick to load
- **Open extension** - Add new categories as needed

## Changelog

### 1.0.2 (2026-03-18)
- Add `examples/` directory with full production experience files
- Include 5 complete real-world experience JSON: edit, exec, feishu, message, cron
- Users can drop these directly into their `memory/experiences/` to start

### 1.0.1 (2026-03-18)
- Add template directory with empty category template
- Add complete example JSON from production
- Improve installation documentation

### 1.0.0 (2026-03-18)
- Initial public release
- 25+ experience categories with real-world lessons from production usage
- Complete JSON schema
- Documentation

## Author

jilanfang

## License

MIT
