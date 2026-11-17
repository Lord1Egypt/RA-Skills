# While an agent works, and when it finishes while the person is away

## While it works

Show, at all times:

- **The current step**, in plain words from the app or adapter ("Comparing the three drafts"), with its status word.
  A spinner alone is not a status.
- **What it has done so far**, folded (below), so the thread stays readable but nothing is lost.
- **What it is waiting on**, if anything: a tool call needing a go-ahead, a question, a limit reached. This is the
  most important line on the screen; it sorts to the top and is announced.
- **A way to stop**, and where the product supports it, **a way to steer**: send a message into the run. A steer is
  shown as "sent" until the agent picks it up, and "read" only when the service says so.
- **How long it has been running** only from measured times; **what it has cost so far** only from reported usage.
  Nothing forecast unless labelled an estimate.
- **Liveness**: when nothing has been heard for longer than the threshold, "No update since 10:42" replaces Running
  (see `status-and-states.md`).

Streaming text is marked as arriving (a caret or a shimmer) and is not read out token by token to screen readers; the
complete message is announced once.

Never show "done" for a step the service hasn't confirmed, and never let the client decide a run succeeded because the
stream closed: the status comes from the service.

## When to fold turns

Fold a run of turns into one line ("Drafted three versions and compared them") when:

- They are the agent's intermediate work (tool calls that read, searches, drafts) that the reader doesn't need step by
  step to trust the result.
- The fold's one line is true of everything inside it and comes from the app or the adapter, not from the model.

Never fold:

- An approval or a question, answered or not.
- An error, a cancellation, a guardrail stop.
- Anything that changed something real (a write, a send, a deploy). It stays visible on its own line.
- The most recent turn while the run is live.

Every fold opens to its turns. The count inside is shown ("12 steps"). Folding is presentation; the audit log keeps
everything.

## Checkpoints and recovery

- A checkpoint per turn or step says what it holds (code, conversation, both) and where the person is now.
- A run that stopped shows why, what finished, what didn't, and the choices: retry, skip, stop. A retry that changes
  something asks again before it runs.
- A kill switch stops the agent; it doesn't undo what the agent did, and the screen says so.

## When it finishes while the person is away

The person comes back to a digest, in the order they'd act on it:

1. **Waiting on you**: approvals and questions, each with what it needs and how long it has waited.
2. **Failed**: with the error and the choices.
3. **Finished**: the result first, in a few lines, then the receipt (what it cost, how long, what checked it) and the
   files to open, then the person's actions (accept, ask for changes).

Rules:

- A notification says what happened and what's needed ("Deploy to staging needs your approval", "Weekly report
  finished: 3 findings"), not "Task complete".
- Nothing is auto-dismissed. An unread approval stays until decided; an error stays until acknowledged.
- The result shows what the agent produced and what verified it (tests, checks, a second model's review labelled as
  such). What wasn't checked says "not yet checked".
- Files are listed with type, size and where they stand (checked, not yet checked), and open or download from the
  screen; nothing is applied to the person's system by viewing it.
- If the run stopped at a limit (spend, time, turns), say which limit, what was done up to it, and how to continue.
- A run passed from one person to another while away shows who from, who to, the note, and what did and didn't
  transfer (an approval someone else started doesn't).
