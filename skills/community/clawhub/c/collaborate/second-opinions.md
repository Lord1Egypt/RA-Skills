# Second Opinions — Two Defensible Options, One Decision

For the stuck state: both options survive scrutiny and you keep re-reading them. The exchange exists to surface a difference in consequences, not to award a winner by eloquence. Blind pass by default: an independent read is the whole value (SKILL.md, Where Experts Disagree).

## Before Recruiting Anyone

1. **Check reversibility.** Two-way door with undo cost under `solo_undo_threshold` (default 15 min)? Pick either, ship, observe — the exchange costs more than trying. One-way doors are what second opinions are for.
2. **Write both loss stories.** For each option, one line: what you lose if it is wrong. If one story is clearly worse, you were not stuck — you were avoiding the safe-but-boring option.
3. **Write your leaning and its kill condition** (SKILL.md Rule 5) — but do not show it yet.

## Techniques

- **Loss-function swap.** Judge each option as the person maintaining it 6 months from now: on-call at 3am, original author gone, context lost. Options that tie on elegance rarely tie on maintenance.
- **What would have to be true** (Lafley/Martin): for each option, list the conditions under which it is clearly right. Then check which condition set matches reality you can verify today. Converts "which is better" into checkable claims.
- **Steelman swap.** Argue the option you lean against for one full round, well enough that its advocate would sign your version. Most stuck states dissolve here: you discover you cannot, or you convince yourself.
- **Disconfirming hunt.** For your leaning, actively search for the evidence that would kill it. You have already collected the confirming evidence — that is why you lean.

## Asking For a Second Opinion (You Are the Requester)

- Give: the decision, the real constraints, both options, your kill condition.
- Withhold your leaning when the counterpart might defer to you (they report to you, they want the exchange over, they are an agent inheriting your frame). Present options in an order that does not signal preference.
- Reveal your leaning when the counterpart is senior/blunt and the anchor speeds things up.
- Ask the falsifiable form: "under what conditions is option B the wrong choice?" — not "which do you like?"

## Giving a Second Opinion (You Are the Counterpart)

- First establish what the requester optimizes for; a correct opinion against the wrong objective is noise.
- Answer the decision asked, not the decision you find more interesting.
- If both options are genuinely fine: say so explicitly and name the secondary criterion that breaks the tie. "Either works, pick X for operational simplicity" is a complete, honest answer.

## Ties After an Honest Exchange

A tie that survives the techniques above means the options are equivalent within your resolution. Break by secondary criteria in this order: reversibility → operational simplicity → optionality preserved. Record the tie itself in the decision record; "we chose X on a tie" is a legitimate entry and stops re-litigation.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Laundering a made decision | You already chose; the "opinion" is a witness signature | Skip the exchange, own the decision (SKILL.md Traps) |
| Neutral-framing everything | Stripping your constraints to "be fair" makes the counterpart decide a different, easier problem | Give real constraints; withhold only the leaning |
| Adding options mid-exchange | Three options reset the exchange to divergence | Park new options; finish judging the two |
| Counting opinions | Two agreeing counterparts with the same information are one opinion | One independent counterpart beats three anchored ones |
