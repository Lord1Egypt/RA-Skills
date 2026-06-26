# AKShare 金融数据 Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/akfamily/akshare)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

免费金融数据 API 库，支持 A股、港股、美股、期货、基金等，无需 API Key。

## ✨ 特性

- 🆓 **免费无需注册** - 无需 Token 或 API Key，开箱即用
- 🌐 **全市场覆盖** - A股、港股、美股、期货、期权、基金、债券、外汇
- 🐼 **返回 pandas DataFrame** - 数据直接可用于分析和建模
- 📈 **实时 + 历史数据** - 支持实时行情与历史 K 线数据

## 📥 安装

```bash
pip install akshare --upgrade
```

## 🚀 快速开始

```python
import akshare as ak

# A股实时行情（东方财富）
df = ak.stock_zh_a_spot_em()
print(df.head())

# A股历史K线
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20240101", end_date="20241231", adjust="qfq")
print(df.head())
```

## 📊 支持的数据类型

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| 股票 | A股实时/历史行情 | `stock_zh_a_spot_em()` |
| 港股 | 港股历史K线 | `stock_hk_hist()` |
| 美股 | 美股日线数据 | `stock_us_daily()` |
| 指数 | 指数行情数据 | `index_zh_a_hist()` |
| 基金 | ETF/基金行情 | `fund_etf_spot_em()` |
| 期货 | 期货行情数据 | `futures_zh_daily_sina()` |
| 期权 | 期权行情数据 | `option_sse_underlying_spot_em()` |
| 债券 | 债券行情数据 | `bond_zh_hs_daily()` |
| 外汇 | 汇率数据 | `fx_spot_quote()` |
| 宏观 | 宏观经济指标 | `macro_china_gdp_yearly()` |

## 📖 更多示例

```python
import akshare as ak

# ETF实时行情
etf_df = ak.fund_etf_spot_em()

# GDP年度数据
gdp_df = ak.macro_china_gdp_yearly()

# 个股新闻
news_df = ak.stock_news_em(symbol="000001")

# 港股历史K线
hk_df = ak.stock_hk_hist(symbol="00700", period="daily", adjust="qfq")
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接

### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持全市场金融数据获取

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://github.com/akfamily/akshare
- **ClawHub**：https://clawhub.com
