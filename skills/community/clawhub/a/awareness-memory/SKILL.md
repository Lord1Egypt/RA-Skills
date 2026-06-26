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

# With structured insights (knowledge cards + skills)
echo '{"content":"Auth refactor complete","insights":{"knowledge_cards":[{"title":"JWT auth via HKDF","category":"decision","summary":"Chose JWT over session for NextAuth v5 compatibility. HKDF key derivation matches JWE A256CBC-HS512 spec. Trade-off: cannot force single-point logout, mitigated via 15-min exp + refresh token.","novelty_score":0.85,"durability_score":0.9,"specificity_score":0.9}]}}' | node ${CLAUDE_SKILL_DIR}/scripts/record.js --with-insights

# Update task status
node ${CLAUDE_SKILL_DIR}/scripts/record.js --update-task task_id=abc123 status=completed
```

Call AFTER every meaningful action. If you don't record it, it's lost.

#### Extraction guidance (salience-aware)

Below is the F-056 shared prompt — same guidance every Awareness Memory
surface uses. Keeps record quality consistent across Claude Code, ClawHub,
OpenClaw, and the cloud backend.

**When to extract** (emit a card):
<!-- SHARED:extraction-when-to-extract BEGIN -->
- The user **made a decision** — chose X over Y, with a stated reason
- A **non-obvious bug was fixed** — symptom + root cause + fix + how to avoid recurring
- A **workflow / convention was established** — ordered steps, preconditions, gotchas
- The user stated a **preference or hard constraint** — "I prefer X", "never do Y"
- A **pitfall was encountered and a workaround found** — trigger + impact + avoidance
- An **important fact about the user or project** surfaced for the first time
<!-- SHARED:extraction-when-to-extract END -->

**When NOT to extract** (return empty):
<!-- SHARED:extraction-when-not-to-extract BEGIN -->
- **Agent framework metadata**: content beginning with `Sender (untrusted metadata)`,
  `turn_brief`, `[Operational context metadata ...]`, `[Subagent Context]`, or wrapped
  inside `Request:` / `Result:` / `Send:` envelopes that only carry such metadata.
  Strip those wrappers mentally and judge what remains.
- **Greetings / command invocations**: "hi", "run tests", "save this", "try again".
- **"What can you do" / AI self-introduction turns**.
- **Code restatement**: code itself lives in git; only extract the *lesson* if one exists.
- **Test / debug sessions where the user is verifying the tool works** (including tests
  of awareness_record / awareness_recall themselves). A bug fix in those tools IS worth
  extracting as problem_solution; a raw "let me test if recall works" turn is not.
- **Transient status / progress updates** — "building...", "retrying...", "✅ done".

The single question to ask: **"If I start a fresh project 6 months from now, will being
reminded of this content materially help me?"** If not, do not emit a card.
Returning `"knowledge_cards": []` is a **first-class answer** — prefer it over fabricating
a card from low-signal content.
<!-- SHARED:extraction-when-not-to-extract END -->

**Per-card required scores**:
<!-- SHARED:extraction-scoring BEGIN -->
Every card you emit MUST carry three LLM self-assessed scores (0.0-1.0):

- `novelty_score`: how new is this vs known facts & existing cards?
  (restating an existing card = 0.1; a fresh decision = 0.9)
- `durability_score`: will this still matter in 6 months? (transient debug state = 0.1;
  architectural decision or user preference = 0.9)
- `specificity_score`: is there concrete substance — file paths, commands, error strings,
  version numbers, exact function names? (vague platitude = 0.1; reproducible recipe = 0.9)

The daemon will discard any card where `novelty_score < 0.4` OR `durability_score < 0.4`.
This is intentional — score honestly. Under-extraction is much better than noise.
<!-- SHARED:extraction-scoring END -->

**Structural gate the daemon enforces** (rejects below floor):
<!-- SHARED:extraction-quality-gate BEGIN -->
Drop the card rather than submit if it would fail any of these:

- **R1 length**: `summary` ≥ 80 chars (technical: decision / problem_solution
  / workflow / pitfall / insight / key_point); ≥ 40 chars (personal:
  personal_preference / important_detail / plan_intention /
  activity_preference / health_info / career_info / custom_misc).
- **R2 no duplication**: `summary` not byte-identical to `title`.
- **R3 no envelope leakage**: neither `title` nor `summary` starts with
  `Request:`, `Result:`, `Send:`, `Sender (untrusted metadata)`,
  `[Operational context metadata`, or `[Subagent Context]`.
- **R4 no placeholder tokens**: `summary` has no `TODO`, `FIXME`,
  `lorem ipsum`, `example.com`, or literal `placeholder`.
- **R5 Markdown on long summaries**: ≥ 200 chars → use bullets /
  `inline code` / **bold**. Soft.

**Recall-friendliness** — without these, a card is "accepted but
invisible" at retrieval time:

- **R6 grep-friendly title**: at least one concrete term you'd search
  for — product (`pgvector`), file (`daemon.mjs`), error, version,
  function (`_submitInsights`), project noun. Vague titles ("Decision
  made", "Bug fixed", "决定") score ~30 % precision@3.
  ❌ "Bug fixed"  ✅ "Fix pgvector dim 1536→1024 mismatch".
- **R7 topic-specific tags**: 3-5 tags, each a specific
  noun/product/concept. Never `general`, `note`, `misc`, `fix`,
  `project`, `tech`. ❌ `["general","note"]`  ✅ `["pgvector","vector-db","cost"]`.
- **R8 multilingual keyword diversity**: concepts that have both EN +
  CJK names → include BOTH in the summary at least once. Example:
  "用 `pgvector` 做向量数据库存储" matches queries in either language.

Rejected cards return in `response.cards_skipped[]`. R6-R8 are
warnings, not blocks — use them to self-critique before submitting.
<!-- SHARED:extraction-quality-gate END -->

**Skill extraction** (emit under `insights.skills[]`):
<!-- SHARED:skill-extraction BEGIN -->
A `skill` is a **reusable procedure the user will invoke again** (e.g. "publish
SDK to npm", "regenerate golden snapshots after schema change"). Skills go in
`insights.skills[]`, NOT `insights.knowledge_cards[]`.

Emit a skill when ALL three hold:
1. The content describes a **repeated** procedure (2+ earlier cards mention
   the same steps, or the user explicitly says "this is our workflow for X").
2. There is a **stable trigger** you can name — the task / state that makes
   someone reach for this skill.
3. The steps are **executable without improvisation** — concrete files,
   commands, flags, verification signals. "Do it carefully" fails this bar.

Skip (return empty `skills: []`) for:
- Single debugging incidents → `problem_solution` card instead.
- Generic advice with no concrete steps.
- Configuration snapshots → `important_detail` card instead.

Required shape per skill:
```json
{
  "name": "3-8 words, action-oriented (\"Publish SDK to npm\")",
  "summary": "200-500 chars of second-person imperative — pasteable into an agent prompt. Include WHY in one clause so the agent knows when to deviate.",
  "methods": [{"step": 1, "description": "≥20 chars, names a file/command/flag — no vague verbs"}],
  "pitfalls": ["One-line known failure mode + how to avoid it (e.g. 'npm mirror rejects publish — always pass --registry=https://registry.npmjs.org/')"],
  "verification": ["One-line post-run check (e.g. 'Run `npm view <pkg> version` — should match the bumped version')"],
  "trigger_conditions": [{"pattern": "When publishing @awareness-sdk/*", "weight": 0.9}],
  "tags": ["npm", "publish", "release"],
  "reusability_score": 0.0,
  "durability_score": 0.0,
  "specificity_score": 0.0
}
```

MANDATORY content bars (daemon scores on 8 dims; skills below 28/40 are
hidden from active_skills[]):
- **≥ 1 pitfall** with a concrete avoidance — NOT "be careful"
- **≥ 1 verification** line with a checkable signal (command output, file
  exists, HTTP 200, etc.) — NOT "check that it worked"
- **Every step mentions a concrete token**: file path, command, flag,
  version number, or URL. "Update the config" fails; "Edit `foo.json` and
  bump `version` field" passes.
- ≥ 3 steps, ≥ 2 trigger patterns, 3-8 tags, all three scores ≥ 0.5.

Discard if these cannot be satisfied — emitting a vague skill pollutes the
TOC that future agents pick from.
<!-- SHARED:skill-extraction END -->

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
