# Writing Assistant — Advanced Patterns
**by [The Agent Ledger](https://theagentledger.com)**

---

## Pattern 1: Research → Draft Pipeline

Chain the research-assistant and writing-assistant for evidence-backed content:

```
Phase 1 (Research):
Research [TOPIC] with 3-5 credible sources.
Focus: [specific angle or question]
Output format: research brief with key findings, quotes, and source links.
Save to: research/[topic-slug]-brief.md

Phase 2 (Draft):
Using the research brief at research/[topic-slug]-brief.md,
draft a [blog post / newsletter issue / LinkedIn post] about [TOPIC].
Check writing-state.md for voice. Integrate the research naturally — 
cite sources inline but don't make it feel academic.
```

This produces higher-quality, credible content in less time than either step alone.

---

## Pattern 2: Content Series Drafting

For ongoing series (e.g., weekly tips, recurring newsletter sections):

```
This is issue [N] in the "[SERIES NAME]" series.

Previous entries:
- Issue 1: [Title] — [One-sentence summary]
- Issue 2: [Title] — [One-sentence summary]

This issue: [TOPIC]
Maintain series voice and callback format. Open with a brief anchor to the series
(2 sentences max). Don't repeat full context — readers know the series.
```

**Series consistency tracker** (add to writing-state.md):
```markdown
## Active Series
### "The Real Config" — Monthly deep-dive
- Format: 800-1,000 words, 3 sections + practical takeaway
- Opening pattern: Open with the problem, not the solution
- Recurring element: "What I changed last month" paragraph
- Issues published: 1, 2, 3
- Next: Issue 4 — [TOPIC]
```

---

## Pattern 3: Voice Calibration Session

When output sounds off, run a calibration session:

```
I'm going to give you 3 samples of my writing. Study the voice, rhythm, and patterns.
After each sample, note: sentence length patterns, favorite transitions, punctuation style,
what I'm willing to be direct about, what I hedge.

Then I'll ask you to draft something and you'll match this voice precisely.

Sample 1:
[PASTE 200-400 WORDS OF YOUR ACTUAL WRITING]

Sample 2:
[PASTE ANOTHER SAMPLE — DIFFERENT FORMAT PREFERRED]

Sample 3:
[PASTE A THIRD SAMPLE]

Summarize the voice in 8 bullet points. I'll review and update writing-state.md.
```

Run this whenever you onboard to a new agent instance or after a long gap.

---

## Pattern 4: A/B Headline / Subject Line Testing

Generate testable variants with predicted performance:

```
Generate 6 [subject line / headline / hook] options for [TOPIC].

For each option, predict:
- Open rate appeal (1-10) — curiosity + relevance
- Clarity score (1-10) — reader knows what they're getting
- Brand fit (1-10) — matches voice in writing-state.md
- Risk level (Low/Med/High) — polarizing, clickbait-adjacent, or safe

Highlight your top 2 picks and explain why.
```

Over time, track which subject lines perform well in real campaigns and add to `writing-state.md`:

```markdown
## Subject Line Performance (from real sends)
- Curiosity-gap format → avg 42% open rate (best performer)
- Direct benefit format → avg 34% open rate
- Question format → avg 38% open rate
- Avoid: pun-based → tested poorly with this audience
```

---

## Pattern 5: Editing Tiers

Different editing intensities for different needs:

### Light Edit (Polish Only)
```
Light edit — fix grammar, punctuation, and obvious awkward phrasing only.
Do NOT restructure, cut sections, or change the voice. This is nearly final.
[PASTE DRAFT]
```

### Structural Edit
```
Structural edit — the ideas are good but the organization isn't working.
Suggest a restructured outline first, then get my approval before rewriting.
Tell me what to cut, what to move, what's missing.
[PASTE DRAFT]
```

### Full Rewrite
```
Full rewrite — same core ideas, start fresh. Check writing-state.md.
Keep: [list what to preserve]
Change: [what's not working]
Goal: [what this piece needs to achieve]
[PASTE DRAFT]
```

### Targeted Section Fix
```
Only fix the [opening / closing / [specific section]].
Leave the rest unchanged. Here's the full draft for context:
[PASTE DRAFT]
```

---

## Pattern 6: Email Campaign Sequences

For multi-email sequences (welcome, nurture, launch, re-engagement):

```
Draft a [N]-email [welcome / launch / re-engagement] sequence for [PRODUCT/LIST].
Reader context: [who they are, how they joined, what they expect]
Sequence goal: [what you want them to do by email N]
Spacing: [e.g., Day 0, Day 2, Day 5, Day 9]
Tone: Check writing-state.md

For each email provide:
- Subject line (+ 1 variant)
- Preview text (under 90 chars)
- Body
- CTA
```

**Save sequences to** `writing-sequences/[sequence-name]/`:
```
writing-sequences/
  welcome-sequence/
    email-01.md
    email-02.md
    email-03.md
    sequence-notes.md   ← performance notes, revision history
```

---

## Pattern 7: Social Content Batching

Draft a week's worth of social content in one session:

```
Batch session: 5 LinkedIn posts for the week of [DATE].

Topics:
1. [TOPIC 1]
2. [TOPIC 2]
3. [TOPIC 3]
4. [TOPIC 4]
5. [TOPIC 5]

Rules:
- Each post: 150-250 words
- Vary the format: one tip, one story, one contrarian take, one question, one announcement
- Check writing-state.md for voice
- End each with a question or quiet CTA, not both
```

Add to your content-calendar pipeline:

```markdown
| Format | Status | Agent Drafted | Approved | Scheduled |
|--------|--------|---------------|----------|-----------|
| LinkedIn post | In Progress | ✓ | — | — |
```

---

## Pattern 8: Repurposing Engine

One piece of content → multiple formats:

```
Repurpose the attached [blog post / newsletter / transcript] into:
1. LinkedIn post (200 words, story angle)
2. Twitter/X thread (6 tweets, tip angle)  
3. Email newsletter section (150 words, fits into a "Quick Insight" block)
4. Short-form video script (60-90 seconds, hook + 3 points + CTA)

Source:
[PASTE CONTENT]

Check writing-state.md for format-specific tone preferences.
Don't just summarize — extract the single sharpest insight and build each format around it.
```

---

## Pattern 9: Writing Accountability (Heartbeat Integration)

Add to HEARTBEAT.md for light writing prompts:

```markdown
## Writing Assistant Checks (run 2x/week)
- Check content-calendar: any items in "Overdue Draft" status?
- Check writing-state.md: last content archive entry — when was last piece completed?
- If 5+ days since last published piece: surface as a gentle flag, not a nag
- Suggest one micro-writing task if blocked (tweet, email reply, one paragraph)
```

---

## Pattern 10: Feedback Integration Loop

After getting feedback on your writing (from readers, clients, or yourself), capture it:

```
Writing feedback received on [TITLE]:
[PASTE FEEDBACK]

Based on this feedback:
1. What pattern in my writing does this point to?
2. What should I add or change in writing-state.md?
3. Is this feedback valid for all my writing, or specific to this format?

Update writing-state.md with any relevant changes.
```

Over time, this builds a living style guide that improves every draft.

---

*This file is part of the Writing Assistant skill by [The Agent Ledger](https://theagentledger.com).*

*Subscribe for new skills, deep dives, and the premium guide on building production-grade AI agent setups.*

*License: CC-BY-NC-4.0*
