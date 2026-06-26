# FHA, VA & USDA Mortgage Rate Watch

An OpenClaw skill for monitoring and summarizing daily government-backed mortgage rates across FHA, VA, and USDA loan programs.

## What It Does

- Fetches and formats daily/weekly rate summaries from public sources
- Compares FHA, VA, and USDA rates side-by-side with conventional benchmarks
- Calculates payment impact for rate changes
- Generates newsletter-style rate watch reports
- Supports scheduled rate alerts via cron

## Install

```bash
clawhub install fha-va-usda-mortgage-rate-watch
```

## Structure

```
├── SKILL.md                          # Primary skill definition
├── references/
│   ├── loan-programs.md              # FHA, VA, USDA eligibility and fee details
│   └── newsletter-template.md        # Weekly newsletter format template
├── scripts/
│   └── payment_calc.py               # Monthly payment calculator
└── examples/
    └── sample-request.txt            # Example prompt
```

## Disclaimer

This skill provides educational information only. Mortgage rates depend on individual circumstances. Always consult a licensed mortgage professional.
