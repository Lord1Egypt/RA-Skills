# The Human Side of Shipping Code

Most stalled work is not blocked on a technical problem. It is blocked on an unasked question, an unstated disagreement, or a requirement nobody wrote down.

**Before a conversation that decides something**, read `~/Clawic/data/projects/<project>.md` for what was already agreed, and `~/Clawic/data/contacts/contacts.md` for who owns what and how they prefer to be reached. Re-opening a settled decision because it was only ever in a chat thread is the failure this file exists to prevent.

## Asking for Help

The timebox is ~30 minutes without a new hypothesis (`bugs.md`). Then ask, in this shape:

> What I am trying to do · what I expected · what happened, verbatim · what I have already ruled out · my current best guess.

That format takes two minutes to write, frequently answers itself while writing, and turns a 20-minute interruption into a 2-minute answer. Asking early is not weakness; asking without doing the first 30 minutes is, and so is spending a day on something a colleague has already solved.

## Requirements

Before starting anything over half a day, get these on the record — in the ticket, not in your head:

| Question | Why it matters |
|---|---|
| What does the user do differently after this ships? | Turns a feature description into a testable outcome |
| What happens at the boundaries — empty, huge, concurrent, unauthorized? | These are half the implementation and they are never in the ticket |
| What is explicitly out of scope? | The only defense against scope creep that survives contact |
| How will we know it worked? | The verification, and often the missing metric (`shipping.md`) |
| What breaks if we do nothing? | Reveals the actual priority, occasionally that the work is unnecessary |

An ambiguous requirement is not a request for your judgment — it is a question that has not been asked yet. Guess and you will build the wrong thing at full quality.

## Disagreement

1. **State the tradeoff, not the verdict**: "this is faster to ship but locks the schema; the alternative costs two days and keeps it open".
2. **Ask what they know that you do not.** Most technical disagreements are information asymmetry, not judgment differences.
3. **Name the decision criteria** before arguing solutions — if you cannot agree on what "better" means here, you cannot converge.
4. **Disagree and commit**, once the decision is made by whoever owns it. Put the decision and what you predicted under `## Decisions` in the project file, so the record exists without being an argument.
5. **Escalate the decision, never the person**: "we need someone to pick between A and B by Thursday; here is the one-paragraph tradeoff".
6. **Move to synchronous after two round trips.** A 10-minute call resolves what six comments will not (`reviews.md`).

## Saying No, and Saying What It Costs

Never a bare "no", and never a silent yes. The three forms that work:

- **Trade**: "yes, and X moves to next week — which do you want first?"
- **Reduce**: "the full version is two weeks; there is a version that covers the main case in three days, without the export."
- **Price the shortcut**: "we can do it by Friday by skipping the migration path; that costs us a manual data fix later and a risk of duplicate rows. Your call, and it goes in the project file as a decision we made together."

Deliver bad news early and in one message: what happened, the new forecast, what you need. Every day of delay in telling someone converts a schedule problem into a trust problem.

## Working Asynchronously

- Write the update where the decision lives, not in a DM. A decision in a DM does not exist next quarter.
- One message with the full context beats five with fragments; assume the reader is in a different timezone and will read it once.
- Status in verifiable terms: merged, deployed, blocked on X since Tuesday. Never a percentage (`estimation.md`).
- Say when you are blocked the same day, naming who can unblock you. A silent block is a burned day nobody could have prevented.
- Default to public channels: the answer becomes searchable, and someone you did not think of corrects you.

## Handoffs

Whether you are leaving for a week or handing over an incident (`oncall.md`), the handover has four parts: **what is done and merged · what is in flight and where it sits · what is decided (and what was rejected) · what is still unknown**. Write it in the project file or the ticket, not in a chat message that scrolls away. Everything in flight also belongs in `## Open Threads` of `memory.md`, which is the same list from the other direction.

## Working With Non-Engineers

- Translate to consequences, not mechanisms: "checkout would break for new users" beats "the foreign key constraint fails".
- Give a range and the assumption behind it, never a bare date (`estimation.md`).
- Ask for the *problem*, not the requested solution — a feature request is frequently a workaround for something simpler.
- Show a rough version early. Ten minutes of clicking corrects more misunderstanding than a page of specification.
- Never present technical debt as a moral failing; present it as a rate: "each change to this area costs about twice what it should, and the fix is three days" (`tech-debt`).

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Building from an ambiguous ticket | You deliver the wrong thing, at full quality, having spent the whole estimate | Ask the five questions before starting |
| Silent overrun | Trust is lost at disclosure, not at the delay | Re-forecast the day an assumption breaks |
| Deciding in a DM or a call with no record | Re-litigated in a month, with two versions of what was agreed | One line in the project file, same day |
| Winning the argument | You are still on the team afterwards, with a worse version of the outcome | Tradeoff, criteria, decision, commit |
| Suffering in silence for a day | The answer was 10 minutes away | Timebox at ~30 minutes, then ask in the shape above |
| Answering "how long" instantly to be helpful | The number is anchored and quoted back forever | "Let me look and get back to you within the hour" |
| Treating a code review comment as a personal verdict | Escalates, and the code does not get better | Respond to the claim; ask for the failure it predicts |
| Vague status: "almost done" | Means nothing, and hides the block | Merged / deployed / blocked on X |

## Write Down the Decisions

- **A decision made with someone else** → one line under `## Decisions` in `~/Clawic/data/projects/<project>.md`, the same day, with the date; the full reasoning goes to `artifacts/adr-<topic>.md` when there were real alternatives (`memory-template.md`).
- **A scope agreement or an explicit cut** → the same project file. This is the record that ends "we never agreed to drop that".
- **A person who owns an area, reviews your work, or decides priorities** → `~/Clawic/data/contacts/contacts.md`, one row per person, updated in place, with what they care about in `Context`.
- **Anything in flight, blocked, or handed over** → `## Open Threads` in `memory.md`, deleted the turn it lands.
