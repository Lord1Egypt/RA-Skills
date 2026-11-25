# Concept and synchronization examples

These engineering examples use the [tool encoding](tool-encoding.md). Author concepts and synchronizations using the [specification notation](spec-notation.md).
Interfaces and business rules below are teaching choices; confirm product requirements separately.
The tables specify acceptance checks and counterexamples, not executed test results.
Each scenario's specification is a separate file under `assets/examples/`; read only the scenario you need. The files can be passed directly to `concept_lint.py`.

## Scenario index

| Scenario | Focus | Scope |
| --- | --- | --- |
| [Todo](#complete-todo) | State invariants, action contracts, refusal, and repeated calls | Complete local task behavior; no synchronization needed. |
| [Reservation](#partial-reservation-model) | Type binding, request correlation, success/conflict, and usable subsets | Partial model; arrival and purpose fulfillment remain open. |
| [External login](#external-identity-login) | Shared completions, unordered calls and their join, state reads, error cases, and flow isolation | Required interfaces only; timing, retry, and recovery remain open. |
| [Comment cleanup](#expand-calls-over-query-rows) | Zero/many query rows and deletion races | Starts at successful post deletion; concurrent additions remain open. |

## Complete Todo

A trusted caller adds, completes, and reopens local tasks using one CONCEPT and no SYNCS.
Deletion, ordering, UI, external entries, authorization, and durability are outside this example.

Specification: [assets/examples/todo.concept.md](../assets/examples/todo.concept.md)

| Acceptance from fresh state | Expected observation |
| --- | --- |
| _pending before and after add("report") | Zero rows without an error, then exactly the returned task and input text. |
| add to obtain t; complete(t) twice, then reopen(t) twice, querying after each | t disappears, then returns with unchanged text; repeats succeed without duplicate tasks or other changes. |
| complete(unknown) or reopen(unknown) | Missing with unchanged state. |

## Partial reservation model

This fragment covers a selected slot's success or conflict.

Specification: [assets/examples/reservation.concept.md](../assets/examples/reservation.concept.md)

Availability[V] owns local Slot identities and exposes offered slots without reading Reserving:

- `venue: Slot -> V` associates exactly one venue with each slot.
- `offered: set Slot` is a subset of existing slots.
- `_find [venue: V] => [slot: Slot]` returns all matching offered slots, one per row; no match returns zero rows without a completion.

The application's entry contract is:

```markdown
Requesting/reserve: [user: UserId; slot: Availability.Slot] => [request: RequestId]
Requesting/respond: [request: RequestId; reservation: Reserving.Reservation] => []
Requesting/respond: [request: RequestId; error: Conflict] => []
```

Specification: [assets/examples/reservation.syncs.md](../assets/examples/reservation.syncs.md)

| Acceptance or counterexample | Expected observation |
| --- | --- |
| Reserve a free slot, then request it again while booked | The first request gets a reservation; the second gets Conflict without changing existing facts. |
| Entry and reservation completion belong to different flows | Do not use the other flow's result to respond to this request. |
| _find returns zero or several candidates | No rule waits for that query or implicitly reserves its results; candidate selection needs a product decision. |
| Remove Availability but retain Availability.Slot | The subset is unusable; rebind S to an independently supplied SlotId and update entries and rules. |

Discovery requirements, not type binding alone, justify retaining Availability; a known-slot product may need only Reserving.
Offered state can change before reserve and does not enforce a write-time invariant.
Open: arrival inputs/timing and the grant definition (both must be defined and checked before purpose fulfillment is established), cancel/grant refusal conditions, authentication, venue checks, concurrent withdrawal, display, cancellation entries, and fault handling.

## Synchronization scenarios

### External identity login

After verification succeeds, record the identity, then issue the profile and session calls without ordering them.
Return success only after both complete.
Credential is opaque; Text is a string.
Identity means ExternalIdentity.Identity; SessionId means Session.SessionId.
Web allocates RequestId; LoginError includes InvalidCredentials, VerificationError, and SessionError.

Required interface fragments:

| Action | Result and effect |
| --- | --- |
| `Web/login [credential: Credential]` | Returns a fresh `[request: RequestId]` and starts a flow. |
| `OAuthAuthentication/verify [credential: Credential]` | Returns `[valid: true; namespace: Text; subject: Text; displayName: Text]`, `[valid: false]`, or `[error: VerificationError]`; public state is unchanged. |
| `ExternalIdentity/record [namespace: Text; subject: Text]` | Returns `[identity: Identity]`; the same namespace/subject pair identifies the same identity, creating it if absent; other state is unchanged. |
| `Profile/set [identity: Identity; displayName: Text]` | Returns `[identity: Identity]` and sets only that identity's displayName. |
| `Session/open [identity: Identity]` | On success, creates a fresh session with its identity and token, returns `[session: SessionId]`, and leaves other state unchanged; on failure, returns `[error: SessionError]` with unchanged state. |
| `Web/respond [request: RequestId; identity: Identity; session: SessionId; displayName: Text; token: Text]` | Returns `[]` and writes the login result to that request. |
| `Web/respond [request: RequestId; error: LoginError]` | Returns `[]` and writes the error to that request. |

Profile exposes `displayName: Identity -> Text`, with one value per identity that has been set.
Session exposes `identity: SessionId -> Identity` and `token: SessionId -> Text`, each with one value per session.

Specification: [assets/examples/login.syncs.md](../assets/examples/login.syncs.md)

RecordVerifiedIdentity and PrepareLogin read different fields from the same verification completion; neither consumes it.
Trace PrepareLogin's two calls into CompleteLogin's completion patterns and public-state reads.

| Acceptance scenario | Expected observation |
| --- | --- |
| Verification is valid; profile and session complete | Return that request's identity, profile, and session in one response. |
| Verification returns false | Return InvalidCredentials without recording an identity, setting a profile, or creating a session. |
| Verification returns an error | Return the error to the original request without further business calls. |
| Session creation fails | Return SessionError; retain completed identity and profile effects. An in-flight profile call may still finish. |
| Only one of profile and session completes | Do not return success while the other is pending. |
| The same identity has a session completion in another flow | That completion cannot satisfy CompleteLogin or supply this request's session. |

### Expand calls over query rows

This fragment starts at a successful Posting/delete completion; the deletion entry and refusal response are outside its scope.
Posting/delete takes `[post: PostId]` and returns `[post: PostId]` on success or `[error: DeleteError]` on failure.
Commenting[P] exposes `target: CommentId -> P`, with one target per existing comment.
`remove [comment: CommentId] => [removed: boolean]` deletes the specified comment and its target relation and returns true; other state is unchanged.
If the comment is absent, it returns false with unchanged state.

Specification: [assets/examples/comment-cleanup.syncs.md](../assets/examples/comment-cleanup.syncs.md)

| Acceptance scenario | Expected observation |
| --- | --- |
| No matching comments | Emit no remove calls. |
| Multiple matching comments | Call remove once per row, leaving other posts' comments unchanged. |
| A matched comment is deleted before the call | remove returns false with unchanged state. |
| Posting/delete returns an error | That completion triggers no remove calls; the deletion refusal response is outside this fragment. |
