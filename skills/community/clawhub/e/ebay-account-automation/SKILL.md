---
name: ebay-account-automation
description: "Run eBay seller account activity cycles via ADS Power — search, browse, favorite, and cart actions on a rotating schedule."
metadata:
  homepage: https://github.com/yourrepo/ebay-account-automation
  allowed-tools: []
  user-invocable: true
---

# eBay Account Automation

Execute simulated buyer activity on eBay seller accounts using ADS Power browser automation, on a rotating 30-minute per-account cycle.

## Workflow

### 1. Verify environment

- ADS Power client running with Local API enabled (`http://local.adspower.net:50325`)
- Node.js 18+
- Required packages: `cdp-protocol`, `ws`

### 2. Configure

Create `config_local.js` in the skill directory (gitignored):

```javascript
module.exports = {
  ADS_API_BASE: 'http://local.adspower.net:50325',
  ADS_API_KEY: 'YOUR_ADS_POWER_API_KEY',   // from ADS Power → API Config
  ACCOUNT_RUNTIME_MS: 30 * 60 * 1000,      // 30 min per account
  KEYWORDS_FILE: 'keywords.txt',
  STATE_DIR: 'state',
  CYCLE_STATE_FILE: 'state/cycle_state.json',
  EBAY_BASE_URL: 'https://www.ebay.com',
};
```

Add search keywords to `keywords.txt` (one per line, English preferred):

```
basketball jersey
football gloves
training gear
sports hoodies
```

### 3. Install dependencies

```bash
cd skills/ebay-account-automation/scripts
npm install
```

### 4. Run a quick test (5 min, single account)

```bash
node skills/ebay-account-automation/scripts/test_quick.js
```

### 5. Run one cycle (single account, 30 min)

```bash
node skills/ebay-account-automation/scripts/scheduler.js
```

### 6. Run all accounts once

```bash
node skills/ebay-account-automation/scripts/scheduler.js --full
```

### 7. Schedule with OpenClaw Cron

```bash
# Every 30 minutes, one account at a time
openclaw cron add \
  --name ebay_account_cycler \
  --every-ms 1800000 \
  --session-target isolated \
  --payload-kind agentTurn \
  --payload-message "cd C:\path\to\skills\ebay-account-automation\scripts && node scheduler.js"
```

## Behavior per account

Each 30-minute cycle:

1. Read account list from ADS Power API
2. Rotate to next account (state persisted in `cycle_state.json`)
3. Open browser via ADS Power Local API
4. Connect via WebSocket CDP
5. Execute loop:
   - Search with random keyword
   - Click 2–4 product links
   - On product page: scroll, favorite (60%), add to cart (35%)
   - Random rest 10–25s between rounds
6. Close browser after ACCOUNT_RUNTIME_MS
7. Log results

## State

`state/cycle_state.json` tracks:
- `accountIndex` — next account to run
- `lastRun` — ISO timestamp
- `totalRuns` — cumulative count

To reset rotation: set `accountIndex` back to `0` in that file.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `User_id is not open` | Account not open in ADS Power | Open account manually or wait for sync |
| `SunBrowser is updating` | ADS Power browser updating | Wait 10–30s, auto-retry |
| `Exceeding open daily limit` | ADS Power daily browser limit | Wait 8h or reduce cycle frequency |
| Favorite/cart buttons not found | eBay page structure changed | Run `diag_selectors2.js` to refresh locators |

## Files

```
ebay-account-automation/
├── SKILL.md
├── scripts/
│   ├── scheduler.js          # Cron entry point
│   ├── cycle_runner.js       # Account rotation controller
│   ├── cycle_state.js        # Rotation state persistence
│   ├── ads_api.js            # ADS Power Local API wrapper
│   ├── cdp_ebay_bot.js       # Browser behavior engine (CDP)
│   ├── config.js             # Config loader (prefers config_local.js)
│   ├── test_quick.js         # 5-min quick test
│   ├── diag_selectors2.js   # Selector diagnostics
│   └── keywords.txt         # Search keyword bank
└── references/
    └── README.md             # Full documentation
```
