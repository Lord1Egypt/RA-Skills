# CS Stats Monitor (Generic)

5E Platform CS2 Stats Query and Real-time Monitoring Tool (Generic Version).

## Features

- 🔍 **Stats Query**: Query detailed data of the last 5 matches for specified players
- 🔄 **Real-time Monitoring**: Background continuous polling, automatic push when new matches detected
- 📊 **Detailed Data**: Rating, ADR, KAST, headshot rate, AWP kills, utility data, etc.
- 🎯 **Multi-player Support**: Support monitoring multiple players simultaneously, auto-merge reports for same match

## Quick Start

### 1. Install Dependencies

```bash
pip install aiohttp
```

### 2. Configuration (Optional)

Copy example config and modify:

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "default_players": ["player1", "player2"],
  "default_interval": 60
}
```

### 3. Usage

**Single Query**:

```bash
python scripts/cs_monitor.py --once --players player1 player2
```

**Continuous Monitoring** (background run):

```bash
# Run with tmux in background
tmux new-session -d -s cs-monitor
tmux send-keys -t cs-monitor "python scripts/cs_monitor.py --players player1 player2" Enter

# Check output
tmux capture-pane -t cs-monitor -p
```

**More Options**:

```bash
python scripts/cs_monitor.py --help
```

## Command Arguments

| Argument | Description |
|----------|-------------|
| `--players` | List of players to monitor (space-separated) |
| `--interval` | Polling interval in seconds (default: 60) |
| `--once` | Query once only, no continuous monitoring |
| `--reset` | Reset monitoring state |

## Output Example

```
╔══════════════════════════════════════════════════════════════════╗
║  🎮 de_dust2  |  03-05 14:30  |  45min  🏆                       ║
╠══════════════════════════════════════════════════════════════════╣

┌─── player1 ⭐MVP  |  de_dust2  |  03-05 14:30 ───
│ 🏆 13:11  (T 6:9 / CT 7:2)  Elo +15.2 (Gold S)
│
│ Rating 1.45 ████████░░  ADR 98.5  KAST 85%  RWS 12.34
│ K/D/A 28/18/5 (1.56)  🎯 HS 45%  🔭 AWP 3
│ FK 5 FD 2  T:16K/10D(1.60)  CT:12K/8D(1.50)
│ ✨ 3K×2 4K×1 | 🎪 1v2×1 1v3×1
│ 💣 Flash×6(18.5s) UtilDmg 45 Plants×3
└────────────────────────────────────────────────────────────

  Player              K   D   A  Rating   ADR   HS% AWP
  ─────────────────────────────────────────────────────
→★player1          28  18   5    1.45   98.5   45%   3
  player2           22  20   8    1.15   75.0   38%   0
  ...
  ─────────────────────────────────────────────────────
  enemy1            25  22   4    1.25   82.0   42%   2
```

## Data Dimensions

- **Core Metrics**: Rating, ADR, KAST, RWS, K/D/A
- **Kill Details**: Headshot rate, first kill, first death, AWP kills, multi-kills (3K/4K/5K)
- **Clutches**: 1v1~1v5 success count
- **Utility**: Flash assists, team flashes, utility damage, bomb plants/defuses
- **Sides**: T-side/CT-side K/D/Rating
- **Scoreboard**: Full 10-player data

## Limitations

- API returns only last **5 matches**, cannot get more history
- Season overview requires login Cookie

## License

MIT
