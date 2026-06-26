# Game Deals Skill for OpenClaw

获取 Epic Games 和 Steam 限免/免费游戏信息。

## 安装

### 通过 ClawHub（推荐）
```bash
clawhub install game-deals
```

### 手动安装
```bash
git clone https://github.com/你的用户名/game-deals.git ./skills/game-deals
```

## 使用

```bash
# 查询所有平台
python3 skills/game-deals/scripts/check_deals.py

# 单独查询 Epic
python3 skills/game-deals/scripts/epic_free.py

# 单独查询 Steam
python3 skills/game-deals/scripts/steam_free.py
```

## 触发词

在 OpenClaw 中，说以下话会自动触发：
- "今天有什么免费游戏"
- "Steam 喜加一"
- "Epic 免费游戏"
- "限免游戏"

## 依赖

- Python 3
- requests

```bash
pip3 install requests
```

## 作者

帕西法尔
