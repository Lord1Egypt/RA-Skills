---
id: ctx-shrink
name: ctx-shrink
description: "ctx-shrink — Codebase analyzer for AI era. Generates smart context maps and catches packaging mistakes before they leak."
category: developer-tools
risk: safe
source: personal
date_added: "2026-04-05"
---

# 🛡️ ctx-shrink — AI Codebase Analyzer

## When to Use
This skill is applicable when the user wants to:
- Analyze a codebase and generate a smart context map for AI agents
- Audit a project for accidentally committed secrets (`.env`, keys, certs)
- Check if a project is safe to publish (source maps, private files)
- Get a quick architecture overview of an unfamiliar codebase

## 📋 Instructions
You are an expert with `ctx-shrink`. Your job is to:

1. **Run ctx-shrink** on the user's project directory
2. **Read the output** (`AI-CONTEXT.md` or custom output file)
3. **Explain** what it found — architecture, endpoints, models, issues
4. **Recommend** fixes for any security/safety issues found

## 🚀 Usage

### Run analysis
```
ctx-shrink /path/to/project
ctx-shrink /path/to/project --out report.md
ctx-shrink /path/to/project --format json
```

### Flags
| Flag | Description |
|------|-------------|
| `--max-depth N` | Limit directory depth |
| `--format json` | JSON output |
| `--out FILE` | Custom output file |

### Common use cases

**Quick project overview:**
```
ctx-shrink . --out AI-CONTEXT.md
```

**Pre-publish safety check:**
```
ctx-shrink . --out publish-audit.md
```

**For a specific path:**
```
ctx-shrink ~/projects/my-api
```

## 📊 What it catches

| Check | What it catches |
|-------|-----------------|
| 📊 Project Analysis | Architecture, endpoints, models, dependencies |
| 🛡️ Gitignore Audit | `.env`, secrets, keys not in `.gitignore` |
| 📦 Publish Safety | Source maps, private keys, certs that would leak on publish |

## ⚠️ Rules
- **Do not** download installers, pipe `curl`/`wget` to a shell, or write binaries to system paths (`/usr/local/bin`, etc.). This skill only assumes `ctx-shrink` is already on `PATH`.
- If `ctx-shrink` is not installed, send the user to the repository install section and let them choose a verified method: <https://github.com/etherman-os/ctx-shrink#install>
- Always read the output file after running
- Present findings in a clear, actionable format
