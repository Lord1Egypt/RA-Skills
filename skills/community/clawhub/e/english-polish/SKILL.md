---
name: "english-polish"
description: "Advanced English polish skill for non-native writing. Nativization, style consistency, diff output. CLI scripts: detector.py + polish.py"
version: 1.0.0
---

# english-polish — Professional English Polish & Nativization Skill

## Overview

Polish English text for native-level fluency while preserving the author's voice, argument structure, and analytical depth. Designed for technical/analytical non-fiction writing by non-native speakers.

**Core principle:** We are not translating Chinese to English. We are **nativizing** English that was written by a non-native speaker — making it flow naturally while preserving every fact, judgment, and nuance.

## When to Use

1. Non-native English manuscript chapters (like the 算力简史 project)
2. English-language analysis/reports written with Chinese syntax patterns
3. Any English output intended for native English-speaking readers

## Never Use For

- Creative writing (poetry, fiction, dialogue-heavy narrative)
- Academic papers requiring formal citation style preservation
- Translation from scratch (this is polish, not translate)

---

## CLI Tools

This skill ships with two Python scripts that automate Phase 0 detection and Phase 1-3 polishing:

### Installation

```bash
# Prerequisites
python3 -c "import re"  # stdlib, no deps needed
```

### Detector: `detector.py`

```bash
# Check a file (default: plain text)
python3 scripts/detector.py check document.md

# HTML report (with score bar + table)
python3 scripts/detector.py check document.md --format html

# ANSI-colored terminal report
python3 scripts/detector.py check document.md --format ansi

# Batch scan a directory + JSON report
python3 scripts/detector.py batch /path/to/chapters/

# HTML batch (one HTML file per chapter)
python3 scripts/detector.py batch /path/to/chapters/ --format html --output /tmp/reports/

# Interactive mode (type or paste text)
python3 scripts/detector.py interactive

# List all 19 pattern categories
python3 scripts/detector.py list-patterns
```

**Output formats:**
- `text` (default): Plain text report (same format as above)
- `html`: Beautiful HTML with score bar, severity colors, pattern table
- `ansi`: Terminal-colored report for quick scanning

**Output sample:**
```
============================================================
PHASE 0 DETECTOR REPORT — chapter-09.md
============================================================
  Word count:          4820
  Total issues (wtd):  24.4
  Density (/200 words): 1.0
  Score:               4.9/5.0
  Severity:            Native-level

  Detected patterns (5 categories):

  [Noun Stacking (5+ consec noun/mod)] ×8 (weighted: 5.6)
    → "capital expenditure on cloud infrastructure"
    → "chip design competition is fierce"

  ['Not only...but also' overuse] ×2 (weighted: 1.2)
    → "Not only...but also"

  ['Should' false obligation] ×3 (weighted: 2.1)
    → "China should"
    → "Companies should"

  ...
```

### Polisher: `polish.py`

```bash
# Check + report (no file modification)
python3 scripts/polish.py check document.md

# Colorized check output
python3 scripts/polish.py check document.md --format ansi

# Polish file (creates output + diff report)
python3 scripts/polish.py polish document.md --output output.md

# Polish with HTML summary report
python3 scripts/polish.py polish document.md --output output.md --format html

# Style tweaks only (skip Phase 3 structural changes)
python3 scripts/polish.py polish document.md --style-only

# Batch polish a directory
python3 scripts/polish.py batch /path/to/chapters/
```

**Polish output includes:**
- Phase 1: Grammar & mechanics fixes (articles, prepositions, tenses)
- Phase 2: Fluency/Chinglish pattern replacement (18 categories)
- Phase 3: Style enhancement (sentence rhythm, word choice)
- Diff: side-by-side or inline before/after
- Report: score improvement, changes summary

### Makefile (CI Automation)

```bash
# Quick test suite only
make check

# Full test + book baseline + regression check
make test

# Run full-book baseline and compare with saved reference
make baseline

# Save current baseline as reference for future comparisons
make save-baseline

# Clean temp files
make clean
```

`make baseline` runs the detector on the full book and compares against the saved reference. If the average score changes by more than ±0.1, it flags the change for review.

### Custom Configuration (`config/`)

Extend the skill without modifying code:

```bash
# Copy and customize
cp config/default.json config/user.json
```

**user.json** supports adding custom detection patterns and polish replacement rules:

```json
{
  "user_custom_patterns": [
    {
      "key": "Z_my_custom_pattern",
      "label": "My Custom Pattern",
      "weight": 1.0,
      "patterns": ["\\bmy regex pattern here\\b"],
      "examples": ["Example text"],
      "notes": "What to look for"
    }
  ],
  "user_custom_replacements": [
    {
      "type": "filler",
      "old": "my custom phrase",
      "new": "better phrase",
      "enabled": true
    },
    {
      "type": "weak_verb",
      "old": "perform an evaluation",
      "new": "evaluate",
      "enabled": true
    }
  ]
}
```

---

## Architecture

### Three-Phase Polish Pipeline

```
Phase 0: Detection ────→ Score (0-5)
                             │
                     ┌──────┴──────┐
                     │             │
               score < 3      score ≥ 3
                     │             │
              Phase 1:        Phase 2:
           Full Grammar    Light Polish
             + Syntax       (patterns
             Restructure    only)
                     │             │
              Phase 2:        Phase 3:
           Chinglish      Style-only
           Replacement   (word-level)
                     │             │
              Phase 3:           │
           Style Pass     (skip Phase 1)
                     │             │
               Diff + Report
```

### 19 Pattern Categories (A-S)

| Code | Pattern | Weight | Example |
|:----|:--------|:------:|:--------|
| A | Subject Dangling | 1.0 | "For chip design, competition is fierce..." |
| B | Redundant "As For" / "Regarding" | 0.8 | "As for the energy cost, it is..." |
| C | Passive Chain Stacking | 1.0 | "It can be seen that..." |
| D | "Make + abstract noun" | 0.8 | "make a decision" → "decide" |
| E | "Not only...but also" overuse | 0.6 | default connector overuse |
| F | Noun Stacking (5+ consec noun/mod) | 0.7 | "Data center GPU market growth prediction models" |
| G | "Should" false obligation | 0.7 | "China should develop its own chip..." |
| H | "The" overuse for generic | 0.5 | "the computing power is..." |
| I | Chinese filler expressions | 0.7 | "to a certain extent", "in the process of" |
| J | "This is because" structure | 0.6 | Chinese-pattern explanatory |
| K | Redundant modifiers | 0.6 | "actively strengthen", "continuously improve" |
| L | Weak verb + nominalization | 0.7 | "conduct research" → "research" |
| M | Emphasis inversion (Chinese '是...的') | 0.7 | "It is X that..." → "X..." |
| N | List cadence enumeration | 0.5 | "First...Second...Finally" aggregation |
| O | Concessive cluster (虽然...但是) | 0.8 | "Although...but..." double conjunction |
| P | Topic-comment fronting | 0.7 | "As for X... / When it comes to..." |
| Q | False inclusive "We" | 0.5 | "We can see/observe/conclude..." |
| R | Logical sawtooth contrast | 0.5 | "On one hand...on the other hand..." |
| S | List summarizer | 0.5 | "All these factors contribute to..." |

### Scoring

- **0-5 scale**: normalized from weighted detection density
- **5.0**: Perfect (0 issues) or native-level
- **4.5+**: Native-level (minor style tweaks only)
- **4.0-4.5**: Near-native (phrase-level polish)
- **3.0-4.0**: Light polish needed (pattern-level)
- **2.0-3.0**: Full polish needed (sentence-level)
- **<2.0**: Heavy rewrite needed (structural issues)

**Scoring formula (per 200 words):**
- 0 weighted issues → score 5.0
- 1-3 medium → score 4.0-4.5
- 4-8 heavy → score 3.0-4.0
- >8 → score drops below 3.0

---

## Workflow

### Phase 0: Detection

Run automated detection before deciding to polish:

```bash
# Quick check
python3 scripts/detector.py check chapter.md

# Decision matrix:
# Score < 3:   Full polish (Phase 1 → 2 → 3)
# Score 3-4:   Light polish (Phase 2 → 3)
# Score 4+:    Style-only (Phase 3)
```

### Phase 1: Full Chapter Polish (score < 3)

For each chapter:
1. **Read-through**: Understand argument structure, key claims, data points
2. **Sentence-by-sentence reform**: Fix grammar, syntax, flow WITHOUT changing:
   - Any factual claim
   - Any analytical judgment
   - The chapter's core argument structure
   - Technical terms (DO NOT rename "chiplet" → "modular chip" etc.)
3. **Style pass**: Check for
   - Overuse of "However," at sentence start (replace with "But" or restructure)
   - Overuse of "In the previous chapter..." transitions (merge into judgments)
   - Chinese-pattern "Not only...but also..." (use sparingly)
   - "This is because..." → restructure
   - "Therefore, we can see that..." → delete, just state the conclusion
4. **Diff output**: Produce markdown diff showing before/after

### Phase 2: Light Polish (score 3-4)

Target specific patterns only:
- Article corrections (a/an/the)
- Preposition fixes
- Verb tense adjustments
- Comma splice repairs
- Chinglish pattern replacement (see 19-pattern library)

### Phase 3: Style-Only (score 4+)

- Rhythm adjustments (vary sentence length)
- Passive→active where natural
- Word choice: elevate from "correct but flat" to "natural and precise"

---

## Quality Gates

### Gate 1: Content preservation check
- Every data point in the original must still appear in the polished version
- Every core argument must be present
- Nothing added that changes meaning

### Gate 2: Nativization check
- Read aloud test: does it sound like a native speaker wrote it?
- If you stumble on reading, mark and fix
- No Chinese syntax traces: subject-drop, topic-comment structure, redundant "the" usage

### Gate 3: Style consistency check
- Tone matches the original author's voice (not overwritten with a new style)
- Technical terms preserved
- The polish feels invisible — reader shouldn't notice "this was translated" or "this was AI-polished"

---

## Output Format

For each polished chapter:

```markdown
# Chapter X: Title

## Polish Summary
- Original word count: X
- Changed words: X
- Sentences rewritten: X
- Nativization score: before X / after Y

## Changes
### Major Restructures (>50% rewritten)
1. [Original sentence]
   → [Polished sentence]
   Reason: [syntax pattern detected + fix]

### Moderate Changes (sentence-level)
1. [Original fragment]
   → [Polished fragment]

### Word-Level Tweaks
1. [original word] → [new word]: reason

## Critical Notes
- Any factual concerns found during polish
- Any argument structure notes for author review
- Questions about intended meaning (for ambiguous phrases)
```

## Integration with Star1

When used for 算力简史 polishing:
1. Reference StarKB for technical terms that should NOT be changed
2. Preserve the Wang Jialin-style analytical voice (judgments before details, facts before emotions)
3. Do NOT:
   - Add unnecessary hedging
   - Soften strong judgments
   - Remove skepticism/critical analysis
   - Convert "this is bad" to "this may be considered challenging"

## Dependencies
- Python 3 (stdlib only — `re`, `sys`, `json`)
- Star1 or any advanced LLM (for sentence rewriting)
- `diff` command (for before/after comparison)
- No external API required

## Directory Structure

```
english-polish/
├── SKILL.md                  ← This file
├── Makefile                  ← CI targets (test, baseline, check, clean)
├── config/
│   ├── default.json          ← Built-in configuration
│   ├── user.json             ← User custom patterns & replacements (optional)
│   ├── baseline-reference.json ← Saved book baseline for regression checking
│   └── save-baseline.py      ← Baseline compare/save script
├── scripts/
│   ├── detector.py           ← Phase 0: Chinglish pattern detection (19 classes)
│   ├── detector.py.bak       ← Backup of original 12-class version
│   └── polish.py             ← Phase 1-3: full polish pipeline
├── tests/
│   ├── test_suite.py         ← Automated test suite (29 test cases)
│   └── known_chinglish.md    ← 19-pattern test corpus
└── references/
    └── (optional: comparison reports, benchmark data)
```
