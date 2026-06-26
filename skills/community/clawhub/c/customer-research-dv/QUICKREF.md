# Quick Reference Card

One-page cheat sheet for customer research commands.

## Installation

```bash
cd ~/.openclaw/workspace/skills/customer-research
./setup.sh
```

## Commands

### Mine Reddit for Insights
```bash
customer-research mine \
    --category "product category" \
    --subreddits sub1,sub2,sub3 \
    --limit 200 \
    --time-filter month \
    --output data/insights.json
```

**Output:** Pain points, feature requests, sentiment analysis

---

### Generate Survey
```bash
customer-research survey \
    --hypothesis "Your product hypothesis" \
    --template product_validation \
    --output data/survey.json \
    --markdown data/survey.md
```

**Templates:** `product_validation`, `pricing`

**Output:** 10-question survey + distribution templates

---

### Create Interview Script
```bash
customer-research interview \
    --persona persona_type \
    --framework jobs_to_be_done \
    --output data/interview.json \
    --markdown data/interview.md
```

**Personas:** `tech_pm_high_earner`, `solopreneur`, `corporate_exec`, `small_business_owner`

**Frameworks:** `jobs_to_be_done`, `problem_validation`

**Output:** 30-45 min interview script

---

### Validate Persona
```bash
customer-research validate \
    --persona data/persona.json \
    --insights data/reddit-insights.json \
    --output data/validated.json \
    --markdown data/report.md
```

**Output:** Confidence score (0-100) + validation report

---

### Scrape Competitor Reviews
```bash
customer-research scrape \
    --platform url \
    --url "https://example.com/reviews" \
    --output data/competitor-reviews.json \
    --delay 2
```

**Platforms:** `gumroad`, `producthunt`, `url`

**Output:** Reviews + sentiment analysis + feature mentions

---

## Workflow

```bash
# 1. Mine Reddit
customer-research mine --category "tax software" --subreddits personalfinance,tax --output insights.json

# 2. Create persona (copy template)
cp examples/persona-template.json data/persona.json
# Edit data/persona.json

# 3. Validate persona
customer-research validate --persona data/persona.json --insights insights.json --output validated.json --markdown report.md

# 4. Generate interview script
customer-research interview --persona tech_pm_high_earner --output interview.json --markdown interview.md

# 5. Generate survey
customer-research survey --hypothesis "AI tax optimizer" --output survey.json --markdown survey.md

# 6. Scrape competitors
customer-research scrape --platform url --url "competitor-reviews-page" --output competitor.json
```

## Confidence Score Interpretation

| Score | Action |
|-------|--------|
| 0-49  | ⚠️ LOW - Conduct 5-10 customer interviews |
| 50-74 | 🔶 MODERATE - Run targeted surveys on gaps |
| 75-100| ✅ HIGH - Proceed to campaign planning |

## Common Flags

- `--help`: Show detailed help for any command
- `--output`: JSON output file (required)
- `--markdown`: Optional human-readable markdown output
- `--limit`: Number of items to fetch (default varies)
- `--time-filter`: Reddit time filter (hour/day/week/month/year/all)

## Files & Directories

```
customer-research/
├── SKILL.md              # Full documentation
├── QUICKREF.md           # This file
├── customer-research.sh  # CLI wrapper
├── setup.sh              # Installation script
├── requirements.txt      # Python dependencies
├── scripts/              # Python scripts
│   ├── reddit-miner.py
│   ├── survey-gen.py
│   ├── interview-script.py
│   ├── persona-validator.py
│   └── competitor-scraper.py
├── examples/             # Sample outputs
│   ├── persona-template.json
│   ├── reddit-insights-example.json
│   ├── interview-script-example.md
│   └── validated-persona-example.json
└── data/                 # Your working directory (created by you)
```

## Tips

1. **Start with Reddit mining** - fastest way to find real pain points
2. **Use multiple subreddits** - cross-validate signals
3. **Interview 5-10 people minimum** before building
4. **Track evidence** - keep URLs to customer quotes
5. **Iterate** - validation is ongoing, not one-time

## Help

```bash
# General help
customer-research help

# Command-specific help
customer-research mine --help
customer-research survey --help
customer-research interview --help
customer-research validate --help
customer-research scrape --help
```

## Troubleshooting

**Missing dependencies:**
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

**Reddit rate limit:**
- Reduce `--limit`
- Wait 60 seconds between runs
- Free tier: 60 requests/min

**Low confidence score:**
- Expected for early-stage ideas
- Conduct customer interviews
- Gather more Reddit data from different subreddits

---

**Remember:** Data beats opinions. Validate before you build.
