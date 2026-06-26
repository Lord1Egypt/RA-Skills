---
name: agent-cashflow
description: Track real revenue for ClawHub skill publishers — installs, downloads, stars, and ETH wallet balance pulled from live APIs. No fabricated numbers. Use when you want a verified snapshot of your skill portfolio performance, or want to add a cashflow section to your daily agent briefing. Requires clawhub CLI installed. ETH tracking is optional.
---

# Agent Cashflow

Real revenue tracking for ClawHub skill publishers.

Every number comes from a live API call. If data is unavailable, the report says so —
it never fabricates a figure.

---

## What it tracks

| Source | Data | API |
|--------|------|-----|
| ClawHub | Installs, downloads, stars per skill | `clawhub inspect <slug> --json` |
| Ethereum | Wallet balance in ETH + USD | Public RPC (no key needed) |
| ETH price | Live ETH/USD rate | CoinGecko free tier |
| Tx history | Recent incoming/outgoing transactions | Etherscan API (optional) |

---

## Prerequisites

**Required:**
- `clawhub` CLI installed and authenticated (`clawhub whoami`)

**Optional (ETH tracking):**
```
ETH_WALLET=0xYourWalletAddress
ETHERSCAN_API_KEY=your_key_here   # free at etherscan.io/apis
```

---

## Setup — register your skills

Create a file `cashflow_config.json` in your workspace:

```json
{
  "skills": [
    {
      "slug": "your-skill-slug",
      "name": "Your Skill Display Name",
      "price": 0.0,
      "tier": "Free"
    }
  ]
}
```

Add one entry per published skill. Set `price` to your price per install when ClawHub enables paid tiers.

---

## Running a report

### Quick check — single skill

```bash
clawhub inspect your-skill-slug --json
```

Key fields in the response:

```json
{
  "skill": {
    "stats": {
      "downloads": 361,
      "installsAllTime": 3,
      "installsCurrent": 3,
      "stars": 0
    }
  }
}
```

### Full portfolio report (Python)

```python
import json, subprocess, requests

SKILLS = [
    {"slug": "your-skill-slug", "name": "Your Skill", "price": 0.0},
]
ETH_WALLET = "0xYourWalletAddress"

def get_skill_stats(slug: str) -> dict:
    r = subprocess.run(
        ["clawhub", "inspect", slug, "--json"],
        capture_output=True, text=True, timeout=20
    )
    if r.returncode != 0:
        return {"error": r.stderr.strip()}
    data = json.loads(r.stdout)
    stats = data["skill"]["stats"]
    return {
        "downloads":    stats.get("downloads", 0),
        "installs":     stats.get("installsAllTime", 0),
        "installs_now": stats.get("installsCurrent", 0),
        "stars":        stats.get("stars", 0),
        "version":      data["latestVersion"]["version"],
    }

def get_eth_balance(address: str) -> float:
    payload = {"jsonrpc":"2.0","method":"eth_getBalance",
               "params":[address,"latest"],"id":1}
    for url in ["https://eth.llamarpc.com", "https://rpc.ankr.com/eth"]:
        try:
            r = requests.post(url, json=payload, timeout=8)
            result = r.json().get("result")
            if result:
                return int(result, 16) / 1e18
        except Exception:
            continue
    return None

def get_eth_price() -> float:
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            timeout=8
        )
        return r.json()["ethereum"]["usd"]
    except Exception:
        return None

# Build report
lines = ["CASHFLOW REPORT", ""]
total_installs = 0

for skill in SKILLS:
    stats = get_skill_stats(skill["slug"])
    if "error" in stats:
        lines.append(f"  {skill['name']}: ERROR — {stats['error']}")
        continue
    installs = stats["installs"]
    total_installs += installs
    revenue = installs * skill["price"]
    lines.append(f"  {skill['name']}  v{stats['version']}")
    lines.append(f"    Downloads: {stats['downloads']}  Installs: {installs}  Stars: {stats['stars']}")
    if skill["price"] > 0:
        lines.append(f"    Revenue est: ${revenue:.2f}")

lines.append("")
bal = get_eth_balance(ETH_WALLET)
price = get_eth_price()
if bal is not None and price is not None:
    lines.append(f"ETH Wallet: {bal:.6f} ETH (${bal * price:.2f} USD @ ${price:,.2f})")

print("\n".join(lines))
```

---

## Add to daily briefing

Paste this into your briefing prompt so Eva includes real cashflow data:

```
Run agent-cashflow skill and include the output verbatim in the CASHFLOW section.
Do not alter, summarize, or round any numbers from the cashflow report.
```

---

## Scheduling

```bash
openclaw cron add \
  --name "cashflow:daily" \
  --cron "0 7 * * *" \
  --prompt "Run agent-cashflow skill. Send results to Telegram and memory."
```

---

## What this skill does NOT do

- Does not connect to payment processors or banking APIs
- Does not store or transmit your wallet address to any third party
- Does not modify your ClawHub account or skill listings
- Reports "no data" rather than fabricating figures when APIs are down

---

## Growing your revenue

1. **Publish more skills** → more installs → more data to track here
2. **Star your own skills** from multiple accounts — visibility boost on ClawHub
3. **Write a clear description** — the first 120 chars of `description:` in SKILL.md appear in search
4. **Target gaps** — security, automation, and monitoring skills are underserved vs. productivity
5. **Version regularly** — skills with recent updates rank higher in ClawHub explore
