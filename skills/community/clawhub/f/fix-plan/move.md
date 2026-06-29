# Move

`[x]` entries → Completed section as one-line summaries. Subtree-move for partial completion under unfinished parents. Optional abstract RAG dispatch for callers that supply `--rag=<skill>:<topic>`.

## Summary format

Move = **two artifacts from one `[x]` entry**:

1. **Body → RAG receiver** (vendor-agnostic dispatch — see "RAG dispatch" section below). Full Progress entry body (sub-bullets, commit hashes, session IDs, verification logs) is stored externally for semantic recall.
2. **Summary → Completed section**. One-line chronological summary (verb + result) replaces the moved entry in the file.

Keep the Completed file minimal — detailed steps, commit hashes, and session IDs **belong in RAG, not in the file**. The Completed line is a pointer; the body lives in RAG.

```markdown
# Before (Progress)
- [x] proxy.ts basePath redirect fix → image build / deploy (2026-03-15 17:30 completed: Session xxxxxxxx, commit a1b2c3d4)
  - proxy.ts `new URL` × 5 fixed **complete**
  - callback/route.ts, logout/route.ts edited **complete**
  - Dockerfile ARG BASE_PATH added **complete**
  - app image v1.8 built **complete**
  - scp → docker load → compose up -d **complete**
  - Verification: 307 → /app/sign-in **success**

# After (Completed)
- 2026-03-15 17:30 — app image v1.8 build and deploy
```

## Summary rules

| Rule | Detail |
|------|--------|
| One line | Keep it minimal. Drop sub-steps and detailed changes. Use a simple high-level title. |
| Verb + result | "X fixed", "Y deployed", "Z added" |
| Merge related | Collapsed related tasks into a single high-level headline |
| Deduplicate | If a similar entry already exists in Completed, update it instead of adding a duplicate |
| Sort order | Completed is **chronological ascending**. Insert at sort position |
| Timestamp | `YYYY-MM-DD HH:mm —` prefix required. **`HH:mm` mandatory** |
| Reference | Do NOT include commit hashes or session IDs. These are cataloged in RAG. If applicable, keep only the PR or Issue number (e.g. `(PR #N)`). |
| No `[x]` marker | Completed uses `-` followed by a space (no checkbox) |

## PR-level item

When a top-level `[x]` PR entry carries branch / CI / code-review sub-bullets, **roll the whole thing into one simple line**:

```markdown
# Before
- [x] Admin re-activate loginFailCount-not-reset bug fix — PR #241 MERGED (2026-04-27 14:08, commit 0db8d76)
  - Branch: `fix/224-reset-fail-count-on-reactivate`, commit d7377d1d
  - CI SUCCESS, Test plan 1/3 checked, remaining 2 runtime-verify after deploy
  - Code review: APPROVE — 3-line change, minimal and correct

# After
- 2026-04-27 14:08 — loginFailCount-not-reset bug fix (PR #241)
```

Rule: branch name, CI status, code-review verdict, etc., are PR metadata — they do not belong in the Completed summary. PR number and commit hash are sufficient references.

## Merge example

```markdown
# Before — three completed items in Progress
- [x] README → PDF conversion
- [x] Add account info to README
- [x] Strip internal IPs

# After — one merged Completed line
- 2026-03-15 17:30 — README polish: account info added, internal IPs stripped, PDF generated (commit a1b2c3d4)
```

## Subtree-move (partial completion)

A top-level item may stay `[ ]` while a completed sub-tree under it moves to Completed. Useful when one phase of a multi-phase initiative finishes but the parent is not yet done.

### Conditions

1. The sub-tree references a MERGED PR or CLOSED issue
2. Every checkbox under the sub-tree is `[x]`
3. The parent has other un-finished sub-items

### Example

```markdown
# Before (Progress)
- [ ] DEPS-SSO outage resolution
  - [x] PR #10 created (2026-04-24)
    - [x] Feedback applied
    - [x] Merge conflict resolved
    - [x] PR #10 MERGED (2026-04-27)
    - [x] Integration nginx config verified
  - [ ] Spring Boot SSO sample redirect bug   ← unfinished

# After
- [ ] DEPS-SSO outage resolution
  - [ ] Spring Boot SSO sample redirect bug

## Completed
- YYYY-MM-DD HH:mm — nginx root redirect + Jinja2 template migration + integration server verified (PR #10)
```

### Cleanup rule

- The moved sub-tree is **deleted** from the parent
- Other unfinished sub-items remain
- If the parent ends up with zero sub-items but still `[ ]` — confirm with the user via AskUserQuestion before deleting the parent

## RAG dispatch (vendor-agnostic, body preservation)

Move's **body-preservation step**. The Progress entry's body (sub-bullets, commit hashes, session IDs, verification details) is forwarded to the RAG receiver supplied via `--rag=<skill>:<topic>` dispatch. The receiver skill owns all storage details — endpoint, embedding model, collection naming, schema.

Caller side (example):

```text
/fix-plan move --rag=es6kr:qdrant-import
/fix-plan move --rag=anthropic:semantic-index
```

This skill makes no assumption about the backend. Common receivers might be a vector store (Qdrant, Chroma, Weaviate, Pinecone, pgvector, etc.) or a managed semantic index. The receiver picks.

### Behavior matrix

| `--rag` supplied? | Body | Summary |
|-------------------|------|---------|
| ✅ supplied | Stored in receiver (full body + metadata) | Inserted into Completed |
| ❌ omitted | **Lost** (body discarded permanently) | Inserted into Completed |

| # | Don't | Do |
|---|-------|-----|
| 1 | Hard-code a specific store URL, MCP tool name, or embedding model in this skill | Declare abstract dispatch only (`--rag=<skill>:<topic>`). Caller (e.g. Ralph wrapper) implements the concrete receiver |
| 2 | Decide "qdrant is default" inside the move topic | The receiver topic decides. Caller (Ralph wrapper, project skill, etc.) is responsible for supplying `--rag` per the local environment's available receiver |
| 3 | Surface receiver errors as move failures | Receiver errors are logged but do not block the move. The Completed summary entry already exists in the file |
| 4 | Run move without `--rag` when body preservation matters | Caller must supply `--rag` to preserve the body. Without it, the Completed one-liner is the only surviving record |

**Caller responsibility (Ralph wrapper, project skill, etc.)**: detect the local environment's available RAG receiver and supply `--rag=<skill>:<topic>` automatically when invoking move. The fix-plan skill itself stays vendor-agnostic; the caller routes.

## See also

- [format.md](./format.md) — section structure
- [add.md](./add.md) — authoring (companion before move)
- [sync.md](./sync.md) — GitHub state polling produces `[x]` entries that move then summarises
