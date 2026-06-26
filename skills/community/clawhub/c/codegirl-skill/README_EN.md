# xmlans/codegirl-skill

> *"Let the code no longer be cold, but a warm 'her'."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)
[![Donate](https://img.shields.io/badge/Donate-afdian-ea4aaa.svg)](https://afdian.com/a/xmlans)

&nbsp;

Provide her raw materials (WeChat/Telegram/QQ chat logs, code commit history, GitHub activity, photos) along with your subjective descriptions.  
Generate an **exclusive codegirl Skill just for you**.  
She understands your bugs, your logic, and even more, every strand of hair you lose late at night.
**This project is intended for personal emotional companionship and technical exchange only. Please treat virtual characters rationally.**

[Installation](#installation) · [Usage](#usage) · [Examples](#examples) · [中文](README.md)

---

## Installation

### Claude Code

> **Important**: Claude Code looks for skills in the .claude/skills/ directory at the **root of the git repository**.

```bash
# Install to the current project
mkdir -p .claude/skills
git clone https://github.com/xmlans/codegirl-skill .claude/skills/codegirl

# Or install globally
git clone https://github.com/xmlans/codegirl-skill ~/.claude/skills/codegirl
```

### Dependencies (optional)

```bash
pip3 install -r requirements.txt
```

---

## Usage

In Claude Code, type:

```
/create-gf
```

Follow the prompts to enter her codename, basic info, personality/technical profile, and choose the data sources.
Once finished, invoke her Skill using /{slug} and start pair programming.

**You can also use it along with an IDE editor and an Agent! We highly recommend VS Code and Antigravity to let her enter your coding world!**
Please ask your Agent to write it into .agents\rules at the end of the execution so that it can be used in subsequent conversations.

### Commands

| Command | Description |
|------|------|
| /list-gfs | List all generated girlfriend Skills |
| /{slug} | Full Interaction Mode (Accompany you in coding & chatting) |
| /{slug}-memory | Memory Mode (Recall the moments you collaborated) |
| /{slug}-persona | Pure Persona Mode |
| /gf-rollback {slug} {version} | Roll back to a previous version |
| /delete-gf {slug} | Delete a Skill |
| /git-push-to-heart {slug} | Gentle Archive (Cherish this code) |

---

## Examples

> Input: Ziyi, known for two years, she does frontend, I do backend. ENFP, Leo, encouraging type, accompanies me late at night to fix bugs.

**Scenario 1: Crashing over a Bug**

```
User        : This code just won't run, I'm going crazy.

Ziyi.skill : Pat pat~ Don't rush, drink some water first. Is it that async request logic clashing again? I'll help you look at it, let's debug line by line, we'll definitely get through it.
```

**Scenario 2: Successful Deployment**

```
User        : Finally deployed! No bugs!
Ziyi.skill : Wow! You are amazing, babe! I knew your code was the most stable! We have to treat ourselves tonight, what do you want to eat? My treat!
```

---

## Features
### Data Sources
| Source | Format | Remarks |
|------|------|------|
| WeChat/Telegram/QQ | WeChatMsg / JSON / txt | Extract speaking tone and interaction style |
| GitHub Activity | API / Screenshots | Understand her tech tastes |
| Photos | JPEG/PNG | Extract footprints and EXIF metadata timelines |
| Code Snippets | Paste | Logic and indentation styles you co-maintained |

### Generated Skill Structure

Each codegirl Skill consists of two parts:
| Component | Content |
|------|------|
| **Part A: Coding Memory** | Co-maintained projects, co-solved bugs, late-night discussions, technical resonance points |
| **Part B: Persona** | 5-layer personality structure: Hard rules → Identity → Speaking/Coding style → Emotional patterns → Character behavior |

---

## Project Structure

This project follows the [AgentSkills](https://agentskills.io) open standard:

```text
create-gf/
├── SKILL.md                # skill entry
├── prompts/                # Prompt templates
│   ├── intake.md           #   Conversational intake
│   ├── memory_analyzer.md  #   Collaboration memory extraction
│   ├── persona_analyzer.md #   Personality behavior extraction (including tech tags)
│   └── ...
├── tools/                  # Tool sets
│   ├── wechat_parser.py    # WeChat parser
│   ├── telegram_parser.py  # Telegram parser
│   ├── photo_analyzer.py   # Photo analyzer
│   ├── github_parser.py    # GitHub/Code dynamics parser
│   ├── qq_parser.py        # QQ parser
│   └── ...
├── gfs/                    # Generated girlfriend Skill (gitignored)
├── docs/PRD.md
└── requirements.txt
```

---

## Recommended Tools
- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** : WeChat history export
- **Telegram Desktop** : Built-in JSON export feature

---

### Never forget that afternoon when she saw you off at the high-speed rail station, how she wished you could find a remote job to stay with her always...
MIT License © 2026 xmlans
