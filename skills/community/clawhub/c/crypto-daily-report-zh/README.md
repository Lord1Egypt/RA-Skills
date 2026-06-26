# Crypto Daily Report Skill

一个用于生成和发送加密货币日报的 OpenClaw Skill。

## 功能

- 📊 **大盘速览** - BTC、ETH、SOL、BNB 实时价格
- 😨 **市场情绪** - 恐慌贪婪指数及解读
- 💥 **爆仓数据** - 24小时全网爆仓统计
- 📅 **重要日历** - 代币解锁、美联储决议、经济数据
- 🔥 **热点新闻** - Cointelegraph、TokenInsight 聚合

## 安装

1. 克隆仓库到 OpenClaw skills 目录：
```bash
cd ~/.openclaw/skills
git clone https://github.com/RenYuKe-CN/crypto-daily-report.git
```

2. 确保已安装依赖：
- `onchainos` CLI 工具
- `curl`
- `web_fetch` 和 `web_search` 工具（OpenClaw 内置）

## 使用

### 手动生成日报

对 AI 说：
- "币圈日报"
- "crypto daily"
- "跑个日报"

### 设置定时推送

```bash
# 每天早上8点（UTC+8）推送到指定群组
./scripts/setup-cron.sh -1002009088194
```

或直接问 AI：
> "每天早上8点发送币圈日报到 -1002009088194"

## 数据源

| 数据 | 来源 |
|------|------|
| ETH/SOL/BNB | onchainos CLI |
| BTC | Web Search |
| 恐慌贪婪指数 | alternative.me API |
| 爆仓数据 | CoinGlass / Gate |
| 新闻 | Cointelegraph RSS, TokenInsight RSS |
| 日历 | Incrypted Calendar |

## 报告格式

```
📰 币圈日报
2025年3月12日 星期四

💰 大盘速览
BTC: $69,469
ETH: $2,039.68
SOL: $85.79
BNB: $645.90

😨 市场情绪
恐慌贪婪指数: 18 🔴 极度恐惧
昨天: 15 | 上周: 22 | 上月: 9
💡 解读: 市场情绪持续低迷...

💥 爆仓数据 (24h)
数据来源: CoinGlass / Gate
总爆仓金额: ~$131M
...
```

## 目录结构

```
crypto-daily-report/
├── SKILL.md                    # 技能主文档
├── README.md                   # 本文件
├── scripts/
│   ├── generate-report.sh      # 生成报告
│   ├── setup-cron.sh           # 设置定时任务
│   └── test-send.sh            # 测试发送
├── references/
│   └── data-sources.md         # 数据源文档
└── assets/
    └── report-template.txt     # 报告模板
```

## 触发词

- 币圈日报
- crypto daily
- daily report
- market update
- 跑个日报

## License

MIT
