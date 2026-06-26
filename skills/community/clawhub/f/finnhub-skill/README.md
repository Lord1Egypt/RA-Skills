# Finnhub Skill

A lightweight **read-only OpenClaw skill** for Finnhub market data.

This skill lets an agent use the Finnhub API to retrieve:
- real-time quotes
- company profiles
- company news
- market news
- earnings calendar
- economic calendar

It also includes a reusable **daily stock news report template** for trader-style summaries.

## Scope

**Read-only only.**

This skill does **not**:
- place trades
- modify accounts
- store credentials in files
- support arbitrary HTTP hosts

## Files

```text
finnhub-skill/
├── SKILL.md
├── README.md
├── scripts/
│   └── finnhub.py
└── references/
    ├── api.md
    └── daily-report-template.md
```

## Requirements

- Python 3
- A valid Finnhub API key

## Configuration

Set your API key in the environment:

```bash
export FINNHUB_API_KEY=your_api_key
```

Optional base URL override is supported **only for the official Finnhub domain**:

```bash
export FINNHUB_BASE_URL=https://finnhub.io/api/v1
```

## Usage

### Quote

```bash
python3 scripts/finnhub.py quote --symbol AAPL
python3 scripts/finnhub.py quote --symbol TSLA --raw
```

### Candles

```bash
python3 scripts/finnhub.py candles --symbol AAPL --resolution D --from-ts 1711584000 --to-ts 1712188800
```

### Company profile

```bash
python3 scripts/finnhub.py profile --symbol NVDA
```

### Company news

```bash
python3 scripts/finnhub.py company-news --symbol TSLA --date-from 2026-03-29 --date-to 2026-03-29
```

### Market news

```bash
python3 scripts/finnhub.py market-news --category general
```

### Earnings calendar

```bash
python3 scripts/finnhub.py earnings --date-from 2026-03-30 --date-to 2026-04-06
```

### Economic calendar

```bash
python3 scripts/finnhub.py economic --date-from 2026-03-30 --date-to 2026-04-06
```

## Output Modes

- Default: **human-readable summary**
- Optional: `--raw` for JSON output

## Daily Report Workflow

This skill supports a structured daily stock report workflow, combining:
1. quote / price summary
2. key company news
3. narrative interpretation
4. trader-style final rating

See:
- `references/daily-report-template.md`

## Security Notes

- Requests are restricted to the official Finnhub domain
- API tokens are not printed in logs or errors
- This skill is intentionally read-only
- Arbitrary host override is blocked to reduce exfiltration risk

## Known Limitations

Finnhub access depends on your API plan.

For example, some keys may support:
- quote ✅
- company news ✅

but not:
- stock candles / volume ❌

If a Finnhub endpoint is unavailable under the current plan, the skill should:
- fail clearly
- avoid fabricating data
- fall back where possible (for example: quote + news report without volume detail)

## Status

Current version: **draft v0.2 / v1-ready candidate**

## License

MIT (recommended when publishing; add a LICENSE file if needed)
