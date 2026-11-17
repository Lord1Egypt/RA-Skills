# Writing — Line-Level Compression

The craft below the structure: how individual lines earn their place. Voice preferences (directness, person, formality floor) live under the **Voice** preference area in config.

## Bottom-Line Formulas

Two shapes cover most briefs:
- State + consequence: "[What is true] — [what it means for the reader]." → "Q3 launch slips 2 weeks unless we cut analytics."
- Change + so-what: "[What changed] — [what it changes for the reader]." → "Vendor raised prices 20%; the build-vs-buy math now favors build."

Test: the reader stops after this sentence and still acts correctly. "And" inside it = two takeaways = pick one (SKILL.md Rule 4).

## Bullets

- Verb or fact first; the qualifier trails: "Payments passed review — critical path is now analytics", never "Following the review process, it was determined that...".
- One fact per bullet. Two facts sharing a bullet hide whichever the reader needed.
- Two lines maximum per bullet; a third line means it wants to be two bullets or a linked doc.

## Hedge Blacklist

Each hedge becomes either a commitment or a named uncertainty — never stays a hedge:

| Hedge | Replace with |
|-------|--------------|
| "somewhat behind" | "3 days behind" |
| "it seems / appears that" | The claim, plus its evidence — or cut the claim |
| "may potentially impact" | "will cost X if Y happens" |
| "broadly on track" | "On track" or "At risk" — Rule 7 has no third state between them |
| "we should probably" | "Recommend X by [date]" |
| "hopefully" | The plan, or the risk line |

Named uncertainty is not hedging: "60% confident; the vendor's Friday response settles it" gives the reader something to act on. "It's somewhat uncertain" gives them nothing.

## Numbers

- Decision-grade rounding: 2-3 significant figures ($1.23M, not $1,234,567.89). False precision slows the read and implies confidence the data doesn't have.
- Comparator attached at the line, not in a footnote (SKILL.md Rule 6).
- Direction words match the sign: "up 8%", "down 3 days" — never "changed by 8%".
- Volatile numbers carry as-of dates inline: "pipeline $2.1M (as of Jul 21)".
- Percentages of small bases expose the base: "2 of 3 customers churned", not "67% churn".
- Currency and dates render per `locale` (config.yaml, else `~/Clawic/profile.yaml`, else en-US): `$1.2M` / `Jul 21` for en-US, `1,2 M€` / `21 Jul` for a European reader — decimal/thousands separators flip with it (`1,234.5` vs `1.234,5`). Match the reader's convention, not the source's; timestamps carry the reader's timezone (`14:00 CET`, not the server's UTC).

## The Cutting Pass

Draft, then cut before delivering — in this order, because each pass exposes the next:

1. Delete throat-clearing: openers ("I wanted to give you an update on..."), meta-commentary ("as you may know"), and closers that restate.
2. Merge duplicate points — two bullets sharing a so-what are one bullet.
3. Demote context that doesn't change the reader's action (SCQA test, `templates.md`) to a link or an appendix.
4. Replace phrases with their numbers: "significantly over budget" → "$40k over".

Over `default_length` after all four passes → the brief has too many points, not too many words; return to Rule 5 and cut a point.

## The Ask

Owner + verb + date + consequence: "Ana to approve the cut by Friday, or launch slips 2 weeks."
- An ask without a date is an FYI wearing a costume.
- An ask without an owner is a wish.
- Multiple asks: number them, one owner each — "the team" owns nothing.

## Bad News

- State the fact plainly, mitigation in the same breath: "We lost the Acme renewal ($120k ARR). Two comparable deals are in late stage; pipeline still covers the Q4 target."
- No adjective softeners: "slight miss", "minor slip", "a bit of a challenge" — the number already says how big it is; the softener says you're managing them.
- Never let the reader discover the size of bad news later than sentence two of its section — delayed magnitude reads as concealment.
