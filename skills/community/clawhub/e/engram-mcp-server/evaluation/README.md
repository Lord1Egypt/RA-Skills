# Engram Case Study Evaluation

English | [中文](./README_zh.md)

This folder provides a lightweight, reproducible way to compare:

- baseline answer (same model, without loading Engram)
- Engram answer (same model, with Engram loaded)

The goal is not leaderboard benchmarking. The goal is to produce a clear,
public case study that shows whether Engram improves answer quality.

## 1) Prepare cases

Copy and edit `case_study_template.json`:

```bash
cp evaluation/case_study_template.json evaluation/my_case_study.json
```

For each case, fill:

- `baseline_answer`
- `engram_answer`
- `expected_keywords` (facts/processes that should appear)
- `forbidden_keywords` (hallucinations or anti-patterns)
- `checkpoints` (weighted rule checks, supports `mode=all/any`)

Scoring dimensions:

- **content**: checkpoint pass ratio (or expected keyword coverage if no checkpoints)
- **safety**: forbidden keyword penalty
- **structure**: objective formatting/process/risk signals

Default weights: content 0.65 + safety 0.25 + structure 0.10  
You can override via per-case `weights`.

## 2) Run scoring

```bash
python3 evaluation/score_case_study.py --input evaluation/my_case_study.json
```

Optional CSV export:

```bash
python3 evaluation/score_case_study.py \
  --input evaluation/my_case_study.json \
  --csv evaluation/my_case_study_report.csv
```

## 3) Publish the case study

When sharing results, include:

- model name and version
- exact prompt template
- case file
- raw baseline/Engram answers
- generated report

This keeps your comparison transparent and reproducible.

## Notes on objectivity

- This script is **rule-based**, not LLM-judged, so it is reproducible.
- It still cannot measure deep reasoning quality by itself.
- Recommended: pair this report with a small human review rubric.
