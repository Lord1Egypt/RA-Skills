# Alembic — Conversation Distiller

[![EN](https://img.shields.io/badge/lang-English-blue.svg)](./README.en.md)
[![CN](https://img.shields.io/badge/lang-中文-red.svg)](./README.md)

> **Turn your AI conversations into reusable knowledge notes.**

You spent two hours chatting with ChatGPT and finally understood a concept. Three days later, all you remember is "I think I talked about it once."

Alembic fixes this. It takes the raw material of your LLM conversations — extracts keywords, filters noise, restructures by first principles — and outputs a **structured knowledge note** you can revisit months later and instantly recall the insight.

> **License**
> This repository is released under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

## What It Does

```
                      ┌─────────────┐
  ChatGPT link   ──→  │             │  ──→  keyword1.md (structured note)
  or pasted text ──→  │   Alembic   │  ──→  keyword2.md (structured note)
  + optional kw  ──→  │             │  ──→  ...
                      └─────────────┘
```

1. **Auto-parses** ChatGPT shared links (reverse-engineers React Server Component serialization)
2. **Extracts keywords** — concepts with the highest cognitive delta (≤ 3, fewer is better)
3. **Distills knowledge** — first-principles oriented, problem-driven, signal over noise
4. **Outputs notes** — clean Markdown, ready for Obsidian or any directory

---

## Quick Start

### Installation

```bash
# Option 1: Direct copy
cp -r distill-conversation ~/.claude/skills/distill-conversation

# Option 2: Clone + symlink
git clone https://github.com/yaoyuyang/distill-conversation.git
ln -s $(pwd)/distill-conversation ~/.claude/skills/distill-conversation
```

### Requirements

| Requirement | Details |
|-------------|---------|
| **Claude Code** | With skills support |
| **Python 3.6+** | Stdlib only, zero external dependencies |

> **No curl required.** Since v0.3.0, network requests use Python's built-in `urllib.request`.

### Environment Variables (optional)

| Variable | Description |
|----------|-------------|
| `OBSIDIAN_VAULT_PATH` | Path to your Obsidian vault. When set, notes default to `$OBSIDIAN_VAULT_PATH/00.Inbox/`. Otherwise, notes are written to the current working directory. |

---

## Usage

In Claude Code:

```bash
# Distill from a ChatGPT shared link (auto-extract keywords)
/distill-conversation https://chatgpt.com/share/xxxxx

# Specify keywords manually
/distill-conversation https://chatgpt.com/share/xxxxx hash-function

# Specify output directory
/distill-conversation https://chatgpt.com/share/xxxxx --output-dir ~/notes/inbox

# Paste conversation text directly
/distill-conversation
(then paste conversation content)
```

### Output Directory Priority

1. `--output-dir` argument (highest priority)
2. `$OBSIDIAN_VAULT_PATH/00.Inbox/` (when env var is set)
3. Current working directory (final fallback)

### Recommended Setup for Obsidian Users

```bash
# Add to your shell profile
export OBSIDIAN_VAULT_PATH="$HOME/ObsidianVault"

# Then just use the skill — notes land in your Inbox automatically
/distill-conversation https://chatgpt.com/share/xxxxx
```

---

## Distillation Principles

| Principle | Description |
|-----------|-------------|
| **First Principles** | Start from "what is this fundamentally", not a list of conclusions |
| **Problem-Driven** | Each note answers ONE core question |
| **Signal over Noise** | Keep insights & correct conclusions, discard tangents & pleasantries |
| **Preserve Your Thinking** | Your follow-up questions and "aha" moments are part of the note |
| **Structured** | What → Why → How → Key Details |

---

## Output Note Structure

```markdown
---
tags: [domain, subcategory, distilled]
created: 2026-04-05
source: https://chatgpt.com/share/xxxxx
---
# Keyword Title
> Core Question: one sentence framing what this note answers

## Essential Definition    ← One-liner + intuitive analogy
## Why It Matters          ← What problem does it solve
## Core Mechanism          ← Main body (flexibly organized)
## Key Details & Gotchas   ← Edge cases, common mistakes, tips
## My Learning Path        ← Your reasoning journey through the chat
## Related Concepts        ← Wiki-links
## References              ← Source conversation + external materials
```

---

## Real-World Example

### Input

```
/distill-conversation https://chatgpt.com/share/69d11ccd-4a20-8330-adb9-2a39f1dbfbc9
```

A 4-turn, ~8000-word conversation where the user asked about "differences between Rust and C++ in quant research".

### Alembic Auto-Detection

- **Keyword**: `Language Selection in Quant (Rust vs C++ vs Python)` (1 keyword — entire conversation is one topic)
- **Conflict check**: No existing note in vault

### Output (Excerpt)

> Full file: [`examples/量化场景下的语言选型(Rust vs C++ vs Python).md`](./examples/量化场景下的语言选型(Rust%20vs%20C++%20vs%20Python).md)

**Result**: 8000 words of raw conversation → ~1500-word structured note. 80%+ noise filtered, all core insights preserved.

---

## Security Notes

- **Domain allowlist**: The parser only accepts URLs matching `https://(chatgpt.com|chat.openai.com)/share/<uuid>`. All other URLs are rejected before any network request.
- **No third-party data transmission**: All processing happens locally. No data is sent to any server other than fetching the ChatGPT shared page itself.
- **Stdlib only**: Network requests use Python `urllib.request` — no subprocess calls, no `shell=True`.
- **Local-only writes**: Notes are written only to the directory you specify.
- **Offline mode**: To avoid all network access, use Mode B (paste text directly) or pass a local HTML file via `--html`.

---

## Troubleshooting

| Issue | Suggestion |
|-------|------------|
| Parser returns 0 messages | ChatGPT frontend format may have changed. Check that the link is a valid public share link. |
| "Unsupported URL format" | URL must match `https://chatgpt.com/share/<uuid>`. Conversation home page links are not supported. |
| "Page content too short" | Link may have expired or been unshared. Try opening it in a browser. |
| `OBSIDIAN_VAULT_PATH` not found | Use `--output-dir` explicitly, or set the env var in your shell profile. |
| Network timeout | Check connectivity, or use Mode B (paste text) / local HTML. |

---

## File Structure

```
distill-conversation/
├── SKILL.md                          # Skill definition (read by Claude Code)
├── scripts/
│   └── parse_chatgpt_share.py        # ChatGPT shared link parser (stdlib only)
├── examples/
│   └── 量化场景下的语言选型(...).md    # Real distillation example
├── README.md                         # 中文说明
├── README.en.md                      # English README (this file)
└── LICENSE                           # MIT
```

## How the Parser Works

ChatGPT shared pages use **React Server Component (RSC/Flight)** serialization — a non-standard streaming format where:

- Strings are interned (`"user"` and `"assistant"` appear only once)
- Subsequent references use numeric IDs pointing to interned roles
- Data is often double-escaped (nested inside JSON strings)

The parser handles all of this automatically and warns clearly when the format is unrecognized.

## Known Limitations

- **ChatGPT format dependency**: The RSC parser may break if ChatGPT significantly changes their frontend. The parser will warn you if this happens.
- **Short message loss**: User messages under 20 chars may occasionally be missed (doesn't affect distillation).
- **ChatGPT links only**: For other LLMs (Claude, DeepSeek, etc.), paste the conversation text directly.

---

## Naming

- **Skill ID / slug**: `distill-conversation`
- **Display name**: Alembic (an alchemical distillation vessel — metaphor for distilling knowledge from conversations)
- **Functional description**: Conversation Distiller
