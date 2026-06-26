# BaoStock 数据平台 Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://www.baostock.com)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

免费 A 股数据平台，支持 K 线、财务、行业分类查询，无需注册。

## ✨ 特性

- 🆓 **免费无需注册** - 无需 Token，登录即用
- 📈 **A股数据 1990 至今** - 覆盖全部 A 股历史数据
- 💰 **财务数据** - 盈利能力、营运能力、成长能力、偿债能力
- 📊 **指数成分** - 沪深300、中证500、上证50 成分股

## 📥 安装

```bash
pip install baostock --upgrade
```

## 🚀 快速开始

```python
import baostock as bs

# 登录
lg = bs.login()

# 查询K线数据
rs = bs.query_history_k_data_plus(
    "sh.600000",
    "date,code,open,high,low,close,volume",
    start_date='2024-01-01',
    end_date='2024-12-31',
    frequency="d",
    adjustflag="3"  # 不复权
)
df = rs.get_data()
print(df.head())

# 登出
bs.logout()
```

## 📊 支持的数据类型

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| K线数据 | 日/周/月/分钟线 | `query_history_k_data_plus()` |
| 证券列表 | 全部证券代码 | `query_all_stock()` |
| 交易日历 | 交易日查询 | `query_trade_dates()` |
| 行业分类 | 证监会行业分类 | `query_stock_industry()` |
| 盈利能力 | ROE/ROA等 | `query_profit_data()` |
| 营运能力 | 周转率等 | `query_operation_data()` |
| 成长能力 | 增长率等 | `query_growth_data()` |
| 偿债能力 | 资产负债率等 | `query_balance_data()` |
| 指数成分 | 沪深300/中证500 | `query_hs300_stocks()` |

## 📖 复权说明

```python
# adjustflag 参数
# "1" = 后复权
# "2" = 前复权
# "3" = 不复权（默认）
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持 A 股全量数据查询

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://www.baostock.com
- **ClawHub**：https://clawhub.com
