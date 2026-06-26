---
name: a-share-analysis
description: A股全面分析工具，支持实时行情、技术分析、基本面分析、情绪分析，生成美观的Markdown分析报告。Use when user asks for: A股股票分析、市场行情查询、技术指标分析、财务数据获取、投资建议、龙虎榜数据、北向资金流向、综合投资报告等A股相关分析需求。
---

# A股分析技能

## 功能概述

本技能提供全方位的A股分析能力，包括：

- 📊 **实时行情** - 指数、个股实时价格、涨跌幅、成交量
- 🔧 **技术分析** - MA均线、MACD、RSI、成交量分析、趋势判断
- 📉 **基本面分析** - 财务报表、估值指标、业绩分析
- 💡 **情绪分析** - 北向资金、市场情绪、龙虎榜
- 📝 **综合报告** - 美观的Markdown格式分析报告

## 快速开始

### 基本使用流程

1. **收集数据** - 使用 `fetch_realtime_data.py` 获取实时行情
2. **技术分析** - 使用 `fetch_technical_indicators.py` 分析技术指标
3. **基本面分析** - 使用 `fetch_fundamental_data.py` 获取财务数据
4. **情绪分析** - 使用 `fetch_sentiment_data.py` 分析市场情绪
5. **生成报告** - 使用 `generate_report.py` 生成美观的分析报告

### 示例：分析贵州茅台

```python
# 1. 获取实时行情
from scripts.fetch_realtime_data import AShareRealTimeFetcher
fetcher = AShareRealTimeFetcher()
data = fetcher.fetch_stock_data("600519")

# 2. 技术分析
from scripts.fetch_technical_indicators import AShareTechnicalAnalyzer
analyzer = AShareTechnicalAnalyzer()
technical = analyzer.analyze_technical_indicators("0.600519")

# 3. 基本面分析
from scripts.fetch_fundamental_data import AShareFundamentalFetcher
fund_fetcher = AShareFundamentalFetcher()
fundamental = fund_fetcher.fetch_financial_report("600519")

# 4. 生成报告
from scripts.generate_report import AShareReportGenerator
generator = AShareReportGenerator()
report = generator.generate_markdown_report({
    "stocks": {
        "600519": {
            "name": "贵州茅台",
            **data,
            "technical": technical,
            "fundamental": fundamental
        }
    }
})
print(report)
```

## 主要功能

### 1. 实时行情查询

#### 获取指数行情
```python
from scripts.fetch_realtime_data import AShareRealTimeFetcher

fetcher = AShareRealTimeFetcher()

# 获取单个指数
sh_index = fetcher.fetch_index_data("sh000001")  # 上证指数
sz_index = fetcher.fetch_index_data("sz399001")  # 深证成指

# 批量获取指数
indices = fetcher.fetch_multiple_indices([
    "sh000001",  # 上证指数
    "sz399001",  # 深证成指
    "sz399006",  # 创业板指
    "sz399005",  # 科创50
])
```

#### 获取个股行情
```python
# 获取单个股票
stock_data = fetcher.fetch_stock_data("600519")  # 贵州茅台

# 批量获取股票
stocks_data = fetcher.fetch_multiple_stocks([
    "600519",  # 贵州茅台
    "000858",  # 五粮液
    "300750",  # 宁德时代
])
```

#### 返回数据结构
```python
{
    "code": "600519",
    "name": "贵州茅台",
    "price": 1800.50,           # 当前价格
    "change": 8.50,             # 涨跌额
    "change_percent": 0.47,     # 涨跌幅 (%)
    "volume": "12.5万",         # 成交量
    "amount": "22.5亿",         # 成交额
    "high": 1810.00,            # 最高价
    "low": 1790.00,             # 最低价
    "open": 1792.00,            # 开盘价
    "pre_close": 1792.00,       # 昨收价
    "time": "2026-02-27 14:30:00"  # 更新时间
}
```

### 2. 技术指标分析

#### 均线分析
```python
from scripts.fetch_technical_indicators import AShareTechnicalAnalyzer

analyzer = AShareTechnicalAnalyzer()

# 获取技术指标
technical = analyzer.analyze_technical_indicators("0.600519")
```

#### 返回数据结构
```python
{
    "code": "0.600519",
    "name": "贵州茅台",
    "current_price": 1800.50,
    "ma": {
        "5": 1795.23,  # MA5
        "10": 1788.45, # MA10
        "20": 1775.67, # MA20 (中期趋势)
        "60": 1750.89  # MA60 (长期趋势)
    },
    "macd": {
        "dif": 5.23,   # DIF
        "dea": 3.45,   # DEA
        "macd": 3.56,  # MACD柱
        "signal": "bullish"  # 看多/看空信号
    },
    "rsi": 65.32,      # RSI值
    "volume_ratio": 1.85,  # 成交量比
    "trend": "bullish",    # 趋势: bullish/bearish/neutral
    "support": 1780.00,    # 支撑位
    "resistance": 1830.00  # 阻力位
}
```

#### 技术信号解读

**均线排列**:
- MA5 > MA10 > MA20 > MA60: 多头排列 (强势)
- MA5 < MA10 < MA20 < MA60: 空头排列 (弱势)
- 其他: 震荡整理

**MACD信号**:
- `bullish`: DIF > DEA 且金叉，看多信号
- `bearish`: DIF < DEA 且死叉，看空信号

**RSI信号**:
- RSI > 70: 超买区域，警惕回调
- RSI < 30: 超卖区域，可能反弹
- 30-70: 正常区间

### 3. 基本面分析

#### 财务数据查询
```python
from scripts.fetch_fundamental_data import AShareFundamentalFetcher

fund_fetcher = AShareFundamentalFetcher()

# 获取财务报表
financial = fund_fetcher.fetch_financial_report("600519", "20231231")
```

#### 返回数据结构
```python
{
    "code": "600519",
    "name": "贵州茅台",
    "report_date": "20231231",
    "total_revenue": 1234567890,    # 营业总收入
    "operating_revenue": 1234567890, # 营业收入
    "net_profit": 617283945,        # 净利润
    "total_profit": 617283945,      # 利润总额
    "total_revenue_growth": 12.34,  # 营收同比增长
    "net_profit_growth": 15.67,     # 净利润同比增长
    "roe": 32.56,                   # ROE (%)
    "debt_to_asset": 20.15,         # 资产负债率 (%)
    "gross_margin": 91.23,          # 毛利率 (%)
    "net_margin": 50.00,            # 净利率 (%)
    "return_on_asset": 25.67,       # ROA (%)
    "current_ratio": 3.45,          # 流动比率
    "quick_ratio": 2.34,            # 速动比率
    "psr": 4.56,                    # 市销率
    "pe_ttm": 28.56,                # 市盈率TTM
    "pb": 8.23,                     # 市净率
    "market_cap": 2256789000000,    # 总市值
    "circulating_market_cap": 2256789000000  # 流通市值
}
```

#### 估值指标计算
```python
# 计算估值指标（需要传入当前股价）
valuation = fund_fetcher.calculate_valuation_metrics("600519", 1800.50)
```

#### 返回数据结构
```python
{
    "code": "600519",
    "name": "贵州茅台",
    "current_price": 1800.50,
    "market_cap": 2256789000000,
    "pe": 28.56,      # PE = 净利润 / 股价
    "pb": 8.23,       # PB = 市值 / 总资产
    "ps": 4.56,       # PS = 市值 / 营收
    "roe": 32.56,
    "net_margin": 50.00
}
```

### 4. 情绪分析

#### 市场情绪查询
```python
from scripts.fetch_sentiment_data import AShareSentimentAnalyzer

sentiment_analyzer = AShareSentimentAnalyzer()

# 获取情绪分析
sentiment = sentiment_analyzer.analyze_sentiment_summary()
```

#### 返回数据结构
```python
{
    "date": "2026-02-27",
    "northbound": {
        "stock_count": 3567,
        "total_inflow": 45.67,     # 总成交额 (亿元)
        "net_inflow": 23.45,       # 净流入 (亿元)
        "avg_net_inflow": 0.0066,  # 平均净流入 (亿元/只)
        "signal": "强势流入"       # 信号: 强势流入/小幅流入/小幅流出/强势流出
    },
    "market_sentiment": {
        "bullish_ratio": 45.23,    # 看多比例
        "bearish_ratio": 30.45,    # 看空比例
        "neutral_ratio": 24.32,    # 观望比例
        "signal": "NEUTRAL"        # bullish/bearish/neutral
    },
    "l2h_list": [
        {
            "code": "300750",
            "name": "宁德时代",
            "change_percent": 10.01,
            "limit_type": "首次上榜",
            "net_amount": 12300000,  # 净买入 (元)
            "buy_amount": 25000000,
            "sell_amount": 12700000
        }
    ]
}
```

### 5. 综合报告生成

#### 生成Markdown报告
```python
from scripts.generate_report import AShareReportGenerator

generator = AShareReportGenerator()

# 生成报告
report = generator.generate_markdown_report(
    analysis_data={
        "summary": "今日A股市场震荡调整...",
        "indices": {...},
        "stocks": {
            "600519": {
                "name": "贵州茅台",
                **stock_data,
                "technical": technical_data,
                "fundamental": fundamental_data
            }
        },
        "sentiment": sentiment_data,
        "recommendations": {
            "indices": {...},
            "stocks": {...},
            "risk_level": "中等风险"
        }
    },
    report_title="贵州茅台深度分析报告"
)

print(report)
```

#### 保存报告
```python
# 保存到文件
filepath = generator.save_report(report, "a-share-analysis-report.md")
print(f"报告已保存至: {filepath}")
```

#### 报告包含内容
- 📊 市场摘要
- 📈 主要指数行情（表格形式）
- 📋 个股分析（包含实时行情、技术指标、基本面）
- 🔧 技术指标分析（均线、MACD、RSI、成交量）
- 📉 基本面分析（财务指标、估值指标）
- 💡 市场情绪分析（北向资金、市场情绪、龙虎榜）
- 💼 投资建议
- ⚠️ 风险提示

## 指数代码对照表

### 主要指数
| 指数名称 | 代码 | 说明 |
|---------|------|------|
| 上证指数 | sh000001 | 上海主板综合指数 |
| 深证成指 | sz399001 | 深圳主板综合指数 |
| 创业板指 | sz399006 | 创业板综合指数 |
| 科创50 | sz399005 | 科创板50指数 |
| 沪深300 | sh000300 | 沪深300指数 |
| 中证500 | sz399905 | 中证500指数 |
| 中证1000 | sz399910 | 中证1000指数 |

### 个股代码格式
- **上海市场**: `0.600519` (贵州茅台)
- **深圳市场**: `1.000858` (五粮液)

## 分析建议框架

### 个股分析建议

1. **技术面**:
   - 均线排列判断趋势
   - MACD判断买卖信号
   - RSI判断超买超卖
   - 成交量分析资金动向

2. **基本面**:
   - 营收和利润增长情况
   - ROE、毛利率、净利率等盈利能力指标
   - 资产负债率等财务健康度
   - 估值指标（PE、PB、PS）

3. **情绪面**:
   - 北向资金流向
   - 市场整体情绪
   - 龙虎榜资金动向

4. **综合判断**:
   - 技术面+基本面+情绪面综合分析
   - 给出具体投资建议（买入/持有/卖出）
   - 提供支撑位和阻力位参考

### 指数分析建议

1. **趋势判断**:
   - 均线排列
   - MACD信号
   - 成交量变化

2. **市场情绪**:
   - 北向资金流向
   - 市场情绪指标
   - 龙虎榜活跃度

3. **投资建议**:
   - 看多/看空/观望
   - 操作策略建议

## 注意事项

1. **数据延迟**: 实时行情数据可能有1-2秒延迟
2. **API限制**: 频繁请求可能被限流，建议适当间隔
3. **历史数据**: 财务数据为历史数据，不是实时更新
4. **投资建议**: 报告仅供参考，不构成投资建议，投资有风险
5. **数据准确性**: 数据来源于东方财富网，以官方数据为准

## 技能文件结构

```
a-share-analysis/
├── SKILL.md (本文件)
├── scripts/
│   ├── fetch_realtime_data.py      # 实时行情获取
│   ├── fetch_technical_indicators.py # 技术指标分析
│   ├── fetch_fundamental_data.py    # 基本面分析
│   ├── fetch_sentiment_data.py      # 情绪分析
│   └── generate_report.py           # 报告生成
└── references/
    └── data_sources.md              # 数据源说明
```

## 常见使用场景

### 场景1: 分析个股
- 用户说"分析一下贵州茅台"
- 获取实时行情 → 技术分析 → 基本面分析 → 生成报告

### 场景2: 市场概览
- 用户说"今天A股怎么样"
- 获取主要指数行情 → 市场情绪分析 → 生成摘要报告

### 场景3: 技术分析
- 用户说"宁德时代的MACD和RSI怎么样"
- 获取技术指标 → 详细分析 → 给出信号

### 场景4: 投资决策
- 用户说"五粮液值得买入吗"
- 综合分析技术面、基本面、情绪面 → 给出投资建议

## 更新日志

- **2026-02-27**: 初始版本，支持实时行情、技术分析、基本面分析、情绪分析、报告生成
