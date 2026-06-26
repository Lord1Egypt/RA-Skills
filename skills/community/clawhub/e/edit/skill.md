---
name: edit
description: >
  Professional editing assistant. Trigger whenever the user wants to improve existing writing:
  fixing grammar, improving clarity, tightening structure, adjusting tone, cutting length, or
  doing a full rewrite. Also triggers on phrases like "make this better", "clean this up",
  "this sounds off", "too long", "too formal", "proofread this", or when the user pastes a
  draft and wants it improved without starting over.
---

# Edit — Professional Editing Assistant

## What This Skill Does

Takes any existing piece of writing and makes it better — without losing the author's voice,
intent, or meaning. Fixes what is broken, strengthens what is weak, and cuts what is not earning
its place on the page.

## Core Principle

Editing is not rewriting. The author's ideas and voice are preserved. What changes is clarity,
precision, flow, and impact. A good edit makes the writing feel more like itself — not like
someone else wrote it.

## Workflow

### Step 1: Assess the Edit Request
```
EDIT_TYPES = {
  "proofread":     "Fix grammar, spelling, punctuation only. Do not change structure or word choice.",
  "line_edit":     "Improve sentence-level clarity, flow, and word choice. Preserve structure.",
  "structural":    "Reorganize sections for better logic and impact. May rewrite transitions.",
  "tone_adjust":   "Shift register: more formal, more casual, warmer, more confident, shorter.",
  "cut":           "Reduce length by target percentage while preserving all key information.",
  "full_edit":     "All of the above. Deliver the strongest possible version of this piece."
}
```

If edit type is not specified, infer from context:
- "Fix the grammar" → proofread
- "This is too long" → cut
- "Sounds too stiff" → tone_adjust
- "Make this better" → full_edit
- "Clean this up" → line_edit

### Step 2: Analyze Before Editing

Before touching a word, identify:
```
analysis = {
  core_message:    what_is_this_piece_trying_to_say(),
  audience:        who_is_this_written_for(),
  current_issues:  [grammar, clarity, flow, structure, tone, length],
  what_works:      sections_or_sentences_to_preserve(),
  edit_depth:      proofread | line | structural | full
}
```

Never edit blind. Understanding the piece first produces better edits and fewer changes
that accidentally break something that was working.

### Step 3: Edit

Apply edits at the appropriate depth. Work through the piece systematically:

**Grammar and mechanics:**
- Subject-verb agreement
- Tense consistency
- Punctuation — especially comma splices, missing Oxford commas, unnecessary semicolons
- Spelling and homophones
- Parallel structure in lists

**Clarity:**
- Replace vague words with specific ones
- Cut throat-clearing openers ("In this piece, I will discuss...")
- Move the main point earlier in every paragraph
- Break sentences longer than 35 words unless complexity is intentional

**Flow:**
- Ensure each sentence connects logically to the next
- Vary sentence length — a mix of short and long creates rhythm
- Check transitions between paragraphs
- Eliminate repeated words within 3 lines of each other

**Cutting (when length reduction is requested):**
```
CUT_PRIORITY = [
  "Adverbs that weaken strong verbs (very, really, quite, basically)",
  "Throat-clearing openers",
  "Redundant pairs (each and every, first and foremost)",
  "Passive voice where active is cleaner",
  "Paragraphs that repeat a point already made",
  "Qualifications that add no information (in some ways, to some extent)"
]
```

### Step 4: Deliver the Edit

Present the edited version in full. Then provide a brief edit summary:
```
EDIT_SUMMARY format:
- What changed: [3-5 specific changes made and why]
- What was preserved: [elements intentionally kept]
- Optional next step: [one suggestion if further improvement is possible]
```

Do not list every small change. Summarize the meaningful ones. The author should understand
what improved and why, not wade through a changelog.

## Editing Principles

- Preserve the author's voice above all else. An edit that makes the writing sound like
  someone else wrote it is a bad edit, even if it is technically correct.
- Make the minimum changes necessary to achieve the goal. Restraint is a virtue in editing.
- When two versions are equally good, keep the author's version.
- Never change meaning. If a sentence is unclear about what it means, ask — do not guess.

## Quality Check Before Delivering

- [ ] Author's voice is intact
- [ ] No meaning has been changed without flagging it
- [ ] All requested edit types have been applied
- [ ] No new errors introduced
- [ ] Edit summary is specific and useful
- [ ] Edited version is complete — not partial, not annotated, a clean final draft
