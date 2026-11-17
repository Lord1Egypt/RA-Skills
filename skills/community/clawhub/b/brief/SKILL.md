---
name: Brief
slug: brief
version: 1.0.4
description: >-
  Turns raw material into decision-ready briefs: executive summaries, status updates,
  meeting pre-reads, and decision documents. Use when asked to brief someone, write a
  TL;DR or weekly update, prepare a board, investor, or incident update, hand off a
  project, compare options with a recommendation, or condense a long report, thread,
  transcript, or doc pile into what the reader needs to act. Also when updates run long,
  readers skim past the point, or the lede keeps getting buried. Not for plain
  compression with no decision to serve, or for recurring digests pulled from external
  sources.
homepage: https://clawic.com/skills/brief
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 📋
    os:
    - linux
    - darwin
    - win32
    displayName: Brief
    configPaths:
    - ~/Clawic/data/brief/
---

User configuration and learned preferences live in `~/Clawic/data/brief/` (see `setup.md` on first use, `preferences-template.md` for the learned-preferences file format). If you have data at an old location (`~/brief/` or `~/clawic/brief/`), move it to `~/Clawic/data/brief/`.

## When To Use

- User asks for an executive brief, TL;DR, or bottom-line summary of material they provide
- A recurring status or project update is due and the reader needs the delta, not a restate
- A meeting, board session, or review is coming up and the reader needs decisions-needed plus prep
- An incident is live and stakeholders need impact, status, and a committed next-update time
- A transition, offboarding, or vacation cover needs a handoff with gotchas and open questions
- The reader must choose between options and needs a recommendation with tradeoffs
- A long report, thread, transcript, or doc pile must be condensed to what drives a decision

Not for: compressing content when there is no decision or action to serve — use `summarizer` for shorter-content-only needs.

## Quick Reference

| Situation | Play |
|-----------|------|
| Reader must choose between options | Decision brief: recommendation first, 2-3 options including do-nothing (`templates.md`) |
| Recurring status update | Project brief: lead with the delta since last brief, never a full restate (`recurring.md`) |
| Meeting coming up | Meeting brief: decisions needed + prep checklist; deliver the day before, not the morning of (`delivery.md`) |
| Board or investor update due | Board brief: metrics vs plan, lowlights before highlights, explicit asks (`templates.md`) |
| Something is on fire right now | Incident brief: impact in user terms, status, committed next-update time (`templates.md`) |
| Findings must become a decision | Research brief: answer with confidence level, evidence split from interpretation (`templates.md`) |
| Transition, offboarding, vacation cover | Handoff brief: gotchas and open questions outrank achievements (`templates.md`) |
| Source is huge or messy | Triage by decision-relevance, never proportionally to source length (`sources.md`) |
| Sources disagree or have gaps | Show the conflict and name the gap — never average or silently narrow (`sources.md`) |
| Audience unclear or mixed | Name the decider; their action sets depth and jargon (`audiences.md`) |
| Formal channel (exec email, external doc) | Same structure, strip emoji markers, plain headers (`delivery.md`) |
| Brief keeps coming back "too long" | Cutting passes, hedge blacklist, decision-grade rounding (`writing.md`) |
| User reacts to a delivered brief | Record it in `~/Clawic/data/brief/preferences.md`; signal mapping in `dimensions.md` |
| Anything else | Executive structure: bottom line, 3 key points, explicit ask |

Depth on demand: `templates.md` section-by-section structures per type · `sources.md` raw-material triage, conflicts, gaps · `audiences.md` reader calibration · `delivery.md` channels, register, timing · `writing.md` line-level compression · `recurring.md` running a brief series · `dimensions.md` preference taxonomy · `setup.md` first-use loading.

## Core Rules

### 1. User Specifies Sources
When the user requests a brief:
1. User provides the information OR specifies where to get it
2. If a source requires access, the user grants it explicitly
3. Skill structures and formats the output

Example:
```
User: "Brief me on project X status"
Agent: "I'll need access to the project docs. Can you share
        the status doc or grant access to the project folder?"
User: [shares doc or grants access]
→ Brief generated from user-provided source
```

### 2. A Brief Is Not a Summary
A summary compresses content; a brief serves the reader's next action. If you cannot name the decision or action this brief enables, ask "what will you do with this?" before writing. Competent people summarize; briefers select.

### 3. Write in Reverse Reading Order
Compose ask → bottom line → key points → context; the reader consumes the opposite order. Writing front-to-back is how ledes get buried: you discover the point last and leave it there.

### 4. Bottom Line Commits
One sentence, no hedge. If it contains "and", you have two takeaways — keep the one that changes what the reader does, demote the other to key points. "Mostly on track, but..." is not a bottom line; it is a decision you refused to make.

### 5. Three Key Points, Five Hard Max
A point qualifies only if removing it would change the reader's decision. Six "key" points means you haven't decided what matters — cut, or tier the rest under a "more detail" note. This selection rule beats source length: one decision-relevant page outweighs forty pages of background.

### 6. Every Number Carries a Comparator
"$1.2M revenue" is decoration; "$1.2M, 8% under plan" is a brief line. Valid comparators: target, prior period, benchmark. None available → write "no baseline yet" or drop the number.

### 7. Status Words Have Definitions
- **On track** — schedule/scope buffer intact
- **At risk** — buffer being consumed; the first slip counts, no grace period
- **Blocked** — cannot proceed without a named external action

Declaring at-risk early is cheap. A green-to-red flip with no warning destroys trust in every future brief you send. (`status_scheme: rag` in config maps these 1:1 to Green/Amber/Red.)

### 8. Learn Only From Explicit Feedback
"Too detailed" / "missing X" / "perfect" → one line in `~/Clawic/data/brief/preferences.md` with a level (`pattern`/`confirmed`/`locked`, promotion rules in `dimensions.md`). Check the file before writing any brief — a well-built brief in the wrong learned format still misses.

## Scope

This skill:
- ✅ Structures information the user provides into briefs (act-as writer: it drafts; the user sends)
- ✅ Learns format preferences from explicit feedback
- ✅ Stores configuration and preferences in `~/Clawic/data/brief/`

**User-driven model:** the user specifies WHAT information to include and grants access to any needed sources; the skill handles STRUCTURE and FORMAT.

This skill does NOT:
- ❌ Access files, email, or calendar without user request
- ❌ Pull data from sources the user hasn't specified
- ❌ Store brief content (only configuration and format preferences)

## Output Gates

Run before delivering any brief:
- [ ] Bottom line survives alone — if the reader stops there, they still have the takeaway
- [ ] Every metric has a comparator or an explicit "no baseline yet"
- [ ] The ask names an owner and a date, or states "no action needed" — never an implied ask inside an FYI
- [ ] Bad news sits above the fold, next to its mitigation, not in section four
- [ ] Data that can go stale carries source and as-of date
- [ ] Conflicting sources are shown as a conflict, never averaged into one number
- [ ] Jargon calibrated to the least-technical decider, not the most technical reader
- [ ] Format matches `~/Clawic/data/brief/config.yaml` and `preferences.md` — checked, not remembered

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/brief/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_length | one-screen \| one-page \| two-page | one-page | Sizing target: one-page = 450-500 words (`templates.md`); one-screen = fits without scrolling (chat cap, `delivery.md`); two-page only when the reader asked for depth |
| status_scheme | words \| rag | words | Status labels everywhere a status renders: On track/At risk/Blocked vs Green/Amber/Red (definitions in Rule 7 apply to both) |
| emoji_markers | bool | true | Section markers (⚡📊🎯) on informal channels; false = plain headers everywhere (formal channels strip them regardless, `delivery.md`) |
| default_channel | chat \| email \| doc | chat | Assumed delivery surface; sets register and length caps per `delivery.md` |
| locale | text (BCP-47, e.g. en-US) | en-US | Date order (Jul 21 vs 21 Jul), decimal/thousands separators, and currency symbol + placement in every rendered number and date (`writing.md`); falls back to `~/Clawic/profile.yaml` before the default |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:
- **Audience mix**: who reads most briefs (boss, board, clients, team) — shifts the default template and jargon level (`audiences.md`)
- **Conventions**: section names, bullet style, status-word extensions — shifts the structures in `templates.md`
- **Timing**: lead times, cadence, delivery day — shifts the scheduling guidance in `delivery.md`
- **Exclusions**: topics or metrics never to include (confidential, legal) — screens extraction in `sources.md`
- **Voice**: bad-news directness, person (I/we/team), formality floor — shifts the register rules in `writing.md`
- **Localization**: beyond the `locale` tag — timezone for timestamps and deadlines, and multi-currency policy (show native vs converted, which symbol) when amounts span currencies — affects number lines in `writing.md` and the incident/board timestamps in `templates.md`

Config vs learned preferences: `config.yaml` holds what the user declared; `preferences.md` holds what feedback revealed (levels in `dimensions.md`). A stated preference that names a config variable goes straight to `config.yaml`. Precedence: config > `confirmed`/`locked` learned preferences > defaults. Universal variables (`locale`, timezone) additionally fall back to `~/Clawic/profile.yaml` before their table default: config > `profile.yaml` > default.

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Burying the lede | Readers triage; the point placed last is the point never read | Bottom line first — and write it first (Rule 3) |
| Hedged bottom line | Reader cannot act on a hedge | Commit to one takeaway; nuance goes in key points |
| Watermelon status (green outside, red inside) | The eventual flip costs more trust than early honesty ever would | First buffer slip → At risk (Rule 7) |
| Summarizing proportionally to source length | Background volume drowns the decision material | Select by decision-relevance (Rule 5, `sources.md`) |
| Averaging conflicting sources | Reader inherits a number nobody actually reported | Show both figures with provenance; the conflict may be a key point (`sources.md`) |
| Sandwiching bad news | In a brief, softening reads as hiding | Bad news first, mitigation beside it |
| Options without a recommendation | "Neutral" presentation transfers your analysis work to the reader | Recommend one; keep tradeoffs honest and visible |
| Exactly two options | Frames a false binary and hides the status quo | Price do-nothing as an explicit option (`templates.md` → Decision) |
| One brief for decider and spectators | Too deep for one, too shallow for the other | Write for the decider; spectators get the same brief, not a longer one (`audiences.md`) |
| Restating unchanged items every edition | Trains readers to skim; they miss the week something changes | Delta only, unchanged sections collapse to one line (`recurring.md`) |
| Precision theater ($1,234,567.89) | False confidence and a slower read | Decision-grade rounding: 2-3 significant figures (`writing.md`) |
| Emoji markers on formal channels | Reads unserious to exec/external audiences | Same structure, plain headers (`delivery.md`) |

## Where Experts Disagree

- **Bullets vs narrative memos.** The Amazon six-page school argues prose forces complete thinking; the BLUF school argues readers triage and bullets respect that. Boundary: match the reading ritual — narrative where the room reads silently before discussing; bullets where the brief replaces the meeting. Default here: bullets, with a prose-memo variant in `templates.md`.
- **Recommendation-first vs neutral staffing.** Staff tradition separates information briefs from decision briefs and warns against advocacy; operators say a briefer who won't recommend transfers the analysis work. Boundary: recommend by default; go neutral only when brokering between peer factions — and say you're doing it.
- **How much context.** "Context is respect for the reader" vs "context is where ledes go to die." Boundary: context earns lines only when it changes how the reader acts on the points; SCQA-test it (`templates.md`), otherwise cut.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/brief (install if the user confirms):
- `summarizer` - compression when there is no decision to serve, just shorter content
- `digest` - recurring curated updates pulled from external sources on a schedule
- `report` - recurring configured reports with fixed data sources
- `meetings` - the full meeting system (notes, agendas, follow-ups); brief covers only the pre-read

## Feedback

- If useful, star it: https://clawic.com/skills/brief
- Latest version: https://clawic.com/skills/brief

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/brief.
