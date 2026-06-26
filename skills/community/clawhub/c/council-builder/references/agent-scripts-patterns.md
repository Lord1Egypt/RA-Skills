# Agent Scripts

Each agent gets a `scripts/` directory for executable helpers. Scripts let Claude compose existing tools instead of regenerating logic every time.

## Why Scripts

Claude is good at writing code from scratch, but it's better at calling existing scripts. A research agent that runs `./scripts/validate-sources.sh` is faster and more consistent than one that reinvents source validation each time.

## Structure

```
agents/[name]/scripts/
├── [helper-1].sh
├── [helper-2].py
└── README.md          # What each script does, when to use it
```

## Examples by Role

### Research Agent
- `fetch-feed.sh` — pull RSS/Atom feed and extract latest entries
- `validate-sources.py` — check if URLs are reachable and recent
- `summarize-links.sh` — batch-fetch URLs and extract key content

### Content Agent
- `word-count.sh` — count words in a draft, flag if outside target range
- `check-prohibited.sh` — scan text for banned words/phrases
- `format-tweet.py` — validate character count and thread formatting

### Dev Agent
- `run-lint.sh` — execute project linter and return summary
- `run-tests.sh` — run test suite and report pass/fail counts
- `check-build.sh` — verify the project builds cleanly

### Finance Agent
- `calc-vat.py` — calculate VAT with correct rate per category
- `currency-convert.sh` — fetch current exchange rate and convert
- `margin-check.py` — validate profit margins against thresholds

### Ops Agent
- `check-calendar.sh` — query today's events and conflicts
- `format-reminder.sh` — create properly formatted reminder entry
- `email-draft.py` — generate email from template with variables

## Script Standards

1. Scripts should be self-contained (minimal dependencies)
2. Include a one-line comment at the top explaining purpose
3. Accept inputs as arguments, output to stdout
4. Exit codes: 0 = success, 1 = failure, 2 = warning
5. Keep scripts under 50 lines when possible

## When to Create Scripts

- A task repeats more than twice with the same logic
- Verification steps that should run consistently
- Data transformations that are error-prone when done manually
- Any operation where consistency matters more than flexibility
