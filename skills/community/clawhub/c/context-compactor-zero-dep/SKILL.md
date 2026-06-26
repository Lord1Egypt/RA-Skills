---
name: context-compactor
description: >
  Automatic context compression for OpenClaw sessions. Summarizes long conversations
  into structured digests (decisions, facts, pending items, technical details), saves
  compressed summaries to disk, and injects them into new sessions. Reduces token waste
  from redundant context repetition. Use when conversation exceeds ~50 turns, when
  context feels bloated, when starting a new session and prior context is needed, or
  when the user says "compact", "summarize this conversation", "start fresh but remember".
---

# Context Compactor

Compresses long conversations into structured summaries. Saves token by replacing
raw conversation history with dense, searchable digests.

## Requirements

- **Runtime**: Python 3.10+ (standard library only)
- **OS**: Linux, macOS
- **Environment variables**:
  - `OPENCLAW_WORKSPACE` — Workspace root (default: `~/.openclaw/workspace`)
- **Environment**: `OPENCLAW_WORKSPACE` (default: `~/.openclaw/workspace`)

## Security

### Write Restrictions (Hard Rules)
The agent may ONLY write to these locations:
- `memory/compacts/` — compact files only
- `SESSION-STATE.md` — via smart-memory skill (not this skill)

The agent MUST NOT write to:
- Any directory outside the workspace
- System directories (/etc, /usr, /var, /tmp except session cache)
- User home directory root (~/.ssh, ~/.config, ~/.aws, etc.)
- Any `.*` dotfile or dotdir in workspace root
- Any file not matching `memory/compacts/*.md`

### Read Restrictions
The agent may ONLY read from:
- The current conversation context (already available)
- `memory/compacts/` — for listing/reading past compacts

The agent MUST NOT read from:
- `/etc/passwd`, `/etc/shadow`, or any system credential file
- `~/.ssh/`, `~/.aws/`, `~/.config/openclaw/` or similar
- Any file outside the workspace unless explicitly asked by the user

### Redaction Enforcement
Before writing ANY compact, the agent MUST run this checklist:
1. ✅ No file paths (replace with `<REDACTED_PATH>`)
2. ✅ No URLs (replace with `<REDACTED_URL>`)
3. ✅ No internal IPs (replace with `<INTERNAL_URL>`)
4. ✅ No passwords, tokens, API keys (delete entirely)
5. ✅ No personal info beyond work context

If any item fails → do not write the compact until fixed.

### Privacy Boundaries

### What Compacts May Contain
- Decisions, facts, pending actions, blockers
- Project names and feature descriptions

### What Compacts Must NOT Contain
- File system paths (use `<REDACTED_PATH>` placeholder)
- Internal URLs, endpoints, or infrastructure details
- API keys, tokens, passwords, secrets (script-level regex filter)
- Private keys or certificates
- User personal information beyond work context

### Agent Rules
- Before saving a compact, strip or redact all paths, internal URLs, and credentials
- Use placeholders: `<PROJECT_ROOT>`, `<INTERNAL_URL>`, `<DB_CONFIG>`
- If unsure whether something is sensitive, redact it
- Compacts are for "what was decided" not "where things live"

### Data Isolation
- **Keyword extraction**: Fully local — no network calls, no external transmission
- **LLM extraction** (opt-in): Sends conversation text to the agent's configured LLM provider. This is inherent to using any LLM-based compaction and is **not** controlled by this skill. The skill only provides the prompt template; the agent/platform handles the actual API call.
- Maximum 30 compacts retained, oldest auto-deleted
- Compacts are stored locally and read locally — the skill itself never makes network calls

## How It Works

```
Long conversation (10,000+ tokens)
    ↓
compact_session.py --extract
    ↓
Structured digest (~500 tokens)
    ↓
Saved to memory/compacts/YYYY-MM-DD-HHMM.md
    ↓
New session reads latest compact on startup
```

**Compression ratio: ~20:1** — a 10,000 token conversation becomes ~500 token digest.

## Quick Reference

| Action | Script |
|--------|--------|
| Write compact (agent-authored) | `python3 scripts/compact_session.py --write < compact.md` |
| List compacts | `python3 scripts/compact_session.py --list` |
| Read latest compact | `python3 scripts/compact_session.py --latest` |
| Show compact stats | `python3 scripts/compact_session.py --stats` |

**How compaction works**: The agent drafts the compact content, then pipes it through `--write` which enforces security checks (no paths, URLs, IPs, secrets) before saving. This ensures programmatic enforcement — the agent never writes directly to disk.

## Compact Format

```markdown
# Session Compact — 2026-03-31 17:00 UTC
**Turns**: 45 | **Est. tokens saved**: ~9,500

## Decisions Made
- [2026-03-31] Chose SQLite over Redis for golden3 prompts
- [2026-03-31] Decided to use zero-dependency approach for smart-memory

## Facts Established
- [PROJ] golden3 site at golden3.killclaw.xyz, repo github.com/zgjq/golden3
- [TECH] Prompts stored in data/golden3.db, table `prompts`, category `scoring`
- [PREF] User prefers direct, no-nonsense communication style

## Pending Actions
- [ ] Publish smart-memory to ClawHub
- [ ] Fix scoring display from 100-point to 10-point scale

## Technical Context
- Server: ubuntu-4gb-hel1-1, Node v24.14.0
- Golden3 uses node:sqlite (DatabaseSync)

## Blockers / Open Questions
- Need ClawHub login token to publish

## Session Summary
Built smart-memory skill from Claude Code architecture study. Published to ClawHub
as smart-memory-zero-dep. Memory system now active with WAL protocol, type
classification, temporal decay, and snapshot/restore.
```

## Agent Behavior

### When to Compact
- Conversation exceeds ~50 turns
- Context window approaching limits (see AGENTS.md token discipline rules)
- User says "compact", "summarize", "fresh start", "压缩"

### How to Compact
The agent drafts the compact content, then saves it via:
```
echo "compact content" | python3 scripts/compact_session.py --write
```
The `--write` flag enforces all security checks programmatically: redaction of paths/URLs/IPs/secrets, path containment within workspace, and file naming. The agent NEVER writes directly to disk.

### When to Inject Compact
- New session startup — check for recent compact
- User asks "what were we working on"
- Context search returns nothing but a compact exists

### Extraction Rules
From the conversation, extract:
1. **Decisions** — anything with "chose X over Y", "decided to", "going with"
2. **Facts** — URLs, file paths, configs, technical details, user preferences
3. **Pending** — uncompleted tasks, "later", "TODO", "next step"
4. **Blockers** — "need X first", "blocked by", "waiting for"
5. **Summary** — 2-3 sentence overview of what happened

Skip:
- Greetings, small talk, "ok", "嗯"
- Repeated information already in MEMORY.md
- Debugging noise (unless it led to a LESSON)
- Sensitive data (tokens, passwords)

## Integration with smart-memory

This skill works with `smart-memory`:
- Compacts reference `[TYPE]` tags from smart-memory's classification system
- Pending items from compacts can feed into `wal pending`
- Facts from compacts can be promoted to MEMORY.md
- Compacts live in `memory/compacts/` — decayed by smart-memory's archival system

## File Structure

```
~/.openclaw/workspace/
├── memory/
│   └── compacts/
│       ├── 2026-03-31-1700.md   # Session compact
│       ├── 2026-03-30-1430.md
│       └── ...
```
