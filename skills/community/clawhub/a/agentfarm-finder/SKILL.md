# agentfarm-finder

AI Agent 早期项目发现工具。监控 Twitter 上与 AI Agent、Crypto、DeFi 相关的新项目发布。

## 功能

- 搜索关键词：bot, agent, auto, openclaw, aiagent, 8004 + mint, farm, yield, puzzle
- 自动过滤噪音（GTA、游戏、新闻、主播撕逼等）
- 输出原始数据 + 项目精选
- 每天 16:00 自动运行

## 使用方法

```bash
# 手动运行
bash ~/.openclaw/workspace/skills/agentfarm-finder/scripts/run.sh

# 或使用 cron
# 0 16 * * * bash /Users/moer/.openclaw/workspace/skills/agentfarm-finder/scripts/run.sh
```

## 输出文件

| 文件 | 内容 |
|------|------|
| `output/results_YYYY-MM-DD.csv` | 原始数据 |
| `output/results_YYYY-MM-DD_projects.csv` | 项目精选 |

## 配置

修改 `scripts/run.sh` 中的参数：
- `HOURS=24` - 时间范围
- `COUNT=30` - 每词搜索数量

## 排除列表

搜索排除：nvidia, meta, tesla, slowmist 等
过滤排除：grok, nft, 闲聊用户等
