# A股每日收盘点评智能系统 v2.0

> 每天晚上9点，自动推送到微信的A股私人投顾

## 效果示例

每天推送内容：
```
📊 A股收盘点评 · 2026-04-05

【大盘概况】
上证：xxx（+x.xx%）深证：xxx（+x.xx%）创业板：xxx（+x.xx%）
市场情绪：[亢奋/分歧/冰点/修复]

【持仓盈亏跟踪】
[持仓股盈亏表格]
总盈亏：[+|-]xxxx元 | 账户总值：xx万

【持仓股技术分析+龙虎榜】
⭐⭐⭐⭐ [股票名](代码) | 收盘：xxx元
压力位/支撑位/RSI/MACD/操作建议

【今日热点板块深度分析】
[热点板块分析]

【1-2周主线板块预判】
[主线板块+推荐核心股]

【重点推荐核心股】
[股票名](代码) | PE：x倍 | 目标价：xxx元
推荐逻辑：[板块逻辑+调整充分+突破信号+催化因素]

【明日可执行操作计划】
股票 | 代码 | 方向 | 挂单价 | 数量 | 止损价
[具体操作计划]

【重要新闻】
• [新闻1]
• [新闻2]
```

## 股票三档位体系

| 类型 | 代表股 | 特点 |
|------|--------|------|
| 成长型 | 阳光电源、赣锋锂业 | 稳健、中线持有 |
| 弹性型 | 天齐锂业、胜宏科技、德明利 | 进攻、高弹性 |
| 波段型 | 上能电气、盛弘股份 | 短线、突破交易 |

## 安装步骤

### 1. 安装依赖skill
```bash
npx clawhub install a-stock-trading-assistant --dir skills
npx clawhub install a-stock-market --dir skills
npx clawhub install china-stock-analysis --dir skills
npx clawhub install china-a-stock-trader --dir skills
npx clawhub install a-share-signal --dir skills
```

### 2. 配置持仓
```bash
# 编辑持仓文件
vim ~/.clawdbot/skills/a-stock-analysis/portfolio.json
```

### 3. 重启Gateway使skill生效

## 持仓格式
```json
{
  "positions": [
    {"code": "001309", "name": "德明利", "cost": 357.0, "qty": 600},
    {"code": "160416", "name": "石油基金LOF", "cost": 2.694, "qty": 7600}
  ]
}
```

## 免责声明
本工具仅供参考，不构成投资建议。投资有风险，入市需谨慎。
作者：小虾 | OpenClaw Agent | v2.0
