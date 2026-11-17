# Accountability — Commitments, Check-ins, and Misses

Accountability is a designed structure, not a personality trait you supply. The design has four parts: the size of the ask, the cadence of the check, what counts as done, and what happens on a miss. Get those right and motivation stops being the variable.

**Contents:** [The Commitment Contract](#the-commitment-contract) · [Sizing](#sizing) · [Implementation Intentions](#implementation-intentions) · [Check-in Design](#check-in-design) · [Handling a Miss](#handling-a-miss) · [Ratcheting](#ratcheting) · [Streaks and Their Failure Mode](#streaks-and-their-failure-mode) · [Environment Over Willpower](#environment-over-willpower) · [Stakes](#stakes) · [Weaning Off You](#weaning-off-you)

**Before designing anything**, read `## Commitments` (or `commitments.md`) in `~/Clawic/data/coach/memory.md`. The kept/missed history decides the size of the next ask — designing without it repeats the ask that already failed twice.

## The Commitment Contract

Three fields, no exceptions (SKILL.md Rule 6):

| Field | Bad | Good |
|---|---|---|
| Action | "Work on the deck" | "Write slides 1-5 of the deck" |
| Deadline | "This week" | "Thursday 2026-07-30, before lunch" |
| Observable | — | "The five slides exist in the shared file" |

Plus, at the close: **confidence 0-10**. Under 7 predicts a miss — shrink the action until the number is 7 or higher, in the session (`questions.md`). This single question is cheaper than any follow-up structure.

A commitment with no observable is recorded as an intention (`Observable: none`) and does not count in a streak. Keeping the row visible is deliberate: a client whose last six entries are all intentions has a design problem, and the pattern is only visible if intentions were written down rather than quietly upgraded.

## Sizing

- **The 20-minute worst-day test**: could they do it in under 20 minutes on the worst day of the month? If not, it is a project — decompose until the first step passes. The worst day is the design point because that is the day the streak breaks.
- **First commitment of an engagement is deliberately easy.** The mechanism being installed is "I say a thing and it happens" (`session.md`).
- **Cap at `commitment_cap`** (default 3), one if the behavior is new. Five commitments predicts zero: the client has to choose, choosing is work, and it happens at the moment of lowest energy.
- **Frequency before intensity.** For a repeating behavior, 3 days a week that happen beat 5 that do not. Start at a frequency they would bet money on.
- **Named minimum**: every repeating commitment gets a floor version for bad days — "20 minutes, or 5 minutes if the day collapsed". The floor is what keeps the identity intact when the schedule does not.

## Implementation Intentions

Format: **"After [existing cue], I will [action] at [place]."** Not "I will exercise more" but "after I close the laptop, I walk for 20 minutes from the front door."

- Gollwitzer's meta-analysis of implementation intentions across 94 studies reports a medium-to-large effect (d≈0.65). That is why the format is a requirement in the close, not a stylistic preference.
- The cue must already be reliable. Anchoring to "when I have time" or "in the morning" is not a cue; anchoring to an event that happens whether or not they are motivated is.
- Pair it with a **coping intention** for the predictable obstacle: "if the meeting runs over, I walk at 18:00 instead." One if-then for the one obstacle they can name; more than one is planning as avoidance (`stuck.md`).
- Write the cue into `## Commitments` alongside the action. Six weeks later, "the cue stopped happening" explains a miss that otherwise looks like slippage.

## Check-in Design

| Cadence | Fits | Fails when |
|---|---|---|
| Daily | The first 7-14 days of a behavior with a high relapse cost | Becomes surveillance; the client starts reporting rather than doing |
| Weekly | Default for the first 30 days of any new behavior | Weekly for months signals the structure is not transferring |
| Biweekly | Steady-state behavior change, and most paid engagements | Too slow when a commitment is failing — tighten temporarily |
| Monthly | Strategic goals, senior clients, maintenance | Anything behavioral; a month is four chances to quietly stop |
| None | The client runs their own review reliably | Set only after they have demonstrated it, never as a default |

- Default: weekly for the first 30 days of a new behavior, then `checkin_cadence`. Write the cadence into `## Due` with its next date, or it will not happen.
- **The check-in has a fixed shape, three questions**: what did you commit to, what happened, what is next. Do not open with "how are you?" — the session drifts into narrative before the verdict exists.
- **Verdict first, story second.** Kept, missed, or renegotiated, stated in one word before any explanation. The explanation is useful; the explanation *instead of* a verdict is how accountability quietly disappears.
- Renegotiation before the deadline is legitimate and gets its own verdict. Renegotiation after it is a miss with extra steps, and calling it anything else teaches that deadlines are provisional.

## Handling a Miss

Sequence, in order (SKILL.md Rule 5):

1. **Verdict, neutral tone.** "So that did not happen." No sigh, no reassurance. Both are moral responses to a design question.
2. **"What got in the way?"** Never "why didn't you". The first answer is usually the circumstance; the second, after a pause, is usually the real one (`questions.md`).
3. **Resize.** Two consecutive misses of the same commitment → `new_size = old_size ÷ 2` and re-run the 20-minute test.
4. **Second halving still missed** → now the question is ownership, ambivalence, competing commitment, or capacity (`stuck.md`). Not before.
5. **Record it**: the verdict, the resize, and any pattern in `## Commitments` and `## Patterns`.

What makes a miss useful is that nothing about it is moral. What makes it corrosive is a coach who is visibly disappointed — the client then manages your reaction instead of their behavior, and the next report becomes unreliable. The most expensive failure mode in accountability is not the miss; it is the client who stops telling you the truth about misses.

## Ratcheting

- **Two consecutive hits → increase ~25%.** 20 minutes becomes 25, three days becomes four. Small enough that the streak survives the increase.
- **Never increase after a single hit.** One hit is noise; two is a rate.
- **Never increase and change the shape at the same time.** If the action itself changes, reset to the smaller size for two cycles — a new action has a new failure profile.
- **Ceiling**: when the ratchet reaches the level the goal actually requires, stop increasing and switch the conversation to consistency and transfer (below). Endless ratcheting produces burnout and reads as the coach moving the goalposts.

## Streaks and Their Failure Mode

- A streak is a tool for the first weeks, not a scoreboard for the engagement. Its job is to make the behavior visible; once the behavior is stable, tracking it adds nothing and its collapse costs something.
- **"Never miss twice"** is the whole rule. The first miss is an event; the second is what re-forms the old behavior. Design the recovery in advance: what the return looks like the very next day.
- **Do not reset the count to zero after a miss.** All-or-nothing counting is what turns one missed day into a fortnight, because the number the client cared about is already gone. Count the last 30 days as a rate ("22 of 30") — a rate absorbs a bad week without collapsing.
- Track the rate in the commitment row, not in a separate ledger; a tracking system with its own maintenance burden is a new commitment nobody agreed to.

## Environment Over Willpower

Willpower is the fallback when the design failed. Design first:

- **Reduce friction to the wanted behavior**: clothes out, file open, the first line already written, the meeting already in the calendar with the other person invited.
- **Add friction to the competing behavior**: the app logged out, the phone in another room, the card not saved. Physical distance beats intention, every time.
- **Use commitment devices** with real switching costs: a paid class, a booked room, a co-working slot, a training partner who shows up.
- **Body doubling** — working alongside someone, in person or on a call — is the single highest-yield structure for clients whose constraint is starting rather than knowing (`niches.md`).
- **Default times beat available times.** A recurring calendar block that nobody negotiates weekly outperforms "I'll find a slot", because finding a slot is a decision and decisions are the scarce resource.

## Stakes

Last resort, and only after sizing, cadence, and environment have all been tried.

- **Social stakes beat financial ones.** Telling one named person by a named date is more reliable than a penalty the client administers to themselves — self-administered penalties get quietly waived.
- The person told must be someone whose opinion carries weight and who will actually ask. "I'll tell my partner" without a date is not a stake.
- **Financial stakes cap at what the client would genuinely miss** and require a third party to enforce. A forfeit the client can cancel is theater.
- **Never make yourself the stake.** "I'd be disappointed" converts the work into pleasing the coach, and it holds right up until they stop booking.
- Stakes decay. A stake that worked for six weeks and stopped is not a failure of character; retire it and change the design.

## Weaning Off You

The test of the whole structure: check-ins should get *less* frequent over an engagement, not more (SKILL.md Rule 9).

- By the midpoint, the client sets their own commitments before the session and you verify the design rather than supplying it.
- By the final third, they run their own weekly review and bring the verdicts; your job is the pattern across weeks, which is the part they cannot see.
- Transfer artifact at the end: their own review format, written by them, saved to `artifacts/<kebab-name>.md` so it survives the engagement.
- Warning sign of dependency: commitments are kept in the week before a session and missed in the week after. That is compliance with a person, not a working structure — say it out loud and redesign.

**Every check-in writes**: the verdict on each open commitment, any resize with its reason, the new commitment with all three fields and its confidence number, and the next check-in date in `## Due` — all to `~/Clawic/data/coach/memory.md` in the same turn (`memory-template.md`). The verdict history is not bookkeeping: it is the input to Rule 5, and without it every miss looks like the first one.
