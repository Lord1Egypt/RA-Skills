---
name: game-library
description: 跨平台游戏库查询工具（含中文名）。统一查询 Steam 和 Epic Games 游戏库，支持搜索、统计、推荐等功能，自动显示中文游戏名。当用户问游戏库相关问题时触发，包括"我有什么游戏"、"搜索XX游戏"、"没玩过的游戏推荐"、"游戏统计"、"Steam游戏"、"Epic游戏"、"跨平台游戏"等。触发词：游戏库、游戏统计、我的游戏、游戏推荐、game library、cross-platform games。
version: "1.0.0"
metadata:
  openclaw:
    emoji: "🎮"
    requires:
      bins: ["steam", "legendary"]
      env: ["STEAM_API_KEY"]
---

# Game Library - 跨平台游戏库查询（含中文名）

统一查询 Steam 和 Epic Games 游戏库，自动显示中文游戏名。

## 已配置平台

| 平台 | 用户 | CLI |
|------|------|-----|
| Steam | <your-steam-id> | `steam` |
| Epic | <your-epic-account> | `legendary` |

> 首次使用前，请将上述占位符替换为你自己的 Steam ID 和 Epic 账号名。
> Steam CLI 需要设置 `STEAM_API_KEY` 环境变量。
> Epic 平台使用 [legendary](https://github.com/derrod/legendary) CLI，需先 `pip install legendary-gl` 并登录。

## 核心脚本

```bash
bash {skill_dir}/scripts/game_query.sh <command> [options]
```

### 命令一览

| 命令 | 说明 |
|------|------|
| `stats` | 跨平台游戏库统计 |
| `list` | 列出所有平台游戏（含中文名） |
| `search <关键词>` | 跨平台搜索（支持中文名搜索） |
| `unplayed` | 列出未玩过的游戏 |
| `recommend` | 推荐高分未玩游戏 |
| `steam [opts]` | 直接调用 Steam CLI（透传参数） |
| `epic` | 列出 Epic 游戏库（含中文名） |
| `cn-update` | 更新中文名缓存（从 Steam API 批量获取） |
| `cn-update-xhh` | 从小黑盒补充中文名（无需 API Key） |
| `duplicates` | 查找跨平台重复游戏 |
| `help` | 显示帮助 |

### 中文名机制（双源）

中文名来自两个数据源，互补覆盖：

1. **Steam API**（`l=schinese` 参数） — 覆盖约 33% 的游戏
2. **小黑盒网页版**（`api.xiaoheihe.cn/game/share_game_detail`） — 无需 API Key，覆盖约 87% 的游戏

- 先运行 `cn-update`（Steam API），再运行 `cn-update-xhh`（小黑盒补充）
- 最终缓存到 `cn_names_cache.json`
- 游戏同时显示中文名和英文名，如：`黑神话：悟空（Black Myth: Wukong）`
- 无独立中文名的游戏只显示英文名
- 搜索同时匹配中文名和英文名
- 定期运行两个更新命令刷新缓存

### 中文名工具脚本

```bash
# 更新中文名缓存（Steam API，约 7-8 分钟）
python3 {skill_dir}/scripts/cn_names.py update

# 从小黑盒补充（无需 API Key，约 1 分钟）
python3 {skill_dir}/scripts/xhh_cn_names.py

# 查询单个游戏中文名
python3 {skill_dir}/scripts/cn_names.py lookup "Darkest Dungeon"

# 导出所有中英文映射
python3 {skill_dir}/scripts/cn_names.py export
```

### 示例

```bash
# 查看统计
bash {skill_dir}/scripts/game_query.sh stats

# 搜索跨平台（支持中文关键词）
bash {skill_dir}/scripts/game_query.sh search 悟空
bash {skill_dir}/scripts/game_query.sh search borderlands

# Steam 高级筛选（透传 steam CLI 参数）
bash {skill_dir}/scripts/game_query.sh steam --unplayed --tag "Roguelike" --min-reviews 7 --limit 10
```

## 直接使用 Steam CLI

Steam CLI 功能更丰富，需要精细筛选时直接使用：

```bash
steam library --unplayed --min-reviews 7 --deck-compat verified --limit 10
steam tags --json
steam genres --json
steam whoami
```

## 注意事项

- Epic 平台没有公开的游玩时长/评价 API，功能受限（仅能列出游戏库）
- 脚本自带 1 小时数据缓存，避免频繁 API 调用；需要刷新时删 `/tmp/game-library-cache/`
- 中文名缓存更新：`cn-update` 约 7-8 分钟（按游戏数 × 1.5s 限速），`cn-update-xhh` 约 1 分钟（0.3s/个），建议每周运行一次
- 小黑盒网页版不需要 API Key，直接爬取页面 title 标签获取中文名
- Legendary CLI 安装：`pip install legendary-gl`，然后 `legendary auth` 登录
