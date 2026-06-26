---
name: okx-trading-analyst
description: OKX加密货币技术分析工具 — 使用欧易API获取实时行情数据，计算技术指标（MA、MACD、RSI、布林带等），生成交易信号。当用户需要加密货币行情分析、技术指标计算、或交易信号时触发此skill。
---

# OKX Trading Analyst

使用欧易OKX API进行加密货币技术分析和交易信号生成。

## API配置

你需要在 OKX 交易所申请 API Key（只需要**读取权限**即可），然后在项目根目录创建 `.env` 文件：

```env
OKX_API_KEY=your-api-key-here
OKX_API_SECRET=your-api-secret-here
```

OKX 公开接口免费使用，不需要签名认证，只需要 API Key 即可。

**权限要求**: 仅需要行情读取权限，不要给交易权限。

## 功能

- **实时数据**: 获取OKX K线数据和最新行情
- **技术指标**: MA、MACD、RSI、布林带、ATR
- **交易信号**: 综合评分系统，生成买卖建议
- **多周期**: 支持1m/5m/15m/30m/1H/4H/1D等周期

## 使用方法

### 命令行

```bash
# 分析BTC 4小时周期
python3 scripts/okx_analyst.py BTC-USDT

# 分析ETH 1小时周期
python3 scripts/okx_analyst.py ETH-USDT --timeframe 1H

# 只输出交易信号
python3 scripts/okx_analyst.py BTC-USDT --signal-only
```

### Python调用

```python
from scripts.okx_analyst import OKXAnalyzer

analyzer = OKXAnalyzer()

# 获取数据并分析
df = analyzer.get_klines("BTC-USDT", bar="4H", limit=200)
df = analyzer.calculate_indicators(df)
signals = analyzer.generate_signals(df)

print(f"信号: {signals['recommendation']['signal']}")
print(f"强度: {signals['strength']}/+10")
```

## 输出示例

```
============================================================
📊 BTC-USDT 技术分析报告 (4H周期)
============================================================

【价格信息】
当前价格: $67,423.50

【交易信号】
🟢 温和看涨 (强度: +3/+10)
建议操作: 轻仓试多
止损: $65,423 (-3%)
目标: $70,795 (+5%)

信号详情:
✅ [趋势] MA20 > MA60，中长期趋势向上
✅ [趋势] 价格站上MA20短期均线
✅ [动量] MACD金叉，动量转强
ℹ️ [动量] RSI中性 (58.32)
============================================================
```

## 信号说明

| 强度 | 信号 | 建议 |
|:---:|:---:|:---|
| +5以上 | 🟢 强烈看涨 | 逢低做多 |
| +2~+4 | 🟡 温和看涨 | 轻仓试多 |
| -1~+1 | ⚪ 中性 | 观望 |
| -2~-4 | 🟠 温和看跌 | 轻仓试空 |
| -5以下 | 🔴 强烈看跌 | 逢高做空 |

## 风险提示

⚠️ 技术分析仅供参考，不构成投资建议。加密货币市场波动剧烈，请严格设置止损。

## 依赖

```bash
pip install requests pandas numpy
```

## 文件结构

```
okx-trading-analyst/
├── SKILL.md
└── scripts/
    └── okx_analyst.py
```
