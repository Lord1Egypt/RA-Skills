---
name: finance-tools
description: |
  财务分析工具集 v1.1.0。7个子命令覆盖财务分析全流程。
  自动识别CSV中的金额、日期、类别列。
  纯Python标准库，无外部依赖。

  Use when: 需要快速分析交易数据、计算财务比率、
  查看收支趋势、分类汇总、预算对比、同比环比、趋势预测。

  🎉 v1.1.0 功能:
  - analyze — 收支汇总 + 分位数 + 月度净额
  - ratios — 财务比率(毛利率/净利率/ROE/ROA/ROI/负债率)
  - trend — 月度趋势(含MA移动平均和YoY)
  - category (NEW) — 分类汇总(ASCII条形图+占比)
  - budget (NEW) — 预算 vs 实际对比(执行率)
  - yoy (NEW) — 同比/环比增长分析
  - forecast (NEW) — 趋势预测(线性回归/移动平均)

  触发关键词：财务分析、收入支出、财务比率、趋势分析、
  分类汇总、预算管理、同比环比、数据预测
  适用范围：CSV 格式的财务/交易数据
  运行模式：纯本地，无网络请求 ❎
  外部依赖：Python标准库（无需额外安装）
---

# 💰 Finance Tools v1.1.0

## Overview
自动识别CSV中的金额列(amount/收入/支出)、日期列(date/日期)、类别列(category/类型)，无需手动指定列名。7个子命令覆盖从基础分析到预测的全流程。

## Usage

### analyze — 收支分析（扩展版）
```bash
python3 scripts/finance_tools.py analyze --file transactions.csv

# 📊 财务分析 — transactions.csv
#    总交易数: 1,200
#    收入合计:         485,230.00
#    支出合计:         312,450.00
#    净额:            172,780.00
#    收支比:               1.55x
#    P25:            120.00 | P75: 850.00
#
#    月度净额:
#     2026-01:  145,000.00
```

### ratios — 财务比率（扩充版）
```bash
python3 scripts/finance_tools.py ratios --file financials.csv

# 📈 财务比率分析 — financials.csv
#    revenue: 1,250,000.00   cost: 875,000.00
#    毛利率: 30.00%
#    ROE(净资产收益率): 18.50%
#    ROI(投资回报率): 12.30%
```

### trend — 月度趋势（含移动平均）
```bash
python3 scripts/finance_tools.py trend --file income.csv --ma 3

# 📈 月度趋势分析 — income.csv
#    月份       金额          环比     同比     MA-3
#    2026-01   98,500.00     —       —     98,500.00
#    2026-02  102,300.00  +3.9%      —    100,400.00
```

### category — 分类汇总 (NEW)
```bash
python3 scripts/finance_tools.py category --file transactions.csv

# 📂 分类汇总 — transactions.csv
#    ████████████████ 工资                350,000.00 (72.1%)
#    ██████           餐饮                 45,200.00 ( 9.3%)
```

### budget — 预算对比 (NEW)
```bash
python3 scripts/finance_tools.py budget --file actual.csv --budget-file budget.csv

# 📋 预算 vs 实际
#    类别        实际       预算        差异       执行率
#    工资     350,000  360,000   -10,000   97.2%
```

### yoy — 同比环比 (NEW)
```bash
python3 scripts/finance_tools.py yoy --file revenue.csv

# 📊 同比/环比增长分析
#    月份       金额       环比(MoM)   同比(YoY)
#    2026-01  98,500       —           —
#    2026-02 102,300     +3.9%       +5.2%
```

### forecast — 趋势预测 (NEW)
```bash
python3 scripts/finance_tools.py forecast --file revenue.csv --periods 6

# 🔮 趋势预测 — revenue.csv
#    模型: 线性增长 (斜率=+2,350.00/月, R²=0.923)
#    2026-07: 112,000.00  (+3.2% 预测增长)
```

## 列名自动识别
| 角色 | 匹配关键词 |
|------|-----------|
| 金额 | amount, 金额, revenue, 收入, expense, 支出, cost, 成本, profit, 利润, actual, budget |
| 日期 | date, 日期, time, 时间, month, 月份, period, 期间 |
| 类别 | category, 类别, type, 类型, name, 名称, department, project |

## Use Cases
- **个人理财**: analyze 月度汇总 + category 分类 + forecast 支出预测
- **小企业**: ratios 财务比率 + yoy 同比 + budget 预算管理
- **团队预算**: budget 执行率 + trend 趋势 + forecast 预测

## Security
- ✅ 纯本地运行，无网络请求
- ✅ 只读输入文件
- ❌ 无任意代码执行
- ❌ 无系统命令执行
