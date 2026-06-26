# Session Classify

Analyzes all Claude sessions in a project and classifies them as delete/keep/extract-then-delete.

## Quick Start

```
/session classify                        # classify current project sessions (default: --depth=fast)
/session classify <project_name>         # classify sessions for a specific project
/session classify --depth=medium         # also parse Todo items for analysis
/session classify --depth=full           # apply full AI summarize to each session (slow)
/session classify --execute              # execute after classification (archive, not hard-delete)
/session classify --rag                  # store RAG-worthy B/C sessions to RAG before archiving
```

> **Archive, not delete**: `--execute` **archives** category A sessions via the
> [`archive`](./archive.md) topic (moves the `.jsonl` to
> `~/.claude/projects/.bak/<project-key>_<uuid>.jsonl` — recoverable) instead of
> hard-deleting via `delete_session`. This follows the safe-delete principle. Add `--rag`
> to store distilled knowledge from B/C sessions to a detected RAG MCP before archiving.

## Analysis Depth Options

| Option | Method | Characteristics |
|--------|--------|----------------|
| `--depth=fast` (default) | First user message + last 3 user messages | Fast, sufficient for general classification |
| `--depth=medium` | fast + TodoWrite item parsing | Can identify actual completed task list |
| `--depth=full` | Full AI summarize applied to each session | Most accurate but slow |

> ⚠️ **Sessions scheduled for split must use `--depth=medium` or higher**
> `--depth=fast` only reads the last 3 user messages, so it may miss different topics mixed in at the end of the session.
> Always check TodoWrite items and last message flow before deciding split points.

## Instructions

### 1. Run classify-sessions.py Script

**Always use the script first** — do not inline grep/sed/jq for JSONL parsing:

```bash
python3 ~/.claude/skills/claude-session/scripts/classify-sessions.py <project-name>
```

Output: TSV with columns `ID | Lines | UserMsgs | FirstDate | LastDate | Title | LastMessages`

### 2. Immediately Classify Empty Sessions

Sessions with Lines <= 10 and UserMsgs = 0 are immediately classified as **Delete Recommended**.

### 3. Analyze Each Session

#### --depth=fast (default)

Use the script output directly. The script extracts:
- Custom title (priority) or first user message (fallback)
- Last 3 user messages for completion status
- Message counts and date range
- Command tag cleanup (e.g., `<command-name>/chezmoi</command-name>` → `/chezmoi`)

#### --depth=medium

In addition to fast analysis, parse TodoWrite items:

```bash
scripts/extract-todos.py {project} {session_id}
```

Example output:
```
[completed] k3s node etcd re-join setup
[completed] ArgoCD Application YAML backup
[in_progress] Helm chart deployment validation
[pending] monitoring alert setup
```

→ Concretely understand "what was done" from actual completed/incomplete items

#### --depth=full

Apply AI summarization to each session:

```
mcp__claude-sessions-mcp__summarize_session({
  project_name: "<project>",
  session_id: "<id>"
})
```

→ Use AI summary result as the title and reason

### 4. Classification Criteria

| Category | Criteria | Action |
|----------|----------|--------|
| **A) Delete Recommended** | Empty sessions, test sessions, simple Q&A (completed), sessions terminated with errors | Archive (§6-A) — empty sessions may use `clear_sessions` |
| **B) Keep** | Important task records, ongoing work, decisions worth referencing | Keep as-is |
| **C) Extract then Delete** | Contains knowledge/patterns but the session itself is not needed; agentify candidates | Save to Serena memory (+ RAG if `--rag`) then archive |

### 5. Output Classification Results

**Title**: Show actual first message content instead of slug (`robust-leaping-crab`).
**Reason**: Write one sentence in the format `"[key content] — [task scope/status] (N messages)"`.

```markdown
## Session Classification Results: {project_name}

### A) Delete Recommended (N)
| Session ID | Title | Reason |
|------------|-------|--------|
| a1b2c3d4-e5f6-7890-abcd-ef1234567890 | npm install openclaw failure analysis | Short Q&A completed, no need to reference again (8 messages) |
| d4e5f6a7-b8c9-0123-def0-123456789abc | MCP server connection test | Test session, terminated without conclusion (3 messages) |

### B) Keep (N)
| Session ID | Title | Reason |
|------------|-------|--------|
| 12345678-abcd-ef01-2345-67890abcdef0 | session classify skill description improvement | Skill refactoring in progress, current work session (1317 messages) |
| abcdef01-2345-6789-0abc-def012345678 | k3s node re-join work | Successful infrastructure work record, worth referencing (420 messages) |

### C) Extract then Delete (N)
| Session ID | Title | Extract Target |
|------------|-------|---------------|
| 98765432-fedc-ba09-8765-432fedcba098 | Helm chart deployment workflow | Repeatable pattern → Extract as Skill |
| fedcba09-8765-4321-fedc-ba0987654321 | ArgoCD ignoreDifferences configuration | Configuration know-how → Save to Serena memory |
```

### 6. Execute (when --execute flag is provided)

#### Note on split_session behavior direction

> ⚠️ `split_session` **works counter-intuitively**:
>
> | Result | Actual Content |
> |--------|---------------|
> | **New session** | Messages **before** the split point (front portion) |
> | **Original session** | Messages **after** the split point (back portion) |
>
> So if you want to "split the latter half of a session into a new session" → the original session ID ends up with the new topic.
> Think of the split point as "up to here is the original session", not "from here is the new session".

#### A) Archive (recoverable — replaces hard delete)

**Do not use `delete_session` (hard delete).** Archive each category A session via the
[`archive`](./archive.md) topic, which moves the `.jsonl` to
`~/.claude/projects/.bak/<project-key>_<uuid>.jsonl` (preserves the UUID, recoverable, not
re-scanned by Claude Code):

```bash
bash ~/.claude/skills/claude-session/scripts/archive-session.sh <session_id>
```

- The session disappears from the session list (same UX as delete) but stays recoverable.
- See [`archive`](./archive.md) for the destination convention, restoration, and ledger.
- Empty (0-message) sessions may instead use `clear_sessions` (§7) — nothing to preserve.

#### C) Extract → (RAG if `--rag`) → Archive

1. Extract knowledge:
```
mcp__claude-sessions-mcp__extract_project_knowledge({
  project_name: "<project>"
})
```

2. Save to Serena memory:
```
mcp__serena__write_memory({
  memory_file_name: "session-knowledge-{session_id}.md",
  content: "<extracted-knowledge>"
})
```

3. If `--rag` and a RAG MCP is detected (see Section 8), store the distilled knowledge
   to RAG before archiving.

4. Archive via the [`archive`](./archive.md) topic (same `archive-session.sh` as A — not hard delete)

### 7. Bulk Cleanup of Empty Sessions

`clear_sessions` is acceptable **only for truly empty sessions** (0 user messages / 0-byte
hook-only files) — these have no content to preserve, so hard removal is fine:

```
mcp__claude-sessions-mcp__clear_sessions({
  project_name: "<project>",
  clear_empty: true,
  clear_invalid: true
})
```

**Non-empty category A sessions** (short Q&A, test sessions with actual content) must be
**archived** via the `mv` procedure in §6-A, not bulk-deleted — they may still hold
recoverable context.

### 8. RAG Save Recommendation (when a RAG / vector store MCP is available)

**Trigger detection** — Skip this entire section if no RAG / vector store MCP is registered in the current context. Do not hard-wire to a specific vendor.

Detection patterns (any match qualifies — scan deferred tool list or system reminders):

| Vendor | Tool name pattern |
|--------|-------------------|
| Qdrant | `mcp__qdrant__qdrant-store`, `mcp__qdrant__qdrant-find` |
| Chroma | `mcp__chroma__*-add`, `mcp__chroma__*-query` |
| Weaviate | `mcp__weaviate__*-store`, `mcp__weaviate__*-search` |
| Pinecone | `mcp__pinecone__*-upsert`, `mcp__pinecone__*-query` |
| Generic | Any MCP tool whose name matches `*-(store|add|upsert|index)` paired with `*-(find|query|search)` against a vector index |

If at least one RAG MCP is detected, evaluate every session classified as **B (Keep)** or **C (Extract then Delete)** for semantic-search value and emit an additional table. Sessions in category A (Delete Recommended) are excluded.

#### Criteria — sessions worth saving to RAG

| Criterion | Rationale |
|-----------|-----------|
| Problem-solving narrative with concrete diagnosis → fix flow | Future similar problems benefit from semantic match |
| Decision rationale (why X over Y, with discarded alternatives) | Decisions are hard to re-derive; semantic recall avoids re-litigation |
| Successful troubleshooting with root cause + remediation | High recall value when symptoms recur |
| Domain-specific knowledge accumulation (infra finding, vendor quirk, undocumented behavior) | RAG preserves the explanation, not just the action |
| Anti-pattern + correct alternative pair | Future drift detection benefits from semantic comparison |

**Exclude**:
- Pure routine work (deployment commands, scripted operations already covered by skills)
- Sessions already covered by an existing skill / rule (the skill is the canonical reference)
- Time-bound state snapshots (CI run status, ephemeral debugging logs)
- Sessions classified A (Delete Recommended) — no semantic value worth retaining

#### Output

```markdown
### D-RAG) Save to RAG (N) — vendor: <detected-tool>

| Session ID | Title | RAG Value | Suggested chunk |
|------------|-------|-----------|-----------------|
| <id> | <title> | <reason — 1 sentence> | <what to embed: full summary / per-decision excerpt / problem-fix pair> |
```

RAG save is **additive** to the primary classification — it does not change the A/B/C action. A session marked C (Extract then Delete) still extracts to Serena memory and archives (§6-A, not hard delete) after the RAG store call.

#### Execution (when `--execute` is provided + user approves)

For each approved row, call the detected RAG store tool. Use a stable metadata schema so cross-session queries remain filterable:

```
<rag-store-tool>(
  information: "<chunk content — 1~3 paragraphs of the distilled knowledge>",
  metadata: {
    type: "session-summary" | "decision" | "troubleshooting" | "infra-finding" | "anti-pattern",
    project: "<project-name>",
    session_id: "<uuid>",
    date: "YYYY-MM-DD",
    category: "<domain — infrastructure | security | networking | build | ...>"
  }
)
```

**Tool selection**:
- One RAG MCP detected → use it directly
- Multiple RAG MCPs detected → present an AskUserQuestion to choose the destination
- Zero RAG MCPs → skip Section 8 entirely (do not prompt the user, do not record placeholder rows)

**Chunking**:
- One `store` call per logical chunk. Long sessions may split into multiple chunks (e.g., one per decision, one per troubleshooting episode).
- Keep each chunk self-contained — the retriever returns chunks in isolation, so context that would normally come from the surrounding session must be inlined.

**Idempotency**:
- Before storing, query the RAG with the proposed `session_id` to detect prior stores from earlier classify runs. If a chunk for the same `session_id` + `type` already exists, ask the user whether to overwrite or skip.

## Classification Hints

### Reason Format

```
"[session key content] — [task scope/status] (N messages)"
```

- Good example: `"k3s etcd node re-join work — completed successfully, contains recurrence-prevention know-how (215 messages)"`
- Bad examples: `"infrastructure work"`, `"work in progress"`

### Delete Recommended Criteria

- messageCount < 10 and simple Q&A
- First message is test-like (test, check, try it, etc.)
- Terminated with error, no conclusion
- No content beyond default slug

### Keep Criteria

- messageCount > 100 and complex work
- Updated within the last 7 days
- Work in progress (last message in incomplete state)
- Important decisions or successful troubleshooting records

### Extract then Delete Criteria

- Contains repeatable workflow patterns
- Successful configuration/deployment/infrastructure work records
- Has patterns but the session itself is not needed for reference

### Agentify Candidate Identification

- **Repetitive work**: Sessions performing the same pattern 2+ times
- **Manual workflows**: Multiple steps executed sequentially
- **Tool combinations**: Grep → Read → Edit pattern repeated
- **User request patterns**: "every time ~", "always do ~", "each time ~"
- **Successful troubleshooting**: Problem-solving process + clear solution
- **Successful configuration/deployment**: Infrastructure, CI/CD, environment setup completed

**Agentify types:**
| Session Characteristic | Conversion Target |
|----------------------|-------------------|
| Repeatable workflow | Skill |
| Mistake prevention pattern | Hook (hookify) |
| Complex multi-step task | Agent |
| Domain-specific knowledge | Memory (Serena) |

## Output

After execution:
1. Classification result table (title: actual content, reason: one-sentence format)
2. Count summary per category
3. Recommended actions (if no --execute flag, ask via AskUserQuestion)

## Requirements

- claude-sessions-mcp MCP server required
- Serena MCP server (when using extraction features)
