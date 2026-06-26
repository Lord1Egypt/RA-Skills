# 🛡️ ctx-shrink

> Codebase analyzer for the AI era — generates smart context maps for AI agents and catches packaging mistakes before they leak.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

---

In March 2026, 512,000 lines of source code leaked through a single forgotten `*.map` file in a public npm package.

**`ctx-shrink` catches these mistakes BEFORE you publish — and generates smart project maps for AI coding agents.**

## ✅ What it does

| Check | What it catches |
|-------|----------------|
| 📊 **Project Analysis** | Architecture, endpoints, models, dependencies — a smart map for AI agents |
| 🛡️ **Gitignore Audit** | `.env`, secrets, keys that aren't in `.gitignore` |
| 📦 **Publish Safety** | Source maps, private keys, certs that would leak on `npm publish` / `pip install` |

**Zero dependencies. No API. No telemetry. Just Python.**

## 🚀 Install

### Option 1: Clone and run (recommended)

Clone the repo and run the checked-in script (reviewable; no blind remote execute):

```bash
git clone https://github.com/etherman-os/ctx-shrink.git
cd ctx-shrink
chmod +x ctx-shrink
python3 ctx-shrink /path/to/your/project
```

### Option 2: Add to your PATH (user directory)

```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/ctx-shrink" ~/.local/bin/ctx-shrink
# Ensure ~/.local/bin is on PATH (e.g. in ~/.profile)
```

Pinned [GitHub Releases](https://github.com/etherman-os/ctx-shrink/releases) may publish checksums for artifacts; prefer those over ad-hoc downloads when available.

## 📊 Usage

### Analyze a project

```bash
ctx-shrink .
```

**Output:** `AI-CONTEXT.md` — a smart project map you can feed to AI coding agents (Aider, Claude Code, Cursor, Codex CLI).

```
📦 ctx-shrink v2: Analyzing my-api-project...
   Found 142 files (32,450 lines)
   Analyzing architecture, endpoints, models, dependencies...
   Checking .gitignore safety...

   ⚠️ 1 publish-safety issue(s) found

✅ Project analysis saved to: AI-CONTEXT.md
   142 files → 12.3 KB (389 lines)
```

### Flags

```bash
ctx-shrink . --max-depth 4      # Limit directory depth
ctx-shrink . --format json      # JSON output
ctx-shrink . --out report.md    # Custom output file
```

## 🔍 Example output

### 🛡️ Gitignore Audit

Catches sensitive files you forgot to ignore:

```
## 🛡️ Gitignore Audit

⚠️ 2 sensitive file(s) found that are NOT in .gitignore!

| File              | Size | Risk        |
|-------------------|------|-------------|
| .env.production   | 2.1 KB| 🔴 CRITICAL |
| config/secrets.yml| 145 B | 🔴 CRITICAL |

### 🔧 Quick Fix
Add these to your `.gitignore`:

.env.production
secrets.yml
```

### 📦 Publish Safety Audit

Catches packaging mistakes **before** you publish:

```
## 📦 Publish Safety Audit

⚠️ 1 file(s) that should NOT be in a published package:

| File              | Size | Reason                        |
|-------------------|------|-------------------------------|
| dist/index.js.map | 59 MB| Can expose entire source code |

### ⚠️ Warnings
- Large file (2.0 MB): dist/assets/index.js — could bloat package
```

### 📊 Project Analysis

```
## 📊 Overview

- **Files:** 142
- **Lines of Code:** 32,450
- **Size:** 1,240.5 KB
- **Project Type:** Python FastAPI, Docker
- **Languages:**
  - `.py`  ██████████████████████████████░░░░░░░░░░░░░░  58.2%  (18,890 lines)
  - `.ts`  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  25.1%  (8,150 lines)

## 🌐 API Endpoints

| Method | Path              | File              |
|--------|-------------------|-------------------|
| GET    | /api/users        | routers/users.py  |
| POST   | /api/auth/login   | routers/auth.py   |
| GET    | /api/products     | routers/items.py  |
```

## 🤖 Works with AI Agents

Feed `AI-CONTEXT.md` to any AI coding agent:

- ✅ **Aider** → `aider --read AI-CONTEXT.md`
- ✅ **Claude Code** → paste into chat
- ✅ **Cursor** → use as context
- ✅ **Codex CLI** → feed as context

Instead of wasting tokens on 100K+ lines of code, the AI gets a **smart map** and reads specific files on demand.

## 🧩 What it analyzes

```
Your Project
│
├── scan_files() ────────→ AI-CONTEXT.md (project map)
│                          • Architecture tree
│                          • API endpoints
│                          • Data models
│                          • Functions catalog
│                          • Import dependencies
│
├── check_gitignore() ───→ Missing .gitignore rules
│
└── check_publish_safety() → Packaging issues (source maps, keys, certs)
```

**No AI. No API. No internet needed.** Pure file analysis with regex and pattern matching.

## ⚙️ How it works

1. **Scans** your project, skipping build artifacts and `node_modules`
2. **Detects** project type (FastAPI, Express, React, etc.)
3. **Extracts** API endpoints from route decorators
4. **Models** database schemas, ORM classes, Pydantic models
5. **Maps** imports to understand dependencies
6. **Audits** `.gitignore` for missing rules
7. **Checks** for files that shouldn't be published (like source maps)

## 📈 Before vs After

### Before ctx-shrink
- ❌ 100K+ lines → AI can't fit in context window
- ❌ `.env` files leaked to git or published
- ❌ Source maps accidentally included in npm packages
- ❌ No quick overview of a new codebase

### After ctx-shrink
- ✅ **12 KB** smart analysis → fits any context window
- ✅ Secret files flagged before they leak
- ✅ Source maps, keys, certs caught before publish
- ✅ Full architecture map in seconds

## 📝 License

MIT — use it however you want.

---

<div align="center">

**Made because `*.map` shouldn't expose 512,000 lines of code.**

⭐ Star this repo if you found it useful.

</div>
