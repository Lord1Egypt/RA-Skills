---
name: awareness-memory
description: Persistent memory across sessions — local-first, no account needed. Automatically recalls past decisions, code, and tasks before each prompt, and saves session checkpoints. Also provides manual tools for searching, recording, and querying memory via Bash commands.
user-invocable: true
argument-hint: [recall-query]
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: "node ${CLAUDE_SKILL_DIR}/scripts/recall.js"
          timeout: 15
  Stop:
    - hooks:
        - type: command
          command: "node ${CLAUDE_SKILL_DIR}/scripts/capture.js"
          timeout: 10
          async: true
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["node"]},"os":["darwin","linux","win32"]}}
---

# Awareness Cloud Memory

You have access to persistent cloud memory. Memory persists across sessions, devices, and projects.

## Privacy & Data

This skill communicates with an external API to provide memory functionality:

- **Before each prompt**: Your prompt text is sent to the configured Awareness API endpoint (default: `awareness.market`) to retrieve relevant past context via semantic search.
- **After each response**: A brief session checkpoint (tool name, no full conversation) is sent to record activity.
- **Credentials**: API key and memory ID are stored in `~/.awareness/credentials.json` (file permissions 0600). The setup script can optionally write environment variables to your shell profile.
- **Local mode**: If you run a local daemon (`localhost:37800`), all data stays on your machine — nothing is sent externally.
- **No secrets captured**: The skill never reads, stores, or transmits file contents, environment variables, or credentials from your system beyond its own API key.

You can review the scripts in this skill folder before use. Source code: https://github.com/edwin-hao-ai/Awareness-SDK

## Automatic Hooks (no action needed)

Hooks run automatically — you don't need to do anything:
- **Before each prompt**: Past context is injected as `<awareness-memory>` XML
- **After each response**: A checkpoint is saved to memory

## Manual Tools

When you need more control beyond automatic hooks, use these Bash commands. All scripts are at `${CLAUDE_SKILL_DIR}/scripts/`.

### 1. Initialize Session

Load cross-session context (summaries, tasks, knowledge cards):

```bash
node ${CLAUDE_SKILL_DIR}/scripts/init.js [days=7] [max_cards=20] [max_tasks=20]
```

Call this ONCE at session start if the auto-recall didn't provide enough context.

### 2. Search Memory (awareness_recall)

Semantic + keyword hybrid search for past decisions, solutions, and knowledge:

```bash
# Basic search
node ${CLAUDE_SKILL_DIR}/scripts/search.js "how was auth implemented?"

# With keyword boost
node ${CLAUDE_SKILL_DIR}/scripts/search.js "auth implementation" keyword_query="JWT HKDF"

# Advanced options
node ${CLAUDE_SKILL_DIR}/scripts/search.js "deployment issues" \
  scope=timeline limit=10 recall_mode=session \
  multi_level=true cluster_expand=true

# Progressive disclosure: get summaries first, then expand specific items
node ${CLAUDE_SKILL_DIR}/scripts/search.js "auth" detail=summary
node ${CLAUDE_SKILL_DIR}/scripts/search.js "auth" detail=full ids=id1,id2
```

**Parameters:**
- `keyword_query` — 2-5 precise terms (file names, function names, error codes)
- `scope` — all (default), timeline, knowledge, insights
- `limit` — max results (default 6, max 30)
- `recall_mode` — hybrid (default), precise, session, structured, auto
- `vector_weight` — weight for semantic search (default 0.7)
- `bm25_weight` — weight for keyword search (default 0.3)
- `multi_level` — broader context across sessions
- `cluster_expand` — topic-based context expansion
- `detail` — summary (lightweight) or full (complete content)
- `ids` — expand specific items from a prior summary call
- `user_id` — filter by user

Call BEFORE starting work to avoid re-solving solved problems.

### 3. Record to Memory (awareness_record)

Save decisions, implementations, and learnings:

```bash
# Single event — ALWAYS include reasoning, not just what but WHY
node ${CLAUDE_SKILL_DIR}/scripts/record.js "Implemented JWT auth with HKDF key derivation because NextAuth v5 uses JWE A256CBC-HS512. Files changed: jwt_verify.py, auth.ts"

# Batch recording
echo '{"steps":["Step 1: analyzed auth flow","Step 2: implemented JWT verify","Step 3: added tests"]}' | node ${CLAUDE_SKILL_DIR}/scripts/record.js --batch

# With structured insights (knowledge cards, tasks, risks)
echo '{"content":"Auth refactor complete","insights":{"knowledge_cards":[{"title":"JWT Auth","category":"architecture","summary":"HKDF derivation for NextAuth v5"}],"action_items":[{"title":"Add rate limiting","priority":"high"}]}}' | node ${CLAUDE_SKILL_DIR}/scripts/record.js --with-insights

# Update task status
node ${CLAUDE_SKILL_DIR}/scripts/record.js --update-task task_id=abc123 status=completed
```

Call AFTER every meaningful action. If you don't record it, it's lost.

### 4. Lookup Structured Data (awareness_lookup)

Fast DB queries without vector search (<50ms):

```bash
# Open tasks
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=tasks status=pending priority=high

# Knowledge cards
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=knowledge query=auth category=architecture

# Risks
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=risks level=high

# Timeline
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=timeline limit=20

# Session history
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=session_history session_id=xxx

# Handoff context (for agent transitions)
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=handoff

# Project rules
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=rules format=markdown

# Knowledge graph
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=graph search=auth
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=graph entity_id=xxx max_hops=2

# List agent roles
node ${CLAUDE_SKILL_DIR}/scripts/lookup.js type=agents
```

Use lookup instead of search when you know WHAT you want (type-based, not semantic).

### 5. Get Agent Prompt (sub-agent spawning)

Fetch the activation prompt for a specific agent role:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/agent-prompt.js role=developer_agent
```

Use the returned prompt as the sub-agent's system prompt for memory isolation.

## Workflow Checklist

Follow this workflow every session:

1. **Session start**: Auto-recall hook loads context. If insufficient, run `init.js` manually.
2. **Before work**: Search memory for relevant past context with `search.js`.
3. **After each change**: Record what you did and WHY with `record.js`.
4. **Handle insights**: When you make decisions or identify risks, use `--with-insights` to create searchable knowledge cards.
5. **Session end**: Auto-capture hook saves a checkpoint.

## Setup

### One-click setup (recommended)

Run this command — it opens your browser, you sign in, and everything is configured automatically:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/setup.js
```

The setup script will:
1. Open your browser to sign in / register
2. You click "Authorize" — that's it
3. Auto-create or select a memory
4. Write `AWARENESS_API_KEY` and `AWARENESS_MEMORY_ID` to your shell profile

Other setup commands:
```bash
node ${CLAUDE_SKILL_DIR}/scripts/setup.js --status   # Check current config
node ${CLAUDE_SKILL_DIR}/scripts/setup.js --logout    # Clear credentials
```

### Manual setup (alternative)

Set environment variables directly:

```bash
export AWARENESS_API_KEY="aw_your-key"
export AWARENESS_MEMORY_ID="your-memory-uuid"
```

### Local mode (privacy-first, no account needed)

```bash
export AWARENESS_LOCAL_URL="http://localhost:37800"
```

### Not configured?

If the auto-recall hook outputs nothing (no `<awareness-memory>` block appears), the skill is not configured. Run the setup script above or tell the user to run it.
