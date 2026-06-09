# RA-Skills 🛡️

> A comprehensive, high-performance offline-compatible registry of **90,896** Hermes Agent skills across 7 registries, including official built-in, optional, and community skills.

[![Total Skills](https://img.shields.io/badge/Total%20Skills-90,896-blue.svg)](#)
[![Built-in Skills](https://img.shields.io/badge/Built--in-75-green.svg)](#)
[![Optional Skills](https://img.shields.io/badge/Optional-95-yellow.svg)](#)
[![Community Skills](https://img.shields.io/badge/Community-90,726-orange.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 📁 Repository Structure

- **`skills/`**: The core repository of skills:
  - **`built-in/`**: Official built-in Hermes Agent skills with full prompt content.
  - **`optional/`**: Official optional Hermes Agent skills with full prompt content.
  - **`community/`**: Structured registry of over 90,726 community skills (from ClawHub, skills.sh, LobeHub, browse.sh, gstack). Organized efficiently to avoid filesystem bottlenecks:
    - Path format: `skills/community/<source>/<first_char>/<identifier>/SKILL.md`
- **`registry.json`**: Consolidated metadata catalog for fast search.
- **`tools/`**: Command-line utilities to search and fetch content:
  - **`tools/search.py`**: Find any skill in milliseconds.
  - **`tools/fetch_content.py`**: Download community skill implementations on-demand.

---

## ⚙️ How to Search Skills

Use the offline search CLI tool to browse the entire registry of 90,896 skills:

```bash
# Run interactive search
python3 tools/search.py

# Search with query
python3 tools/search.py "apple-notes"

# Search with filters
python3 tools/search.py "security" --source "ClawHub" --category "security"
```

---

## 📥 How to Fetch Community Skills Content

Since community skills are hosted on external platforms, their `SKILL.md` contains metadata. You can download the actual content for any community skill with `tools/fetch_content.py`:

```bash
# Download content for a community skill by name or identifier
python3 tools/fetch_content.py "aso-playbook"
```

The script will fetch the raw contents from the source URL and save it as `CONTENT.md` within the skill's subdirectory.

---

## 📊 Skill Registry Stats

| Source Registry | Description | Skills Count |
|-----------------|-------------|--------------|
| **Built-in** | Official Hermes core skills | 75 |
| **Optional** | Official optional extension skills | 95 |
| **ClawHub** | Community skills cataloged by ClawHub.ai | 69,842 |
| **skills.sh** | Community skills published via skills.sh | 19,938 |
| **LobeHub** | Lobe Chat Agent personas | 505 |
| **browse.sh** | Browser automation tasks | 389 |
| **gstack** | Developer agent stacks | 52 |
| **Total** | **All registries** | **90,896** |

---

Made with ❤️ for the AI Agent Community. Compatibility built for Claude Code, Hermes Agent, and any LLM agent.
