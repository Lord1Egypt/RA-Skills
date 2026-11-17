# Writing — Item Craft and Summaries

The digest wins or loses per item. Every item has the same anatomy; every line in it has one job.

## Per-Item Anatomy

```
Headline → 1-line summary → why it matters to this user → (source)
```

- Four parts, in that order, every time. The reader learns the rhythm and scans at full speed.
- Depth overrides per topic come from preferences (`dimensions.md` → Depth); the anatomy never changes, only the summary's length.

## Headlines

- Front-load **actor + delta**: "Stripe cuts EU card fees" — not the outlet's curiosity-gap headline ("The pricing change nobody saw coming"). You are de-clickbaiting on the user's behalf.
- One line, no colon-subtitle constructions, no question headlines. A headline that asks a question is a summary that failed.
- Keep original-language proper nouns and product names untranslated; the summary carries the translation (`digest_language` variable).

## The Why-Line

- Must reference **this user's stake**: a tracked interest, entity, or stated goal. "Their main competitor now undercuts them on the exact tier you sell against" — not "this is big news for the industry".
- The anyone-test: could this line ship to a different subscriber unchanged? Then it is not a why-line; rewrite or demote the item to Worth Noting.
- Second-order items carry the connection chain explicitly (`triage.md` → Filter).

## Summaries

- One line: what happened, with the load-bearing number or name kept — "raised $40M Series B led by Index", not "raised a significant round".
- Facts come from the source; anything you inferred is prefixed "Likely:" or "My read:" (SKILL.md rule 2). Attribution vocabulary is fixed in `verification.md` → Attribution Grammar.
- Units, comparators, and timeframes survive compression: "up 40% YoY" never becomes "way up".

## Highlights

- Each Highlight must stand alone: a user who reads only the Highlights got the digest. If a Highlight needs a body item to make sense, it is not a Highlight.
- Highlight summaries may run two lines; the why-line is mandatory and does the heavy lifting.

## Update Items

- "Update:" + delta only — what changed since the last shipped version, never a re-summary of the whole story. "Update: the acquisition cleared EU review; closing moved to Q3."
- Link back in words to the prior frame ("the outage from Tuesday's digest") so the user doesn't have to remember.

## Worth Noting

- One clause + (source) per item. No why-line — its placement in Worth Noting IS the signal ("adjacent, judged minor").
- If a Worth Noting line needs a second clause to be understood, it belongs in the body or it belongs nowhere.

## Tone and Register

- Default: mirror the register of the user's own messages (`dimensions.md` → Format). A learned tone preference overrides.
- No editorial exclamation, no "exciting news!" — enthusiasm is the user's to have, not yours to perform. Dry wit survives; hype does not.

## Length Pressure

- The cut order is fixed: item count first, then Worth Noting tail, then summary length. The why-line is never cut — an item that loses its why-line loses its seat instead (SKILL.md rule 5).
