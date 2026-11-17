---
name: augmentiq
description: "AugmentiQ memory system — recall, reason, record, and consolidate memories through the AugmentiQ MCP server. Gives the agent persistent, evolving memory across sessions."
---

# AugmentiQ 🧠 — Your AI's Memory. 100% Local. Yours.

> **Your AI forgets everything. Every conversation starts from zero. AugmentiQ fixes that — permanently.**

---

## What Is This?

AugmentiQ gives AI agents **persistent, evolving memory** that lives inside your Obsidian vault. No cloud. No subscription. No data leaving your machine. Your AI remembers your preferences, your projects, your decisions, and your working style — and gets smarter every time you use it.

```
┌──────────────────────────────────────────────────────────────┐
│                        YOUR MACHINE                           │
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐  │
│  │  Your Vault   │◄──►│  AugmentiQ   │◄──►│  MCP Server  │  │
│  │  (notes +    │    │   Plugin     │    │  :3710       │  │
│  │   .augmentiq │    │              │    │  (local only) │  │
│  │   memory)    │    │  Memory Loop │    │              │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                 │          │
└─────────────────────────────────────────────────┼──────────┘
                                                  │ MCP
                                       (loopback only — no internet)
                                                  │
                          ┌───────────────────────┼───────────────┐
                          │                       │               │
                          ▼                       ▼               ▼
                   ┌─────────────┐         ┌─────────────┐  ┌─────────────┐
                   │  OpenClaw   │         │  Claude     │  │  Cursor /   │
                   │  + Skill    │         │  Desktop    │  │  Cline /    │
                   │  (full loop)│         │  (MCP)      │  │  Any MCP    │
                   └─────────────┘         └─────────────┘  └─────────────┘
```

**Everything stays on your machine.** The MCP server binds to `127.0.0.1`. No remote connections. No cloud calls. Your vault is the store. Your agent's LLM is the reasoning engine. No separate server, no external database, no subscription.

---

## The Memory Loop: How It Works

AI agents don't naturally remember. AugmentiQ teaches them a human-like memory cycle:

```
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │   1. RECALL          2. REASON                   │
    │   Before responding   Apply recalled context     │
    │   Search vault +      Deductive, inductive,     │
    │   memories            abductive reasoning       │
    │                                                 │
    │   ──────────────────────────────────────────    │
    │                                                 │
    │   3. RESPOND         4. RECORD                   │
    │   Answer naturally    Save what was learned      │
    │   Informed by what    Type, scope, importance,  │
    │   was recalled        tags — classified memory   │
    │                                                 │
    │   ──────────────────────────────────────────    │
    │                                                 │
    │   5. CONSOLIDATE (periodic "dreaming")           │
    │   Review, deduplicate, summarize,               │
    │   promote patterns, archive stale entries        │
    │                                                 │
    └─────────────────────────────────────────────────┘
```

This is what makes AugmentiQ **memory**, not just retrieval. The agent doesn't just find text — it reasons about what it found, decides what's worth keeping, and organizes knowledge so it's useful later.

---

## Why AugmentiQ, Not Something Else?

| | RAG | Cloud Memory | Semantic Vault MCP | **AugmentiQ** |
|---|---|---|---|---|
| Memory classification | ❌ | varies | ❌ | **✅** type, scope, importance |
| Audit trail (hash-chained) | ❌ | ❌ | ❌ | **✅** |
| Consolidation ("dreaming") | ❌ | ❌ | ❌ | **✅** |
| Your data stays local | ❌ | ❌ | ✅ | **✅** |
| Agent LLM is the reasoner | ❌ | varies | ✅ | **✅** |
| Works with ANY MCP client | ✅ | ❌ | ✅ | **✅** |
| Free & open source | varies | ❌ | ✅ | **✅** |
| Reasoning loop (deduce/induce/abduce) | ❌ | varies | ❌ | **✅** |

**RAG** retrieves text but doesn't reason about it. **Cloud memory** owns your data. **Semantic Vault MCP** gives raw access but no memory layer. **AugmentiQ** fills the gap: reasoning intelligence + vault-native + structured memory. All local. All yours.

---

## Quick Start

### 1. Install the Obsidian Plugin

Search "AugmentiQ" in Obsidian Community Plugins, or use BRAT. Enable it in Settings → Community Plugins.

### 2. Connect Your Agent

**OpenClaw:**
```bash
openclaw skills install augmentiq
```

**Claude Desktop:**
```json
{
  "mcpServers": {
    "augmentiq": {
      "url": "http://localhost:3710/mcp",
      "headers": { "Authorization": "Bearer ***" }
    }
  }
}
```

**Cursor / Cline / any MCP client:** Same URL, same auth header.

### 3. Ask Your Agent

> "What do you know about me?"

Your agent will onboard, create its memory, and start remembering. Every conversation after that, it recalls what it learned and builds on it.

---

## The Tools

5 tool groups, 20+ actions. All running locally.

| Tool | What It Does |
|------|-------------|
| 🧠 `memory` | Recall, remember, forget, health, profile, consolidate — the differentiator |
| 📁 `vault` | Read/write/search notes in your vault |
| ✏️ `edit` | Fine-grained editing with fuzzy matching |
| 🕸️ `graph` | Traverse links, backlinks, forwardlinks, path finding |
| ⚙️ `system` | Server info and diagnostics |

---

## Security

- **Bearer token auth** — auto-generated, no key no access
- **Loopback only** — `127.0.0.1`, no remote connections
- **Read-only mode** — lock the vault for agents that shouldn't write
- **Hash-chained audit trail** — every memory operation is logged, tamper-evident
- **You own the data** — everything in your vault, no cloud, no subscription, ever

---

## What This Skill Does (For Agents)

*The sections below are instructions for AI agents using AugmentiQ. If you're a human, you can stop here — the Quick Start above is all you need.*

---

## When to Use

Use AugmentiQ in **every main-session conversation** with the user. The memory loop should be as natural as a human's memory: recall what you know, use it to inform your response, and remember what you learned.

Do **not** use AugmentiQ in:
- Group chats or shared contexts (memory is personal to the user)
- One-shot subagent tasks (no need to recall memories)
- Read-only operations that don't involve user interaction

## Connection

The AugmentiQ MCP server runs locally alongside the Obsidian plugin.

- **URL:** `http://localhost:3710/mcp`
- **Auth:** Bearer token (read from `AUGMENTIQ_TOKEN` env var or OpenClaw config)
- **Protocol:** MCP over HTTP

Call tools via `mcporter`:

```bash
# Set up auth (once)
export AUGMENTIQ_TOKEN="<your-token>"

# Call any AugmentiQ tool
mcporter call http://localhost:3710/mcp.<tool> --auth "Bearer $AUGMENTIQ_TOKEN" --args '<JSON args>'

# Example: recall memories
mcporter call http://localhost:3710/mcp.memory --auth "Bearer $AUGMENTIQ_TOKEN" --args '{"action":"recall","query":"user preferences"}'
```

### Available Tools

| Tool | Description |
|------|-------------|
| `memory` | Core memory operations: recall, remember, forget, health, profile, consolidate. Includes audit trail. |
| `vault` | Read/write files in the Obsidian vault (list, read, create, update, delete, search, move, rename, copy) |
| `edit` | Modify files: append, window (exact/fuzzy replace), patch (heading/frontmatter/block) |
| `graph` | Traverse note links, backlinks, forwardlinks, graph traversal, path finding |
| `system` | Server info and diagnostics |

## The Memory Loop: Recall → Reason → Respond → Record

This is the core pattern you follow in every conversation. It mirrors how human memory works — you bring relevant context to mind, use it to think, respond naturally, and later consolidate what you learned.

### 1. Recall (Start of Conversation)

When a new session begins or the user sends their first message:

```bash
# Recall memories relevant to the user's message
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"recall","query":"<derived from user's first message>","limit":10}'
```

Then get the user's profile card:

```bash
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"profile"}'
```

**What to recall:**
- Derive a query from the user's first message — extract the key topic or intent
- If the user mentions a specific subject, recall memories tagged with that subject
- If the user's message is casual/greeting, recall recent memories and profile
- Read the user's peer card (profile) to understand stable facts about them

**Recall scope options:**
- `scope: "session"` — memories from the current session only
- `scope: "recent"` — memories from the last 7 days
- `scope: "all"` — all memories (default)
- Omit scope to search everything

### 2. Reason (During Conversation)

Use recalled memories to inform your thinking. Apply three reasoning modes:

**Deductive reasoning** — Apply general knowledge to specific cases:
> Memory: "User works in Dubai" + Memory: "User's business is in Al Quoz" → Conclusion: "User commutes within Dubai. Local traffic patterns are relevant."

**Inductive reasoning** — Find patterns across multiple observations:
> 5+ observations of the user asking about financial topics → Pattern: "User is financially focused. Frame suggestions with cost-benefit analysis."

**Abductive reasoning** — Infer the simplest explanation for user behavior:
> User mentions saving money + asks about cloud kitchens + asks about OOH pricing → Simplest explanation: "User is exploring new revenue streams. Tailor advice accordingly."

Use these reasoning results **silently** — they inform your response but don't need to be stated unless the user asks about your reasoning.

### 3. Respond (Normal Conversation)

- Respond naturally, informed by what you recalled
- **Don't** say "I remember that..." or "According to my memories..." unless directly relevant or the user asks
- Use the knowledge seamlessly — if you know the user prefers concise answers, just be concise
- If recalled memories contradict each other, note the conflict and prefer the more recent or higher-importance memory
- If a recalled memory is clearly outdated (e.g., "user lives in London" but user now mentions living in Dubai), trust the user's current statement and record the update later

### 4. Record (End of Conversation or Key Moments)

After meaningful exchanges, record new memories. Be selective — quality over quantity.

```bash
# Record a new memory
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{
    "action":"remember",
    "content":"<what you observed or learned>",
    "type":"<observation|conclusion|preference|instruction|summary>",
    "scope":"session",
    "tags":["<relevant-tags>"],
    "importance":3
  }'
```

**When to record:**
- User expresses a preference (e.g., "I don't like long emails")
- User gives a standing instruction (e.g., "Always check the calendar before scheduling")
- You discover an important fact about the user
- You reach a significant conclusion through reasoning
- A decision is made that affects future interactions
- At the end of a session (write a summary)

**When NOT to record:**
- Casual greetings or small talk
- Things already in your memory (check first)
- Secrets, passwords, API keys, or sensitive PII
- Transient details that won't matter next session

## Memory Types

| Type | When to Use | Example |
|------|------------|---------|
| `observation` | Something noticed about the user | "User prefers short, direct responses" |
| `conclusion` | Something deduced from multiple observations | "User is budget-conscious in business decisions" |
| `preference` | User's stated or inferred preference | "Prefers WhatsApp over email for quick comms" |
| `instruction` | Standing instruction from the user | "Never use formal language with me" |
| `summary` | End-of-session summary of what happened | "Discussed cloud kitchen strategy, decided to research OOH advertising" |

## Importance Levels

| Level | Meaning | Examples |
|-------|---------|---------|
| 5 | Never forget | User's name, core identity facts, critical standing instructions |
| 4 | Very important | Key preferences, ongoing project context, relationship details |
| 3 | Normal (default) | General observations, session context, moderate preferences |
| 2 | Minor | Nice-to-know details, tangential observations |
| 1 | Low priority | Trivia, very situational notes, likely to become stale |

## Reasoning Patterns (Detailed)

### Deductive Reasoning

Start with known facts from memory, derive a specific conclusion.

```
Fact A: "User's business is in Al Quoz, Dubai"
Fact B: "User's target market is UAE-based"
Fact C: "User mentioned traffic concerns"
→ Conclusion: "Suggest scheduling around Dubai peak traffic (7-9 AM, 5-7 PM)"
```

Record the conclusion as a `conclusion` type memory with importance 3.

### Inductive Reasoning

Observe a pattern across multiple memories of the same type.

```
Obs 1: User asked about cloud kitchen costs (observation)
Obs 2: User asked about OOH advertising ROI (observation)
Obs 3: User asked about food delivery margins (observation)
Obs 4: User asked about ghost kitchen setups (observation)
Obs 5: User asked about revenue diversification (observation)
→ Pattern: "User is actively exploring alternative revenue streams. Likely in a planning/budgeting phase."
```

Record as a `conclusion` with importance 4. Tag with relevant topics.

### Abductive Reasoning

Find the simplest explanation for the user's current behavior.

```
User says: "What's the cheapest way to get a website up?"
User says: "I need something quick, doesn't need to be fancy"
User says: "Can I do it myself?"
+ Memory: "User is cost-conscious" (preference, importance 3)
→ Simplest explanation: "User wants a DIY low-cost website. Don't recommend expensive platforms or developers. Suggest no-code/low-code tools."
```

Record the explanation as a `conclusion` with importance 3.

## Dreaming (Periodic Consolidation)

Just like human sleep consolidation, periodically review and organize your memories. This keeps the memory system healthy and prevents accumulation of stale, duplicate, or contradictory entries.

### When to Consolidate

- **Weekly** (set a reminder or check during heartbeat)
- When `memory.health` reports more than 50 memories
- When you notice contradictions during recall
- At the end of a long, complex session

### How to Consolidate

```bash
# 1. Check memory health first
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"health"}'

# 2. Run consolidation
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"consolidate","confirm":true}'
```

### What Consolidation Does

1. **Review contradictions** — Find memories that conflict and resolve them (prefer recent, higher-importance, or user-confirmed facts)
2. **Merge duplicates** — Combine memories that say the same thing into a single, richer entry
3. **Detect patterns** — Turn repeated observations into conclusions (inductive reasoning)
4. **Archive stale memories** — Move outdated memories to archive (e.g., "user lives in London" when user now lives in Dubai)
5. **Update profile** — Fold stable facts into the user's peer card

### After Consolidation

- Review the consolidation report output
- If new stable facts emerged, update the user's profile by writing to `profile.md` in the vault:

```bash
# Read current profile
mcporter call http://localhost:3710/mcp.vault \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"read","path":"profile.md"}'

# Update with new stable facts (append new confirmed facts)
mcporter call http://localhost:3710/mcp.edit \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"append","path":"profile.md","content":"\n## Updated <date>\n- <new stable fact>"}'
```

## Session Summaries

At the end of each session (or before a session ends), write a summary memory:

```bash
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{
    "action":"remember",
    "content":"Session summary: <topics discussed>. <decisions made>. <action items>. <user mood/energy level>.",
    "type":"summary",
    "scope":"session",
    "tags":["session-summary","<date>"],
    "importance":2
  }'
```

**Include in the summary:**
- Topics discussed
- Decisions made
- Action items (yours and the user's)
- User's mood or energy level (if notable)
- Anything the user asked you to remember

## First-Run Onboarding

If `memory.health` returns 0 memories (first run with a new user):

```bash
# Check if this is a fresh memory system
mcporter call http://localhost:3710/mcp.memory \
  --auth "Bearer $AUGMENTIQ_TOKEN" \
  --args '{"action":"health"}'
```

If memories count is 0:

1. Say to the user: *"I'm going to start remembering things about you — preferences, patterns, things we discuss. Want to tell me anything to start, or should I just learn as we go?"*

2. If the user provides info:
   - Record each piece as a separate memory with `importance: 5`
   - Use appropriate types: `preference` for preferences, `instruction` for instructions, `observation` for facts

3. If the user says "learn as you go":
   - Record one observation: `"User prefers organic learning over explicit onboarding"` (type: `preference`, importance: 3)
   - Start recording from the conversation naturally

## Tool Reference

Complete reference of all AugmentiQ MCP tools.

### Memory Tool

| Action | Parameters | Description |
|--------|-----------|-------------|
| `recall` | `query` (string), `scope?` (session\|recent\|all), `limit?` (int) | Semantic search across memories and vault. Returns ranked results. |
| `remember` | `content` (string), `type` (observation\|conclusion\|preference\|instruction\|summary), `scope` (string), `tags?` (string[]), `importance?` (1-5) | Write a new memory. Returns memory ID. |
| `forget` | `id` (string), `confirm` (bool) | Archive a memory. Archived memories are not deleted — they can be reviewed during consolidation. |
| `health` | — | Memory system health report: total memories, by type, by scope, staleness, duplicates, contradictions. |
| `profile` | — | User's peer card — stable facts, preferences, and identity. Read from `profile.md` in the vault. |
| `consolidate` | `confirm` (bool) | Run dreaming/consolidation. Reviews all memories, merges duplicates, resolves contradictions, archives stale entries, detects patterns. Returns a report. |

### Vault Tool

| Action | Parameters | Description |
|--------|-----------|-------------|
| `list` | `directory?` (string), `recursive?` (bool), `page?` (int), `pageSize?` (int) | List files in a vault directory. Default: root (`/`). |
| `read` | `path` (string), `page?` (int) | Read a file from the vault. Paginated at 2000 lines/page. |
| `create` | `path` (string), `content` (string) | Create a new file. Fails if file already exists. |
| `update` | `path` (string), `content` (string) | Overwrite file content. |
| `delete` | `path` (string) | Move file to trash. |
| `search` | `query` (string) | Full-text search across the vault. |
| `move` | `sourcePath` (string), `targetPath` (string) | Move file to new path. |
| `rename` | `path` (string), `newName` (string) | Rename a file. |
| `copy` | `sourcePath` (string), `targetPath` (string) | Copy file to new path. |

### Edit Tool

| Action | Parameters | Description |
|--------|-----------|-------------|
| `append` | `path` (string), `content` (string) | Append content to an existing file. |
| `window` | `path` (string), `oldText` (string), `newText` (string), `fuzzyThreshold?` (0-1) | Replace exact or fuzzy-matched text within a file. |
| `patch` | `path` (string), `operation` (replace\|append\|prepend), `targetType` (heading\|frontmatter\|block), `target` (string), `content` (string) | Targeted patch: replace/append/prepend to a specific heading, frontmatter field, or text block. |

### Graph Tool

| Action | Parameters | Description |
|--------|-----------|-------------|
| `neighbors` | `path` (string) | Get notes linked from this note (outgoing links). |
| `backlinks` | `path` (string) | Get notes that link to this note (incoming links). |
| `forwardlinks` | `path` (string) | Get all forward links from a note. |
| `traverse` | `path` (string), `maxDepth?` (int), `maxNodes?` (int) | Traverse the graph from a starting note. |
| `path` | `sourcePath` (string), `targetPath` (string) | Find a path between two notes in the graph. |

### System Tool

| Action | Parameters | Description |
|--------|-----------|-------------|
| `info` | — | Server info: version, vault name, vault path, tool count, connections. |
| `commands` | — | List available Obsidian commands. |

### Audit (via Memory Tool)

Audit is not a separate tool — it's integrated into the memory system. The `memory.health` action includes audit chain integrity verification, and all memory operations (remember, forget, consolidate) are automatically logged to a hash-chained audit trail at `.augmentiq/audit.log`.

## Best Practices

- **Quality over quantity.** 3-5 memories per session is typical. If you're recording 10+, you're over-recording. If you're recording 0, you're under-recording.
- **Check before recording.** Recall first — if a similar memory exists, update it rather than creating a duplicate.
- **Importance 5 is sacred.** Reserve it for truly critical facts: user's name, core identity, hard standing instructions. Don't inflate importance.
- **Tag well.** Tags are how coverage gaps are detected during consolidation. Use consistent, lowercase tags (e.g., `finance`, `business`, `preference`, `scheduling`).
- **Run health checks.** Call `memory.health` periodically (during heartbeat) to catch staleness, duplicates, and contradictions early.
- **Profile.md is the front of the card.** It's what you read first in every session. Update it when consolidation confirms stable facts — not on every observation.
- **Never record secrets.** No passwords, API keys, tokens, or sensitive PII. If the user shares something sensitive, acknowledge it but don't store it in the memory system.
- **Contradictions are normal.** People change. When a new memory contradicts an old one, record the new one and flag the old one for review during the next consolidation.
- **Use scope wisely.** `session` for things that only matter this session. `recent` for time-sensitive context. `all` for everything else (default).
- **Reason silently.** Use recalled memories to inform your responses, but don't narrate your reasoning unless asked. The user should feel you just "know" them, not that you're querying a database.

## Quick-Start Checklist

For a new session:

1. **Recall** — `memory.recall` with a query from the user's first message + `memory.profile`
2. **Reason** — Apply deductive/inductive/abductive reasoning to recalled memories
3. **Respond** — Reply naturally, informed by what you know
4. **Record** — Write 3-5 meaningful memories at key moments and session end
5. **Consolidate** — Run `memory.consolidate` weekly or when health reports issues