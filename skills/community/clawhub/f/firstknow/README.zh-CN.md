**[English](README.md)** | 中文

# FirstKnow

**你持有的股票出事了，我比你先知道，而且告诉你这对你意味着什么。**

AI 驱动的持仓情报 agent，实时监控你持有的股票/加密货币/ETF 的突发新闻、SEC 文件、价格异动和分析师动态，通过 Telegram 推送个性化提醒。全天候。支持中文。

## 你会收到什么

新闻一出，几分钟内收到 Telegram 提醒：

```
🔔 摩根士丹利维持英伟达"增持"评级，上调目标价至 $1,100

📌 你的持仓: NVDA (占组合20%)
📈 分析师评级 | NVDA +1.8% | $892

📰 摩根士丹利分析师 Joseph Moore 维持英伟达 (NASDAQ:NVDA)
"增持"评级，将目标价从 $960 上调至 $1,100，理由是 AI
数据中心需求持续加速。

🔗 https://finnhub.io/api/news?id=12345

💬 回复 "深度" 获取AI深度分析
```

回复 "深度" 获取完整的 AI 持仓分析：

```
📊 NVDA 分析师上调目标价 — 深度分析

核心逻辑：
这是近两个月第 5 家主要机构上调目标价。摩根士丹利新目标
$1,100 意味着较当前价格有 23% 上行空间...

历史对比：
上次同一周内 3 家以上机构同时上调目标价（2026年1月），
NVDA 在随后 3 周内上涨了 12%...

压力测试：
• 最好情景 (30%): AI 资本开支周期延续至 2027 → $1,200+
• 基准情景 (50%): 维持当前增长轨迹 → $950-1,050 区间
• 最坏情景 (20%): 需求透支担忧 → $780-850

行动建议：
• 维持当前 20% 仓位 — 暂不操作
• 如果跌破 $840: 加仓 3%（仓位提升至 23%）
• 设置 $810 移动止损以防下行风险

📌 关注: NVDA Q1 财报 5月28日，AMD 财报 5月6日
```

## 安装

### OpenClaw（通过 ClawHub）

```bash
clawhub install firstknow
```

然后在 OpenClaw 的任意频道（Telegram、飞书、Discord 等）发送：
"设置 firstknow"

### OpenClaw（手动安装）

```bash
git clone https://github.com/cdpiano/firstknow.git ~/.claude/skills/firstknow
cd ~/.claude/skills/firstknow/scripts && npm install
```

### Claude Code

```bash
git clone https://github.com/cdpiano/firstknow.git ~/.claude/skills/firstknow
cd ~/.claude/skills/firstknow/scripts && npm install
```

然后在 Claude Code 中说 "设置 firstknow" 或输入 `/firstknow`。

### 更新

```bash
cd ~/.claude/skills/firstknow && git pull
```

## 快速开始

安装后，直接告诉 agent "设置 firstknow"。全程对话引导，不需要编辑任何配置文件。

Agent 会询问：
- 你的持仓（如 "NVDA 25%, BTC 20%, TSLA 15%"）
- 语言偏好（English / 中文 / 双语）
- 推送级别（全部 / 仅重要 / 每日摘要）
- 免打扰时段
- Telegram bot 设置（逐步引导）

**就这样。** 5 分钟内开始收到提醒。

## 新闻来源

| 来源 | 覆盖内容 |
|------|---------|
| **Finnhub** | 股票新闻（路透社、Benzinga、MarketWatch） |
| **SEC EDGAR** | 监管文件（10-K、10-Q、8-K、内部人交易、activist 持仓） |
| **Yahoo Finance** | 价格异动（日涨跌幅 > 5%） |
| **CoinGecko** | 加密货币价格（BTC、ETH、SOL 等） |

所有数据抓取在中心化后端完成。基础提醒不需要你提供任何 API key。

## 深度分析

回复 "深度" 获取 AI 深度分析，包括：

- 标题背后真正发生了什么
- 历史对比（类似事件，股价如何反应）
- 持仓压力测试（最好/基准/最坏情景）
- 具体行动建议（"如果跌到 $780 以下，加仓 3%"）
- 关键日期和指标

深度分析使用 Claude Sonnet，需要你自己的 Anthropic API key（设置时会询问）。

## 修改设置

所有设置都可以通过对话修改：

- "切换中文" / "Switch to English"
- "只推送重大事件"
- "免打扰时间改为晚 11 点到早 7 点"
- "我卖了 TSLA，买了 GOOGL 15%"
- "显示设置"
- "显示持仓"

## 防刷屏

- 每个股票每天最多 3 条提醒
- 同一股票两条提醒间隔至少 30 分钟
- 免打扰时段（默认凌晨 12 点到早 8 点）
- 提醒级别可选（全部 / 仅重大 / 每日摘要）

## 隐私

- 你的持仓存储在后端用于匹配新闻事件，不与第三方共享
- 新闻 API 只接收股票代码，不涉及个人信息
- 随时可以删除所有数据：告诉 agent "删除我的账户"

## 许可证

MIT
