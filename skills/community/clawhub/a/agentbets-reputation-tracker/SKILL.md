---
name: agent-reputation-tracker
description: "Track and display your agent's betting reputation. Computes win rate, ROI, volume, streaks, max drawdown, and Sharpe proxy from local bet history. Formats output for Moltbook profiles or plaintext reputation cards. Use when asked about agent stats, performance, win rate, ROI, reputation, or track record."
metadata:
  openclaw:
    emoji: "🏆"
    requires:
      bins: ["python3", "sqlite3"]
    credentials:
      - id: "moltbook-api-key"
        name: "Moltbook API Key"
        description: "Optional — API key from https://moltbook.com for publishing agent profiles"
        env: "MOLTBOOK_API_KEY"
---

# Agent Reputation Tracker

Compute and display your betting agent's performance metrics from local bet history.

## When to Use

Use this skill when the user asks about:
- Agent stats, performance, or track record
- Win rate, ROI, or profit/loss summary
- Current winning or losing streak
- Rolling performance (last 7 days, 30 days, etc.)
- Publishing or updating a Moltbook profile
- Generating a reputation card to share
- Comparing agent performance across time periods
- Max drawdown or risk-adjusted performance

## Database Schema

The skill expects a SQLite database at `~/.openclaw/data/bet_log.db` with this schema:

```sql
CREATE TABLE IF NOT EXISTS bets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,           -- ISO 8601 format
  platform TEXT NOT NULL,            -- e.g., 'draftkings', 'polymarket', 'kalshi'
  event TEXT,                        -- event description
  selection TEXT,                    -- what was bet on
  bet_type TEXT DEFAULT 'moneyline', -- moneyline, spread, total, prop, binary
  odds REAL NOT NULL,                -- American odds for sportsbooks, decimal for prediction markets
  odds_format TEXT DEFAULT 'american', -- 'american' or 'decimal'
  stake REAL NOT NULL,               -- amount wagered
  result TEXT,                       -- 'win', 'loss', 'push', 'pending'
  payout REAL DEFAULT 0,             -- amount returned (including stake if won)
  notes TEXT
);
```

If the database doesn't exist, offer to create it with the schema above.

## Operations

### 1. Lifetime Stats

Compute overall performance across all resolved bets:

```bash
python3 -c "
import sqlite3, json, math, os
db = os.path.expanduser('~/.openclaw/data/bet_log.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute(\"SELECT stake, payout, result FROM bets WHERE result IN ('win','loss')\")
rows = c.fetchall()
if not rows:
    print(json.dumps({'error': 'No resolved bets found'}))
else:
    wins = sum(1 for r in rows if r[2]=='win')
    losses = sum(1 for r in rows if r[2]=='loss')
    total_staked = sum(r[0] for r in rows)
    total_payout = sum(r[1] for r in rows)
    profit = total_payout - total_staked
    roi = (profit / total_staked * 100) if total_staked > 0 else 0
    returns = [(r[1]-r[0])/r[0] for r in rows if r[0]>0]
    avg_ret = sum(returns)/len(returns) if returns else 0
    std_ret = (sum((x-avg_ret)**2 for x in returns)/len(returns))**0.5 if len(returns)>1 else 0
    sharpe = avg_ret/std_ret if std_ret>0 else 0
    # Max drawdown
    cumulative = 0; peak = 0; max_dd = 0
    for r in rows:
        cumulative += r[1] - r[0]
        if cumulative > peak: peak = cumulative
        dd = peak - cumulative
        if dd > max_dd: max_dd = dd
    # Streaks
    streak = 0; max_w = 0; max_l = 0; cur = 0; cur_type = ''
    for r in rows:
        if r[2] == cur_type:
            cur += 1
        else:
            cur_type = r[2]; cur = 1
        if cur_type == 'win' and cur > max_w: max_w = cur
        if cur_type == 'loss' and cur > max_l: max_l = cur
    print(json.dumps({
        'total_bets': len(rows), 'wins': wins, 'losses': losses,
        'win_rate': round(wins/(wins+losses)*100, 1),
        'total_staked': round(total_staked, 2),
        'total_payout': round(total_payout, 2),
        'profit': round(profit, 2),
        'roi_pct': round(roi, 1),
        'sharpe_proxy': round(sharpe, 3),
        'max_drawdown': round(max_dd, 2),
        'longest_win_streak': max_w,
        'longest_loss_streak': max_l,
        'current_streak': f'{cur} {cur_type}s' if cur_type else 'N/A'
    }, indent=2))
conn.close()
"
```

### 2. Rolling Window Stats

Compute stats for a recent time period. Replace DAYS with the window (7, 30, 90):

```bash
python3 -c "
import sqlite3, json, os
from datetime import datetime, timedelta
db = os.path.expanduser('~/.openclaw/data/bet_log.db')
days = DAYS
conn = sqlite3.connect(db)
c = conn.cursor()
cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
c.execute(\"SELECT stake, payout, result, platform FROM bets WHERE result IN ('win','loss') AND timestamp >= ?\", (cutoff,))
rows = c.fetchall()
if not rows:
    print(json.dumps({'error': f'No resolved bets in last {days} days'}))
else:
    wins = sum(1 for r in rows if r[2]=='win')
    losses = sum(1 for r in rows if r[2]=='loss')
    total_staked = sum(r[0] for r in rows)
    total_payout = sum(r[1] for r in rows)
    profit = total_payout - total_staked
    roi = (profit / total_staked * 100) if total_staked > 0 else 0
    platforms = {}
    for r in rows:
        p = r[3]
        if p not in platforms: platforms[p] = {'bets':0,'profit':0}
        platforms[p]['bets'] += 1
        platforms[p]['profit'] += r[1] - r[0]
    for p in platforms: platforms[p]['profit'] = round(platforms[p]['profit'], 2)
    print(json.dumps({
        'window_days': days,
        'total_bets': len(rows), 'wins': wins, 'losses': losses,
        'win_rate': round(wins/(wins+losses)*100, 1),
        'profit': round(profit, 2),
        'roi_pct': round(roi, 1),
        'by_platform': platforms
    }, indent=2))
conn.close()
"
```

### 3. Moltbook Profile JSON

Generate a JSON payload compatible with Moltbook's agent profile schema:

```bash
python3 -c "
import sqlite3, json, os
from datetime import datetime
db = os.path.expanduser('~/.openclaw/data/bet_log.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute(\"SELECT stake, payout, result, platform, timestamp FROM bets WHERE result IN ('win','loss') ORDER BY timestamp\")
rows = c.fetchall()
if not rows:
    print(json.dumps({'error': 'No resolved bets found'}))
else:
    wins = sum(1 for r in rows if r[2]=='win')
    losses = sum(1 for r in rows if r[2]=='loss')
    total_staked = sum(r[0] for r in rows)
    profit = sum(r[1] for r in rows) - total_staked
    roi = (profit / total_staked * 100) if total_staked > 0 else 0
    platforms = list(set(r[3] for r in rows))
    first_bet = rows[0][4]
    last_bet = rows[-1][4]
    # Monthly returns
    monthly = {}
    for r in rows:
        mo = r[4][:7]
        if mo not in monthly: monthly[mo] = {'staked':0, 'profit':0}
        monthly[mo]['staked'] += r[0]
        monthly[mo]['profit'] += r[1] - r[0]
    monthly_roi = {k: round(v['profit']/v['staked']*100, 1) if v['staked']>0 else 0 for k,v in monthly.items()}
    profile = {
        'schema_version': '1.0',
        'agent_type': 'openclaw',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'stats': {
            'total_bets': len(rows),
            'win_rate': round(wins/(wins+losses)*100, 1),
            'roi_pct': round(roi, 1),
            'total_volume': round(total_staked, 2),
            'net_profit': round(profit, 2),
            'first_bet': first_bet,
            'last_bet': last_bet,
            'active_days': len(set(r[4][:10] for r in rows))
        },
        'platforms': platforms,
        'monthly_roi': monthly_roi
    }
    print(json.dumps(profile, indent=2))
conn.close()
"
```

To publish to Moltbook (requires MOLTBOOK_API_KEY):

```bash
# Save profile to file first, then push
python3 -c \"<above script>\" > /tmp/agent_profile.json
curl -s -X POST https://api.moltbook.com/v1/agents/profile \
  -H "Authorization: Bearer $MOLTBOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/agent_profile.json | jq .
```

### 4. Reputation Card (Plaintext)

Generate a human-readable reputation card for sharing:

```bash
python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.openclaw/data/bet_log.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute(\"SELECT stake, payout, result FROM bets WHERE result IN ('win','loss')\")
rows = c.fetchall()
if not rows:
    print('No resolved bets found.')
else:
    wins = sum(1 for r in rows if r[2]=='win')
    losses = sum(1 for r in rows if r[2]=='loss')
    total_staked = sum(r[0] for r in rows)
    profit = sum(r[1] for r in rows) - total_staked
    roi = (profit / total_staked * 100) if total_staked > 0 else 0
    streak = 0; cur_type = ''
    for r in rows:
        if r[2] == cur_type: streak += 1
        else: cur_type = r[2]; streak = 1
    card = f'''
╔══════════════════════════════════════╗
║       AGENT REPUTATION CARD         ║
╠══════════════════════════════════════╣
║  Record:     {wins}W - {losses}L{' '*(21-len(f'{wins}W - {losses}L'))}║
║  Win Rate:   {wins/(wins+losses)*100:.1f}%{' '*(22-len(f'{wins/(wins+losses)*100:.1f}%'))}║
║  ROI:        {roi:+.1f}%{' '*(22-len(f'{roi:+.1f}%'))}║
║  Volume:     ${total_staked:,.0f}{' '*(22-len(f'${total_staked:,.0f}'))}║
║  Profit:     ${profit:+,.2f}{' '*(22-len(f'${profit:+,.2f}'))}║
║  Streak:     {streak} {cur_type}s{' '*(22-len(f'{streak} {cur_type}s'))}║
║  Total Bets: {len(rows)}{' '*(22-len(str(len(rows))))}║
╚══════════════════════════════════════╝
    '''
    print(card.strip())
conn.close()
"
```

## Output Rules

1. Always show win rate as a percentage with one decimal place
2. Always show ROI with a sign prefix (+/-)
3. Volume and profit should be in USD with commas
4. When showing rolling windows, always note the time period
5. For Moltbook profiles, validate JSON before publishing
6. If bet count is under 50, add a disclaimer: "Small sample size — stats may not be reliable"
7. Always show current streak in the reputation card

## Error Handling

- If bet_log.db doesn't exist, offer to create it with the schema and explain how to log bets
- If no resolved bets exist, report "No resolved bets found" and suggest logging some bets first
- If MOLTBOOK_API_KEY is not set and user requests publishing, explain how to get a key at https://moltbook.com
- If Moltbook API returns an error, display the error message and suggest checking the key
- If database is corrupted, suggest running `sqlite3 ~/.openclaw/data/bet_log.db "PRAGMA integrity_check"`

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-agent-reputation-tracker-skill/](https://agentbets.ai/guides/openclaw-agent-reputation-tracker-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
