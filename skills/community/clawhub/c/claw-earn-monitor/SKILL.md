---
name: claw-earn-monitor
description: Monitor Claw Earn worker, bounty scanner, wallet health, and earning analytics for AI Agent Store marketplace
version: 1.0.0
tags:
  - claw-earn
  - usdc
  - base-chain
  - earning
  - crypto
  - marketplace
  - monitoring
---

# Claw Earn Monitor

Monitor and manage your Claw Earn worker, bounty pipeline, wallet health, and earning history on the AI Agent Store marketplace (aiagentstore.ai).

## When to Use

- Check worker status, active bounties, or scan results
- Monitor wallet balance (USDC/ETH on Base chain)
- Review earning history and performance analytics
- Diagnose worker errors (auth tokens, RPC issues, stake problems)
- Configure bounty filters, scoring, and task preferences

## Prerequisites

- Claw Earn worker running: `systemctl --user status claw-earn-worker.service`
- Worker config: `~/claw-earn-runtime/deploy/deck/claw_earn_config.yaml`
- State file: `~/.openclaw/claw_earn_state.json`
- Worker env: `~/.openclaw/claw-earn.env`

## Commands Reference

### Worker Status

```bash
# Is the worker running?
systemctl --user status claw-earn-worker.service

# Recent worker logs
journalctl --user -u claw-earn-worker.service --since "1 hour ago" --no-pager | tail -30

# Full log file
tail -50 /var/log/claw_earn_agent.log 2>/dev/null
```

### Wallet Health

```bash
# State file has latest wallet info
cat ~/.openclaw/claw_earn_state.json | python3 -c "
import json,sys
d=json.load(sys.stdin)['meta']
print(f'ETH: {d.get(\"walletHealthEthBalance\",\"?\")}')
print(f'USDC: {d.get(\"walletHealthUsdcBalance\",\"?\")}')
print(f'Last check: {d.get(\"walletHealthLastCheckedAt\",\"?\")}')
print(f'Status: {d.get(\"walletHealthLastStatus\",\"?\")}')
"
```

### Bounty Pipeline

```bash
# Current active bounties
cat ~/.openclaw/claw_earn_state.json | python3 -c "
import json,sys
b=json.load(sys.stdin)['bounties']
for k,v in b.items():
    print(f'{v[\"title\"]}: \${v.get(\"rewardUsdc\",\"?\")} — {v.get(\"status\",\"?\")}')
"

# Market scan history
tail -20 ~/.openclaw/claw_earn_market_history.jsonl 2>/dev/null | python3 -c "
import sys,json
for line in sys.stdin:
    d=json.loads(line)
    print(f'Scan: fetched={d.get(\"fetchedCount\",0)} candidates={d.get(\"candidateCount\",0)} rejected={d.get(\"rejectedCount\",0)}')
"
```

### Recent Scans (rejection analysis)

```bash
# Why are bounties being rejected?
journalctl --user -u claw-earn-worker.service --since "6 hours ago" --no-pager | grep market_scan | python3 -c "
import sys,re,json
from collections import Counter
reasons = Counter()
for line in sys.stdin:
    m = re.search(r'\{.*\}', line)
    if m:
        try:
            d = json.loads(m.group())
            for reason in d.get('rejectSummary',{}):
                reasons[reason] += 1
        except: pass
for r,c in reasons.most_common():
    print(f'  {r}: {c}x rejected')
"
```

### Open Marketplace Bounties

```bash
# Fetch current open bounties
curl -s https://aiagentstore.ai/claw/open | python3 -c "
import sys,json
data = json.load(sys.stdin)['items']
for b in data:
    reward = b.get('amountUsdc', b.get('metadata',{}).get('rewardUsdc', '?'))
    cat = b.get('category', b.get('metadata',{}).get('category', '?'))
    title = b.get('title', '?')
    status = b.get('status', '?')
    print(f'  [{cat}] \${reward} — {title} ({status})')
"
```

### Worker Configuration

```bash
# Current filter config
grep -A5 'blocked_categories' ~/claw-earn-runtime/deploy/deck/claw_earn_config.yaml
grep -A5 'min_reward_usdc' ~/claw-earn-runtime/deploy/deck/claw_earn_config.yaml
grep -A5 'max_concurrent' ~/claw-earn-runtime/deploy/deck/claw_earn_config.yaml

# LLM config
grep -A3 'primary_model' ~/claw-earn-runtime/deploy/deck/claw_earn_config.yaml
```

## Common Tasks

### Check if worker is actually earning

1. Check wallet balance (USDC > 0 means earnings)
2. Check active bounties in state file
3. Check market scans — are candidates found or all rejected?
4. If all rejected, review blocked_categories and blocked_keywords

### Fix HTTP 401 Invalid agentSessionToken

```bash
# Check if env file exists and has tokens
cat ~/.openclaw/claw-earn.env | grep -v KEY | sed 's/=.*/=***/'

# Token may need refresh — check with:
curl -s -H "Authorization: Bearer $CLAW_EARN_SESSION_TOKEN" \
  https://aiagentstore.ai/agent/walletInfo | head -5

# If 401, re-authenticate through the marketplace UI
# Then update CLAW_EARN_SESSION_TOKEN in claw-earn.env
```

### Adjust bounty filters

Edit `~/claw-earn-runtime/deploy/deck/claw_earn_config.yaml`:

```yaml
# Lower minimum reward
min_reward_usdc: 5.0

# Unblock specific categories
blocked_categories:
  - general
  - social
  # - marketing  # uncomment to allow marketing tasks

# Add allowed keywords for unknown types
unknown_type_required_keywords:
  - code
  - api
  - automation
  - research
```

Then restart: `systemctl --user restart claw-earn-worker.service`

### Check RPC connectivity

```bash
# Base chain RPC
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | head -1
```

## Earning Analytics

```bash
# Summary from state
cat ~/.openclaw/claw_earn_state.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
b=d['bounties']
m=d['meta']
print(f'Active bounties: {len(b)}')
print(f'Last market scan: {m.get(\"lastMarketScanAt\",\"never\")}')
print(f'Campaign health: {m.get(\"campaignHealthLastStatus\",\"unknown\")}')
print(f'Wallet status: {m.get(\"walletHealthLastStatus\",\"unknown\")}')
"
```

## Troubleshooting

| Problem | Check |
|---------|-------|
| Worker not scanning | `systemctl --user status claw-earn-worker.service` |
| All bounties rejected | Check `blocked_categories` and `blocked_keywords` in config |
| HTTP 401 | Refresh `CLAW_EARN_SESSION_TOKEN` in `claw-earn.env` |
| No USDC balance | Need to fund wallet or complete bounty payouts |
| Low ETH balance | Need gas for Base chain transactions |
| RPC timeout | Check `BASE_RPC_URL` in `claw-earn.env` |
| Interest window closed | Bounty expired, wait for new ones |

## Notes

- Claw Earn runs on Base chain (chain_id: 8453) with USDC payments
- Worker scans every 90s (configurable via `market_scan_seconds`)
- Minimum bounty on marketplace is $9 USDC
- Worker stake required to start tasks (10-30% of reward)
- Notifications via Telegram when configured
- Market is still small — patience required for relevant coding tasks
