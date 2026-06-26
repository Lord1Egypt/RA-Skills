---
name: Coin Identifier
slug: coin-identifier
version: 1.0.0
homepage: https://clawic.com/skills/coin-identifier
description: "Identify coins from photos using evidence-based visual checks, ranked candidates, mint-mark reasoning, and a reusable local catalog."
changelog: "Initial release with ranked photo identification, evidence-based follow-up, and optional local coin memory."
metadata: {"clawdbot":{"emoji":"C","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/coin-identifier/"]}}
---

## When to Use

Use when the user wants to identify a coin from one or more photos, narrow down similar issues, log a collection piece, or separate likely type from later grading or pricing work.

## Architecture

Memory lives in `~/coin-identifier/`. If `~/coin-identifier/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/coin-identifier/
├── memory.md
├── identifications/
│   └── YYYY-MM/
│       └── {entry-id}.md
└── exports/
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Coin evidence checklist | `evidence-guide.md` |

## Scope

This skill ONLY:
- identifies coins from visible evidence in user-supplied images
- returns ranked candidates with explicit confidence and missing evidence
- asks for the next best photo or measurement when the evidence is incomplete
- stores local identification notes only if the user approves

This skill NEVER:
- guarantee authenticity, grade, mint error status, metal purity, or market value from photos alone
- recommend cleaning, polishing, or altering a coin
- upload images or coin data to external services

## Security & Privacy

**Data stored locally if approved by the user:**
- activation and response preferences in `~/coin-identifier/memory.md`
- one note per saved identification in `~/coin-identifier/identifications/`

**This skill does NOT:**
- make network requests
- claim professional grading or authentication
- write local files without user approval

## Core Rules

### 1. Clear the photo gate before naming a coin
- Check subject isolation, glare, blur, crop, orientation, and whether the obverse, reverse, or edge are missing.
- If the coin is angled, reflective, inside a sleeve, or mixed with other coins, ask for a tighter straight-on view first.

### 2. Return ranked candidates with confidence, not one blind guess
- Give one to three candidates with confidence bands: High 85-95, Medium 60-84, Low 35-59.
- For each candidate, cite the visible evidence and the missing evidence.
- If the signal is weak, say the result is an unresolved shortlist instead of pretending certainty.

### 3. Use coin evidence in a fixed order
- Open `evidence-guide.md` before deciding.
- Work from country or script, portrait or emblem, denomination, date, mint mark, metal color, shape, rim or edge, then commemorative cues.
- Keep obverse, reverse, and edge evidence separate.

### 4. Ask for the next best view, not generic more photos
- Prefer straight obverse, straight reverse, edge, mint-mark crop, and scale or weight.
- Explain which missing feature would separate candidate A from candidate B.

### 5. Separate identification from value, grading, and authenticity
- Photo identification can narrow the type and likely issue without proving grade, rarity, or authenticity.
- If the user wants value or authenticity, treat identification as step one and keep the rest provisional.

### 6. Keep memory useful and lightweight
- Save only durable preferences and approved identification notes.
- One saved entry should record date, coin label, best match, confidence, evidence, and unresolved questions.
- Do not write files unless the user approves local storage.

### 7. Say what could change the answer
- Highlight wear, glare, missing edge data, foreign-script ambiguity, and similar commemoratives when they limit certainty.
- Update the shortlist immediately if a better image or measurement changes the balance.

## Common Traps

- Guessing from one reflective angled photo -> dates, mint marks, and legends disappear.
- Treating any silver-colored coin as silver bullion -> composition and coin type get conflated.
- Calling a commemorative theme the country or denomination -> wrong catalog family.
- Jumping from identification to market value -> grade, authenticity, and demand remain unverified.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `image` - inspect and optimize photos before identification
- `image-edit` - crop, isolate, and clean up the subject for clearer review
- `inventory` - maintain a broader catalog once coins are identified
- `scanner` - improve flat top-down captures of coins, cards, or documents

## Feedback

- If useful: `clawhub star coin-identifier`
- Stay updated: `clawhub sync`
