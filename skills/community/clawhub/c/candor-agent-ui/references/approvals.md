# Approvals, blast radius and undo

An approval is a person deciding whether an agent may do one specific thing. The screen's job is to give them exactly
what that decision needs, no less and not much more, and to make the decision mean what they meant.

## What an approval shows

In this order, because people read from the top and stop:

1. **What will happen**, in one plain sentence from your app, not from the model: "Update 3 fields on Account in
   staging." The agent's own explanation can follow, labelled as the agent's.
2. **Where**: the environment or account in scope, in its own colour band if production.
3. **The change itself**: the diff, the fields with old and new values, the records, the amount, the recipients. A
   description alone is not enough to approve.
4. **What it touches** (the blast radius, below) and **whether it can be undone**, how, and for how long.
5. **Why it reached this person**: the rule that routed it ("writes to production ask first", "over the $50 limit",
   "the agent's permission mode is ask-every-time").
6. **Who asked**: the agent, named by the app, and the run or thread it belongs to.
7. **The decision**: two or more answers, none pre-selected; an optional reason on deny; what happens if nobody
   answers by the deadline, if there is one.

The hash or version of what's shown is part of the request. The decision carries it back, and the system applies the
change only if they still match.

## How much to show

- Summary first, detail on demand: the sentence and the counts always visible; the full diff, the full list of records
  and the agent's reasoning behind a disclosure that is open by default for anything irreversible.
- Never fold the decision below the fold. On a phone the buttons are reachable without scrolling past the change, or
  the change is summarised above them with the full view one tap away.
- Show the agent's recommendation only when it has one, marked as its pick and never selected.
- Don't pad with the model's confidence or a progress bar; show the evidence (a test run, a dry run) if there is one.

## The buttons

- Neither answer focused or selected on open. Enter and Space do nothing until the person moves focus to an answer.
- The committing answer (Approve, Allow, Apply, Send) is not under a single key, not the leftmost in a row people
  click through, and not the primary colour if that colour is used for a default elsewhere on the screen.
- Deny takes an optional reason; the agent sees it. Approve may let the person edit the change first; editing re-hashes.
- "Always allow" exists only if the app wants it, is never ticked for the person, and says what it will skip from now
  on and how to turn it off.
- A decision in flight shows "submitting"; one that failed to record says so and keeps the answers available. Never
  show "approved" before the server recorded it.

## When a second person is needed

The app decides, by policy; the screen shows the policy. Common reasons:

- The change reaches production, or a named protected environment.
- It is irreversible, or its undo window is short.
- Money, data export or access grants over a threshold.
- The person approving is the one who asked for the change, or the one who built the agent (self-approval).
- Regulation or the customer's own rule.

Show it plainly: "Needs a second approver (production). You approved; waiting on an owner." The second approver sees
the same change and hash, and who approved first. Both decisions go to the audit log with ids, not just names.

## Approving away from the screen

- A notification (email, chat, phone) says what is waiting and gives a short id or a route to the approval page; it is
  not itself the Approve button, and a link in it never acts on its own. The page re-shows the change and takes the
  decision there.
- The compact approval page carries the same summary, change, blast radius, undo note and hash as the full one.
- Approvals outlive the request that asked: keep them in a store, so a server restart or a reload finds the same
  waiting request and the run resumes when it's answered.

## Blast radius

What a change can reach, grouped by kind of thing (records, fields, files, schedules, people notified), with counts.

- Counts are measured by your system before the request is shown, never estimated by the model. If a count can't be
  measured, say so ("rows affected: not measured; the query has no limit").
- Lead with the largest or most sensitive group. Name the environment.
- Make each group openable to the actual list, or say why it can't be listed.
- When a step's reach changes between proposal and apply, the hash changes and the approval is asked again.

## Undo

- Before: what the action removes or changes, whether it comes back, how (an undo button, a restore point, a support
  request) and for how long (a bin that empties in 30 days; a deploy that can be rolled back until the next one).
- Riskiest actions confirm by typing a name; the confirm button stays locked, and says why, until the text matches.
- Checkpoints: one per turn or step, each saying what it holds (code, conversation, both). A restore says what it
  restores and what it doesn't, and shows what the app checked afterwards; never "Restored" without a check.
- After: "Undone" or "Restored" always comes with what was not undone.
- A kill switch for a running agent stops the agent; it doesn't undo what it already did, and the screen says so.
