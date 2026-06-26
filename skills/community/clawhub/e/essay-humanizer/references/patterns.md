# 24 AI writing patterns (reference)

Derived from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). Each pattern is scored in `scripts/analyze_patterns.py`; weights land in `data/analysis/weights.json` after you run analysis on your corpora.

**Humanization rule:** Address patterns in **descending weight** (higher = more AI-distinctive in your data). Remove or replace; do not swap one cliché for another.

---

## Content (1–3)

### P01 — Undue emphasis
- **Detection:** phrases inflating importance ("plays a vital role", "stands as a testament", "lasting impact").
- **Fix:** State the fact plainly; cut evaluative puff unless the prompt requires evaluation.

### P02 — Superficial analysis
- **Detection:** empty scene-setting ("in today's world"), claims without evidence.
- **Fix:** Add concrete detail, dates, names, mechanisms; delete generic framing.

### P03 — Regression to the mean
- **Detection:** generic noun piles ("various stakeholders", "numerous aspects") replacing specifics.
- **Fix:** Name who/what; prefer one precise example over three vague ones.

---

## Vocabulary (4–8)

### P04 — AI vocabulary
- **Detection:** delve, intricate, tapestry, pivotal, underscore, landscape, foster, testament, enhance, crucial (overused).
- **Fix:** Plain synonyms; keep "crucial" only if truly warranted.

### P05 — Excessive adverbs
- **Detection:** significantly, notably, remarkably, fundamentally, profoundly repeated.
- **Fix:** Delete or replace with evidence.

### P06 — Cliché metaphors
- **Detection:** tapestry, beacon, cornerstone, journey, landscape of…
- **Fix:** Literal description or one fresh image tied to the topic.

### P07 — Redundant modifiers
- **Detection:** "very unique", "extremely essential", etc.
- **Fix:** Drop intensifier or rephrase.

### P08 — Filler hedging
- **Detection:** "It is worth noting that", "It should be mentioned".
- **Fix:** Delete the frame; say the sentence directly.

---

## Rhetorical (9–14)

### P09 — Negative parallelisms
- **Detection:** "It's not X, it's Y" chains.
- **Fix:** Use one direct claim; vary structure.

### P10 — Rule of threes
- **Detection:** triplet adjectives or lists everywhere.
- **Fix:** Two items, or four; mix sentence lengths.

### P11 — False ranges
- **Detection:** "From A to B" where no continuum exists.
- **Fix:** Two separate points or a real gradient.

### P12 — Present participle tailing
- **Detection:** ", highlighting / underscoring / showcasing…".
- **Fix:** New sentence or integrate as a finite verb.

### P13 — Over-attribution
- **Detection:** "Experts say", "Critics argue" without sources.
- **Fix:** Cite properly or use "Some argue" with named tradition—or drop.

### P14 — Compulsive summaries
- **Detection:** "Overall," / "In conclusion," in short pieces.
- **Fix:** End on the last point; integrate only if length warrants.

---

## Punctuation / mechanics (15–17)

### P15 — Em dash overkill
- **Detection:** em dashes (—) where commas work.
- **Fix:** Commas, parentheses, or split sentences.

### P16 — En dash avoidance
- **Detection:** hyphens in number/year ranges where en dash is standard in formal prose.
- **Fix:** Use typographic en dash for ranges if your style guide requires it.

### P17 — Transition overuse
- **Detection:** Furthermore, Moreover, Additionally every paragraph.
- **Fix:** Pronouns and logic; occasional "But" / "Yet".

---

## Register / tone (18–20)

### P18 — Collaborative register
- **Detection:** "I hope this helps", "Let me know".
- **Fix:** Remove (essay is not chat).

### P19 — Letter-style formality
- **Detection:** "I hope this message finds you well".
- **Fix:** Delete.

### P20 — Instructional condescension
- **Detection:** "Here's how to", "First you should".
- **Fix:** Argumentative stance appropriate to essay, not tutorial.

---

## Formatting (21–24)

### P21 — Markdown artifacts
- **Detection:** `**`, `#`, fences, links in prose meant to be plain.
- **Fix:** Strip; use italics/quotes only if required by style.

### P22 — Excessive lists
- **Detection:** bullets/numbers where prose paragraphs fit.
- **Fix:** Convert to flowing argument.

### P23 — Textbook bolding
- **Detection:** `**term**` glossaries.
- **Fix:** Plain text or defined once in sentence.

### P24 — Emoji / symbols
- **Detection:** decorative emoji, checkmarks in academic tone.
- **Fix:** Remove.

---

## Syntactic complexity (MDD / ADD)

Complements the 24 patterns: compare **mean dependency distance (MDD)** and **absolute dependency distance (ADD)** distributions between human (CAWSE-M/D, LOCNESS) and AI essays. Human text often shows **more variance** in MDD; uniformly "smooth" AI prose can cluster tightly. Use Mann-Whitney U on per-essay MDD and report optional Pearson (nominal subjects/clause vs MDD) mirroring prior L2 research. **Do not** flatten all sentences to short dependencies; aim for **natural variability** consistent with high-merit human writing.
