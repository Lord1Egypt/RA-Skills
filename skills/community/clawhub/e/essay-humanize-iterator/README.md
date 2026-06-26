# Essay Humanize Iterator

A closed-loop ClawHub skill that iteratively refines essays to reduce false positives from oversensitive AI detectors by removing stereotypical AI writing patterns and aligning semantic density and syntactic complexity with native human-writer baselines.

## How It Works

```
Input Essay → Measure → Pass? → Output
                ↓ No
            Rewrite with targeted feedback
                ↓
            Re-measure → Pass or max iters? → Output
                ↓ No
            Rewrite again...
```

Each iteration measures three axes:

| Axis | What It Measures | Human Baseline |
|------|-----------------|----------------|
| AI Pattern Score | 24 Wikipedia AI-writing patterns (em dashes, clichés, markdown, etc.) | 0–5 |
| Syntactic Complexity | Mean Dependency Distance and its variance across sentences | MDD ~2.33, var ~0.020 |
| Semantic Density | Type-token ratio, content-word ratio, specificity | TTR ~0.55, CWR ~0.58 |

## Usage

### Via OpenClaw / ClawHub

After installing the skill, trigger it with phrases like:

- "Rehumanize this essay to improve writing naturalness"
- "Iterate humanize my paper to reduce AI style patterns"
- "帮我迭代改写这篇论文，提升写作自然度"

Paste your essay and the skill will measure, rewrite, and re-measure automatically.

### Standalone Scripts

```bash
# Measure an essay
python skill/scripts/measure.py --file essay.txt

# Measure with JSON output
python skill/scripts/measure.py --file essay.txt --json

# Run measurement + generate rewrite feedback
python skill/scripts/iterate.py --file essay.txt --max-iters 3
```

## Requirements

- Python 3.10+
- spaCy with `en_core_web_sm` model (must be installed manually before first use)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

All rewriting is performed by the orchestrating LLM locally. No external API calls are made and no `requests` library is needed.

## Architecture

```
essay-humanize-iterator/
├── skill.yaml                    # OpenClaw trigger + prompt
├── SKILL.md                      # LLM instruction spec
├── clawhub.json                  # ClawHub metadata
├── triggers.txt                  # Activation phrases (EN + CN)
├── data/analysis/
│   └── weights.json              # Corpus-derived pattern weights
└── skill/
    ├── SKILL.md                  # Duplicate for ClawHub
    ├── scripts/
    │   ├── measure.py            # 3-axis scorer
    │   └── iterate.py            # Feedback loop engine
    └── references/
        ├── patterns.md           # 24 AI pattern definitions
        ├── metrics.md            # Metric formulas + thresholds
        └── iteration_strategy.md # Per-iteration escalation logic
```

## Metrics & Thresholds

| Metric | Pass Threshold |
|--------|----------------|
| AI Pattern Score | ≤ 15 / 100 |
| MDD Mean | 2.15 – 2.55 |
| MDD Variance | ≥ 0.016 |
| Lexical TTR | ≥ 0.50 |
| Content-Word Ratio | 0.52 – 0.65 |

Pattern weights and human baselines are from analysis of 298 human essays (CAWSE/LOCNESS) vs. 216 AI-generated essays using Mann-Whitney U tests.

## License

MIT
