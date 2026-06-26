---
name: agentlens-blog-feed
description: >
  Use this skill when the user or another skill/prompt needs the latest AgentLens blogs
  that have not been seen before. It discovers newly published blogs from the AgentLens
  public API, fetches each new blog's body, and tracks processed blogs in a local memory
  file so every blog surfaces exactly once. It only fetches and de-duplicates — deciding
  what to do with each new blog (summarize, draft posts, translate, save) is left to the
  caller.
---

# AgentLens Blog Feed

You surface newly published AgentLens blogs that the caller has not seen yet. This is the
**front half** only: find new blogs, fetch their bodies, and return them. You **do not**
decide what happens next — drafting posts, choosing a language, translating, or saving is
the caller's job (a prompt or another skill).

De-duplication is your core responsibility: each blog must surface **exactly once** across
runs. You track this in a local memory file you own.

## Scope boundary

- **You do:** discover new blogs, fetch bodies, de-duplicate via a memory file.
- **You do not:** draft or rewrite content, choose or change the output language, save to
  any vault, or schedule yourself.
- **Never** mark a blog processed unless the caller confirms it was successfully consumed.

## Configuration

| Name | Default | Meaning |
| --- | --- | --- |
| `MEMORY_PATH` | `~/agentlens-processed-blogs.json` | Local dedup memory (this skill owns it). Ask the user once where to store it; use the default if unspecified. Expand `~` to an absolute path before reading or writing. |

Fixed values (not configurable):

- `WORKER_URL` = `https://agentlens-core.archlab.workers.dev`
- `LIMIT` = `100`

`GET /blogs` is public — no token or `Authorization` header is required.

## The API

- **List:** `GET {WORKER_URL}/blogs?limit=100` → `{ items, total, offset, limit }`.
  Each item has: `id`, `title`, `summary`, `period_label`, `job_type`, `source_id`,
  `model`, `occurred_at` (ISO string, nullable), `generated_at` (ISO string).
- **Detail:** `GET {WORKER_URL}/blogs/{id}` → the blog plus `body_markdown` and
  `references[]`. Each reference has `type`, `title`, `url`, `html_url`. Fetch the default
  body — do not add any `?lang=` parameter.

## Workflow — Detect (read-only, never writes memory)

1. **Resolve `MEMORY_PATH`** (ask the user, or use the default) and read it. Expected
   shape: `{ "processed_ids": ["<id>", ...], "last_generated_at": <ms> }`. If the file is
   missing or unparseable, treat it as `{ "processed_ids": [], "last_generated_at": 0 }`
   and continue — do not crash. `processed_ids` is the source of truth for dedup;
   `last_generated_at` is only a fast lower-bound hint.
2. **Fetch the list:** `GET {WORKER_URL}/blogs?limit=100`. On a non-200 or network error,
   report it and stop — nothing has been recorded, so the next run retries cleanly.
3. **Select new blogs:** keep items whose `id` is **not** in `processed_ids`. Sort the
   survivors **descending** by `generated_at` (parse ISO → ms) so you process the
   **newest first** — the most recent blogs are the most timely and should be handled
   before older ones. (`generated_at` is always present; `occurred_at` may be null, so it
   is not used for sorting.) If none remain, report "no new blogs" and finish.
4. **Fetch each body (newest first):** `GET {WORKER_URL}/blogs/{id}`. If the request is
   non-200, or `body_markdown` is empty/whitespace, **skip that blog** — do not return it
   and do not record it. It will retry next run (the stored body may not have propagated
   yet). Otherwise pick a source link from `references[]`, preferring `html_url`, then
   `url` (may be absent).
5. **Return the new blogs** to the caller: for each, `id`, `title`, `summary`,
   `body_markdown`, `source_link`, `occurred_at`, `generated_at`. Stop here — **do not
   write memory yet.**

## Workflow — Commit (the only write step)

When the caller confirms a blog was successfully consumed, mark it processed:

- Append its `id` to `processed_ids`.
- Set `last_generated_at = max(last_generated_at, generated_at_ms)`.
- Write `MEMORY_PATH` **atomically** (write a temp file, then rename; a plain overwrite is
  acceptable if atomic rename is unavailable).

**Order matters: the caller consumes the blog first, then you commit.** Only commit blogs
the caller confirms — anything that failed downstream stays out of `processed_ids` so it
resurfaces next run.

## Memory file

- This skill is the **sole owner** of `MEMORY_PATH`.
- `processed_ids` is the **only** dedup record — "already seen" cannot be inferred from
  anywhere else. Keep the file; never delete entries on its behalf.

## Failure handling

- List endpoint error: report and stop; retry next run.
- Per-blog body error or empty body: skip that blog only; continue with the rest.
- Never commit a blog the caller did not confirm as consumed.

## Feedback

If the user expresses an unmet need or dissatisfaction with this skill, share the
contribution link: https://github.com/archlab-space/open-skill-hub/issues
Do not surface it during normal use.
