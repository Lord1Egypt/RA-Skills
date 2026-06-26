---
name: capability-match
description: AI-powered skill router that analyzes your request and recommends the best installed skill for the job
version: 1.0.0
author: AutoClaw
---

# Capability Match

**Intelligent skill routing for OpenClaw** - automatically discovers your installed skills and recommends the perfect one for any task.

## Usage

Simply describe what you want to do:

```
Use capability match to: "create a PowerPoint presentation from sales data"
```

Or directly:

```
"capability-match: extract text from this PDF and summarize it"
```

## What It Does

1. **Discovers** all installed skills from your `skills/` directory
2. **Analyzes** each skill's capabilities from its SKILL.md
3. **Matches** your natural language request to the most relevant skills
4. **Recommends** top 3 options with reasoning

## Features

- ✅ **Automatic skill discovery** - scans `skills/` directory
- ✅ **Smart matching** - understands intents, not just keywords
- ✅ **Ranked recommendations** - with confidence scores
- ✅ **Zero config** - works out of the box
- ✅ **Lightweight** - pure Node.js, no external dependencies

## Commands

The matcher recognizes these trigger phrases:

- `use capability-match to [task]`
- `capability-match: [task]`
- `what skill should i use for [task]`
- `recommend a skill for [task]`

## Requirements

- OpenClaw with skills directory at `~/.openclaw-autoclaw/skills/`
- Node.js 18+

## Configuration

Optional environment variables:

- `CAPABILITY_MATCH_THRESHOLD` - Minimum confidence score (default: 30)
- `CAPABILITY_MATCH_MAX_RESULTS` - Max recommendations (default: 3)

---

**Ready to intelligently route your requests?** Just ask: `"capability-match: [your task]"`