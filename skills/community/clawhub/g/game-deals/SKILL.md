---
name: game-deals
description: "获取 Steam 和 Epic Games 的限免游戏信息。触发条件：用户询问'今天有什么免费游戏'、'Steam 喜加一'、'Epic 免费游戏'、'限免游戏推送'等。支持查询当前免费游戏、即将结束的限免、以及设置定时推送。"
version: 1.0.0
author: testc0de
---

# Game Deals Skill

获取 Steam 和 Epic Games 平台的限免游戏信息。

## 触发条件

当用户说以下话时，使用此技能：
- "今天有什么免费游戏"
- "Steam 喜加一"
- "Epic 免费游戏"
- "限免游戏推送"
- "免费游戏推荐"
- "有什么游戏在免费送"

## 功能

### 1. 查询当前限免

**Steam 限免：**
```bash
# 获取 Steam 免费游戏（需要 Steam API Key）
curl -s "https://api.steampowered.com/ISteamApps/GetAppList/v2/" | jq '.applist.apps[] | select(.name | contains("Free"))'
```

实际使用：访问 Steam 商店免费游戏页面解析
```bash
curl -s "https://store.steampowered.com/genre/Free%20to%20Play/" -H "User-Agent: Mozilla/5.0" | grep -oP 'data-ds-appid="\d+"[^>]*>[^<]*<[^>]*>[^<]*' | head -10
```

**Epic 限免：**
```bash
# Epic Games Store 免费游戏 API
curl -s "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN" | jq '.'
```

### 2. 解析 Epic 响应

Epic API 返回结构：
```json
{
  "data": {
    "Catalog": {
      "searchStore": {
        "elements": [
          {
            "title": "游戏名称",
            "description": "游戏描述",
            "keyImages": [{"url": "封面图"}],
            "promotions": {
              "promotionalOffers": [{
                "startDate": "2024-01-01T00:00:00Z",
                "endDate": "2024-01-08T00:00:00Z"
              }]
            }
          }
        ]
      }
    }
  }
}
```

### 3. 推送设置（可选）

使用 OpenClaw cron 设置定时检查：
```bash
# 每天上午 10 点检查限免
openclaw cron add --name "game-deals-check" --schedule "0 10 * * *" --command "check-game-deals"
```

## 使用方法

### 手动查询

```bash
# 查询 Epic 当前限免
python3 skills/game-deals/scripts/epic_free.py

# 查询 Steam 限免
python3 skills/game-deals/scripts/steam_free.py

# 查询全部
python3 skills/game-deals/scripts/check_deals.py --all
```

### 输出格式

```
🎮 今日限免游戏

【Epic Games】
━━━━━━━━━━━━━━━━
🎯 游戏名: 《XXX》
💰 原价: ¥99
📅 截止: 2024-01-08 00:00
🔗 领取: https://store.epicgames.com/zh-CN/p/xxx

【Steam】
━━━━━━━━━━━━━━━━
🎯 游戏名: 《YYY》
💰 原价: ¥68 → 免费
📅 截止: 限时免费开玩
🔗 领取: https://store.steampowered.com/app/xxx
```

## 文件结构

```
skills/game-deals/
├── SKILL.md              # 本文件
├── scripts/
│   ├── epic_free.py      # Epic 限免查询
│   ├── steam_free.py      # Steam 限免查询
│   └── check_deals.py    # 统一入口
├── cache/                # 缓存目录
│   └── last_check.json   # 上次检查结果
└── config.json           # 配置（可选）
```

## 依赖

- Python 3
- requests
- jq (可选，用于命令行解析)

安装：
```bash
pip3 install requests
```

## 注意事项

1. Epic API 不需要 Key，但有频率限制
2. Steam 免费游戏页面需要解析 HTML，可能因页面结构变化而失效
3. 建议缓存结果，避免频繁请求
4. 部分限免可能有区域限制

## 未来扩展

- [ ] GOG 平台支持
- [ ] Humble Bundle 限免
- [ ] 邮件/消息推送
- [ ] 游戏评分和简介
- [ ] 历史限免记录
