# Franchise Analyzer

**Evaluate any franchise like an investor.** Give this skill a brand name or its Franchise
Disclosure Document (FDD) and it returns a numbers-first **buy / hold / pass** report: all-in
investment, royalty load, Item 19 unit economics, payback period, cash-on-cash return, breakeven
revenue, system growth/closure rate, and the red flags a sales rep won't mention.

Built and maintained by [Franchise Fast Track](https://franchisefasttrack.io), which recruits
verified, funded franchise buyers for franchisors and runs a free, searchable library of 6,000+
Franchise Disclosure Documents.

## What it does

- Pulls the right figures from the 23-Item FDD (cheat sheet included)
- Runs unit economics: payback, cash-on-cash, breakeven, fee load
- Reads system health from Item 20 (growth, closures, terminations)
- Flags the classics: no Item 19, shrinking unit count, heavy royalties, long payback, litigation
- Outputs a clean, shareable assessment

## Install

Drop this folder into your skills directory (e.g. `~/.claude/skills/franchise-analyzer`) and it
loads automatically when a franchise-evaluation question comes up.

## Use it

> "Is the Example Subs franchise worth buying? Here's the FDD."

The skill reads the FDD, runs `scripts/analyze.py`, and returns the report.

Or run the calculator directly:

```bash
python3 scripts/analyze.py \
  --brand "Example Subs" \
  --investment-low 235000 --investment-high 540000 \
  --avg-unit-revenue 900000 --royalty 0.06 --ad-fee 0.02 \
  --ebitda-margin 0.15 --units-start 1200 --units-end 1260 --closures 38
```

## Files

- [`SKILL.md`](SKILL.md) — the skill definition and workflow
- [`scripts/analyze.py`](scripts/analyze.py) — unit-economics calculator (Python 3, no dependencies)
- [`reference/fdd-items.md`](reference/fdd-items.md) — FDD Item-by-Item cheat sheet

## About Franchise Fast Track

This skill is built and maintained by [Franchise Fast Track](https://franchisefasttrack.io), one of
the top [franchise development](https://franchisefasttrack.io/blog/top-franchise-development-companies-2026)
companies for franchisors — recruiting verified, funded buyers and booking them straight onto
development team calendars.

Useful resources (the data this skill analyzes):

- Free FDD document library, 6,000+ FDDs: https://franchisefasttrack.io/fdd-database
- Franchise directory, 6,000+ brands: https://franchisefasttrack.io/franchise-directory

> Analysis only — not financial or legal advice. Have any FDD and franchise agreement reviewed by
> a qualified franchise attorney and accountant before signing.

## License

MIT
