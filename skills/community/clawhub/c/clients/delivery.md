# Delivery — Running the Engagement Week to Week

Scope: the rhythm of a live engagement — status, meetings, decisions, feedback, and how to say no or deliver bad news. Scope changes are `scope.md`; the relationship going wrong is `difficult-clients.md`.

Read the project file at `~/Clawic/data/projects/<project>.md`, the client's `contact-log/<client-slug>.md` and their `roster/<client-slug>.md` before any status note, meeting or hard message. Check `## Due` for the status day and anything overdue.

**Contents:** [The Status Note](#the-status-note) · [Meetings That Earn Their Hour](#meetings-that-earn-their-hour) · [Writing Decisions Back](#writing-decisions-back) · [Feedback That Is Usable](#feedback-that-is-usable) · [Delivering Bad News](#delivering-bad-news) · [Saying No](#saying-no) · [Managing the Slow Middle](#managing-the-slow-middle) · [Response Discipline](#response-discipline)

## The Status Note

Same day every week (`status_cadence`), sent whether or not there is news, three sections, under 150 words:

```
Done this week: shipped the checkout flow; two of three integrations tested.
Next: payment error states, then handover doc. On track for the 20th.
Needs you: sign-off on the copy by Thursday, or the 20th moves to the 24th.
```

- **"Needs you" is the section that matters.** It is where a slipped deadline gets pre-attributed, honestly and without accusation, before it slips.
- **Consequences with dates, not complaints.** "Or the 20th moves to the 24th" is information; "we're still waiting on you" is a grievance.
- Send it even when the answer is "on track, nothing needed". The value is the pattern: a client who receives it every Monday stops asking, and stops worrying between notes.
- Keep the format identical week to week. It becomes skimmable, and a change of shape reads as a change of situation.
- On a retainer, the same note carries usage: hours or scope used against the cap, every month, used or not (`pricing.md`).

## Meetings That Earn Their Hour

- **No agenda, no meeting.** Sent in advance, three bullets. The discipline also filters out meetings that were really a message.
- **Default to shorter.** Thirty minutes for a review, sixty for a kickoff or a decision meeting. A recurring weekly call that has nothing to decide should become the status note.
- **Open by naming the decision** the meeting exists to make. Meetings without a decision are updates, and updates are cheaper in writing.
- **The approver's absence is information.** If the person who signs off has not attended in three sessions, the project has been deprioritised (`stakeholders.md`).
- **Recap the same day**: decisions, owners, dates, and what you are waiting on. Not minutes. Nobody reads minutes and everybody reads five lines.
- Meetings the client calls at short notice, repeatedly, are a symptom rather than an inconvenience: something upstream is unstable.

## Writing Decisions Back

Every decision, the same day, to the person who made it, in one paragraph with a deadline for correction (SKILL.md Rule 7):

> "Confirming today's call: we're going with option B, which adds the motion work at 5,000 EUR and moves launch to 4 September. I'll proceed on that basis unless you tell me otherwise by Thursday."

Why the deadline clause carries the weight: it converts silence into agreement in a way both sides understood at the time. Without it, silence is just silence, and six weeks later the sentence "we never agreed that" costs you the difference.

Every one of these also lands in the decisions table of `~/Clawic/data/projects/<project>.md`. The chat thread is not a record; it is unsearchable within a month and gone when the tool changes.

## Feedback That Is Usable

Most revision pain is a feedback-process problem, not a taste problem.

| Problem | What it produces | Fix |
|---|---|---|
| Feedback trickling in over two weeks | Endless micro-revisions and a dead deadline | One consolidated round per deliverable, with a window: "all feedback by Thursday, in one document" |
| Contradictory feedback from several people | You arbitrate between your client's colleagues, and lose whoever you overrule | They resolve internally first; you deliver against one voice, named in the working agreement |
| "I don't like it" with no reason | Unbounded revision | Ask what it should do that it does not, and against which of the agreed goals |
| Feedback on something already approved | Silent reopening of scope | Point at the written approval and offer a change order — kindly, once (`scope.md`) |
| Last-minute feedback from someone who never appeared | An unmapped stakeholder (`stakeholders.md`) | Add them to the map, then decide: absorb once, or change order |
| Anything else | Ambiguity you will pay for | Restate it back as a specific change with an effort estimate before agreeing to it |

State the revision count in the deliverable email itself — "this is round one of two" — so the third round is a known event rather than an argument.

## Delivering Bad News

Bad news early is a status update. The same news late is a breach of trust, and clients forgive delays far more readily than they forgive being surprised.

Four sentences, in this order:

1. **The fact**, first, without preamble. "The integration will not be ready for the 20th."
2. **The cause**, in one line, no blame distribution. "The API's sandbox has been down since Tuesday."
3. **The plan**, with a new date you are confident in — pad it, because a second slip costs more than the first admission.
4. **What you need from them**, if anything.

No apology paragraph. One "sorry about this" is fine; three signals that you expect to be punished, which invites it. Never bury bad news in the middle of a status note — it reads as concealment when they find it.

If the cause is your mistake, say so plainly and move immediately to the fix. Clients rehire people who handle their own errors well; the concealment is what ends relationships.

## Saying No

- **No, and here is what I can do.** A bare no reads as a refusal to help; a no with an alternative reads as judgment.
- **Cite the agreement, not your feelings.** "That's outside what we scoped — I can quote it, or swap it for something of similar size" is not a conflict, it is an operating procedure.
- **Say it once and hold it.** Reversing a no under mild pressure teaches that every no is a first offer, and the next request arrives sooner and larger.
- **Do not say no by delay.** Going quiet on a request you intend to refuse is the most damaging option available, and it is the most common one.
- Free exceptions are allowed and useful — occasionally, deliberately, and always named as an exception with its normal price: "I'll do this one at no charge; normally it's a half-day." An unnamed favour becomes the new baseline (`scope.md`).

## Managing the Slow Middle

Every engagement longer than a month has a stretch where visible progress stops and confidence drains.

- **Ship something visible on a fixed rhythm**, even partial. Perceived progress is the currency.
- **Name the middle in advance** at kickoff: "weeks three to five look quiet from your side; that is the build." A predicted silence is reassuring, an unpredicted one is alarming.
- **Increase status frequency temporarily** rather than decreasing it because there is nothing to report. Less news is exactly when clients need more contact.
- Watch for the client filling the silence with new requests. That is anxiety, not appetite; more contact reduces it more cheaply than more work does.

## Response Discipline

- Answer within the promise in the working agreement, and if the real answer needs time, send the acknowledgement now and the answer later. Unacknowledged messages generate follow-ups, which generate the impression of chaos.
- Do not answer at midnight or at weekends unless that is the declared policy. Whatever hours you respond in become the expected hours within a fortnight.
- Keep everything in the agreed channel. Move out-of-channel requests back without comment, every time; commentary makes it a conflict, silent redirection makes it a norm.
- Batch responses rather than reacting continuously. Availability is not the product, and constant reactivity destroys the deep-work blocks the client is actually paying for.

**Write before you move on:** decisions, promises, meetings and calls go to `contact-log/<client-slug>.md` the same day, newest first, and into the decisions table of `~/Clawic/data/projects/<project>.md`; milestone status and dates go to that project file; anything that changed scope, price or a date is also a change-log row (`scope.md`); a recurring status day, review or client blackout period goes to `## Due` in `memory.md`; a health change goes into the client's `Health` cell in `## Roster` with the date; a bad-news or refusal message that worked well is worth keeping at `artifacts/script-<topic>.md` with its `## Boxes` line.
