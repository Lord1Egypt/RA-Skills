# Symptom to Cause

Start by identifying which layer produced the message. Half of JMAP debugging is people widening a token to fix an envelope error.

**Before diagnosing**, read `## Pain Points` in `~/Clawic/data/fastmail-api/memory.md` — a failure this setup has hit before usually has the same cause. **After diagnosing anything non-obvious**, write one line there with the date, the symptom and the actual cause; if the fix is a repeatable procedure, it becomes `artifacts/<name>.md` with its `## Boxes` line (`memory-template.md`). A cause found twice was written down zero times.

**Contents:** [Which Layer](#which-layer) · [Authentication and Scope](#authentication-and-scope) · [Envelope Errors](#envelope-errors) · [Method Errors](#method-errors) · [SetError Reference](#seterror-reference) · [Nothing Errored But Nothing Happened](#nothing-errored-but-nothing-happened) · [Slow and Timing Out](#slow-and-timing-out) · [Sending Problems](#sending-problems) · [When the Answer Is Not Here](#when-the-answer-is-not-here)

## Which Layer

| Where it appears | Layer | What it is about |
|---|---|---|
| HTTP status + `problem+json` | Transport | The token, the URL, the connection |
| A problem type with no `methodResponses` | Request | The envelope: JSON, `using`, size, call count |
| `["error", {...}, "cN"]` inside `methodResponses` | Method | That one call. Earlier calls already ran |
| A `SetError` under `notCreated`/`notUpdated`/`notDestroyed` | Object | One object. The rest of the batch succeeded |
| No error at all, wrong outcome | Logic | The query, the patch shape, or the account |

Read them in that order. A request-level failure means no method ran, so debugging the method is wasted work.

## Authentication and Scope

| Symptom | Cause | Move |
|---|---|---|
| `401` on the session endpoint | Token invalid, revoked, or the header is missing `Bearer ` | Check the header shape first; it is the more common of the two |
| `401` on `apiUrl`, session works | Hardcoded or stale `apiUrl` | Take it from the live session every time (`session.md`) |
| `unknownCapability` | The URN is not in `session.capabilities` | Token scope. A new token is the only fix; the payload cannot grant it |
| `403` on an operation that used to work | Scope changed, or the account grant changed | Re-read the session; compare against `## Account Map` |
| `accountNotFound` | The `accountId` is from another token, another account, or an example | Re-resolve from `accounts` / `primaryAccounts` |
| `accountReadOnly` | Delegated read-only grant | `isReadOnly` said so before the call; no retry helps |
| `accountNotSupportedByMethod` | Account lacks the capability the token has | Per-account `accountCapabilities`, not the top-level list |
| Everything 401s suddenly, nothing changed | Token expired or was revoked elsewhere | Re-issue; then revoke the old one rather than leaving it live |

The distinction that saves the most time: **`401` is the token, `unknownCapability` is the token's scope, `accountReadOnly` is the grant on one account.** All three get called "auth problems" and only the first is one.

## Envelope Errors

| Problem type | Cause | Move |
|---|---|---|
| `notJSON` | Body is not valid JSON — usually shell quoting around a `-d` payload | Write the payload to a file and post the file |
| `notRequest` | Valid JSON, wrong shape — missing `using` or `methodCalls`, or `methodCalls` is not a list of triples | Every call is exactly `[name, arguments, callId]` |
| `unknownCapability` | See above | — |
| `limit` | One of `maxSizeRequest`, `maxCallsInRequest`, `maxConcurrentRequests` | The `limit` property names which; fix that dimension, not batch size by reflex (`requests.md`) |

`limit` with `maxConcurrentRequests` deserves its own note: it means too many requests in flight, so the fix is serializing, and reducing batch size makes it strictly worse by producing more requests.

## Method Errors

| Error type | Cause | Move |
|---|---|---|
| `invalidArguments` | An argument is missing or the wrong type — the response usually names it | Read the named argument; do not rebuild the whole call |
| `invalidResultReference` | A back-reference `resultOf`, `name`, or `path` does not resolve | Check the JSON pointer against the actual previous response (`requests.md`) |
| `unknownMethod` | Method does not exist for that capability version | Often a contacts object-model mismatch (`contacts.md`) |
| `stateMismatch` | Something changed between read and write | Re-query, re-derive ids, rebuild. Never replay |
| `cannotCalculateChanges` | No delta available from that state | Full resync; retrying returns the same error forever (`sync.md`) |
| `requestTooLarge` | The call itself is oversized | Split by byte budget, not only by object count |
| `serverFail` / `serverUnavailable` | Transient server-side | Bounded retry with backoff and jitter |
| `serverPartialFail` | Some of the call was applied | **Do not retry.** Query the current state and reconcile from what is actually there |

## SetError Reference

Inside `notCreated` / `notUpdated` / `notDestroyed`, keyed by id or creation id:

| Type | Means | Move |
|---|---|---|
| `notFound` | The id does not exist in this account | It was destroyed, moved, or copied from another account |
| `invalidProperties` | The `properties` list names the bad fields | Usually a patch/whole-property mix, or an unknown property name |
| `invalidPatch` | Malformed JSON pointer patch | `mailboxIds` and `mailboxIds/<id>` in the same object is the usual cause |
| `forbidden` | Permission on this object — check `myRights` on the mailbox or calendar | Not a token problem |
| `overQuota` | Account storage full | Nothing writes until space is freed |
| `tooLarge` | Object over the limit | Attachments: recompute with `× 1.33` (`sending.md`) |
| `rateLimit` | Too fast | Back off; smaller batches, not more of them |
| `willDestroy` | Referenced an object destroyed in the same call | Reorder: destroys last |
| `alreadyExists` | Import found the message present | Expected on a resumed import; not a failure (`migration.md`) |
| `singleton` | Tried to create or destroy a singleton object | The object exists and can only be updated |

**Report the distribution, not the first one.** "38 `notFound`, 2 `forbidden`" is a diagnosis: the first group is a stale id list, the second is a permissions boundary, and they need different fixes.

## Nothing Errored But Nothing Happened

The hardest class, because every layer reports success.

| Symptom | Cause |
|---|---|
| Threads still in the Inbox after "340 archived" | `collapseThreads: true` — one message per thread was moved (`search.md`) |
| Messages appear in both mailboxes | Destination added, source never removed (SKILL.md Rule 7) |
| Every keyword except the one you set has vanished | Whole-property write on `keywords` instead of a patch (`triage.md`) |
| Marked as junk, still in the Inbox | Keyword set without the move (`triage.md`) |
| Sent, and still sitting in Drafts | Two separate requests instead of `onSuccessUpdateEmail` (`sending.md`) |
| Filter returns nothing but the mail is visibly there | Wrong account, or `inMailbox` id from another account |
| A "before 90 days" filter matches less every quarter | A literal date stored in a saved query (`search.md`) |
| The mirror stopped updating, no errors anywhere | EventSource connection dropped with no `ping`, or a push subscription expired (`sync.md`) |
| A recurring event edit did nothing | Override keyed to a start time the current rule no longer generates (`calendar.md`) |
| A contact update lost half the card | Whole-object write instead of a patch (`contacts.md`) |

## Slow and Timing Out

- **`Email/get` without `properties`** returns bodies. That is the first thing to check on a slow fetch, before anything server-side is suspected.
- **`calculateTotal: true`** costs real time on a large mailbox. Ask for it when the count matters (before a write), not on every query.
- **Unindexed-shaped filters** — broad `body` text searches across an entire account — are slow by nature. Narrow by mailbox and date first, then text.
- **Parallel requests against a mailbox you are mutating** produce `stateMismatch` storms that look like slowness. Serialize writes.
- A batch that consistently needs several attempts is too big. Halve it once; if that fixes it, record the working size in `## Pain Points`.

## Sending Problems

Full table in `sending.md`. The two-second triage:

- Rejected **before** submission → identity or content: `forbiddenFrom`, `invalidEmail`, `tooLarge`.
- Rejected **after** acceptance → the recipient side. The bounce carries the reason, and SPF/DKIM/DMARC questions are `dns` territory.
- Accepted and delivered but landing in spam → not an API problem at all. Authentication records and sending reputation.

## When the Answer Is Not Here

1. Reproduce with the smallest possible request: one method call, one object, `properties` narrowed.
2. Capture the exact request and the exact response, with the token replaced by `<env:FASTMAIL_API_TOKEN>` before either is shown, saved, or pasted anywhere.
3. Re-run the session call and compare against `## Account Map`: a surprising number of "impossible" failures are a stale account picture (`session.md`).
4. Check the object directly with `/get` on the single id. Half of "the write failed" turns out to be "the write succeeded on an object the user was not looking at".
5. Write the finding into `## Pain Points` with the date, whichever way it resolves.
