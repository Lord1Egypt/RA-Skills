# RA-Skills 🛡️

> A comprehensive, high-performance offline-compatible registry of **90,896** Hermes Agent skills across 7 registries, including official built-in, optional, and community skills.

[![Total Skills](https://img.shields.io/badge/Total%20Skills-90,896-blue.svg)](#)
[![Offline Folders](https://img.shields.io/badge/Offline%20Folders-79,455%20(88%25)-success.svg)](#-offline-content--downloading)
[![PyPI](https://img.shields.io/pypi/v/ra-skills?label=pip%20ra-skills&color=3776AB)](https://pypi.org/project/ra-skills/)
[![npm](https://img.shields.io/npm/v/ra-skills?label=npm%20ra-skills&color=CB3837)](https://www.npmjs.com/package/ra-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## ⚡ Install the search tool (pip / npm)

Don't want to clone 90k skills? Install the lightweight **`ra-skills`** CLI — it bundles the metadata index so you can **search offline**, then **download any skill's full folder on demand**.

```bash
pip install ra-skills          # Python   →  https://pypi.org/project/ra-skills/
npm install -g ra-skills       # Node.js  →  https://www.npmjs.com/package/ra-skills
```

```bash
ra-skills search github --limit 5     # search 90,896 skills by keyword (offline)
ra-skills search "" --source ClawHub  # filter by source/category
ra-skills show apple-notes            # show one skill's metadata
ra-skills stats                       # registry totals by source
ra-skills get aso-playbook            # download the FULL skill folder from GitHub
```

Python / JS API:

```python
from ra_skills import search, stats, download
search("security", source="ClawHub", limit=5)   # -> list of skill dicts
download("aso-playbook", dest="./skills")        # -> full folder on disk
```

```js
const { search, download } = require('ra-skills');
search('security', { source: 'ClawHub', limit: 5 });
await download('aso-playbook', './skills');
```

---

## 📦 Works fully offline — no API keys, no network

**79,455 of 90,726 community skills (88%) ship as complete, ready-to-run folders right here in the repo** — not metadata stubs. Clone it once and every bundled skill is on your disk:

```
skills/community/clawhub/a/aso-playbook/
├── SKILL.md          # the real skill prompt
├── skill-card.md     # summary card
├── _meta.json        # source metadata
└── references/       # docs, scripts & assets bundled with the skill
```

That's the full `SKILL.md` **plus** its bundled `scripts/`, `references/`, and assets for ClawHub, skills.sh, LobeHub, and gstack — usable on a plane, in an air-gapped box, or wherever you have no connection. See [offline coverage](#offline-coverage) for the per-source breakdown.

---

## 📁 Repository Structure

- **`skills/`**: The core repository of skills:
  - **`built-in/`**: Official built-in Hermes Agent skills with full prompt content.
  - **`optional/`**: Official optional Hermes Agent skills with full prompt content.
  - **`community/`**: Structured registry of over 90,726 community skills (from ClawHub, skills.sh, LobeHub, browse.sh, gstack). **~88% are stored as complete, fully-offline skill folders** — not just metadata — so you get the real `SKILL.md` plus its bundled `scripts/`, `references/`, `skill-card.md`, `_meta.json`, and assets. Organized efficiently to avoid filesystem bottlenecks:
    - Path format: `skills/community/<source>/<first_char>/<identifier>/`
- **`registry.json`**: Consolidated metadata catalog for fast search.
- **`tools/`**: Command-line utilities to search and fetch content:
  - **`tools/search.py`**: Find any skill in milliseconds.
  - **`tools/fetch_content.py`**: Fetch a single skill's content on-demand (for the ~12% not yet bundled, or to refresh).
  - **`tools/bulk_download.py`**: Bulk-download **full skill folders** for every community source (resumable).

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

## 📥 Offline Content & Downloading

Most community skills (~88%) already ship as **complete offline folders** in this repo — open `skills/community/<source>/<first_char>/<identifier>/` and you'll find the real `SKILL.md` alongside its scripts, references, and assets. No network needed.

For the remaining skills (genuinely delisted/removed upstream), or to refresh a skill, use the downloaders:

```bash
# Fetch one skill's full folder by name or identifier
python3 tools/fetch_content.py "aso-playbook"

# Bulk-download full folders for a whole source (resumable via .ra_complete markers)
CLAWHUB_TOKEN=<token> GITHUB_TOKEN=$(gh auth token) \
  python3 tools/bulk_download.py --source clawhub,skills_sh --threads 10
```

Tokens: `CLAWHUB_TOKEN` authenticates the ClawHub API; `GITHUB_TOKEN` raises GitHub's rate limit (5,000/hr vs 60) for skills.sh/gstack.

### Offline coverage

| Source | Full folders | Total | % |
|--------|-------------:|------:|--:|
| ClawHub | 61,945 | 69,842 | 89% |
| skills.sh | 16,969 | 19,938 | 85% |
| LobeHub | 476 | 505 | 94% |
| gstack | 52 | 52 | 100% |
| browse.sh | 13 | 389 | 3% ¹ |
| **Total** | **79,455** | **90,726** | **88%** |

¹ The upstream `browserbase/browse.sh` repository was removed from GitHub, so most browse.sh skills are no longer fetchable.

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
