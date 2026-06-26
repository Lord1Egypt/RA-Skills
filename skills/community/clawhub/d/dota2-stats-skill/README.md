<p align="right"><b><a href="./README_EN.md">English</a></b> | 中文</p>

# Dota 2 数据查询 - Agent Skill

基于 [OpenDota API](https://docs.opendota.com/) 的 Dota 2 / 刀塔2 数据查询技能，面向常用的玩家战绩、玩家ID、Steam ID、比赛ID、英雄数据、英雄克制、职业赛事、战队、联赛、实时比赛、段位和胜率查询场景，供 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)/[OpenClaw](https://openclaw.ai) 使用。

## ✨ 功能 (27 个命令)

### 🧑 玩家
| 命令 | 说明 |
|------|------|
| `search <name>` | 搜索玩家 |
| `player <id>` | 段位、MMR、胜率 |
| `wl <id>` | 胜负统计（支持筛选） |
| `recent <id>` | 最近 ~20 场 |
| `matches <id>` | 完整历史 |
| `heroes <id>` | 英雄统计 |
| `peers <id>` | 一起玩的人 |
| `totals <id>` | 生涯累计数据 |
| `counts <id>` | 分类统计 |
| `rankings <id>` | 英雄排名百分位 |
| `ratings <id>` | 段位变化历史 |
| `refresh <id>` | 刷新数据 |

### ⚔️ 比赛
| 命令 | 说明 |
|------|------|
| `match <match_id>` | 10 人完整数据 |

### 🦸 英雄
| 命令 | 说明 |
|------|------|
| `hero_list` | 英雄列表 |
| `hero_stats` | 全局统计 |
| `hero_matchups <hero_id>` | 对抗胜率 |
| `hero_rankings <hero_id>` | Top 玩家 |
| `benchmarks <hero_id>` | 表现基准 |

### 🌍 全局
| 命令 | 说明 |
|------|------|
| `pro_players` | 职业选手 |
| `pro_matches` | 职业比赛 |
| `public_matches` | 公开比赛 |
| `live` | 实时比赛 |
| `teams` | 战队列表 |
| `team <team_id>` | 战队详情+阵容+赛果 |
| `leagues` | 联赛列表 |
| `constants <resource>` | 游戏常量 |
| `find_matches` | 按英雄阵容搜索 |

## 📁 项目结构

```
dota2-stats-skill/
├── SKILL.md                  # Claude Code/OpenClaw 技能描述
├── README.md                 # 本文件
├── README_EN.md              # 英文版
├── scripts/
│   └── dota2_query.py        # Python 查询脚本（27 个常用命令）
└── data/
    ├── translations.json     # 中英双语翻译字典 (仅含界面文本)
    ├── dota_constants.json   # 游戏静态常量映射 (段位、模式、大厅等)
    ├── hero_zh_names.json    # 英雄中文名映射 (127 个)
    └── hero_en_names.json    # (自动生成) 英雄英文名本地缓存
```

## 🚀 使用

### 在 Claude Code 中

将目录放在 `~/.claude/skills/dota2-stats-skill/`，然后直接用自然语言提问：

```
> 查一下 <id> 的 Dota 2 战绩
> 看看影魔对抗谁胜率最低
> 最近有什么职业比赛
```

也可以直接运行脚本：

```bash
python ~/.claude/skills/dota2-stats-skill/scripts/dota2_query.py <command> [args]
```

### 在OpenClaw中

将目录放在 `~/.openclaw/plugin-skills/dota2-stats-skill/`，然后直接用自然语言提问：

```
> 查一下 <id> 的 Dota 2 战绩
> 看看影魔对抗谁胜率最低
> 最近有什么职业比赛
```

也可以直接运行脚本：

```bash
python ~/.openclaw/plugin-skills/dota2-stats-skill/scripts/dota2_query.py <command> [args]
```

### 命令行独立使用

以下短路径适用于当前目录已经在本 skill 根目录时：

```bash
python scripts/dota2_query.py search Miracle
python scripts/dota2_query.py player 105248644
python scripts/dota2_query.py recent 105248644
python scripts/dota2_query.py hero_matchups 11          # 影魔对抗数据
python scripts/dota2_query.py hero_rankings 74          # 祈求者 Top 玩家
python scripts/dota2_query.py pro_matches --limit 10
python scripts/dota2_query.py live
python scripts/dota2_query.py team 8291895              # 查战队
python scripts/dota2_query.py constants items           # 物品数据
```

### 筛选参数

```bash
python scripts/dota2_query.py wl 105248644 --days 30 --lobby_type 7    # 近30天排位
python scripts/dota2_query.py matches 105248644 --hero_id 11 --limit 5 # 影魔最近5场
python scripts/dota2_query.py --lang en player 105248644                # English output
```

## 🔧 技术

- **API**: OpenDota API v31（免费，无需 Key）
- **依赖**: 仅 Python 3.6+ 标准库
- **网络**: 需要能访问 `https://api.opendota.com/api`
- **Headers**: 使用浏览器风格 HTTP Headers，降低 403 风险
- **本地化**: 内置 127 个英雄中文名 + 段位/模式中英双语

## 📄 License

MIT
