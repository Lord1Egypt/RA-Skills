# Incremental Sync and Push

Keeping a local view current without re-downloading the mailbox. Everything here turns on one primitive: the opaque `state` string.

**Before any sync cycle**, read `## Sync State` in `~/Clawic/data/fastmail-api/memory.md` — the stored state per account and type is the difference between a delta and a full download. **After every cycle**, replace the row with the new state and the date, in the same turn; after a forced resync, note the resync date too (`memory-template.md`). A state that is never written down means the next session starts from zero, every time.

**Contents:** [State Strings](#state-strings) · [The Changes Cycle](#the-changes-cycle) · [cannotCalculateChanges](#cannotcalculatechanges) · [queryChanges](#querychanges) · [Choosing Poll, EventSource, or Push](#choosing-poll-eventsource-or-push) · [EventSource](#eventsource) · [Push Subscriptions](#push-subscriptions) · [Building a Mirror That Stays Honest](#building-a-mirror-that-stays-honest)

## State Strings

Every type in every account has a state string, returned by `/get`, `/query`, `/set` and `/changes`.

- **Opaque.** Not a timestamp, not a counter, not sortable. Never parse, compare, order, truncate, or generate one. Storing it verbatim is the entire contract.
- **Scoped to one account and one type.** The `Email` state of account A says nothing about its `Mailbox` state or about account B. `## Sync State` therefore has one row per pair.
- **`/set` returns `oldState` and `newState`.** After a write of your own, the new state is already in hand — a `/changes` call to discover your own change is a wasted round trip.
- The session object has its own `state` for "has the account/capability picture changed" (`session.md`), unrelated to type states.

## The Changes Cycle

```
stored state  →  Foo/changes(sinceState)  →  created / updated / destroyed ids + newState
              →  Foo/get for the ids you care about  →  store newState
```

The response carries:

| Field | Use |
|---|---|
| `oldState` | Echo of what you asked from |
| `newState` | Store this, but only after processing the ids |
| `created` / `updated` / `destroyed` | Id lists; a `destroyed` id may already be unknown to you and that is fine |
| `hasMoreChanges` | **Loop while true**, feeding `newState` back in. Stopping at the first page silently loses changes |
| `updatedProperties` | On `Email/changes`, sometimes names which properties changed — lets you skip a `/get` when it is only `keywords` |

- Chain `/changes` and `/get` in one envelope with a back-reference on `/created/*` and `/updated/*` (`requests.md`).
- **Store `newState` only after the fetched objects are safely processed.** Storing it first and then failing means those changes are never seen again — the state has moved past them and there is no way back.
- `Mailbox/changes` matters as much as `Email/changes`: a mailbox renamed, created, or destroyed invalidates ids in `## Mailbox Map`.

## cannotCalculateChanges

The server cannot produce a delta from the state you gave — usually because it is older than the change history kept, or the type does not support deltas from that point.

- **Retrying is futile.** The same call returns the same error forever. There is no backoff that fixes it.
- The only correct response is a **full resync**: re-query the current set, reconcile against the local mirror, store the fresh state.
- Reconciliation is not "download everything and overwrite". Compare id sets: ids present locally and absent remotely were destroyed; ids present remotely and absent locally are new; the rest need their changed properties fetched.
- Note the resync and its date in `## Sync State`. A mirror that resyncs weekly is not synced, it is polled expensively, and the cadence is the signal to change the design.

## queryChanges

`Foo/queryChanges` answers "how did *this filtered list* change", which is not the same question as "what objects changed".

- Takes the query's own state plus `upToId`, returns `removed` and `added` (with positions) for that result set.
- Support is conditional: some filters and sorts cannot be diffed and return `cannotCalculateChanges` immediately. Fall back to re-running the query — for a bounded, sorted list that is cheap.
- Use it for a live view of one list (an inbox pane, a saved search). For a full mirror, `/changes` is the right primitive.

## Choosing Poll, EventSource, or Push

| Approach | Latency | Cost | Fails by |
|---|---|---|---|
| Scheduled `/changes` poll | The interval | One request per cycle | Nothing surprising; it just lags |
| EventSource | Seconds | A held-open connection | Disconnects that are not noticed |
| Push subscription | Seconds | A public endpoint plus a verification handshake | Never delivering, silently, if unverified |

Decision rule: **sub-minute freshness required → EventSource or push; anything looser → poll.** A 15-minute poll on a personal mailbox is invisible to the user and has no failure mode worth debugging. Reach for push when something else must react immediately, not because it is more sophisticated.

Whichever is chosen, `/changes` still does the work — notifications carry state strings, never content.

## EventSource

A long-lived GET on the session's `eventSourceUrl`, a URI template with three parameters:

| Parameter | Meaning |
|---|---|
| `types` | Which types to be told about, or `*` for all |
| `closeafter` | `state` to receive one event and close; `no` to hold the connection |
| `ping` | Interval in seconds for keep-alive comments, so a dead connection is detectable |

- Each event carries the changed types and their **new state strings**. That is the whole payload: no ids, no subjects, no bodies. Act by running `/changes` from your stored state.
- **Set `ping`.** Without keep-alives, a silently dropped connection is indistinguishable from a quiet mailbox, and the mirror stops updating with no error anywhere.
- Reconnect with backoff, and on reconnect run one `/changes` cycle immediately — events during the gap are gone and only the state comparison recovers them.
- The connection carries the bearer token for its whole lifetime. It belongs in a process, not in a shell history line (`memory-template.md`).

## Push Subscriptions

`PushSubscription/set` registers an endpoint the server POSTs to. Two things trip everyone:

1. **Verification is mandatory.** The server sends a `PushVerification` containing a code to the endpoint; the subscription only becomes active once that code is written back to the subscription object. Skip it and the subscription exists, looks fine, and never delivers.
2. **Subscriptions expire.** `expires` is set by the server (and can be requested); a subscription past it stops delivering with no error on your side. Renew before expiry, and keep the fallback poll running.

Push payloads, like EventSource events, contain state strings and type names only. The keys used to encrypt them (`keys.p256dh`, `keys.auth`) and the verification code are credentials: pointer only, never written under `~/Clawic/data/` (`memory-template.md`).

`PushSubscription` objects are visible across the whole token, not per account — an unexplained subscription belongs to some other client and is not yours to destroy.

## Building a Mirror That Stays Honest

1. **Bootstrap**: full query for the scope you mirror, `/get` in pages, store the state per type.
2. **Steady state**: `/changes` loop while `hasMoreChanges`, fetch, process, then store the new state.
3. **Handle destroys as first-class.** An id in `destroyed` that you never had is normal; an id you had and never remove is a ghost that shows up in counts forever.
4. **Reconcile periodically** — a full id-set comparison on a cadence recorded in `## Due`, because deltas drift when a cycle half-fails.
5. **Never mirror bodies you do not need.** Ids, headers and keywords are small; bodies turn a mirror into an unencrypted copy of the mailbox on disk, which the Data rules in `SKILL.md` do not permit by default.
6. **One mirror per account.** Merging accounts into one local store loses the account scoping that keeps writes safe.
