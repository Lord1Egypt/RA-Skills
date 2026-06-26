
<div align="center">

<img src="./docs/assets/banner.png" alt="Agent Memento Banner" width="100%">

# 🧠 Agent Memento

**Your AI agent forgets everything every 5 minutes. That's the point.**

A tick-driven autonomous execution framework that turns any LLM into a reliable production factory — by embracing amnesia instead of fighting it.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-Install-ff69b4.svg)](https://clawhub.com/yangwenyu2/agent-memento)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](./README.md) | [简体中文](./README_zh.md)

</div>


> Inspired by the film *Memento*: if you can't form new memories, 
> tattoo the instructions on your body.


> ⚠️ **Security & Risk Warning**:
> This skill deploys a highly privileged autonomous shell pipeline. Please read carefully before initializing:
> 1. **Arbitrary Command Execution**: The core Tick Engine (`memento_tick.sh`) strictly and autonomously executes commands defined in the `verify` field of your `MASTER_PLAN.md`. Always run this system in an isolated Virtual Machine or Sandbox environment to prevent unintended side effects.
> 2. **Automated Git Rollbacks**: On task failure, the system executes `git checkout -- .` and `git stash push -u` to revert the workspace to a clean state. **Never initialize Memento in a directory containing pre-existing valuable files or untracked manual edits**, as they may be inadvertently stashed or overwritten.
> 3. **Optional HTTP Directory Exposure**: The companion Dashboard can run a Node.js web server to statically mount and serve your entire project directory via the `/preview` endpoint (if started with `--enable-preview`). **Do not place API keys, secrets, or sensitive private files in the project directory**.



## The Problem

Every AI coding agent hits the same wall:

| Without Memento | With Memento |
|----------------|--------------|
| 🧠 "I'll remember the whole project" | 📋 "I'll read the blueprint fresh each time" |
| 💀 OOM at 2000 lines | ✅ Built a 15,000-line app overnight |
| 🎭 Hallucinates after 30 min | 🔬 Every change verified by real tests |
| 🔄 Rewrites your files from scratch | 🔪 Surgical edits only, always |

## How It Works

![Agent Memento Architecture](docs/assets/architecture.png)


1. **You** describe what you want in natural language
2. **The Architect** (your main AI session) breaks it into a checklist
3. **Tick Workers** wake up every 5 minutes via cron, pick the next `[ ]`, do the work, run tests, and check it off `[x]`
4. If stuck → flag it `[!]` → Architect adjusts → loop continues
5. You check the Dashboard when you feel like it. Or don't.


## Key Features

*   **⚡️ Tick-Driven Architecture**: Runs autonomously in the background via `cron` or a loop script. It spins up short-lived, pinpoint-accurate Tick Workers to perform atomic tasks.
*   **🛡️ Iron Discipline & Fallback**: Each worker is forced to run a `verify` command after modifying code. If it returns anything other than `Exit 0`, the system triggers an aggressive 3-phase git rollback (checkout, clean, stash) to guarantee no dirty code ever pollutes the main branch.
*   **🎨 Staff-Level Craftsmanship Profile**: Tick Workers are injected with a high-standard Persona prompt demanding elegant UI/UX, responsive design, animations, and robust asset handling. No more ugly, raw "gray box" Proof-of-Concept outputs.
*   **📺 Holographic Mission Dashboard**: A Node.js web monitor to track your AI's building process.
    *   **▶ Live Preview**: Instantly mounts your HTML5/Web project directory so you can test and play the generated app *while* the AI is coding it.
    *   **📊 Robust Progress Sync**: A progress bar heavily fortified by Regex that accurately parses the `[x]` checks in the real markdown file.
    *   **💬 Read-Only Observer Console**: Talk to the dashboard Architect to get an instant summary of the project without risking jailbreaks or unprompted codebase edits.
*   **🌏 Native Bilingual**: Seamlessly adapts to English or Chinese (or any language) based purely on your `MASTER_PLAN.md` context.

## Quick Start (30 Seconds)

1. Initialize project scaffolding:
   ```bash
   bash skills/agent-memento/scripts/init_memento.sh MyProject
   ```

2. Have your Architect (main session LLM) draft the `MASTER_PLAN.md` and `PROJECT_MAP.md`

3. Wire it to crontab:
   ```bash
   crontab -e
   # Add: */5 * * * * /path/to/MyProject/scripts/memento_tick.sh
   ```

4. Monitor via real-time Mission Control Dashboard:
   ```bash
   bash skills/agent-memento/scripts/dashboard.sh
   ```

## How is this different?

| Feature | Agent Memento | AutoGPT / CrewAI | Cursor / Copilot | Devin |
|---|---|---|---|---|
| Memory model | Stateless ticks | In-memory loop | Session context | Persistent agent |
| Fails at scale? | No (by design) | Yes (OOM/drift) | Yes (context limit) | Unclear |
| Verification | Mandatory per task | Optional | None | Internal |
| Human oversight | Async dashboard | Real-time babysitting | Inline | Web UI |
| Runs overnight? | ✅ | ❌ | ❌ | ✅ |
| Fully local? | ✅ | ❌ | ❌ | ❌ |

## Philosophy

> "The best AI system is one that assumes it will forget everything, and builds the world around that assumption."

Agent Memento doesn't make AI smarter. It makes AI *reliable* — by giving it a notebook it can't lose, a checklist it must follow, and a reset switch every 5 minutes.

## Documentation
- See [SKILL.md](./SKILL.md) for full technical architecture and execution rules.
- Contains Node/Express based real-time monitoring WebUI hooks (`/dashboard`).

