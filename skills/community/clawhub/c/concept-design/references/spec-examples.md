# Concept and synchronization examples

These engineering examples use the [tool encoding](tool-encoding.md). Author concepts and synchronizations using the [specification notation](spec-notation.md).
Interfaces and business rules below are teaching choices; confirm product requirements separately.
The tables specify acceptance checks and counterexamples, not executed test results.

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

```markdown
# concept Todo
coverage: complete
## purpose
Remember unfinished work and distinguish it from completed work.
## state
tasks: set Task
text: Task -> Text
done: set Task
Task is a local identity, never reused; Text is any string, including empty text.
Initially tasks and done are empty.
text has domain exactly tasks, with one Text per task; done is a subset of tasks.
Missing is the singleton error for an unknown task.
## actions
add [text: Text] => [task: Task]
  requires true
  ensures creates and returns one fresh t; tasks = old tasks union {t};
          text = old text plus (t, input text); done is unchanged
// Retain identity and text so the task can be reopened.
complete [task: Task] => []
  requires task belongs to tasks
  ensures done = old done union {task}; other state is unchanged
complete [task: Task] => [error: Missing]
  requires task does not belong to tasks
  ensures returns Missing; state is unchanged
reopen [task: Task] => []
  requires task belongs to tasks
  ensures done = old done minus {task}; other state is unchanged
reopen [task: Task] => [error: Missing]
  requires task does not belong to tasks
  ensures returns Missing; state is unchanged
## operational principle
after add [text: "report"] => [task: t], pending work includes t;
then complete [task: t] => [] removes it from pending work;
then reopen [task: t] => [] restores the same t and text.
## queries
_pending [] => [task: Task; text: Text]
  returns exactly tasks minus done, one row per task with its text;
  zero rows when empty; order unspecified; no completion

## Execution constraints
- Completion: the declared result and local state effects are observable to subsequent queries before the action completes.
- Concurrency: each state change atomically preserves the declared invariants.
- Failure/repetition: use the action cases above; repeated add calls create distinct tasks.
- Timing/recovery: no timing bound is specified; durability and restart recovery are outside this example.
```

| Acceptance from fresh state | Expected observation |
| --- | --- |
| add("report"), then _pending | Exactly the returned task and input text. |
| add to obtain t; complete(t), then reopen(t), querying after each | t disappears, then returns with unchanged text. |
| add to obtain t; complete(t) twice, then reopen(t) twice | Repeats succeed without duplicate tasks or other changes. |
| complete(unknown) or reopen(unknown) | Missing with unchanged state. |
| _pending before add | Zero rows without an error. |

## Partial reservation model

This fragment covers a selected slot's success or conflict.

```markdown
# concept Reserving [U, S]
coverage: partial
## purpose
Commit a resource slot to a user for future use.
## state
reservations: set Reservation
user: Reservation -> U
slot: Reservation -> S
status: Reservation -> Status
Reservation is local; Status = booked | canceled | granted.
Conflict is the singleton error for a slot with a booked reservation.
Initially reservations is empty.
Each reservation has one user, slot, and status.
Each S has at most one booked reservation; S has no assumed fields.
After reserve [user: u1; slot: s1] => [reservation: r1] from empty state:
{ reservation: r1, user: u1, slot: s1, status: booked }
One row is one current reservation, identified by reservation; fields map to the same-named relations.
## actions
reserve [user: U; slot: S] => [reservation: Reservation]
  requires slot has no booked reservation
  ensures atomically creates and returns fresh r with input user/slot and booked status;
          adds r to reservations; existing facts are unchanged
reserve [user: U; slot: S] => [error: Conflict]
  requires slot has a booked reservation
  ensures returns Conflict; state is unchanged
cancel [reservation: Reservation] => []
  requires reservation is booked
  ensures changes only its status to canceled
grant [reservation: Reservation] => []
  requires reservation is booked; arrival conditions are open
  ensures changes only its status to granted
## operational principle
after reserve [user: u; slot: s] => [reservation: r],
then, if not canceled and arrival conditions hold, grant [reservation: r] => [] fulfills the commitment.

## Execution constraints
- Completion: reserve completes with its declared reservation or Conflict result and state effects.
- Concurrency: the no-booked-reservation check and reservation creation are atomic for each slot.
- Failure/repetition: reserve uses its declared cases; retry identity and cancel/grant refusal behavior remain open.
- Timing/recovery: arrival conditions, timing, and restart recovery remain open.
```

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

```markdown
# app Reservations
include Availability [VenueId]
include Reserving [UserId, Availability.Slot]
include Requesting

### Request a reservation
sync reserve
when { Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request] }
then { Reserving/reserve: [user: ?user; slot: ?slot] }

// The entry completion supplies the request ID absent from the reservation result.
### Return the reservation
sync accepted
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [reservation: ?reservation]
}
then { Requesting/respond: [request: ?request; reservation: ?reservation] }

### Return the reservation conflict
sync rejected
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [error: ?error]
}
then { Requesting/respond: [request: ?request; error: ?error] }

## Execution constraints
- Flow/correlation: each Requesting/reserve starts its own flow with one attempt; repeated attempts need occurrence correlation.
- Reads/order: the selected slot comes from the entry; _find is a read and never satisfies when.
- Outcomes: accepted/rejected match the entry and reservation completion in that flow and respond using its RequestId. Response-delivery failure handling remains open.
- Timing/recovery: timing, retry, and restart recovery remain open.
```

| Acceptance or counterexample | Expected observation |
| --- | --- |
| Reserve a free slot, then request it again while booked | The first request gets a reservation; the second gets Conflict without changing existing facts. |
| Entry and reservation completion belong to different flows | Do not use the other flow's result to respond to this request. |
| _find returns zero or several candidates | No rule waits for that query or implicitly reserves its results; candidate selection needs a product decision. |
| Remove Availability but retain Availability.Slot | The subset is unusable; rebind S to an independently supplied SlotId and update entries and rules. |

Discovery requirements, not type binding alone, justify retaining Availability.
A known-slot product may need only Reserving.
Arrival inputs/timing, cancel/grant refusal conditions, authentication, venue checks, concurrent withdrawal,
display, cancellation entries, and fault handling remain open.
Offered state can change before reserve and does not enforce a write-time invariant.
Arrival and grant must be defined and checked before purpose fulfillment is established.

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

```markdown
# app ExternalLogin
include Web
include OAuthAuthentication [Credential]
include ExternalIdentity
include Profile [ExternalIdentity.Identity]
include Session [ExternalIdentity.Identity]

### Verify login credentials
sync VerifyLogin
when { Web/login: [credential: ?credential] => [request: ?request] }
then { OAuthAuthentication/verify: [credential: ?credential] }

### Record the verified external identity
sync RecordVerifiedIdentity
when {
  OAuthAuthentication/verify: []
    => [valid: true; namespace: ?namespace; subject: ?subject]
}
then { ExternalIdentity/record: [namespace: ?namespace; subject: ?subject] }

### Set the profile and create a session
sync PrepareLogin
when {
  OAuthAuthentication/verify: [] => [valid: true; displayName: ?displayName]
  ExternalIdentity/record: [] => [identity: ?identity]
}
then {
  Profile/set: [identity: ?identity; displayName: ?displayName]
  Session/open: [identity: ?identity]
}

### Join completions and read response data
sync CompleteLogin
when {
  Web/login: [] => [request: ?request]
  Profile/set: [identity: ?identity] => [identity: ?identity]
  Session/open: [identity: ?identity] => [session: ?session]
}
where {
  Profile: { ?identity displayName: ?displayName }
  Session: { ?session identity: ?identity; token: ?token }
}
then {
  Web/respond: [request: ?request; identity: ?identity; session: ?session;
                displayName: ?displayName; token: ?token]
}

### Refuse invalid credentials
sync RefuseLogin
when {
  Web/login: [] => [request: ?request]
  OAuthAuthentication/verify: [] => [valid: false]
}
then { Web/respond: [request: ?request; error: "InvalidCredentials"] }

### Return a verification error
sync ReportVerificationError
when {
  Web/login: [] => [request: ?request]
  OAuthAuthentication/verify: [] => [error: ?error]
}
then { Web/respond: [request: ?request; error: ?error] }

### Return a session error
sync ReportSessionError
when {
  Web/login: [] => [request: ?request]
  Session/open: [] => [error: ?error]
}
then { Web/respond: [request: ?request; error: ?error] }

## Execution constraints
- Flow/correlation: each Web/login starts its own flow with one verification attempt. Each other action is called at most once within that flow; repeated attempts need occurrence correlation.
- Reads/order: actions may execute synchronously or asynchronously; CompleteLogin matches completed Profile/set and Session/open actions. Successful completions require their declared state effects to be queryable. No other flow changes the queried profile or session between completion and response in this example.
- Outcomes: if actions complete with the listed cases and matched rules eventually execute, each request gets exactly one response. A session failure preserves completed identity/profile effects. The error response does not wait for the profile update or imply cancellation of that pending call.
- Timing/recovery: timing, retry, and restart recovery remain open.
```

RecordVerifiedIdentity and PrepareLogin read different fields from the same verification completion; neither consumes it.
Trace PrepareLogin's two calls into CompleteLogin's completion patterns and public-state reads.

| Acceptance scenario | Expected observation |
| --- | --- |
| Verification is valid; profile and session complete | Return that request's identity, profile, and session in one response. |
| Verification returns false | Return InvalidCredentials without recording an identity, setting a profile, or creating a session. |
| Verification returns an error | Return the error to the original request without further business calls. |
| Session creation fails | Return SessionError; retain completed identity and profile effects. An in-flight profile call may still finish. |
| Only the profile completes | Do not return success while the session is pending. |
| Only the session completes | Do not return success while the profile is pending. |
| The same identity has a session completion in another flow | That completion cannot satisfy CompleteLogin or supply this request's session. |

### Expand calls over query rows

This fragment starts at a successful Posting/delete completion; the deletion entry and refusal response are outside its scope.
Posting/delete takes `[post: PostId]` and returns `[post: PostId]` on success or `[error: DeleteError]` on failure.
Commenting[P] exposes `target: CommentId -> P`, with one target per existing comment.
`remove [comment: CommentId] => [removed: boolean]` deletes the specified comment and its target relation and returns true; other state is unchanged.
If the comment is absent, it returns false with unchanged state.

```markdown
# app Discussion
include Posting
include Commenting [Posting.PostId]

### Remove existing comments on the deleted post
sync RemovePostComments
when { Posting/delete: [] => [post: ?post] }
where { Commenting: { ?comment target: ?post } }
then { Commenting/remove: [comment: ?comment] }

## Execution constraints
- Flow/correlation: emitted remove calls retain the successful Posting/delete occurrence's flow.
- Reads/order: comments are read at rule evaluation after Posting/delete completes.
- Outcomes: each matched row emits one remove call; zero rows emit none. A comment deleted before remove produces the declared false result.
- Timing/recovery: concurrent additions, other removal failures, timing, retry, and restart recovery remain open.
```

| Acceptance scenario | Expected observation |
| --- | --- |
| No matching comments | Emit no remove calls. |
| Multiple matching comments | Call remove once per row, leaving other posts' comments unchanged. |
| A matched comment is deleted before the call | remove returns false with unchanged state. |
| Posting/delete returns an error | That completion triggers no remove calls; the deletion refusal response is outside this fragment. |
