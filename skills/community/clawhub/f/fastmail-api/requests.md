# Request Envelopes, Back-References, and Batching

One POST to `apiUrl` can carry a whole workflow. Getting the envelope right is what turns six round trips into one, and what makes a failure legible instead of mysterious.

**Before building anything beyond a single call**, read the observed limits line in `## Account Map` of `~/Clawic/data/fastmail-api/memory.md` — batch sizes are derived from it, not guessed. **After a `limit` problem type or any change in those numbers**, update that line in the same turn (`memory-template.md`); a stale limit produces the same failed envelope every time.

**Contents:** [The Envelope](#the-envelope) · [Back-References](#back-references) · [ifInState and Optimistic Concurrency](#ifinstate-and-optimistic-concurrency) · [Patch Objects](#patch-objects) · [Reading the Response](#reading-the-response) · [Batch Sizing](#batch-sizing) · [Retry Discipline](#retry-discipline)

## The Envelope

```json
{
  "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
  "methodCalls": [
    ["Email/query", {"accountId": "u1a2b3c4", "filter": {"inMailbox": "Mb1001", "notKeyword": "$seen"},
                     "sort": [{"property": "receivedAt", "isAscending": false}], "limit": 50}, "c0"],
    ["Email/get", {"accountId": "u1a2b3c4",
                   "#ids": {"resultOf": "c0", "name": "Email/query", "path": "/ids"},
                   "properties": ["id", "threadId", "subject", "from", "receivedAt", "keywords", "mailboxIds"]}, "c1"]
  ]
}
```

Three things carry weight:

- **`using`** — exactly the capabilities this request needs, all of them present in `session.capabilities` (`session.md`). A missing one fails the whole envelope.
- **`accountId`** — on every call, every time. There is no ambient account; a call without it is an error, and a call with the wrong one is worse.
- **The third element is the call id** — your label, echoed in the response. Make it meaningful (`c0`, `query-unread`, `set-archive`) because with eight calls in an envelope the id is how you find your result. Responses come back in the order the server processed them, which for independent calls is the order you sent, but you match on the id, never on position.

**`properties` is not optional discipline.** `Email/get` without it returns everything including body parts, which on 50 messages can exceed `maxSizeRequest` on the way back and always wastes context. Ask for the fields you will read.

## Back-References

A back-reference feeds the output of one call into the input of the next, inside the same request:

```json
["Email/get", {"accountId": "u1a2b3c4",
               "#ids": {"resultOf": "c0", "name": "Email/query", "path": "/ids"}}, "c1"]
```

- The argument name is prefixed with `#`, and the plain form of that argument must be absent — `ids` and `#ids` together is an error.
- `resultOf` is the **call id**, `name` is the **method name** of that response, and `path` is a JSON pointer into its arguments. Get any of the three wrong and you get `invalidResultReference`, which looks like a permissions failure to anyone who has not seen it before.
- Common pointers: `/ids` from a `/query`; `/list/*/id` to collect ids from a `/get`; `/created/<creationId>/id` to use the id of something you just created; `/list/*/threadId` to jump from messages to threads.
- A creation id (`#sendIt`) is the other kind of reference — inside one `/set`, `"#creationId"` refers to an object created earlier in the same call. Used constantly in `sending.md`.

Why this matters beyond speed: two round trips are two server states. Between your query and your fetch, mail arrives, the user archives something from their phone, and your id list is fiction. One envelope is one consistent view.

## ifInState and Optimistic Concurrency

Every `/set` accepts `ifInState`, and every `/get` and `/query` returns the `state` to feed it.

```
read state s1  →  build the write with ifInState: s1  →  server applies it only if nothing changed
```

- Without `ifInState`, a write applies to whatever exists now, including messages that moved since you looked. That is how "archive these 40" archives 40 different messages.
- On `stateMismatch`: **re-run the query, re-derive the ids, rebuild the payload.** Replaying the same payload against the new state is the exact mistake the error exists to prevent.
- State strings are opaque. Never parse, compare, order, or truncate them. Store them verbatim in `## Sync State` when they are part of a mirror (`sync.md`).
- `oldState` and `newState` come back from a successful `/set` — the new one is what the next write uses.

## Patch Objects

An `update` map takes either a whole property or a JSON-pointer patch, and **never both for the same property in the same object**:

```json
"update": {
  "M8f21": {"mailboxIds/Mb1002": true, "mailboxIds/Mb1001": null, "keywords/$seen": true}
}
```

- `true` adds, `null` removes. This is the entire vocabulary for set-valued properties like `mailboxIds` and `keywords`.
- `{"mailboxIds": {"Mb1002": true}}` **replaces** the whole set — every other mailbox membership disappears. That is occasionally what you want and almost never what was intended.
- Mixing `mailboxIds` and `mailboxIds/Mb1002` in one update object is rejected outright.
- A patch to a property that does not exist yet creates it; a patch removing the last member of `mailboxIds` is invalid, because a message must live somewhere. To make it vanish, that is `destroy` (SKILL.md Rule 6).

## Reading the Response

Three levels of failure, and they are not interchangeable:

| Level | Shape | Means |
|---|---|---|
| HTTP | Status code, `problem+json` body | Transport or token: `401`, `403`, `404` on a wrong URL |
| Request | A problem type: `notJSON`, `notRequest`, `unknownCapability`, `limit` | The envelope is wrong. No method ran |
| Method | `["error", {"type": "..."}, "c1"]` in `methodResponses` | That call failed. Earlier calls in the envelope still ran |
| Object | `notCreated` / `notUpdated` / `notDestroyed`, keyed by id, each a `SetError` | Some objects failed. The rest were written |

Method calls in an envelope are **not a transaction**. If call `c2` fails, `c0` and `c1` have already happened. When a sequence must not half-apply, either put it in one `/set` (which is atomic per object, not per call) or order the calls so the irreversible one is last.

`SetError` types worth recognizing on sight: `notFound` (the id is gone or belongs to another account), `invalidProperties` (with a `properties` list naming which), `stateMismatch`, `forbidden`, `overQuota`, `tooLarge`, `rateLimit`, `willDestroy` (referenced an object destroyed in the same call), `invalidPatch`.

Report both sides. "1,840 updated, 2 failed with `notFound`" is a result; "done" is not.

## Batch Sizing

```
batch = min(max_batch_size from config, the account's maxObjectsInSet)
calls per envelope ≤ maxCallsInRequest
envelope bytes ≤ maxSizeRequest
in-flight requests ≤ maxConcurrentRequests
```

- On a long id list, `maxSizeRequest` binds before `maxObjectsInSet` does: an id is ~20-30 bytes, so tens of thousands of ids is a megabyte-scale envelope. Split by byte budget, not only by count.
- **First batch is always one object.** It costs one round trip and it catches the malformed patch, the wrong mailbox id, and the read-only account before 1,800 objects find out.
- A request-level `limit` problem type names which limit in its `limit` property. Read it and fix that dimension; halving the batch when the real problem is `maxConcurrentRequests` changes nothing.
- Serial batches with a verify call between them beat parallel batches. Parallelism against a mailbox you are also mutating produces `stateMismatch` storms.

## Retry Discipline

| Situation | Retry? |
|---|---|
| Network timeout, `503`, `serverUnavailable` | Yes — exponential backoff with jitter, bounded attempts |
| `rateLimit` SetError or `limit` problem type | Yes, after reducing the dimension named; backoff, never tighter loops |
| `stateMismatch` | Not the same payload — re-query first, then write |
| `invalidArguments`, `invalidProperties`, `invalidResultReference` | No. The payload is wrong; retrying it is wrong the same way |
| `accountReadOnly`, `forbidden`, `unknownCapability` | No. These are grants, not conditions |
| `overQuota` | No, until space is freed — otherwise every retry fails identically |
| A `/set` whose response never arrived | **Check before retrying.** `/set` is not idempotent: a repeated `create` makes a second object, a repeated `destroy` returns `notFound` harmlessly. Query for the created object first |

Log every retried batch into `operations/<year>.md` with the attempt count. A batch that needed four attempts is telling you the batch is too big.
