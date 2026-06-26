<p align="right">English | <b><a href="./README.md">中文</a></b></p>

# Dota 2 Stats Query - Agent Skill

A Dota 2 / DOTA2 data query skill based on [OpenDota API](https://docs.opendota.com/), focused on common player stats, Steam ID/account ID, match ID, hero data, hero matchups, pro-scene, team, league, live game, rank and win-rate workflows for use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)/[OpenClaw](https://openclaw.ai).

## ✨ Features (27 commands)

### 🧑 Player
| Command | Description |
|---------|-------------|
| `search <name>` | Search for a player |
| `player <id>` | Rank, MMR, winrate |
| `wl <id>` | Win/loss stats (with filters) |
| `recent <id>` | Recent ~20 matches |
| `matches <id>` | Full history |
| `heroes <id>` | Hero statistics |
| `peers <id>` | Frequent teammates |
| `totals <id>` | Career cumulative data |
| `counts <id>` | Categorized stats |
| `rankings <id>` | Hero ranking percentiles |
| `ratings <id>` | Rank change history |
| `refresh <id>` | Refresh data |

### ⚔️ Match
| Command | Description |
|---------|-------------|
| `match <match_id>` | 10-player complete data |

### 🦸 Hero
| Command | Description |
|---------|-------------|
| `hero_list` | Heroes list |
| `hero_stats` | Global statistics |
| `hero_matchups <hero_id>` | Matchup winrates |
| `hero_rankings <hero_id>` | Top players |
| `benchmarks <hero_id>` | Performance benchmarks |

### 🌍 Global
| Command | Description |
|---------|-------------|
| `pro_players` | Pro players |
| `pro_matches` | Pro matches |
| `public_matches` | Public matches |
| `live` | Live matches |
| `teams` | Teams list |
| `team <team_id>` | Team details+roster+results |
| `leagues` | Leagues list |
| `constants <resource>` | Game constants |
| `find_matches` | Search by hero lineup |

## 📁 Project Structure

```
dota2-stats-skill/
├── SKILL.md                  # Claude Code/OpenClaw skill description
├── README.md                 # Chinese version
├── README_EN.md              # This file (English version)
├── scripts/
│   └── dota2_query.py        # Python query script (27 common commands)
└── data/
    ├── translations.json     # Chinese-English bilingual translation dictionary (UI text)
    ├── dota_constants.json   # Game static constants mapping (ranks, modes, lobbies, etc.)
    ├── hero_zh_names.json    # Hero Chinese name mapping (127 heroes)
    └── hero_en_names.json    # (Auto-generated) Hero English names cache
```

## 🚀 Usage

### In Claude Code

Place the directory in `~/.claude/skills/dota2-stats-skill/`, then ask questions in natural language:

```
> Check <id> Dota 2 stats
> Show Shadow Fiend's worst matchup winrates
> What pro matches are happening recently
```

You can also run the script directly:

```bash
python ~/.claude/skills/dota2-stats-skill/scripts/dota2_query.py <command> [args]
```

### In OpenClaw

Place the directory in `~/.openclaw/plugin-skills/dota2-stats-skill/`, then ask questions in natural language:

```
> Check <id> Dota 2 stats
> Show Shadow Fiend's worst matchup winrates
> What pro matches are happening recently
```

You can also run the script directly:

```bash
python ~/.openclaw/plugin-skills/dota2-stats-skill/scripts/dota2_query.py <command> [args]
```

### Command Line Standalone

The shorter path below assumes the current directory is this skill root:

```bash
python scripts/dota2_query.py search Miracle
python scripts/dota2_query.py player 105248644
python scripts/dota2_query.py recent 105248644
python scripts/dota2_query.py hero_matchups 11          # Shadow Fiend matchups
python scripts/dota2_query.py hero_rankings 74          # Invoker top players
python scripts/dota2_query.py pro_matches --limit 10
python scripts/dota2_query.py live
python scripts/dota2_query.py team 8291895              # Team info
python scripts/dota2_query.py constants items           # Items data
```

### Filter Parameters

```bash
python scripts/dota2_query.py wl 105248644 --days 30 --lobby_type 7    # Last 30 days ranked
python scripts/dota2_query.py matches 105248644 --hero_id 11 --limit 5 # Shadow Fiend last 5
python scripts/dota2_query.py --lang en player 105248644                # English output
```

## 🔧 Technical

- **API**: OpenDota API v31 (free, no key required)
- **Dependencies**: Python 3.6+ standard library only
- **Network**: Requires access to `https://api.opendota.com/api`
- **Headers**: Uses browser-like HTTP headers to reduce 403 risk
- **Localization**: Built-in 127 hero Chinese names + rank/mode bilingual

## 📄 License

MIT
