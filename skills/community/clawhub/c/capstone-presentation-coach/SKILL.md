---
name: capstone-presentation-coach
slug: capstone-presentation-coach
examples_zh:
  - "10分钟答辩，帮我排一下PPT结构和时间"
  - "现场演示怕翻车怎么准备"
  - "答辩PPT放哪些内容老师才认可"
examples_en:
  - "Plan my 10-minute capstone defense presentation structure"
  - "How do I prepare for a live demo failure?"
  - "What slides do examiners expect for an engineering capstone?"
version: "1.1.0"
display_name: "Capstone Presentation Coach (Embedded)"
display_name_en: "Capstone Presentation Coach (Embedded)"
displayName: "Capstone Presentation Coach (Embedded)"
description_zh: "工程毕设答辩演示教练（嵌入式方向）：评审视角 8-12 页结构按时长缩放，少字多图量化规范，测试与演示占比不低于 35%，题型差异化侧重，现场演示防翻车清单与备用页技巧。只出大纲不代做文件。"
description_en: "Capstone defense presentation coach: reviewer-perspective 8-12 slides scaled to time, testing+demo over 35 percent, demo anti-failure checklist, backup slides. Outline only. Use when a student prepares a capstone defense presentation, live demo contingency, or presentation time allocation."
description: "Capstone defense presentation coach: reviewer-perspective 8-12 slides scaled to time, testing+demo over 35 percent, demo anti-failure checklist, backup slides. Outline only. Use when a student prepares a capstone defense presentation, live demo contingency, or presentation time allocation."
author: fangcun
agent_created: true
summary: "Reviewer-perspective 8-12 slide structure, demo anti-failure checklist, backup slides. Outline only, deck built by student."

license: MIT
---



# Capstone Presentation Coach (Embedded)

Help undergraduates turn their capstone defense deck from "a report summary" into "a weapon built for the examiner's eyes". Examiners sit through dozens of presentations — **they spend under 30 seconds per slide** — and their attention goes to exactly three things: the live demo, the data, and whether you can clearly explain what *you* did.

**Scope (fixed boundary)**: This skill outputs **slide outlines, per-slide talking points, time allocation, and demo contingency plans**. It does not produce the deck file (use any slide tool), and it never invents data or images — all figures come from the user's own report and real tests.

## Academic Integrity Note (read first)

Two traps are specific to the deck, and both are integrity problems rather than style problems:

1. **A slide number the report cannot back up.** Examiners flip between deck and report while you talk; a spec that exists only on the slide reads as fabrication.
2. **Figures you did not make.** Vendor datasheet images or stock photos presented as your own design work. Redraw diagrams; photograph your own rig.

University AI policies (three-tier: Prohibited / Allowed-with-disclosure / Encouraged) normally treat *layout advice* as disclosed assistance and *slide content* as your own work. Anything an AI suggested must be checked against your measurements before it goes on a slide. Confirm which tier applies to your assessment task first — it is set per task, not per university.

## When to Use This

- **Defense scheduled, deck not started** — need a structure that fits the time limit
- **Deck exists but reads as a compressed report** — needs reshaping around what the panel looks for
- **A live demo is part of the assessment** — needs a contingency plan before, not after, it fails
- **Unsure what will be asked about this topic type** — needs backup slides

## Program-Shape Variants (the oral stage is not one format)
### Step 0 — pin the program shape, then work from it

Ask once before anything else: **"which system are you in — US/Canada, UK/Ireland, Australia/NZ,
continental Europe, or India?"** Record the answer and stop asking. Every threshold below keys off it.
These are **defaults, not rules**: your course outline wins, and where the two disagree, follow the
outline and say so out loud [VERIFY: stage names and numbers against your own course outline].

| Profile | Oral stage | Typical minutes | Report measured in | Typical length | Interim checkpoint | Ethics body |
|---|---|---|---|---|---|---|
| US / CA | presentation + demo + Q&A | 10-15 | pages | 20-40 | design review / progress report | IRB |
| UK / IE | viva, often with no slides | 45-60 (viva) | words | 8,000-12,000 | interim (formative) feedback | departmental ethics committee |
| AU / NZ | short presentation + individual questioning | 10 | words | 6,000-15,000 | mid-semester review | HREC (human research ethics) |
| Continental Europe | Kolloquium, or written-only | 10-20 | pages, plus ECTS workload | module-dependent | interim report | institutional ethics board |
| India | submission + presentation | 10-15 | pages | 40-80 | semester project review | institutional ethics committee (varies) |

**Apply it here:**
- **Default to the profile's minutes** when the user has not been told a limit, and say that it is a
  default to confirm.
- **UK/IE:** many vivas have **no slides at all**. Ask before building an outline; if there is no
  presentation, hand the work to capstone-viva-prep and output talking points per report chapter
  instead of a deck.
- **EU:** where assessment is written-only, the same content becomes the report's discussion chapter
  — the slide-by-slide plan converts one-to-one, no material is lost.
- **Team profiles (common in US/CA):** add a per-speaker split and one individual-contribution slide.



| System | What happens on stage | Consequence for the deck |
|---|---|---|
| US / Canada | 10-15 min presentation + demo + Q&A; team members all speak | Split slides by speaker; keep one personal-contribution slide |
| UK / Ireland | Frequently a **viva without slides** — an hour of questioning about the written work | The deck may be optional; the viva drill matters more than the outline |
| Australia / NZ | Short presentation + individual questioning | Keep the data slide dense enough to survive being interrogated on its own |
| Continental Europe | Kolloquium (10-20 min) or submission-only assessment | Where there is no oral, convert the talking points into the report's discussion chapter |
| India | 10-15 min talk to a panel, prototype usually displayed | Expect the demo and the block diagram to be interrogated together; keep a hardware-photo slide ready |

## The Examiner's Perspective: What They Look For

| What examiners care about | Corresponding slide content | Common student mistake |
|------------|----------------|----------------|
| Is the workload real | System diagram + module list + volume of test data | Features narrated, data absent |
| Did the student actually build it | Debug process, pitfalls solved, rig photos | Web images and textbook theory everywhere |
| Will the demo run | Live rig / video demonstration | A demo crash with no recovery plan |
| Will they run over time | Time allocation + rehearsal | Later chapters cut off mid-sentence by the timer |

## Standard Structure (8–12 slides, designed for a 10-minute defense)

| # | Content | Time | Points |
|------|------|------|------|
| 1 | Title | 10s | Topic / name / supervisor — topic must match your approved proposal |
| 2 | Outline | 10s | Five sections max; no nested sub-trees |
| 3 | Background & motivation | 30s | 1 concrete problem + 1 entry-point sentence (compress the report introduction to 3 sentences) |
| 4 | System design | 1.5min | **One full-page system diagram** (a core scoring slide) + one-line design-justification conclusion |
| 5 | Hardware design | 1.5min | Only 2 key modules with three-layer justification (requirement → component → circuit); the rest one sentence |
| 6 | Software design | 1.5min | Main flowchart + 1 core algorithm (filtering / PID / state machine) with key parameters annotated |
| 7 | Testing | 2min | **The data slide is the top scorer**: case table + error analysis + stability curve, all quantified specs on |
| 8 | Live demo | 2min | Rig demo or video (see anti-failure checklist below) |
| 9 | Conclusion | 30s | 3 spec-met items + 1 limitation + 1 improvement |
| 10 | Thanks | 5s | One page, move on |

**Scaling by time limit**:

| Limit | Slides | Allocation points |
|------|------|--------------|
| 8 min | 8–9 | Cut the outline page; design/hardware/software each to 1min; keep testing+demo at 3.5min (total ≈7.75 min, rest is margin) |
| 10 min | 10 | The standard structure above |
| 15 min | 12–14 | Hardware/software may split to two pages each (one module per page); demo may extend to 3min; conclusion to 1min |
| no deck at all (UK/IE viva, some EU submissions) | — | Do not force an outline: convert the same material into per-chapter talking points and hand the drill to capstone-viva-prep |

**Whatever the limit, testing + demo together take at least 35%** — that's where the panel scores. In rehearsal, the final 30 seconds must be your closing line, never cut mid-sentence by the bell.

## Per-Topic-Type Emphasis (the eight types are listed below; this package is self-contained)

Different topic types are examined completely differently — the slide emphasis must follow:

| Your topic type | Slide emphasis | The question they WILL ask (prepare a backup slide) |
|----------|------------|--------------------------|
| Classic control / environment sensing | Volume and precision of test data | "How is this different from a retail product?" |
| Robot car | PID tuning process + line-following algorithm | "How is this different from the kit I can buy?" |
| Wireless networking | Link diagram + network topology | "How do you handle packet loss / disconnection?" |
| AI voice | Demo video (the top scorer) + recognition-rate data | "Why offline recognition vs an online LLM?" |
| Machine vision | Recognition comparison images (correct / misclassified cases) | "Where did training data come from? What's the error rate?" |
| Host-PC + MCU pair | Host app screenshots + comms frame format | "How was the protocol designed? How do you handle message boundaries (partial or coalesced packets)?" |
| Motion control | Tuning curves (before vs after) | "How did you pick the parameters? What about oscillation?" |
| Signal processing / biomedical | Error analysis + sampling-rate rationale | "Is the accuracy sufficient? Regulatory considerations?" |

**Practical trick**: turn the "will-ask" answer into a **backup slide placed after the thanks page** — when the question comes, flip to it directly. The act itself scores (panel reads it as prepared).

## Per-Slide Content Rules (quantified "low-text, high-figure" standard)

- **≤5 bullets per slide**, each ≤2 lines; a page with over 120 words gets cut
- **Figures ≥50% of slide area**: block diagrams, schematics, flowcharts, data curves, rig photos — figure over table, table over text
- **Font minimums**: titles 28pt, body 20pt, in-figure annotations 14pt — text the back row can't read doesn't exist
- **One topic per slide**: what should this slide be remembered for? If unanswerable, merge or split
- **Data must match the report**: every spec and test result on slides is checked against Chapter 5 of the report — examiners flip through the report while listening

## Live-Demo Anti-Failure Checklist (ordered by probability)

1. **Record a demo video beforehand** (mandatory): a full 2–3 minute demonstration; if the rig dies on stage, play the video — with and without a backup video are two different fates
2. **Pre-run checklist** (run 1 hour before): battery charged / latest firmware flashed / wiring solid / demo environment (network / host app) ready / spare cable
3. **Degraded-mode plan**: demo needs internet → prepare a local offline mode; needs a phone → spare phone or screen recording
4. **Demo narration**: before the demo, one sentence: "you are about to see XX"; during, point at the rig: "this step is the XX sensor working" — a silent demo is a wasted demo
5. **Crash line**: if it truly fails, stay calm — "the rig ran X hours straight before this; possibly interference in this room; here is the full demo video recorded earlier." Honesty + preparation = bonus points

## Deduction-Point Self-Check

- ❌ Walls of text (examiners skip them)
- ❌ Three-level nested outlines (useless in a 10-minute defense)
- ❌ Three pages of theory (the examiner knows the theory; they want to hear **how you applied it**)
- ❌ Demo overruns into the timer (rehearse with a stopwatch; leave 30s margin)
- ❌ Stuck on a question → staring down at slides hunting for answers (slides are for figures that support an answer, not for finding one)
- ❌ Slide specs mismatching the report (fatal: the panel suspects the data)
- ❌ Flashy template animations (transitions ≤0.5s or none; the panel wants information, not effects)
- ❌ No page numbers (the panel can't say "go back to page X")

## Visual Design Quick Rules (no artistry required — just don't lose points)

- **Dark or light background, pick one**: in projector rooms, light background with dark text is the safest (dark decks go gray on bright projectors)
- **≤3 colors**: primary (your program's brand color, or deep blue) + accent (data highlights) + gray (auxiliary)
- **Fonts**: one clean sans-serif family throughout; bold titles, no word-art
- **≥30% whitespace per slide**: packed = no focus
- **Rig photos are the ace**: real debugging-scene photos (messy desk is fine) outscore any stock image — they prove the work is yours

## Workflow

1. **collect**: gather from the user — program shape (Step 0), topic, time limit, whether a live demo is possible, a summary of test data from the report, topic type (against the eight categories)
2. **outline**: per-slide outline by the standard structure (title + 3–5 points + suggested figure + time) **After delivering the outline, proactively ask once: "Want me to expand every slide into speakable lines (the expanded version)? If the defense is close, say yes."** User asks, or deadline < 3 days away, or says "just make it usable / don't just give me an outline" → produce the expanded version (below): concrete lines per slide, not a skeleton. This prompt is mandatory — never silently deliver a bare outline.
3. **script**: demo script for the demo slide (lines + actions + contingency)
4. **backup**: backup-slide list (answers to the "will-ask" questions, placed after thanks)
5. **rehearse**: rehearsal checklist (stopwatch points, jump preparations for follow-ups: straight to the testing page / diagram page / backup slide when probed)


## Expanded Version (deadline rescue)

Feedback said a bare outline is too thin when the defense is days away. The expanded version:

- **Trigger**: user says "out of time / give me something I can speak directly / don't just outline", or collect detects defense < 3 days away.
- **What it does**: expand every slide into 3–5 speakable sentences (conversational, with pause cues), and mark "switch slides after this line" per page.
- **Boundary**: what gets expanded is the *delivery*, not a wall-of-text script — data, figures and rig photos stay the user's job (mark them [YOU SUPPLY]); I don't write your slides for you.
- **Why**: defenses are graded on "can you explain it", not "is your script pretty"; speakable lines beat full-page text when time is short, and the no-ghostwriting line holds.

## Configurable Options (the user decides, not the defaults)

- **Slide count / duration**: default 8–12 slides for 10 minutes. A 6- or 15-minute slot → re-plan slide count (~1 slide per minute), never force the default structure.
- **Point density**: default 3–5 points per slide. A user who fears forgetting may want 5–7 prompt-style points — allow it, but warn "a wall of text reads like you're reading your slides".
- **Demo script on/off**: default includes a demo contingency plan. No live demo (talk-only defense) → drop demo-related slides and reallocate the time to test-data slides.
- **Backup slide count**: default 3–5. If the user says examiners probe one direction hard (e.g. algorithm derivations), extend to 6–8.

Once changed, all later output follows the new config.

## Handling Incomplete Input (friendly, not an interrogation)

- **Two hard facts unlock a draft**: topic + time limit. Have both → deliver an outline draft immediately; everything else (demo feasibility, test data summary, topic type) gets default assumptions, declared in one line at the top: "Generated with these assumptions — tell me what's off and I'll adjust."
- **One combined follow-up at most**; no answer → proceed on defaults. Never turn collect into an interrogation.
- **New info mid-way** updates the affected slides on the fly; no restart.

## Companion Skills (full capstone pipeline)

> The skill names below **may or may not be installed**. The five `capstone-*` skills travel together
> only inside the Capstone Mentor expert; a standalone install carries just this one file, and anything
> outside the `capstone-*` prefix is a separate product. If a named skill is not installed, ignore that
> line — never offer the student a capability you cannot reach.

- **Topic / feasibility** → capstone-topic-advisor (topic health-check before slides)
- **Proposal** → capstone-proposal-coach (slides reuse the proposal's diagram and milestones)
- **Report** → capstone-report-reviewer (slide data must match the report; run the consistency check first)
- **Q&A** → capstone-viva-prep (the drill pair: this skill for slides, that one for follow-up questions)

## When NOT to Use It

- **No oral stage in your program** — some continental European assessments are written work plus supervisor sign-off; the outline has no stage to serve
- **You want the deck file produced** — this outputs outlines and talking points; any slide tool makes the file (Hard Rule 2)
- **The report is still moving** — slides built from a changing report guarantee the spec-mismatch failure; finish with capstone-report-reviewer first
- **Graduate-level defenses** — different committee format and depth

## Bundled Assets (load on demand, don't bloat context)

- `{baseDir}/templates/defense-deck-outline-template.md` — 10-minute standard outline + backup-slide list
- `{baseDir}/references/demo-anti-failure-checklist.md` — the 1-hour-before checklist + demo narration structure + crash lines

## Hard Rules

1. **Single data source**: every spec/result on slides defers to the user's report; flag any mismatch immediately
2. **No deck production**: outlines and advice only; the user builds the deck (any slide tool works)
3. **No fabrication**: demo plans are based on the user's real, implemented features — never invent a demo for something that doesn't run
4. Every output ends with the reminder: **slide content must match the report; rehearse fully with a stopwatch at least once before the defense**

## Annotation System (same standard as the other capstone skills)

In outline outputs, mark what the user must do with three tags: [FILL IN: what] (measured data, rig photos, institutional format requirements)[VERIFY: how] (consistency with the report, page numbers, typos)[SUPERVISOR: confirm] (innovation wording, whether a live demo is permitted).
