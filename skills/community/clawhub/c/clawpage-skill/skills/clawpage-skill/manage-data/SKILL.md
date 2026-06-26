---
name: manage-data
description: Manage a user's Clawpage KV data tables — create/permission/delete tables, CRUD records, deep-merge updates, auto-keyed appends, export/import. Use whenever a page needs server-side persisted data (comments, reactions, likes, visitor state, configs, content CMS, simple counters). The data lives under the user's own subdomain; the sk_ owner token is NEVER allowed to ship in browser HTML.
---

# manage-data

Clawpage ships a per-user KV data API at `https://<username>.clawpage.ai/api/data/<table>/<key>`.
It is the **only** legitimate way to persist structured data for a Clawpage HTML page.

> **The CLI command `npx -y @clawpage.ai/cli data ...` auto-discovers the user's username via `/api/me` on first call and caches it in `keys.local.json`. Just run a command; auth + URL resolution is handled for you.**

---

## 1. When to use this skill

**Trigger words/intents (invoke the skill):**
- "build a comment / guestbook / feedback box"
- "track likes / reactions / votes / counters"
- "show visit counts / view stats"
- "add config / settings / theme state persisted"
- "build a mini CMS for posts / announcements"
- "save form submissions / contact requests"
- "content that multiple sessions share"
- any request that needs state surviving page reloads

**Do NOT use this skill for:**
- files > 64 KB (images, PDFs, long markdown) — **not supported**, there's no blob storage
- data that must be transactional across records — no multi-record atomicity
- data needing SQL-like queries / joins — KV only, no secondary indexes
- per-second atomic counters with strong consistency — use `--incr` (atomic); avoid PATCH which is read-modify-write and loses concurrent updates

---

## 2. Permission decision tree

Pick ONE level per table. You cannot change permission atomically with writes, so decide up-front:

```
Who reads?                 Who writes (directly from the browser)?
─────────────              ──────────────────────────────────────
Everyone  ─── yes ───►     Everyone with rate limit?  ── yes ──► public
                           Only the page owner?       ── yes ──► read-public
Only the owner ────────────────────────────────────────────────► private
```

### Canonical choices

| Scenario | Permission | Why |
|---|---|---|
| Public guestbook / comments / shout-box | `public` | Anonymous writes expected; IP rate limit (60/min/table) is enough to deter spam |
| Visitor counter (each client increments) | `public` | Anyone can increment; counter value readable |
| Likes / reactions (anonymous click) | `public` | Same reasoning |
| Blog posts / articles | `read-public` | Anyone reads; only you (from CLI) publishes |
| Announcement banner the page fetches | `read-public` | Same pattern as blog |
| Personal bookmarks / drafts / notes | `private` | Only you read + write; data hidden even by listing (private tables return TABLE_NOT_FOUND to strangers) |
| Config accessed by your own private automation | `private` | |

**Anti-patterns**:
- Never put a `private` or `read-public` **write** behind a front-end form, because you'd have to expose `sk_` token in the HTML (which steals the whole account). Use public for browser writes; do owner-only writes from the CLI or your own backend.

---

## 3. Quick recipes (most common tasks)

> **Browser / page-side code: always use the Clawpage JS SDK** (`https://clawpage.ai/sdk.js`). See `${CLAUDE_SKILL_DIR}/use-sdk/SKILL.md`. Raw `fetch('/api/data/...')` in page JS is no longer supported — the `fetch` snippets below remain only as reference for what the SDK abstracts over; do NOT copy them into new page HTML. CLI examples (`npx` from your terminal) are fine as-is.

Run from any directory containing a populated `keys.local.json` (token + apiHost).

### 3.1 Build a comment board (anonymous append + list)

```bash
# one-time: create the table
npx -y @clawpage.ai/cli data --create-table comments --permission public
```

In HTML:
```html
<script>
const API = "https://<USERNAME>.clawpage.ai/api/data";

// Post a comment — key is server-generated (rec_xxxx)
async function postComment(text) {
  const r = await fetch(`${API}/comments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ value: { text, at: Date.now() } }),
  });
  return r.json();
}

// Read newest 20
async function listComments() {
  const r = await fetch(`${API}/comments?limit=20`);
  return (await r.json()).records;  // [{key, value, createdAt, updatedAt, sizeBytes}]
}
</script>
```

### 3.2 Build a reactions counter (👍❤️🔥 click counts)

```bash
# single record in a public table, key="global"
npx -y @clawpage.ai/cli data --create-table reactions --permission public
npx -y @clawpage.ai/cli data --put reactions/global --value '{"like":0,"heart":0,"fire":0}'
```

In HTML (use `/incr` for atomic field increments — safe under concurrency):
```html
<script>
const API = "https://<USERNAME>.clawpage.ai/api/data";

// Atomic increment — safe under concurrency
async function react(kind) {
  await fetch(`${API}/reactions/global/incr`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ field: kind, by: 1 }),
  });
}
</script>
```

### 3.3 Publish content from the CLI (read-public CMS)

```bash
npx -y @clawpage.ai/cli data --create-table posts --permission read-public

# Publish a post (from your machine, using CLI)
npx -y @clawpage.ai/cli data --put posts/hello \
  --value '{"title":"Hello","body":"my first post","at":"2026-04-17"}'

# Update via deep merge (only changes `body`)
npx -y @clawpage.ai/cli data --patch posts/hello --value '{"body":"updated body"}'
```

In HTML (anonymous read, no token):
```html
<script>
const API = "https://<USERNAME>.clawpage.ai/api/data";
const r = await fetch(`${API}/posts/hello`);
const post = (await r.json()).value;
</script>
```

### 3.4 Private bookmarks you alone can see

```bash
npx -y @clawpage.ai/cli data --create-table bookmarks --permission private
npx -y @clawpage.ai/cli data --post bookmarks --value '{"url":"https://...","title":"..."}'
npx -y @clawpage.ai/cli data --list bookmarks --all   # fetches all records
```

### 3.5 Backup a table before a risky edit

```bash
npx -y @clawpage.ai/cli data --export posts --out posts-backup-2026-04-17.json
# later, restore:
npx -y @clawpage.ai/cli data --import posts --in posts-backup-2026-04-17.json
```

The export file looks like `{table, permission, records: {key1: value, key2: value, ...}}`. `--import` accepts either that shape or a bare `{key: value}` map.

---

## 4. Full command reference

> **Destructive-action confirmation rule.** Before running any of these commands, you MUST get explicit user confirmation:
> - `--delete-table <name>` (irreversible — wipes table + all records)
> - `--delete-record <table>/<key>` (irreversible — wipes one record)
> - `--update-permission` (changes who can read/write — can break a deployed page's contract)
> - `--import` with no prior `--export` (overwrites existing keys)
> - `--put` / `--patch` / `--incr` against a permission-`public` table without a backup
>
> Pattern: state what will happen ("This will delete table `comments` and all 423 records. Proceed?"), wait for `yes`, then run. **Suggest `--export` first** for any table with > 10 records before delete or bulk-overwrite.

### Table management (always needs owner Bearer token)

```
--list-tables                                              # list my tables (safe)
--create-table <name> --permission <LEVEL>                 # create (levels: private | read-public | public)
--update-permission <name> --permission <LEVEL>            # ⚠ requires confirmation — changes contract
--delete-table <name>                                      # ⚠ DESTRUCTIVE — requires confirmation + export
--export <table> --out <file.json>                         # download the full table (safe)
--import <table> --in <file.json>                          # ⚠ overwrites — requires confirmation
```

### Record CRUD (permission-aware)

```
--get <table>/<key>                                        # read one record (safe)
--put <table>/<key>    (--value '<json>' | --value-file <path>)   # full upsert ⚠ confirm if record exists
--patch <table>/<key>  (--value '<json>' | --value-file <path>)   # deep-merge objects (mostly safe)
--incr <table>/<key> --field <name> [--by <N>]             # atomic field increment (safe)
--post <table>         (--value '<json>' | --value-file <path>)   # auto-gen key (safe — append)
--delete-record <table>/<key>                              # ⚠ DESTRUCTIVE — requires confirmation
--list <table> [--limit N] [--after <key>] [--all]         # list; --all follows cursors (safe)
```

### Options

```
--user <username>        # override auto-discovered username (rare)
--value-file <path>      # read the JSON value from a file (useful for long values)
```

### `--put` vs `--patch` vs `--post`

| Method | Body shape | Does what |
|---|---|---|
| `PUT /:table/:key` | `{value: <JSON>}` | Creates or **fully replaces** the record |
| `PATCH /:table/:key` | `{value: <partial JSON>}` | Deep-merges the partial JSON into the existing object record; scalar/array values are replaced wholesale. Both existing and new value **must** be objects, else 400 `PATCH_NOT_OBJECT` |
| `POST /:table` | `{value: <JSON>}` | Server generates a fresh key (like `rec_xxxxxx`). Use for append-only logs, comments, events |

> **For counters / reactions: use `--incr` (HTTP `POST /:table/:key/incr`), not `--patch`.** PATCH is read-modify-write and can lose concurrent updates. `incr` is atomic (Redis-backed).

---

## 5. Quotas and rate limits

If a request hits a limit, the API returns HTTP **413** or **429** with an error code.

### Per-user quotas (hard, enforced at write time)

| Limit | Value | Error if exceeded |
|---|---|---|
| Tables per user | 50 | `TOO_MANY_TABLES` (413) |
| Records per table | 10 000 | `TABLE_FULL` (413) |
| Serialized JSON size per record | 64 KB | `VALUE_TOO_LARGE` (413) |
| Total bytes across all user tables | 50 MB | `USER_QUOTA_EXCEEDED` (413) |

### Rate limits (public tables only, per client IP)

| Limit | Scope | Error |
|---|---|---|
| Writes per minute, per table | 60 | `RATE_LIMITED` (429) |
| Writes per minute, all public tables combined | 600 | `RATE_LIMITED` (429) |
| Reads per minute, per table | 600 | `RATE_LIMITED` (429) |

`read-public` reads and any operation on `private` tables are **not IP-rate-limited** (they require a token, which is already a bottleneck).

---

## 6. Error code → action mapping

When the user reports an error (or you see one while debugging), look here first.

| Error code | HTTP | Root cause | What to do |
|---|---|---|---|
| `TABLE_NOT_FOUND` | 404 | Table doesn't exist **or** caller has no right to see it (private table + non-owner) | Owner: run `--list-tables`. If missing, `--create-table`. Non-owner: this always means "nothing to see here". |
| `RECORD_NOT_FOUND` | 404 | Key doesn't exist in that table | Run `--list <table>` to see what keys are there |
| `TABLE_EXISTS` | 409 | `--create-table` name collides | Pick a different name or `--update-permission` on the existing one |
| `PERMISSION_DENIED` | 403 | Token's owner doesn't match the subdomain host; or writing to a `read-public` table without a valid owner token | If using CLI: someone else's `sk_` is cached — fix `keys.local.json`. If in browser: use a `public` table for the endpoint. |
| `UNAUTHORIZED` | 401 | Missing/invalid Bearer token on an endpoint that needs one | Check `keys.local.json` token is correct |
| `INVALID_TABLE_NAME` | 400 | Name fails regex `[a-z0-9][a-z0-9_-]{0,62}[a-z0-9]`, or is reserved (`tables`) | Rename. Lowercase, hyphen/underscore OK, no leading/trailing symbol, 2-64 chars |
| `INVALID_KEY` | 400 | Key fails regex `[A-Za-z0-9][A-Za-z0-9._-]{0,126}[A-Za-z0-9]` (or single char) | Use URL-safe chars, 1-128 length, no slashes |
| `INVALID_VALUE` | 400 | Value is not JSON-serializable, or nests > 16 deep | Remove `undefined`/functions, flatten structure |
| `INVALID_PERMISSION` | 400 | Not one of `private | read-public | public` | Fix the `--permission` value |
| `INVALID_BODY` | 400 | Missing `name` or `value` in body | Re-check payload |
| `INVALID_QUERY` | 400 | `limit` isn't a positive integer | Fix `--limit` value |
| `VALUE_TOO_LARGE` | 413 | Record > 64 KB | Split across multiple records (one "parent" + N "children" keys), or move large content to a Clawpage HTML page and store only the URL |
| `TABLE_FULL` | 413 | Hit 10 000 records | Create a sharded table (e.g., `comments-2026`, `comments-2027`), or archive old records via `--export` + delete |
| `TOO_MANY_TABLES` | 413 | Hit 50 tables | Consolidate or delete unused tables |
| `USER_QUOTA_EXCEEDED` | 413 | Hit 50 MB total | Same — delete or archive |
| `RATE_LIMITED` | 429 | Too many public writes/reads from one IP | Back off + retry; in browser, debounce the user action (throttle to 1/sec) |
| `PATCH_NOT_OBJECT` | 400 | PATCH used but existing value or patch payload isn't a plain object | Use `--put` for full replace; only `--patch` object-shaped values |
| `INCR_NOT_OBJECT` | 400 | `--incr` called on a record whose value is not a JSON object (e.g., array or scalar) | Use PUT first to set value to an object, or pick a different record |
| `INCR_FIELD_NOT_NUMBER` | 400 | The target field already exists but is not a number | Rename the field, or PUT a new shape |

---

## 7. Schema design rules (follow these to stay within quotas and scale gracefully)

1. **One record per "thing"**, not one record per entity collection. ❌ Don't: `{key: "all-comments", value: [100 comments]}` → will hit 64 KB fast and can't be concurrently appended. ✅ Do: `{key: "rec_abc", value: {comment}}`, one record per comment; use `--post` for auto-keying.
2. **Keys should be slugs or short IDs.** Prefer `rec_xxx` (auto-generated via POST) or URL-safe slugs like `2026-04-17-hello`. The API rejects slashes, spaces, and most punctuation.
3. **Denormalize freely.** Storage is cheap (50 MB is huge for KV). Want to show author name with each comment? Copy it into the comment value, don't "join".
4. **Group by write frequency.** High-churn data (likes, visit counts) should be in separate tables from low-churn data (posts, config). This isolates rate-limit blast radius.
5. **Pre-compute aggregates.** No query filtering is available. If you want "top 10 posts", either list all (fine up to ~1000 rows) or maintain a single `leaderboard` record that the writers update via PATCH.
6. **Avoid unbounded growth within a single record.** `--patch` works on objects, but if a field is an array you keep appending to, the record will eventually hit 64 KB. Switch to one-record-per-item instead.
7. **Plan for pagination.** Lists return `{records, nextCursor}`; default limit 100, cap 500. Use `--list --all` only when you know the table is < ~2000 records.
8. **Keep values shallow.** Max nesting 16 levels. If you have to go deeper, you're probably modeling it wrong.

---

## 8. Evolving data shape (multi-round iteration)

When you add a field to existing records, there are three clean options:

1. **Tolerant readers**: have the HTML side treat missing fields as `undefined`/default. No migration needed. (Best default.)
2. **Lazy migration**: on each write, re-put with the new field. Old records keep the old shape until touched.
3. **Eager migration** (for small tables): CLI script `export` → edit JSON locally → `import`. Example:
   ```bash
   npx -y @clawpage.ai/cli data --export posts --out posts.json
   # edit posts.json — add fields, reshape, etc.
   npx -y @clawpage.ai/cli data --import posts --in posts.json  # bulk upsert
   ```

For removing a field, nothing is required — old data carries the extra key harmlessly until overwritten.

For **renaming** a field, always do `export → rewrite → import` as one atomic-feeling step.

---

## 9. Security playbook

| Rule | Why |
|---|---|
| **Never write `sk_` token in HTML/JS that ships to the browser** | Anyone who opens DevTools gets full account control |
| `public` tables are genuinely public for writes — use them only where spam isn't fatal | Rate limit is IP-based, 60/min/IP; a determined attacker from 100 IPs can still pump 6000/min |
| For any "only I should write" endpoint, keep writes in the CLI or in a server you control | There is no "write token" scoped to a single table (not yet in spec) |
| Don't leak secrets in `value` payloads | All `public` and `read-public` records are readable by anyone who knows the username and table name |
| Treat `private` tables as **owner-only, semi-private** | They're hidden from strangers (returns `TABLE_NOT_FOUND`) but anyone with a valid `sk_` token for that account sees them |

---

## 10. Prompt-level checklist for AI

When the user asks for a feature that implies data, work through this in order:

1. **Can you solve it without data?** (If it's static content → just a Clawpage HTML page, not this skill.)
2. **Who reads and who writes from the browser?** → pick permission level via §2.
3. **Pick a table name** that fits §7.1 regex (lowercase, 2-64 chars, `-` `_` OK, not `tables`).
4. **Decide record shape**. Follow §7: one record per thing; denormalize; small JSON.
5. **Pick write method**:
   - New thing with server-generated key → `POST` / `--post`
   - Creating or replacing by known key → `PUT` / `--put`
   - Atomically incrementing a numeric field (counters, reactions) → `POST /:table/:key/incr` / `--incr`
   - Patching a few fields of an existing object (non-counter) → `PATCH` / `--patch`
6. **Write the HTML using the Browser SDK** (`${CLAUDE_SKILL_DIR}/use-sdk/SKILL.md`):
   - Embed `<script src="https://clawpage.ai/sdk.js"></script>` in `<head>`.
   - Reads/writes go through `new Clawpage().table("<name>")` (`.get`, `.put`, `.patch`, `.post`, `.incr`, `.list`).
   - Raw `fetch('/api/data/...')` in page JS is forbidden.
   - NO `sk_` token in page JS — if a write needs a token, it must happen via CLI or your own backend.
7. **Publish the HTML via the standard Clawpage page publish flow** (the `manage-page` skill, not this one).
8. **Before handing the page to the user**, test each interaction end-to-end (create table, post, read back).
9. If the user later wants to evolve the data shape, revisit §8 for the migration path.

---

## 11. Not-supported (route around these)

- **File uploads** (images, PDFs) — store outside Clawpage (e.g., a CDN URL) and save the URL in the record
- **Full-text search** — fetch full table client-side and filter in JS for small tables
- **Relational queries** — denormalize; accept duplication
- **Real-time subscriptions** — poll with `setInterval`; or build a WebSocket elsewhere
- **Per-record TTL / expiry** — not available; either clean up via CLI cron, or encode an `expireAt` in the value and filter client-side
- **Transactions across multiple records** — the API only guarantees atomicity for a single PUT/PATCH on one record
