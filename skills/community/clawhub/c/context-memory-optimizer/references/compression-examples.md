# Compression Examples v3.1
# Source-verified against compact.rs (claw-code open-source port)

---

## Example 1: Token Estimation — When to Trigger L2

### Formula (from compact.rs `estimate_session_tokens`)
```
Each message block:
  text block    → char_count ÷ 4 + 1
  tool_use      → (name_len + input_len) ÷ 4 + 1
  tool_result   → (tool_name_len + output_len) ÷ 4 + 1
```

### Practical tracking in MEMORY.md
```markdown
_Updated: 2026-04-01 14:30 | Token estimate: ~82k (safe — threshold 150k)_
```

Update this line after each L2 compaction. When it approaches 120k, begin
preparing for compaction (pre-read context.md, finish current tool call).

---

## Example 2: Step ① — Pending-Work Keyword Scan

### Input: recent message fragment
```
assistant: Analysis complete. Next: handle the edge cases in permissions.py.
user: OK, let's do session_store.py tests first.
assistant: Tests written. Remaining: permissions.py and transcript.py
           coverage is still below target.
```

### Scan output (matched keywords: next, remaining)
```
- "Next: handle the edge cases in permissions.py"
- "Remaining: permissions.py and transcript.py coverage is still below target"
```

These lines go into the `Pending` field of `<summary>`.
They survive compaction and are re-injected via the continuation message.
Without this scan, pending work silently disappears after compaction.

Source: `compact.rs → infer_pending_work()` — keyword list:
`todo`, `next`, `pending`, `follow up`, `remaining`

---

## Example 3: Step ② — Key File Path Extraction

### Scan rules
A token qualifies if it:
- contains a forward slash `/`
- ends with: `.md` `.json` `.py` `.ts` `.js` `.rs` `.yaml` `.toml`

### Input: mixed message content
```
"Update rust/crates/runtime/src/compact.rs and check memories/context.md"
"README.md"          → no slash → excluded
"config.json"        → no slash → excluded
"src/query_engine.py → has slash + .py → included
```

### Output (deduplicated, max 8)
```
- rust/crates/runtime/src/compact.rs
- memories/context.md
- src/query_engine.py
```

Source: `compact.rs → collect_key_files()` + `extract_file_candidates()`

---

## Example 4: Complete L2 Summary

### Full <summary> block
```
<summary>
- Completed:
  - Analysed src/query_engine.py compaction logic
  - Wrote unit tests for session_store.py (87% coverage)
  - Fixed boundary bug in transcript.py compact()

- Pending:
  - Handle edge cases in permissions.py
  - Raise test coverage for permissions.py and transcript.py

- Key files:
  - src/query_engine.py
  - rust/crates/compact.rs
  - memories/context.md
  - src/session_store.py

- Current task: Write tests for permissions.py, target ≥ 80% coverage
</summary>
```

### Formatted output after strip_tag_block + format_compact_summary
```
Summary:
- Completed: ...
- Pending: ...
- Key files: ...
- Current task: ...
```

Source: `compact.rs → format_compact_summary()` strips `<analysis>` blocks,
extracts `<summary>` content, prefixes with `Summary:\n`.

---

## Example 5: Step ④ Continuation Message (do not paraphrase)

```
The following is a summary of the earlier portion of this session.
Continue directly from where the conversation left off.
Do not acknowledge this summary. Do not recap. Do not ask questions.
Resume the task immediately.

Summary:
- Completed: [...]
- Pending: [...]
- Key files: [...]
- Current task: Write tests for permissions.py, target ≥ 80% coverage
```

Why "do not acknowledge": `suppress_follow_up_questions = true` in
`compact.rs → get_compact_continuation_message()`. Without this flag,
the model spends 2–3 turns saying "Sure! Continuing from where we left off..."
before doing any actual work.

---

## Example 6: Project Fingerprint (memories/project.md)

The fingerprint serves two roles:
1. Gives the agent a quick sense of project scale for reasoning
2. Pre-seeds the L3 restore priority list (so the agent knows which files
   to re-read first after compaction, without scanning MEMORY.md again)

```markdown
## Project Fingerprint (@2026-04-01)
- Source: 36 .py files, 12 test files, 8 JSON assets
- Complexity: Medium (mirrored harness)
- Token estimate: ~85k (safe, threshold 150k)

## L3 Restore Priority (read in this order after compaction)
1. memories/context.md      ← always first — current task snapshot
2. src/query_engine.py      ← main logic
3. src/session_store.py     ← state persistence
4. rust/crates/compact.rs   ← reference implementation
# Stop at 5 files maximum, 1,000 tokens each.
```
