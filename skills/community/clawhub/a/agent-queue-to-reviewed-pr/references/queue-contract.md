# The queue/ack HTTP contract

The agent is the easy part. This surface is what makes the loop safe.

**What you supply.** This skill specifies the four endpoints and consumes them; it ships no adapter. Either your board speaks this contract directly, or you write the thin translation in front of it (an issue tracker's REST API, a Redis list, a spreadsheet — the agent never knows the difference). The mapping you owe it: your priority field → `column` P0..P3, your workflow states → `ready` / `pr-opened` / `needs-grounding`, and a server-side total order → `globalOrder`.

## Auth — all endpoints

`Authorization: Bearer ${AGENT_API_TOKEN}`, compared **timing-safe** (`crypto.timingSafeEqual` in Node, `hmac.compare_digest` in Python). Missing/wrong → `401`, no body detail.

Use a token dedicated to the agent, distinct from your inbound-webhook secret and from any forge token. Rotating one must not silently disable the others.

## `GET ${QUEUE_URL}` — read-only, safe to poll

```jsonc
{
  "ok": true,
  "count": 2,
  "arrangementUpdatedAt": "2026-07-16T09:00:00.000Z",
  "tickets": [
    {
      "id": "tkt-401",
      "title": "Filter invoices by status",
      "prompt": "Read CLAUDE.md AND AGENTS.md at the root of app-example first…",  // the anchored brief
      "summary": "…",
      "status": "ready",
      "column": "P0",
      "priority": "P0",
      "order": 0,          // index inside the column
      "globalOrder": 0,    // total order across the board; 0 = process first
      "source": "<channel>"  // where the request came in; a label, never an identity
    }
  ]
}
```

| Field | Contract |
|---|---|
| `source` | An opaque channel label (`board`, `support`, `<channel>`). **Never a requester identity.** Whatever intake you put in front of the queue, strip personal identifiers there: nothing downstream needs them, and everything downstream stores them. |
| `globalOrder` | Computed **server-side**: walk P0→P1→P2→P3, and inside each column the exact array order of the board arrangement. The drag-and-drop rewrites that array, so reordering the board reorders the queue. The agent never sorts. |
| `status` | Only `ready` cards are listed (your name may differ: `todo`, `queued`, `approved`…). |
| `column` | Only prioritized columns. `INBOX`, `DONE`, `ARCHIVED` are excluded. |
| `arrangementUpdatedAt` | Lets a preflight detect board changes without an LLM. |

**Empty or missing arrangement → empty queue.** Nothing was triaged, so nothing runs. Fail-safe, not fail-open.

### Why "ready" needs two conditions

```
status = ready        AND        column ∈ {P0,P1,P2,P3}
   ↑                                  ↑
grounded by the pipeline        dragged there by a human
```

A card grounded but left in INBOX is **invisible**. The human triage gate costs one drag and removes an entire class of "the agent worked on something it shouldn't have" incidents.

## `POST ${ACK_URL}` — conditional + idempotent

Body: `{ "card_id": string, "pr_url": string(url) }`. Transition `ready → pr-opened`.

| Case | Response |
|---|---|
| OK | `200 {"ok":true,"status":"pr-opened","pr_url":"…"}` |
| Already acked (race, or crash-then-retry) | `200 {"ok":true,"idempotent":true,"status":"pr-opened","pr_url":"…"}` |
| Unknown id | `404 {"ok":false,"error":"unknown_card"}` |
| Bad/missing Bearer | `401` |

Server-side, the write must be **conditional on the current status** — this is the strongest anti-duplicate lock:

```sql
update tickets set status = 'pr-opened', pr_url = $2
where id = $1 and status = 'ready';
-- 0 rows affected → already consumed → answer idempotent:true, do NOT error
```

If you write `where id = $1` without the status predicate, you have no lock at all: two overlapping runs both "succeed" and you get two PRs.

## `POST ${GROUNDING_ACK_URL}` — the quality gate

Body: `{ card_id, payload: { context, impact, definition, technical, risks[, title] }, prompt }`.
Transition `needs-grounding → ready` (conditional, idempotent, non-destructive merge of `payload`).

| Case | Response |
|---|---|
| OK | `200 {"ok":true,"status":"ready"}` |
| Already grounded | `200 {"ok":true,"idempotent":true}` |
| Gate failed | `400 {"ok":false,"error":"grounding_too_thin"}` |
| Unknown id / bad Bearer | `404` / `401` |

The gate predicate, **identical on client and server** — same checks, same canonical order (prefix → length → technical → definition), so the two sides also fail with the same message:

```
prompt.startsWith(MANDATED_PREFIX)   // exact string, no normalization, no trim
&& prompt.length >= 3000             // a floor against the empty brief, not a quality metric
&& payload.technical.trim() != ""
&& payload.definition.trim() != ""
```

`MANDATED_PREFIX` carries your real repo name, substituted identically in the server, in the brief, and in `BRIEF_GATE_PREFIX` for the local script. A placeholder left in any one of the three fails every card.

Client-side you fail before spending a network call. Server-side because your endpoint cannot assume the client is polite — the next caller will be a retry script or a hand-written curl.

## `POST ${STALE_ACK_URL}` — the only write a drift watcher gets

Body: `{ card_id, reason, commit }`. Conditional flip `ready → needs-grounding`.

| Server state | `action` returned |
|---|---|
| still `ready` | `"auto_flipped"` → the grounding link will re-enrich it |
| `pr-opened` | `"check_pr"` + `pr_url` — **never re-ground a card that already has a PR**; point a human at the PR instead |
| anything else | idempotent / skipped — do not force |

Never issue raw SQL from the agent. One conditional endpoint, one predicate, one place to audit.

## Client scripts — the two rules

```bash
# 1. Fail loudly on non-2xx: -f. Never let a 401 look like an empty queue.
curl -fsS --max-time 30 "${QUEUE_URL}" -H "Authorization: Bearer ${AGENT_API_TOKEN}"

# 2. Never concatenate user-controlled text into JSON.
body="$(python3 -c 'import json,sys; print(json.dumps({"card_id":sys.argv[1],"pr_url":sys.argv[2]}))' "$1" "$2")"
```

A ticket title with a quote in it will break a hand-built JSON body, and the failure looks like a server bug for an hour.

## Deploy gate — assert before going autonomous

```bash
curl -s -o /dev/null -w "%{http_code}\n" "${QUEUE_URL}"                                  # Output: 401
curl -s -o /dev/null -w "%{http_code}\n" "${QUEUE_URL}" -H "Authorization: Bearer ${AGENT_API_TOKEN}"  # Output: 200
```

A desynchronized secret produces a `401` that a swallowing client reports as "empty queue": the loop looks healthy and does nothing, for days. Assert both codes.
