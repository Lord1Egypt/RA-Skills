---
name: dota2-stats-skill
description: Use this for Dota 2 / DOTA2 / OpenDota questions about players, Steam64/account_id, match_id, heroes, hero matchups, pro matches, teams, leagues, live games, ranks and win rates. Runs a Python standard-library CLI with 27 common OpenDota commands. Default output is Chinese; use --lang en for English. 用于刀塔2/Dota2/DOTA2/OpenDota 查询：玩家战绩、玩家ID、Steam ID、比赛ID、比赛详情、英雄数据、英雄克制、英雄胜率、职业赛事、战队、联赛、实时比赛、段位和胜率。
---

# Dota 2 Stats Query Skill

This skill uses a Python script to query Dota 2 data via the [OpenDota API](https://docs.opendota.com/), focused on common player, match, hero, team, league and pro-scene workflows.

## Execution

Use the script from the installed skill directory. Do not assume the current working directory is the skill root unless it has been verified.

### Claude Code
```bash
python ~/.claude/skills/dota2-stats-skill/scripts/dota2_query.py <command> [args]
```

### OpenClaw
```bash
python ~/.openclaw/plugin-skills/dota2-stats-skill/scripts/dota2_query.py <command> [args]
```

When already inside this skill directory, the shorter form is also valid:

```bash
python scripts/dota2_query.py <command> [args]
```

The script uses only the Python standard library, so no pip install is required. It needs network access to `https://api.opendota.com/api` and uses browser-like HTTP headers to reduce 403 risk.

## Command Selection

- Player name / 玩家名: use `search <name>` first, then `player <account_id>` and usually `recent <account_id>`.
- Steam64 ID / Dota 2 account ID / 玩家ID: pass it directly to player commands. The script auto-converts Steam64 IDs to 32-bit account IDs.
- Match ID / 比赛ID / 比赛详情: use `match <match_id>`.
- Recent matches / 最近比赛 / 近期战绩: use `recent <account_id>` for a quick view, or `matches <account_id> --limit N` for a filtered list.
- Win rate / 胜率 / 排位胜率: use `wl <account_id>` with filters such as `--days N`, `--hero_id N`, or ranked lobby `--lobby_type 7`.
- Hero usage / 常用英雄 / 英雄池: use `heroes <account_id>`.
- Hero counters / hero matchup / 英雄克制 / 对抗胜率: use `hero_matchups <hero_id>`.
- Top players for a hero / 绝活玩家 / 英雄排行榜: use `hero_rankings <hero_id>`.
- Pro scene / 职业比赛 / 职业选手 / 战队 / 联赛: use `pro_matches`, `pro_players`, `teams`, `team <team_id>`, or `leagues`.
- Live games / 实时比赛 / 正在进行: use `live`.
- Game constants / 常量 / 物品 / 模式 / 大厅 / 地区 / 版本: use `constants <resource>`.

## Commands (27 total)

### Player Commands
```bash
python scripts/dota2_query.py search <name>              # Search for a player (SLOW: 1-2 min)
python scripts/dota2_query.py player <account_id>         # Player info/rank/winrate
python scripts/dota2_query.py wl <id> [--days/--hero_id/--lobby_type]  # Win/loss stats
python scripts/dota2_query.py recent <id>                 # Recent ~20 matches
python scripts/dota2_query.py matches <id> [--limit/--hero_id/--days]  # Full match history
python scripts/dota2_query.py heroes <id> [--limit N]     # Hero usage stats
python scripts/dota2_query.py peers <id> [--limit N]      # Frequent teammates
python scripts/dota2_query.py totals <id> [filters]       # Career totals (kills/assists etc)
python scripts/dota2_query.py counts <id>                 # Categorized stats
python scripts/dota2_query.py rankings <id>               # Player hero rankings
python scripts/dota2_query.py ratings <id>                # Rank history
python scripts/dota2_query.py refresh <id>                # Refresh player data
```

### Match Commands
```bash
python scripts/dota2_query.py match <match_id>            # Single match details (10 players)
```

### Hero Commands
```bash
python scripts/dota2_query.py hero_list                   # All heroes list
python scripts/dota2_query.py hero_stats                  # Global hero stats
python scripts/dota2_query.py hero_matchups <hero_id>     # Hero matchup winrates
python scripts/dota2_query.py hero_rankings <hero_id>     # Hero leaderboard (Top players)
python scripts/dota2_query.py benchmarks <hero_id>        # Hero performance benchmarks
```

### Global / Pro Commands
```bash
python scripts/dota2_query.py pro_players                 # Pro players list
python scripts/dota2_query.py pro_matches [--limit N]     # Pro matches
python scripts/dota2_query.py public_matches [--min_rank] # Public matches
python scripts/dota2_query.py live                        # Live matches
python scripts/dota2_query.py teams [--limit N]           # Teams list
python scripts/dota2_query.py team <team_id>              # Team details+roster+matches
python scripts/dota2_query.py leagues                     # Leagues list
python scripts/dota2_query.py constants <resource>        # Game constants (heroes/items etc)
python scripts/dota2_query.py find_matches --teamA 1,2 --teamB 3,4  # Search by hero lineup
```

### Common Filters
- `--days N` — Last N days
- `--hero_id N` — Specific hero ID
- `--lobby_type N` — Lobby type (7=Ranked)
- `--game_mode N` — Game mode
- `--limit N` — Limit results
- `--lang zh|en` — Output language (default Chinese)

## Usage Flow

### When user provides a player name:
1. `search <name>` → Get account_id
2. `player <id>` → View basic info
3. `recent <id>` → View recent matches

### Steam ID:
*The tool automatically converts 64-bit Steam IDs to 32-bit Account IDs. You can pass either format.*

## Rank Tier

| Tier | English | 中文 |
|------|---------|------|
| 1 | Herald | 先锋 |
| 2 | Guardian | 卫士 |
| 3 | Crusader | 中军 |
| 4 | Archon | 统帅 |
| 5 | Legend | 传奇 |
| 6 | Ancient | 万古流芳 |
| 7 | Divine | 超凡入圣 |
| 8 | Immortal | 冠绝一世 |

## Notes
1. Uses only Python standard library - no pip install required
2. Requires network access to the OpenDota API
3. Players need to have "Public Match Data" enabled
4. Built-in Chinese names for 127 heroes
5. Select the output language based on the language used in the user's question, use `--lang en` for English, `--lang zh` for Chinese
6. **`search` command can be slow** because the OpenDota search endpoint may take a while. When invoking this command, remind the user that it may take some time. If the user already knows the player's Dota 2 account ID, suggest using `player <account_id>` directly for faster results
