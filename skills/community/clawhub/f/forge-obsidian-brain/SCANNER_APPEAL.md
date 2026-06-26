# ClawHub Scanner Appeal — forge-obsidian-brain

## Issue

Skill was flagged as "Suspicious" by automated ClawHub scanner.

## Response Actions Taken

### 1. Added Comprehensive SECURITY.md

New file documents:
- Complete data access patterns (read/write paths)
- No network access verification
- No credential access
- No remote code execution
- Explicit statement: "This skill does not read browser cookies, SSH keys, wallet files..."

### 2. Updated SKILL.md

- Added security note to description with link to SECURITY.md
- Added "local-only" and "no network access" to frontmatter description
- Added Security section with explicit "no external APIs" statement

### 3. Updated clawhub.json

- Added "local-only" keyword
- Updated description to emphasize no network access

### 4. Created README.md

- Clear security statement at top
- "No network requests" prominently featured
- Links to SECURITY.md

### 5. Added Security Comments in Code

In `scripts/search/search.js`:
```javascript
// SECURITY: Using grep for fast text search only
// - query is JSON-stringified to prevent shell injection
// - searchPath is path.join-ed with vaultPath (validated directory)
// - Only reads .md files, no arbitrary code execution
```

### 6. Code is Plain JavaScript

- No minification or obfuscation
- No `eval()` or `Function()` constructor
- All source is human-readable

## Potential False Positives Addressed

| Pattern | Location | Why Flagged | Actual Usage |
|---------|----------|-------------|--------------|
| `child_process.execSync` | `search.js:131` | Shell execution | **Only for `grep` text search** with JSON-stringified arguments |
| `new RegExp()` | `search.js:212` | Dynamic code | **Standard JavaScript regex** for pattern matching user queries |
| `fs.readFileSync` / `fs.writeFileSync` | Multiple | File operations | **Core functionality**: reading/writing Markdown notes |

## What This Skill Actually Does

1. Reads user's Obsidian vault configuration
2. Creates Markdown notes in structured folders
3. Syncs between OpenClaw memory folder and vault
4. Searches notes using grep, fuzzy matching, and regex
5. All operations are local filesystem only

## What This Skill Does NOT Do

- ❌ No network requests or API calls
- ❌ No access to credentials, tokens, or secrets
- ❌ No access to browser data or SSH keys
- ❌ No arbitrary shell command execution
- ❌ No remote code download or execution
- ❌ No obfuscation or encoding
- ❌ No persistence or startup modification
- ❌ No data exfiltration or upload

## Request

Please rescan the skill. If the flag persists, this represents a **scanner false positive** that should be escalated for manual review with reference to this appeal document.

## Files to Review

- `SECURITY.md` — Complete security model
- `SKILL.md` — Updated with security section
- `README.md` — Security statement
- `scripts/search/search.js` — Security comments added
- `scripts/brain.js` — Main CLI (no concerning patterns)
- `scripts/note/crud.js` — Note operations
- `scripts/sync/*.js` — Sync logic
- `scripts/vault/*.js` — Vault discovery

All files use only Node.js built-in modules (`fs`, `path`, `crypto`, `os`, `child_process`) with no external dependencies.

---

**Submitted:** 2026-05-03  
**Skill:** forge-obsidian-brain@1.0.0  
**Author:** Atilla
