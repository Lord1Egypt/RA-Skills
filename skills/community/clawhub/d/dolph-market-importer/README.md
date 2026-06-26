# 🎯 Polymarket Market Importer

New markets go live on Polymarket every day. If you're finding them manually, you're finding them late. This skill searches Polymarket on a schedule with your keywords and volume filters, skips markets you've already imported, and pulls new ones into Simmer automatically. Set your criteria once, run it every 6 hours, and stop leaving edge on the table because you didn't know a market existed.

---

## Live Demo

```
🎯 Polymarket Market Importer
==================================================

  [LIVE MODE] Importing markets for real.

  Config: keywords=bitcoin,ethereum | min_volume=10000 | max_per_run=5 | categories=crypto

  Searching for: bitcoin
    Found 12 importable markets
    3 already imported, 9 new
    Category match: 7

  Searching for: ethereum
    Found 8 importable markets
    2 already imported, 6 new
    Category match: 5

  Importing: "Will BTC exceed $150k by July 2026?" (vol: $125,000)
    ✅ Imported successfully
  Importing: "Will ETH reach $5k by June 2026?" (vol: $89,000)
    ✅ Imported successfully
  Importing: "Will ETH gas fees stay below 10 gwei this month?" (vol: $34,500)
    ✅ Imported successfully

  Summary: 20 found | 5 already seen | 3 imported (max 5)
{"automaton": {"signals": 20, "trades_attempted": 0, "trades_executed": 3}}
```

Markets already in your Simmer portfolio get skipped. New ones matching your filters get pulled in. The import cap keeps you from burning through your daily quota in one run.

---

## Quick Start

```bash
# 1. Install the SDK
pip install simmer-sdk

# 2. Set your API key
export SIMMER_API_KEY="sk_live_..."

# 3. Dry run to see what it finds
python market_importer.py
```

That's it. When you're happy with the results, add `--live` to actually import.

---

## Configuration

| Parameter | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `keywords` | `IMPORTER_KEYWORDS` | `bitcoin,ethereum` | Comma-separated search terms. Each keyword runs a separate search. |
| `min_volume` | `IMPORTER_MIN_VOLUME` | `10000` | Minimum 24h volume in USD. Filters out thin, illiquid markets. |
| `max_per_run` | `IMPORTER_MAX_PER_RUN` | `5` | Cap on imports per execution. Protects your daily quota. |
| `categories` | `IMPORTER_CATEGORIES` | `crypto` | Comma-separated category filter. Matches against question text and tags. |

Update any setting inline:

```bash
python market_importer.py --set keywords=bitcoin,ethereum,solana
python market_importer.py --set min_volume=25000
python market_importer.py --set max_per_run=10
python market_importer.py --set categories=crypto,politics
```

---

## CLI Reference

### Dry run (default)

```bash
python market_importer.py
```

Shows what would be imported without touching anything. Always start here.

### Live import

```bash
python market_importer.py --live
```

Actually imports markets into Simmer. This is the one you put on cron.

### Show imported markets

```bash
python market_importer.py --positions
```

Lists your most recently imported markets with IDs and timestamps.

### Show config

```bash
python market_importer.py --config
```

Prints current config values, env var names, and defaults.

### Update config

```bash
python market_importer.py --set keywords=bitcoin,xrp,solana
python market_importer.py --set min_volume=50000
```

Persists to the skill config file. Takes effect on next run.

### Quiet mode

```bash
python market_importer.py --live --quiet
```

Suppresses search details. Only outputs on actual imports or errors. Good for cron.

---

## Tips

- **Run every 6 hours.** New markets go live throughout the day. The default cron schedule (`0 */6 * * *`) handles this.

- **Start narrow.** Two or three specific keywords beat a broad sweep. You'll learn what your market looks like before you scale up.

- **Respect the quota.** Free accounts get 10 imports/day, Pro gets 50. Set `max_per_run` accordingly — if you run 4x daily with `max_per_run=5`, that's 20 attempts at the cap.

- **Volume filter matters.** Thin markets waste your import quota and rarely have enough liquidity to trade profitably. Keep `min_volume` at 10,000+ unless you have a specific reason to go lower.

- **Categories stack with keywords.** A keyword search returns candidates, then the category filter narrows them. If you search "bitcoin" with category "politics", you'll only get political markets that mention bitcoin.

---

## Troubleshooting

**"No importable markets found"**
Check your keyword spelling. Try broader terms. Lower `min_volume` — the default of 10,000 is conservative. Some new markets haven't built volume yet.

**"Import failed"**
Your daily import quota is probably hit. Free tier is 10/day, Pro is 50/day. The skill will pick up where it left off next run — already-imported markets are tracked locally.

**"SIMMER_API_KEY not set"**
Get your key from [simmer.markets/dashboard](https://simmer.markets/dashboard) → SDK tab. Export it:
```bash
export SIMMER_API_KEY="sk_live_..."
```

**Markets not matching categories**
Category filtering checks the market question text and tags. If you're filtering for "politics" but the market question doesn't contain that word, it won't match. Try different category terms or leave categories empty to skip this filter.

**"Search failed" errors**
Usually transient API issues. The skill will retry on the next scheduled run. If it persists, check your network and API key validity.

---

## Schedule

Runs every 6 hours via cron (`0 */6 * * *`). Configured in `clawhub.json`. Adjust the schedule there if you want more or less frequent runs.

---

## How It Works

1. Reads your keywords and filters from config
2. Searches Polymarket for each keyword via the Simmer SDK
3. Filters by volume, category, and already-imported status
4. Imports new matches up to `max_per_run`
5. Saves imported market IDs to `imported_markets.json` for dedup
6. Emits an automaton report for OpenClaw tracking

No state beyond the seen-markets file. No external dependencies beyond `simmer-sdk`. Clean and predictable.
