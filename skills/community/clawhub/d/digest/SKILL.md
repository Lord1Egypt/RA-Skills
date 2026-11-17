---
name: Digest
slug: digest
version: 1.0.3
description: >-
  Curates news, feeds, and industry sources into personalized recurring digests: sourcing,
  filtering, ranking, and delivery. Use to set up a daily briefing or morning/evening news
  roundup, track competitors, an industry, people, or markets, or run a scheduled or weekly
  update. Also when a digest feels too long or repetitive, keeps missing stories, or a rumor
  needs checking before it ships. Covers source vetting, deduplication, single-source holds,
  corrections, urgent alerts, slow news days, and channel formats (email, Slack, Telegram,
  audio); learns format, timing, and depth preferences from reactions. Not for summarizing
  documents the user provides or internal business reporting.
homepage: https://clawic.com/skills/digest
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 📰
    displayName: Digest
    configPaths:
    - ~/Clawic/data/digest/
---

User preferences, learned signals, and the sent-item log live in `~/Clawic/data/digest/` (see `setup.md` on first use, `preferences-template.md` for file formats). If you have data at an old location (`~/digest/` or `~/clawic/digest/`), move it to `~/Clawic/data/digest/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/digest/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| item_cap | number (3-15) | 8 | Hard ceiling on items per digest (rule 5); Highlights stay ≤3 at any cap |
| single_source_policy | hold \| hedge | hold | Market-moving or reputational single-source claims: hold one cycle vs ship marked "one source, unverified" (`verification.md`) |
| channel | text | channel where the digest was first requested | Where digests deliver; drives the per-channel format rules in `delivery.md` |
| digest_language | text | the language the user writes in | Digest prose language; items keep original-language names and quotes with translated summaries |
| timezone | text | `~/Clawic/profile.yaml`, else confirm before first scheduled send | Anchors every scheduled slot and recency window |

Preference areas — learned state lives in `~/Clawic/data/digest/preferences.md` and climbs the ladder in `learning.md`:

- **content scope** — topics, industries, competitors, people, regions, exclusions; drives Filter
- **sourcing** — trusted and blocked sources, weighting, recency windows; drives Source
- **format & structure** — medium, structure, length, tone, visuals; drives Format
- **timing & cadence** — schedule, frequency, weekday/weekend split, urgent-signal rules; drives Deliver
- **prioritization & depth** — what leads, what buries, per-topic depth; drives Prioritize

## When To Use

- The user wants a recurring **daily or weekly briefing** on topics they care about
- A **news roundup** filtered to one person's interests, not a generic feed
- **Tracking competitors, an industry, people, or markets** with ongoing updates on their moves
- A **scheduled topic update** is due, or the source list needs building or tuning
- An existing digest feels off: too long, repetitive, missing stories, wrong timing
- Not for: synthesizing documents the user hands you (→ `synthesize`), internal business reporting (→ `brief`), or full competitor dossiers (→ `competitor-monitoring`)

The test of a real digest: every item carries a why-this-matters-to-you line. A digest that could be sent to anyone is a feed, not a digest.

## Quick Reference

| Situation | Play |
|---|---|
| First digest, no preferences | Derive topics from the request; if none derivable, ask the one blocked question (topics) — everything else runs on defaults |
| Story covered by 3+ independent sources | Promote toward Highlights — convergence is an importance signal (rule 4) |
| Surprising claim from a single source | Hold one cycle or ship hedged per `single_source_policy`; independence test in `verification.md` |
| Major global news outside user's topics | One line in Worth Noting, never a Highlight — relevance beats magnitude (rule 1) |
| User says "too long" | Cut item count before per-item depth; log the signal (`learning.md`) |
| Story already shipped in a prior digest | Resurface only as "Update:" + what changed — check the sent log (rule 7) |
| Urgent item mid-cycle | Interrupt only on a [confirmed] or [locked] urgent-signal rule; otherwise hold (`delivery.md`) |
| No reaction for 3 consecutive digests | Ask one concrete question instead of guessing (`learning.md`) |
| Slow news day in their topics | Send the short honest version ("quiet day, 2 items") — never pad |
| Big-event day floods one theme | Cluster the theme into one block that counts as one item (`triage.md`) |
| Competitor activity to report | Moves, not mentions — the move catalog is in `competitors.md` |
| Gap since last digest (vacation, downtime) | One consolidated catch-up covering the period, top items only (`delivery.md`) |
| Anything else | Run Source → Filter → Prioritize → Format → Deliver → Learn with current preferences |

Depth on demand: `sources.md` building and vetting the source list · `triage.md` dedupe, ranking, slow and heavy days · `verification.md` claims, rumors, corrections · `writing.md` item craft and summaries · `delivery.md` channels, timing, interrupts · `learning.md` signals and the preference ladder · `competitors.md` tracking companies and people · `dimensions.md` dimension catalog with defaults · `preferences-template.md` data-file formats.

## Core Rules

1. **Relevance beats magnitude.** Rank by interest match first, freshness second, source weight third. A tracked competitor's pricing change outranks a world-news headline outside their topics.
2. **Every item is attributed.** No source you can name = item does not ship. Never blend your own inference into a summary unmarked — prefix it: "Likely:" or "My read:".
3. **Exclusions are binary, interests are weighted.** One explicit "don't care about Y" beats any number of inferred interest signals for Y. An excluded topic appears only when it intersects a confirmed interest, flagged as such ("normally excluded; included because it hits X").
4. **Dedupe before ranking.** Same story from N outlets = one item; N itself is rank input — 3+ independent sources covering one story promotes it toward Highlights. Independence = separate original evidence, not separate URLs (`verification.md`).
5. **Fixed budget forces curation.** `item_cap` (default 8) items, hard max 3 Highlights. Adding one over cap means deleting one. Worked example: 12 candidates → 3 Highlights (top interest-match), 5 body items, remaining 4 dropped or compressed into one Worth Noting line.
6. **Preference changes climb a ladder** — pattern → confirmed → locked, mechanics in `learning.md`. Never jump from a single signal to locked.
7. **The digest remembers what it sent.** Log every shipped item to `~/Clawic/data/digest/sent-log.md`; repeats resurface only as "Update:" + delta. A digest without memory re-reports yesterday and reads as a broken filter.

## Protocol

```
Source → Filter → Prioritize → Format → Deliver → Learn
```

1. **Source** — pull from configured feeds and the per-entity source kits (`sources.md`). Default weighting: primary > original reporting > aggregators > social; social is discovery, never citation — trace it back before it ships.
2. **Filter** — topic match includes; exclusion match drops (rule 3); recency windows per content type (`dimensions.md` → Sources); single-source surprising claims go to `verification.md`.
3. **Prioritize** — cluster duplicates, then rank per rule 1; bury borderline items into Worth Noting, don't delete (`triage.md`).
4. **Format** — per-item shape: headline → 1-line summary → why it matters to this user → (source). Craft rules in `writing.md`; length pressure cuts item count before per-item depth.
5. **Deliver** — channel and timing per preferences; interrupts, catch-ups, and per-channel formats in `delivery.md`.
6. **Learn** — capture reactions into `preferences.md` after every delivery; signal counting and ladder in `learning.md`.

## Output Format (Default)

```
📰 [DIGEST TYPE] — [DATE/TIME]

🔥 HIGHLIGHTS
• [Item — 1-line summary + why it matters to you (source)]
• [Second item]

📋 FULL DIGEST
[Items in per-item shape, ordered per weighting profile]

💡 WORTH NOTING
[Borderline items, one line each]

---
Sources: [count] | Next digest: [time]
```

Adapt entirely to learned preferences once they exist; the template above is only the cold-start default.

## Output Gates

Before sending, verify:

- Every item has a source and a why-it-matters line?
- ≤3 Highlights, each strong enough that the user could read only those?
- Zero exclusion-list items, unless flagged per rule 3?
- Every single-source claim hedged or held per `single_source_policy`?
- Nothing repeated unchanged from the sent log?
- Channel and time match current preferences; signals from the previous delivery recorded?

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Leading with globally important news | User already saw it everywhere; the digest adds zero | Lead with niche relevance; big news gets one line (rule 1) |
| Padding slow days | Trains skimming; erodes trust in Highlights | Short honest digest ("quiet day") |
| Counting syndicated copies as corroboration | Ten outlets rewriting one press release or tweet are one source | Independence test in `verification.md` before promoting |
| Trusting aggregator timestamps | Aggregators resurface old stories with fresh dates | Check the original dateline against the event date (`sources.md`) |
| Locking a preference from one comment | One signal may be mood, not preference | Climb the ladder in `learning.md` (rule 6) |
| Reading silence as satisfaction | Ignored digests look identical to loved ones | No reaction for 3 consecutive digests → ask one question |
| Unmarked opinion inside summaries | User can't separate reporting from your read | Attribute claims; prefix inference (rule 2) |
| Resurfacing yesterday's story unchanged | Repetition reads as a broken filter | Only resurface as "Update:" + what changed (rule 7) |
| Interrupting off-schedule on your own judgment | "Urgent" without a learned rule is noise at a bad hour | Interrupt only per [confirmed]+ urgent-signal rule (`delivery.md`) |

## Where Experts Disagree

- **Curation vs completeness.** Tight curation is the default — the budget is the product. Some readers want everything as FOMO insurance; the boundary is an explicit request, and the answer is a longer Worth Noting tail, never a bigger Highlights section.
- **Relevance-first vs breaking-first.** Default: highest interest-match leads. Breaking-first is legitimate for users who act on time-sensitivity (markets, on-call, PR); it must be learned or stated, never assumed from topic choice.
- **Neutral summarizer vs opinionated curator.** The why-it-matters line is opinion, and it is the digest's value. The boundary: reporting is attributed, inference is prefixed — the reader always knows which is which (rule 2).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/digest (install if the user confirms):

- `brief` — internal business information summarized rather than external news curated
- `synthesize` — the user provides the documents; you distill instead of sourcing the outside world
- `competitor-monitoring` — full competitor dossiers, pricing alerts, and positioning analysis beyond digest items
- `newsletter` — the user wants to publish to an audience, not receive a personal digest

## Feedback

- If useful, star it: https://clawic.com/skills/digest
- Latest version: https://clawic.com/skills/digest

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/digest.
