# Channel calibration & fact base — template (fill this in with your own material)

Copy Studio ships with **no brand facts and no sample copy on purpose**: inventing a statistic, a prize, or a capability is the worst failure a marketing-copy pipeline can produce, and someone else's samples would teach the wrong voice. This file is the scaffold you fill in. Nothing here is confidential until *you* put something in it — so if your filled-in copy lives in a shared or public repo, check that first.

Two parts: a **fact base** (§FB, the only citable source of truth) and **channel calibration** (§A–§x, 2–3 approved real samples per channel you ship to).

---

## §FB — Fact base (quote verbatim; never round, invent, or re-derive from memory)

The single source for reusable product facts. If a claim isn't on this list, it's `TBD` — mark it and surface it at the gate rather than guessing. When a number changes, change it **here** and let every sample that quotes it follow.

```
Product / offer
- What it is (one sentence, the way you actually describe it publicly):
- Where it lives (URL):
- Positioning line / category claim:
- Pricing / free-tier shorthand:

Capabilities (only what's shipped and verifiable)
- …
- …

Stats — record the exact written form you are allowed to publish
- e.g. `NNN,NNN+ users` · `NN,NNN+ projects`      ← keep the exact formatting
- Anything unconfirmed → write `TBD — unverified, do not cite externally`

Rewards / incentives / programs (if any)
- Contest name → prize, exactly as published:
- Signup / milestone credits:
- Creator or affiliate program terms:

Provenance note: which deck / page / legal source each figure came from, and when.
```

**Rules that make this file load-bearing**
1. One owner per fact. A number appears here once; other sections quote it, never restate it independently.
2. Date anything volatile (tool counts, headcounts, catalogue sizes) and re-verify before citing.
3. Never let a draft round a figure on its own — if the record says `48,207`, the copy says `48,207` (or whatever approved public form you list here), not "nearly 50K".

---

## Channel calibration sections

For each channel you actually ship to, keep **2–3 approved, real samples** plus the format rules the samples demonstrate. Samples teach shape and voice better than any description — that is why this file exists. Suggested sections (drop the ones you don't use, add your own):

| § | Channel | What to capture |
|---|---|---|
| A | Landing page — per-module spec | For each module: the copy, the wireframe note, and the image direction that shipped |
| B | Deck / slides | One sample per audience × scope (launch · single-product spotlight · partner/KOL) |
| C | Community seeding post | The first-person register that passed, not brand-voice |
| D | Contest / event invite comment | The general version *and* the promo-stripped Reddit version |
| E | Creator recruitment comment | Same split; note which rewards may be named where |
| F | Support / objection-handling reply | A real objection and the calm answer that worked |
| G | Comment reply — community invite | 2–3 approved replies showing the "one concrete detail" opener |
| H | Reddit playbook (evidence) | Your own removal/ban log: what was removed, what it carried, what you concluded. Operative rules stay in SKILL.md; this file holds the evidence |
| I | Video cover / thumbnail overlay | Winning overlays + the audience each was tested on |
| K | Template email | The block template + one worked example per variant, plus your image/handoff specs |
| L | Social captions per platform | One sample per platform for the same campaign, showing the link handling differences |

### Per-section skeleton

```
## §X. <Channel> (verbatim approved samples)

Format rules these samples demonstrate:
- Shape:
- Must-include:
- Length & voice:
- CTA / link handling:
- Visual:

Sample 1 (shipped <date>, <result if known>):
> …

Sample 2:
> …

Notes / traps: what got rejected here before, and why.
```

---

## Housekeeping

- **Keep this file out of public repos once it holds real material** — approved samples, unpublished stats, prize structures, and channel performance notes are usually internal. Add it to `.gitignore`, or keep it in a private location and point the skill at that path.
- Record *why* a sample was approved, not just the text. The reason is what generalizes to the next piece.
- When a channel rule changes (a platform stops making links clickable, a subreddit tightens its policy), update the rule **and** date it.
