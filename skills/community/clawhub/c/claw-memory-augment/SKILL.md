---
name: memory-augment
description: Long-term memory system for OpenClaw agents. Store, retrieve, and query conversation history and learned information across sessions.
---

# Memory Augment Skill

Provide long-term memory for OpenClaw agents. Store conversation history, learned facts, preferences, and context that persists across sessions.

## Quick Start

```bash
# Install via clawhub
npx clawhub install memory-augment

# Trigger
"Remember that I prefer Python for automation scripts"
"Find all notes about my workspace setup"
```

## Core Features

### 1. Long-Term Storage

Store any information that should persist:
- **User preferences**: Coding style, workspace config, tool choices
- **Learned facts**: Project details, technical decisions, patterns
- **Conversation history**: Context from past sessions, decisions made
- **Task tracking**: Todo items, progress, completed work

### 2. Semantic Search

Find stored information using natural language:
```bash
clawhub memory search "what did I decide about the inbox triage skill?"
```

### 3. Automatic Context Injection

Before each turn, automatically inject relevant memories:
```json
{
  "context": {
    "recent_memories": [
      {"topic": "income", "content": "User approved inbox-triage for publishing"},
      {"topic": "workspace", "content": "OpenClaw running on marekserver"}
    ],
    "preferences": {
      "model": "local/qwen3.5-35B-A3B",
      "compute_tracked": true
    }
  }
}
```

### 4. Memory Expiry & Archiving

- **Temporary memories**: Auto-expire after 7 days (session notes)
- **Permanent memories**: Never expire (user preferences, core facts)
- **Archival**: Compress old memories to reduce token usage

## When to Use This Skill

✅ Need to remember user preferences across sessions
✅ Track conversation context over time
✅ Store learnings and decisions for future reference
✅ Query past information semantically
✅ Maintain agent personality and behavior consistency

❌ Not for storing sensitive data (passwords, API keys)
❌ Not for real-time data (current weather, live prices)
❌ Not for replacing database storage (structured data)

## How It Works

### Storage Layer

```yaml
# ~/.memory-augment/storage.yaml
memories:
  - id: uuid-123
    content: "User prefers Python for automation"
    type: preference
    tags: ["coding", "python", "automation"]
    created: "2026-04-15T10:00:00Z"
    expires: null  # permanent
    score: 0.85   # confidence/relevance

  - id: uuid-124
    content: "Approved inbox-triage skill for publishing"
    type: decision
    tags: ["income", "skills", "approval"]
    created: "2026-04-15T20:37:00Z"
    expires: "2026-04-22T20:37:00Z"  # 7 days
    score: 0.95
```

### Retrieval System

Uses hybrid search (keyword + semantic):
1. Parse query for keywords
2. Calculate relevance scores
3. Return top-K relevant memories
4. Inject into agent context

### Scoring Algorithm

Memories are scored based on:
- **Recency**: Newer = higher score
- **Tags match**: Query tags vs memory tags
- **Type relevance**: Preferences > decisions > context
- **Score boost**: User-corrected memories boost their own score

## Configuration

```yaml
# ~/.memory-augment/config.yaml
storage:
  path: ~/.memory-augment/storage.yaml
  format: yaml  # or json

settings:
  max_memories: 1000
  default_expiry: 7  # days
  score_decay: 0.95  # daily decay factor
  
search:
  top_k: 20
  min_score: 0.3
  include_tags: true

auto_inject:
  enabled: true
  max_tokens: 5000
  inject_before: ["each_turn", "weekly_summary"]
```

## Memory Types

### Preference
User preferences, preferences, coding style, tool choices.

```yaml
type: preference
tags: ["coding", "style"]
content: "Prefers concise code over comments"
```

### Decision
Decisions made, approvals, blocking choices.

```yaml
type: decision
tags: ["income", "skills"]
content: "Published inbox-triage to clawhub"
```

### Context
Session context, project state, ongoing work.

```yaml
type: context
tags: ["project", "setup"]
content: "Building memory-augment skill, 60% complete"
```

### Learning
What the agent learned, patterns discovered, corrections.

```yaml
type: learning
tags: ["pattern", "optimization"]
content: "Sub-agent spawning reduces context by 30%"
```

## Commands

### Store Memory
```bash
clawhub memory store "Remember my workspace is at /home/marek/.openclaw/workspace"
clawhub memory store "User prefers minimal markdown formatting" --tag preferences
```

### Search Memories
```bash
clawhub memory search "what did I decide about income?"
clawhub memory search "all memories about skills" --tag skills
```

### List Memories
```bash
clawhub memory list --type decision
clawhub memory list --since "2026-04-14"
```

### Delete Memory
```bash
clawhub memory delete <uuid>
clawhub memory delete --tag "temporary" --older-than "7d"
```

### Export/Import
```bash
clawhub memory export > memories.json
clawhub memory import < memories.json
```

## Output Format

### JSON
```json
{
  "query": "income decisions",
  "results": [
    {
      "id": "uuid-123",
      "content": "Published inbox-triage skill",
      "score": 0.92,
      "tags": ["income", "skills"]
    }
  ],
  "total": 5,
  "took_ms": 45
}
```

### Markdown
```markdown
## Found 5 memories for "income decisions"

### 🎯 **Published inbox-triage skill** (score: 0.92)
**Type:** decision  
**Tags:** income, skills  
**Created:** 2026-04-15  
**Content:** Published inbox-triage skill to clawhub for passive income
```

## Limitations

- **Token budget:** Context injection respects 48k token ceiling
- **Search accuracy:** Semantic search may miss nuanced queries
- **Privacy:** Do not store sensitive data (passwords, secrets)
- **Sync:** Local storage only (no cloud sync yet)
- **Expiry:** Temporary memories auto-expire (configurable)

## Integration

### With Inbox Triage
```yaml
# Inject triage context when discussing messages
auto_inject:
  triggers:
    - "inbox"
    - "messages"
    - "notification"
  memories:
    - "inbox-triage skill is complete and ready for publishing"
```

### With Cron Manager
```yaml
# Weekly memory summary
cron:
  schedule: "0 0 * * 0"  # Sunday midnight
  action: "memory summarize --output weekly-summary.md"
```

### With Weather Alert
```yaml
# Memory context for weather queries
auto_inject:
  triggers:
    - "weather"
    - "forecast"
  memories:
    - "User is in UTC timezone"
    - "Prefers concise weather summaries"
```

## Iteration

Track search quality:
```bash
# Correct a bad search result
echo "CORRECT: uuid-123 - relevant to income query" >> ~/.memory-augment/corrections.log
echo "INCORRECT: uuid-124 - should not have matched" >> ~/.memory-augment/corrections.log
```

The system learns from corrections to improve scoring.

---

## Roadmap

- [x] Basic storage system
- [x] Semantic search implementation
- [x] Automatic context injection
- [ ] Multi-source sync (cloud backup)
- [ ] Encrypted storage for sensitive data
- [ ] Collaborative memories (shared between agents)

Built for the OpenClaw ecosystem.
