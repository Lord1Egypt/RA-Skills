# Measuring Change, Reviewing, and Ending

Coaching that cannot show what changed gets renewed on rapport and cancelled on the first budget review. Measurement is not bureaucracy; it is what makes the mid-engagement correction possible and the ending honest.

**Contents:** [What to Measure](#what-to-measure) · [The Baseline Problem](#the-baseline-problem) · [Mid-Engagement Review](#mid-engagement-review) · [When It Is Not Working](#when-it-is-not-working) · [Dependency](#dependency) · [The Renewal Conversation](#the-renewal-conversation) · [The Final Session](#the-final-session) · [After the Engagement](#after-the-engagement)

**Before any review**, read the baseline table in `clients/<name>.md` (or `## Focus` in `memory.md`), the commitment history in `## Commitments`, and `## Due`. A review conducted from memory measures the last two weeks and calls it the engagement.

## What to Measure

Four layers. Most engagements report only the fourth and it is the least reliable.

| Layer | Example | Moves | Use for |
|---|---|---|---|
| Adherence | Kept 7 of 9 commitments | Immediately | Weekly check-ins; the earliest signal that a design is wrong |
| Behavior | Delegates 60% of reviews, was 0% | Weeks | The core evidence of coaching; what others can corroborate |
| Outcome | 12 paying users, was 0 | Months, and not fully controlled | The honest scoreboard, never the commitment |
| Subjective | Confidence delegating 6/10, was 3 | Anytime, noisy | Direction and the client's own experience |

- **Report adherence and behavior to a sponsor; report all four to the client.** Sponsors who are handed only subjective ratings conclude that coaching cannot be evaluated, and act accordingly.
- **Adherence rate is `kept ÷ (kept + missed)` over the engagement**, computed from `## Commitments`. Below ~50% means the design is wrong, not the person (`accountability.md`). Above ~90% sustained means the commitments are too small and the ratchet stalled.
- **Same scale, same wording, every time.** A 0-10 rating re-asked with different phrasing is a new instrument and the comparison is fiction.

## The Baseline Problem

- **Recorded on day one or it does not exist.** A baseline reconstructed at month three is a memory, and memory bends toward the story of progress.
- **Include one verbatim sentence** from the first session about where they are. Reading it back at the end outperforms every chart, because clients forget their starting point completely — that forgetting is itself evidence, and it is why they undervalue their own progress.
- **Where nothing objective exists, two subjective scales are enough** — confidence on the goal, satisfaction in the domain — as long as both are re-read identically.
- **Corroboration where it matters**: for executive work, three named colleagues asked one question at baseline and again at the end. Cheaper and more convincing than a 360 instrument, and it survives a procurement conversation (`teams.md`).

## Mid-Engagement Review

At the midpoint, on a date set at intake and written into `## Due`. Twenty minutes, inside a session, with the baseline open.

1. **Baseline vs now**, on the same markers. Read the numbers out; do not summarize them.
2. **Adherence rate** from the commitment history, stated plainly.
3. **"What has actually changed that you notice?"** Their evidence, not yours.
4. **"What has not moved that you expected to?"** The most valuable question here, and the one people skip because it invites criticism. It arrives anyway, later, as non-renewal.
5. **Is the goal still the goal?** A changed goal at the midpoint is a legitimate outcome, not a failure — write the change into `## Focus` with the date.
6. **One adjustment**: cadence, commitment size, the goal itself, or the coaching approach. One, not four.

Write the review to `clients/<name>.md` (or `## Focus`) with the date, and set the next review in `## Due` in the same turn.

## When It Is Not Working

Diagnose in this order; each is cheaper to fix than the next.

| Check | Signal | Fix |
|---|---|---|
| Commitment sizing | Adherence under 50% | Halve, then halve again (SKILL.md Rule 5) |
| Cadence | Progress in the week before a session, nothing after | Tighten temporarily, then design the transfer (`accountability.md`) |
| Goal ownership | Flat energy for three sessions | Ownership test (`stuck.md`) |
| Approach | Sessions feel good, nothing happens | Fewer insights, more commitments; ban the takeaway that is only a realization |
| Capacity | Life changed materially | Re-size honestly or pause with a return date |
| Craft | The same thing fails with several clients | Yours, not theirs — supervision and a recording review (`craft.md`) |
| Fit | Three re-contracts, three stalls | End it (`referral.md`) |

Say the diagnosis out loud. A coach who privately concludes the engagement is failing and continues to run sessions is selling time, and the client usually knows before you say it.

## Dependency

The failure mode that looks exactly like success: the client keeps booking, speaks warmly about the sessions, and has not changed anything in two months.

Tests, in order of usefulness:

- **Check-in frequency direction.** Getting less frequent over the engagement is health; needing more is dependency (SKILL.md Rule 9).
- **Who sets the commitments.** By the midpoint, they should arrive with them and you verify the design.
- **The between-session pattern.** Kept the week before a session, missed the week after, repeatedly: that is compliance with a person, not a structure.
- **Ask it directly**: "what would you do about this if we did not have a session next week?" A blank answer is the diagnosis.
- **Their language.** "What do you think I should do?" arriving more often at month three than at month one is a direction, not a question.

The fix is structural, not motivational: widen the cadence, transfer the review to them, and set the exit date. Coaches with a full calendar and financial pressure are the population most likely to miss this, which is precisely why it belongs in supervision (`craft.md`).

## The Renewal Conversation

- **Held at least two weeks before the last session**, on a date set at intake. A renewal decided in the final session is decided under goodbye pressure, and both parties know it.
- **Lead with evidence, not with a question about how they feel.** Baseline vs now, adherence, what changed that others noticed.
- **State the honest options, all three**: end as planned because the goal is met; continue on a *new* goal with a new contract; or stop because the constraint is no longer coachable.
- **A renewal on the same goal is a warning.** If the original goal has not moved in six sessions, more sessions of the same are unlikely to move it — change the goal, the approach, or the coach.
- **Do not discount to retain.** A rate cut to keep a client converts the relationship into a negotiation and prices your next client (`practice.md`).
- Write the decision and its date to `clients/<name>.md`; a decision with reasoning that will be re-read goes to `artifacts/` with its `## Boxes` line.

## The Final Session

Design it as a session, not as a goodbye.

1. **Baseline read-back**, including the verbatim sentence from day one.
2. **"What can you do now that you could not do in March?"** — capability, not feelings.
3. **What they will keep doing**: the structures that transfer — their review format, their cue, their floor version.
4. **Their own next 90 days, written by them in the session**, saved to `artifacts/<kebab-name>.md`. Written by you, it is a document they will not open.
5. **What to watch for**: the specific relapse signal for their pattern, named ("when you start researching tools again").
6. **How they can come back**, and on what terms. A clean door beats a vague one.
7. **Ask for feedback properly**: what was most useful, what was missing, what you should stop doing. Asked in the final session, answered honestly; asked by email afterwards, answered politely.

Then the record: `status: ended <date>` in `clients/<name>.md`, the context updated in `contacts.md`, the final markers against baseline, and any recording deleted per the agreement (`memory-template.md`).

## After the Engagement

- **Ask for the testimonial and the referral in the final session**, while the evidence is fresh, and be specific about what you would like it to say. Two weeks later the answer is "of course" and nothing arrives.
- **A check-in at 90 days** is the highest-yield marketing a coach does and the most common one skipped. One message, about them, no offer attached.
- **Former clients stay in `contacts.md`** with `former client, ended <date>` in the context. Their file is never deleted; it is the record of what was delivered and the basis of any return engagement.
- **Record what happened afterwards in `clients/<name>.md`**, with the date, whenever they tell you. Outcomes at six months are the only evidence that distinguishes coaching that worked from a client who enjoyed the sessions — and they are what a corporate buyer asks for.
- Deletion on request is honored in full: the file goes, its `## Boxes` line goes in the same turn, and only the fact and dates of the engagement remain (`referral.md`).

**Every review, renewal decision and ending writes**: the markers against baseline and the adherence rate to `clients/<name>.md` or `## Focus`; the decision and its date; the next review, renewal or check-in date to `## Due`; and the client's own next-90-days plan to `~/Clawic/data/coach/artifacts/<kebab-name>.md` with its `## Boxes` line — in the same turn (`memory-template.md`). Update the person's row in `~/Clawic/data/contacts/contacts.md` rather than duplicating it here.
