# 🥗 Context Diet

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**English** | **[中文](README.zh-CN.md)**

Find out why your agent feels slower and dumber than it used to. Context Diet scans everything loaded into context — system prompt, skills, memory files — measures token weight, flags redundancy, and ships a trim list with exact savings.

**4 weight zones. 1 trim list. 0 guesswork.**

**The problem:** Every skill you install injects its description into every conversation turn. Every memory note sits in context permanently. Every outdated rule in AGENTS.md still gets read. It adds up silently — until your agent is carrying 50,000 tokens of dead weight and giving foggy answers. Context Diet makes the invisible visible.

## Table of Contents

<details>
<summary>Click to expand</summary>

- [How It Works](#how-it-works)
- [The 4 Weight Zones](#the-4-weight-zones)
- [Install](#install)
- [Quick Start](#quick-start)
- [Files](#files)
- [License](#license)

</details>

## How It Works

```
AGENTS.md ──┐
SOUL.md  ──┤
skills/* ──┼──▶ Context Diet ──▶ weight report
MEMORY.md ─┤                      + trim list
memory/* ──┘                      + % savings
```

No API calls, no external tools — the agent reads its own workspace files, estimates token weight (chars ÷ 4 English, ÷ 2 CJK), and cross-references what's actually being used.

## The 4 Weight Zones

| Zone | What it weighs | Common finding |
|---|---|---|
| **1. Directives** | AGENTS.md, SOUL.md, USER.md | Duplicate rules, outdated policies |
| **2. Skills** | Every installed skill's description (permanent tax per turn) | Skills never used, eager-loaded references |
| **3. Memory** | MEMORY.md + memory/ corpus | Stale numbers, finished projects still active |
| **4. Session** | Current conversation length | Above threshold → suggest /compact |

## Install

```bash
# ClawHub
clawhub install context-diet

# Or from source
git clone https://github.com/Thomaszhou22/context-diet.git
cp -r context-diet ~/.openclaw/skills/
```

## Quick Start

Ask your agent: **"run a context diet"** — you get the full weight report with a ranked trim list in under a minute.

## Files

```
context-diet/
├── SKILL.md        # the scan (4 zones + trim list + re-verify loop)
├── README.md       # this file
└── LICENSE         # MIT
```

## License

MIT
