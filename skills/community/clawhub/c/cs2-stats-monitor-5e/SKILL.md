---
name: cs-stats-monitor-generic
description: 5E CS2 Stats Query and Real-time Monitor. Supports custom player lists, query specified players' CS2 match history, analyze match performance, and real-time monitoring for new matches. Keywords: CS stats, 5E, check stats, monitor matches, CS2 stats, match report.
---

# CS Stats Monitor (Generic)

5E Platform CS2 Stats Query and Real-time Monitoring Tool (Generic Version).

## Core Capabilities

### 1. Query Stats
Query detailed data of the last 5 matches for specified players.

```bash
# Query single player's last 5 matches
python {SKILL_DIR}/scripts/cs_monitor.py --once --players <player_name>

# Query multiple players
python {SKILL_DIR}/scripts/cs_monitor.py --once --players player1 player2 player3

# Use default player list (set in config)
python {SKILL_DIR}/scripts/cs_monitor.py --once
```

### 2. Real-time Monitoring
Background continuous polling, automatically output reports when new matches are detected.

```bash
# Start monitoring (default 60s polling)
python {SKILL_DIR}/scripts/cs_monitor.py --players player1 player2

# Custom polling interval
python {SKILL_DIR}/scripts/cs_monitor.py --players player1 --interval 30

# Reset monitoring state
python {SKILL_DIR}/scripts/cs_monitor.py --reset
```

**Start Method**: Use tmux to run monitoring in background, check output regularly.

```bash
# Recommended: tmux background run
tmux new-session -d -s cs-monitor
tmux send-keys -t cs-monitor "python {SKILL_DIR}/scripts/cs_monitor.py --players player1 player2" Enter

# Check output
tmux capture-pane -t cs-monitor -p
```

### 3. Configuration File (Optional)
Create `{SKILL_DIR}/config.json` to set default players:

```json
{
  "default_players": ["player1", "player2", "player3"],
  "default_interval": 60
}
```

## Data Capabilities

**Per Match**:
- Core Metrics: Rating, ADR, KAST, RWS, K/D/A
- Kill Details: Headshot rate, first kill, first death, AWP kills, multi-kills (3K/4K/5K)
- Clutches: 1v1~1v5 success count
- Utility: Flash assists, team flashes, utility damage, bomb plants/defuses
- Sides: T-side/CT-side K/D/Rating
- Scoreboard: Full 10-player data

**Limitations**:
- API returns only last **5 matches**, cannot get more history
- Season overview requires login Cookie

## Analysis Guidelines

When reviewing match reports, analyze from these dimensions:

1. **Core Data Rating**: Rating >1.3 excellent, 1.0-1.3 normal, <0.85 poor; ADR >90 strong, 60-90 average, <60 weak
2. **Style Judgment**: AWP kill ratio, headshot rate, first kill/death ratio, T/CT side differences
3. **Stability**: Standard deviation of Rating across multiple matches, gap between highest and lowest
4. **Team Contribution**: KAST (round participation), utility usage, clutch ability
5. **If multiple players same match**: Horizontal comparison, identify who carried and who underperformed

Language Style: Direct, sharp, with a touch of dark humor. No formalities. Praise when good, roast when bad.

## Dependencies

- Python 3.10+
- aiohttp (`pip install aiohttp`)

## Resources

### scripts/
- `cs_monitor.py` — Main monitoring script, supports `--once` single query and continuous monitoring mode
