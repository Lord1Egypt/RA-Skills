# anti-slop

A Claude skill that detects and removes "AI slop" — the formulaic vocabulary, sentence structures, sycophantic openers, over-formatting, and code anti-patterns that make output read as generic and machine-produced — from both **prose** and **code**.

This isn't a quick word-blacklist. It's built from actual research on why these patterns happen (training-data over-representation, RLHF/reward-model bias toward certain formats, documented sycophancy rates, and peer-reviewed data on AI-generated code quality), and it's specifically designed around one finding that most "avoid these words" approaches ignore: **telling a model to avoid a word while it's writing tends to backfire** (the "pink elephant problem"). So instead of a ban-list-while-drafting approach, this skill runs as a deliberate *second pass* over a completed draft — which is both more reliable and produces less contorted writing.

## What's inside

```
anti-slop/
├── SKILL.md                       # Entry point Claude reads when the skill triggers
├── README.md                      # This file
├── references/
│   ├── prose-tells.md             # Tiered vocabulary, phrases, structural patterns, formatting guidance
│   ├── code-slop.md                # Code-specific anti-patterns (over-engineering, hallucinated APIs, etc.)
│   ├── self-edit-checklist.md      # The condensed, repeatable editing pass
│   └── research-notes.md           # Sources and findings this skill is built on
└── scripts/
    └── slop_scan.py                 # Standalone density scanner (stdlib only, no dependencies)
```

## How it works

1. **Draft normally.** No self-censorship, no word-avoidance while composing.
2. **Run the self-edit pass** (`references/self-edit-checklist.md`) against the finished draft or diff.
3. **For longer or higher-stakes writing**, optionally run the quantitative scanner:
   ```bash
   python3 scripts/slop_scan.py your-draft.md
   ```
   It reports tiered vocabulary density, structural-pattern matches, and formatting-excess signals (bullet ratio, bold density, em-dash count) — as a diagnostic to guide the human editing pass, not a pass/fail gate.
4. **For code**, the same two-pass philosophy applies via `references/code-slop.md`: write the code, then deliberately check it against known over-engineering, error-swallowing, and hallucinated-API patterns before calling it done.

## Try the scanner yourself

```bash
python3 scripts/slop_scan.py path/to/file.md          # human-readable report
python3 scripts/slop_scan.py path/to/file.md --json    # machine-readable
cat file.md | python3 scripts/slop_scan.py -           # read from stdin
```

No installation needed — it's pure Python standard library.

## Why "overkill"

This was built with deep research rather than a quick vocabulary list scraped from one blog post:

- The **prose side** draws on the *Antislop* framework (Paech et al., ICLR 2026) for the mechanism and scale of vocabulary over-representation, the *Pink Elephant Problem* paper (Castricato et al., 2024) for why negative word-avoidance instructions underperform, and the *From Lists to Emojis* format-bias study (2024) for why chat models default to bullets and bold regardless of content.
- The **code side** draws on peer-reviewed surveys of AI-generated code hallucination and bugs, plus large-scale empirical data (GitClear's changed-line analysis, a CMU repository study, CodeRabbit's PR analysis) on complexity and duplication trends since AI coding tools went mainstream.
- Every list in `references/` is framed as a **density-based diagnostic**, not a blacklist — because the research is explicit that single-word bans don't work well and that legitimate uses of these words are common.

Full citations and the reasoning chain are in `references/research-notes.md`, including a maintenance note: word-level slop lists date quickly, so it's worth a fresh search before assuming any specific list is still current.

## Calibration

The point isn't to make writing sound artificially rough or to strip every list and every instance of "crucial" on principle — that's its own tell and often reads worse. The point is writing and code that are specific, earned, and shaped for their actual content, rather than defaulting to whatever pattern was statistically convenient.
