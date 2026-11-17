# Status vocabulary and the states of a tool call

One vocabulary for everything that runs: a run, a plan step, a tool call, a scheduled job, a sub-agent. The same word
means the same thing everywhere on the screen, and every status is a word with a colour beside it, never colour alone.
The source is Candor UI's `lib/status.ts`; the words are replaceable, the meanings are not.

## Run status

| Status | Default label | Means | Emphasis |
| --- | --- | --- | --- |
| `idle` | Not started | Exists, nothing has happened yet. | quiet |
| `queued` | Queued | Accepted, waiting for a worker. | quiet |
| `running` | Running | A worker is on it now, and has been heard from recently. | live (a pulsing dot is fine, with the word) |
| `waiting` | Needs you | Stopped to ask a person: an approval, a question, a decision. | needs a person (warning hue) |
| `blocked` | Blocked | Can't start: something it depends on failed or is itself waiting. | quiet, with what blocks it named |
| `succeeded` | Done | Finished and did what it set out to do. | success |
| `failed` | Failed | Finished and didn't; the error says why. | failure |
| `cancelled` | Cancelled | A person or a policy stopped it. | quiet |
| `skipped` | Skipped | Deliberately not done; say why if the system knows. | quiet |

Terminal statuses, after which nothing changes without a new run: `succeeded`, `failed`, `cancelled`, `skipped`.
Everything else is in flight and may need the person.

Rules:

- The word is always shown. The colour and the dot are extra.
- `waiting` is the status people need first. Sort by it, badge it, notify on it.
- `failed` always comes with an error in a sentence. A status badge that says Failed with no reason is incomplete.
- `blocked` names what blocks it, and that thing is one step away.
- Don't invent statuses ("processing", "almost done", "pending review"). If one is needed, map it to the nine, and if
  the app's words differ ("Standing by" for idle), change the label, not the meaning.

## Liveness: is it really running?

A status of `running` is a claim. Whether the screen may still call it running depends on when the system last heard
from it:

| Liveness | When | Show |
| --- | --- | --- |
| live | Heard from recently, or the app doesn't track it | Running |
| stale | Running, but nothing heard for longer than the threshold (two minutes by default) | "No update since 10:42", not Running |
| offline | Its host can't be reached | "Build runner 3 is offline since 10:40" |
| unchecked | No clock yet (rendering on the server) | The status, with no freshness claim |
| settled | Terminal | The status; silence is expected |

Only a running run goes stale: a queued or waiting one is quiet by design. An unreadable last-heard time is no
evidence of life; treat it as stale.

## A tool call

A tool call is a run with a few fields of its own. Show it as a compact row that opens:

- **Title**: what it did, in plain words from the app or the adapter ("Read Account's fields"), with the tool's own
  name available for people who want it (`metadata.describe`).
- **Status**: one of the nine, as a word.
- **Duration**: only once measured, and never while running. If the service didn't time it, show nothing.
- **Input and output**: text, shown when opened; long values scroll; never rendered as HTML, never run.
- **Error**: required when failed, in a sentence.
- **Approval**: who let it run when it needed a go-ahead (a person, or something automatic: a policy, a classifier,
  a rule) and why, in that source's words. Left out when it needed none or the source doesn't say.
- **Edited**: when the person changed the input before allowing it, mark the call as edited.

A tool call waiting for a person is a `waiting` run: the prompt shows what it will do, why it reached them, and the
permission mode the run is in. Allow and Deny are not pre-selected; "always allow" is never ticked for them.

## A message

| Status | Means | Show |
| --- | --- | --- |
| `streaming` | Still arriving | The text so far, marked as arriving (a caret or shimmer), not announced token by token |
| `complete` | Finished | The text; the attribution (model, cost) only with measured values |
| `interrupted` | Stopped before it finished, by a person or a limit | The text so far and a line saying it was stopped and by what |
| `failed` | The reply didn't arrive | A line saying so, with retry |

## A decision

A question the work stops for, with two or more answers:

| State | Means | Show |
| --- | --- | --- |
| `open` | Waiting on the person | The facts, the answers (none selected), the deadline and what happens if nobody answers |
| `submitting` | The answer is being sent | The chosen answer marked as sending; the others unavailable, saying why |
| `decided` | Recorded | The chosen answer and who chose it |
| `failed` | The answer wasn't recorded | Why, and the answers available again |

## Colour, by emphasis

Whatever the design system, keep four emphases apart from each other and from the brand colour: quiet (idle, queued,
blocked, cancelled, skipped), needs a person (waiting), success (succeeded), failure (failed). Running is live, not
alarming. Check the text on each tinted ground for contrast in every theme the app supports.
