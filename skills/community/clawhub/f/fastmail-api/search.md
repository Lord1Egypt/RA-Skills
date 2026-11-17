# Finding Messages

`Email/query` returns ids in an order, nothing else. Every mistake in this file comes from forgetting that: ids are a snapshot of a server-side sort, and what you do with them depends entirely on how the query was shaped.

**Before writing a filter from scratch**, read `## Saved Queries` in `~/Clawic/data/fastmail-api/memory.md` — or `queries.md` if `## Boxes` points there. The filter that already exists encodes the traps someone already hit. **After a filter takes more than one attempt to get right**, save it there with its name, its JSON, what it is for, and which fields must be recomputed at run time (`memory-template.md`).

**Contents:** [Filter Conditions](#filter-conditions) · [Combining Conditions](#combining-conditions) · [Sorting](#sorting) · [Threads and collapseThreads](#threads-and-collapsethreads) · [Pagination That Survives New Mail](#pagination-that-survives-new-mail) · [Counting Before Acting](#counting-before-acting) · [Search Snippets](#search-snippets) · [Query Recipes](#query-recipes)

## Filter Conditions

A `FilterCondition` is a flat object; every property in it must match.

| Condition | Matches |
|---|---|
| `inMailbox` | Messages in that mailbox id. One id, not a list |
| `inMailboxOtherThan` | A **list** of ids to exclude — the way to say "anywhere but Trash and Junk" |
| `before` / `after` | `receivedAt` bounds, UTC date-time. `before` is exclusive of the instant given |
| `minSize` / `maxSize` | Total message size in octets |
| `hasKeyword` / `notKeyword` | One keyword. `$seen`, `$flagged`, `$draft`, `$answered`, `$forwarded`, `$junk`, `$notjunk` |
| `allInThreadHaveKeyword` / `someInThreadHaveKeyword` / `noneInThreadHaveKeyword` | Thread-level keyword tests — this is how "unread threads" differs from "unread messages" |
| `hasAttachment` | Boolean, server's own notion of a real attachment (inline images generally do not count) |
| `text` | Free text across from, to, cc, bcc, subject, and body |
| `from` / `to` / `cc` / `bcc` / `subject` / `body` | Substring match on that field. `from: "@acme.example"` matches a whole domain |
| `header` | `["Header-Name"]` for existence, `["Header-Name", "value"]` for a match — the reliable way to catch bulk mail via `List-Unsubscribe` or `List-Id` |

Two distinctions that decide correctness:

- **`from: "acme"` is a substring, not an address match.** It hits `acme@example.com`, `noreply@acme.example`, and `not-acme-really@example.com`. For a domain, anchor with `@`; for an exact sender, filter loosely then verify on the fetched `from` field.
- **`before`/`after` are on `receivedAt`, not on the `Date:` header.** A message forwarded from an old archive was received today. For "older than 90 days", compute the timestamp at run time — a stored filter with a literal date silently narrows every quarter (`queries.md`).

## Combining Conditions

`FilterOperator` nests conditions: `{"operator": "AND" | "OR" | "NOT", "conditions": [...]}`.

```json
{"operator": "AND", "conditions": [
  {"inMailbox": "Mb1001"},
  {"notKeyword": "$seen"},
  {"operator": "NOT", "conditions": [{"from": "@acme.example"}]}
]}
```

- `NOT` takes a list and means "none of these match".
- A flat condition object already ANDs its properties, so `{"inMailbox": X, "notKeyword": "$seen"}` needs no operator. Reach for `FilterOperator` only when you need `OR` or `NOT`.
- Deeply nested filters get slower and harder to read; when a filter needs four levels, the honest answer is usually two queries and a set intersection you do yourself.

## Sorting

`sort` is a list of comparators, applied in order:

```json
"sort": [{"property": "receivedAt", "isAscending": false}]
```

- **Always specify it.** An unsorted query returns an unspecified order, which makes pagination meaningless and makes "the 50 oldest" a coin flip.
- Which properties are sortable is per account: `emailQuerySortOptions` in the mail capability (`session.md`). An unsupported property fails the query rather than falling back.
- Comparators worth knowing: `receivedAt`, `size`, `from`, `to`, `subject`, and keyword-based sorts like `hasKeyword` with the keyword named — the last is how "flagged first" is expressed without a second query.
- Multi-comparator sorts break ties deterministically, which is what makes an `anchor` cursor stable.

## Threads and collapseThreads

`"collapseThreads": true` returns **one email id per thread** — the most relevant message of each. It is the right shape for showing the user a list. It is the wrong shape for writing.

| Goal | Query shape | Then |
|---|---|---|
| Show the user their conversations | `collapseThreads: true` | Display; do not write to these ids |
| Act on every message of matching threads | `collapseThreads: true`, then `Email/get` for `threadId`, then `Thread/get` | Write to the full `emailIds` of each thread |
| Act on exactly the matching messages | `collapseThreads: false` | Write directly |
| "Archive this whole conversation" | Thread-level keyword filters (`someInThreadHaveKeyword`) + `Thread/get` | The user means the thread; the query must too |

The signature failure: a batch reports "340 threads archived", the user still sees the conversations in their inbox, and the log shows 340 successful updates. Every one of them moved one message out of a multi-message thread.

## Pagination That Survives New Mail

| Cursor | How | When it breaks |
|---|---|---|
| `position` | Integer offset from the start of the result list | New mail arriving shifts every offset — you skip messages and process others twice |
| `anchor` + `anchorOffset` | Server finds the anchor id in the result list and counts from there | Only if the anchor itself leaves the result set |

For anything larger than one page, or anything running against a live inbox, use the anchor form: pass the last id of the previous page as `anchor` with `anchorOffset: 1`. Negative `position` counts back from the end, which is a neat way to get the oldest N without sorting ascending — and just as fragile under concurrent change.

`limit` is capped by the server; the response's `position`, `total` (when requested) and `ids.length` tell you where you actually landed. Never assume you got `limit` items.

## Counting Before Acting

`"calculateTotal": true` makes the response include `total`, the full size of the result set regardless of `limit`. It costs the server more, so it is not a default — but it is exactly what SKILL.md Rule 5 requires before a bulk write, and one extra round trip is cheaper than an unbounded batch.

Two numbers are needed before any destructive operation and they are different: **how many objects match** (from `total`) and **how many will actually change** (matches that are not already in the target state). Archiving 1,842 messages of which 1,700 are already archived is a 142-message operation being reported as 1,842.

For a coarse count without a query, `Mailbox/get` carries `totalEmails` and `unreadEmails` per mailbox — free, already there, and enough to answer "how big is this mailbox" without touching `Email/query` at all.

## Search Snippets

`SearchSnippet/get` takes the same `filter` plus a list of email ids and returns highlighted fragments of subject and body. Its use is showing the user *why* something matched before they approve a bulk action on it — a purge of 1,800 messages is much easier to confirm when five snippets show they are all shipping notifications.

The filter passed to `SearchSnippet/get` must be the same one used in the query, or the highlights point at nothing.

## Query Recipes

Each one is a filter, not a whole request; wrap it per `requests.md` and pair with `Email/get` through a back-reference.

| Goal | Filter |
|---|---|
| Unread in Inbox | `{"inMailbox": "<inbox>", "notKeyword": "$seen"}` |
| Anything not already filed away | `{"inMailboxOtherThan": ["<archive>", "<trash>", "<junk>"]}` |
| Bulk mail, whoever sent it | `{"header": ["List-Unsubscribe"]}` |
| From one domain, threads intact | `{"from": "@acme.example"}` with `collapseThreads: false` |
| Big messages eating quota | `{"minSize": 10000000}` sorted by `size` descending |
| With real attachments, last quarter | `{"hasAttachment": true, "after": "<computed>"}` |
| Threads where nothing was ever answered | `{"noneInThreadHaveKeyword": "$answered", "inMailbox": "<inbox>"}` |
| Flagged but read — the forgotten pile | `{"operator": "AND", "conditions": [{"hasKeyword": "$flagged"}, {"hasKeyword": "$seen"}]}` — one condition object cannot hold two `hasKeyword` values |
| Old and unread — the purge candidate set | `{"inMailbox": "<inbox>", "notKeyword": "$seen", "before": "<today − 90d>"}` |
| Sent to an address that should not be receiving mail | `{"to": "<masked address>"}` — the audit half of `masked-email.md` |
| Anything else | Start from the closest recipe, add one condition, and check `total` before adding another |
