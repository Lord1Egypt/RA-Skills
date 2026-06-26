# Stock Analyst v3.0 - 股票全面分析系统

专业股票分析工具，支持港股/美股/A股全面分析。

## 功能

- ✅ 实时行情 (富途数据源)
- ✅ 技术指标 (RSI/MACD/均线)
- ✅ 财报分析 (PE/ROE/毛利率)
- ✅ 多源新闻分析
- ✅ 7大板块综合报告

## 数据源

| 市场 | 数据源 |
|------|--------|
| 港股 | 富途牛牛 (推荐) |
| 美股 | Finnhub API |
| A股 | 腾讯财经 |

## 新闻来源

- 富途新闻
- 6551科技新闻
- 财经门户

## 安装

```bash
pip install requests pandas
```

## 使用

```bash
# 分析港股
python report_v3.py 03998

# 分析美股
python report_v3.py JD

# 分析A股
python report_v3.py 600519
```

## 模块说明

```
stock-analyst/
├── tools/
│   ├── indicator_api.py    # 技术指标计算
│   ├── news_api_v2.py     # 多源新闻
│   └── financial_api.py   # 财报分析
├── report_v3.py           # 主程序
└── SKILL.md               # Skill配置
```

## 版本

v3.0.0 - 当前版本

## 作者

- GitHub: gaoren36-arch
