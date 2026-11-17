# 💰 Finance Tools v1.1.0

**财务分析工具集** — 7个子命令覆盖从收支汇总到趋势预测的完整财务分析流程。自动识别CSV中的金额、日期、类别列，无需繁琐配置。

纯 Python 标准库，无任何外部依赖。

---

## 安装

无需安装。确保系统已安装 Python 3（≥3.8）。

```bash
python3 --version
```

## 子命令一览

| 命令 | 功能 | 新增版本 |
|------|------|---------|
| `analyze` | 收支汇总 + 分位数 + 月度净额 | 1.0.0 增强 |
| `ratios` | 财务比率（毛利率/净利率/ROE/ROA/ROI/负债率） | 1.0.0 增强 |
| `trend` | 月度趋势（含移动平均 MA 和同比） | 1.0.0 增强 |
| **`category`** | **分类汇总（ASCII 条形图 + 占比）** | **1.1.0** |
| **`budget`** | **预算 vs 实际对比（差异 + 执行率）** | **1.1.0** |
| **`yoy`** | **同比/环比增长分析** | **1.1.0** |
| **`forecast`** | **趋势预测（线性回归/移动平均/加权平均）** | **1.1.0** |

## 快速上手指南

### 基础分析
```bash
python3 scripts/finance_tools.py analyze --file transactions.csv
python3 scripts/finance_tools.py category --file transactions.csv
```

### 预算管理
```bash
# 预算文件与实际文件分开
python3 scripts/finance_tools.py budget --file actual.csv --budget-file budget.csv

# 或使用同一文件（含预算列和实际列）
python3 scripts/finance_tools.py budget --file plan.csv --actual-budget-file plan.csv
```

### 增长率分析
```bash
# 同比环比
python3 scripts/finance_tools.py yoy --file monthly_revenue.csv

# 趋势预测
python3 scripts/finance_tools.py forecast --file revenue.csv --periods 12 --trend linear
python3 scripts/finance_tools.py forecast --file sales.csv --trend moving_avg --window 6
```

### 财务健康检查
```bash
python3 scripts/finance_tools.py ratios --file financials.csv
```

## CSV 格式要求

```csv
# 示例：transactions.csv
date,amount,category,note
2026-01-15,5000,工资,1月工资
2026-01-16,-200,餐饮,午餐
2026-01-20,-1500,房租,1月房租
```

列名自动适配中英文：
- 金额: `amount`, `金额`, `revenue`, `收入`, `expense`, `支出`, `cost`, `profit`, `actual`, `budget`
- 日期: `date`, `日期`, `month`, `月份`, `period`
- 类别: `category`, `类别`, `type`, `类型`, `department`, `project`

## 预测模型说明

| 模型 | 原理 | 适用场景 |
|------|------|---------|
| `linear`（默认） | 最小二乘法线性回归，含 R² 拟合优度 | 稳定增长/下降趋势 |
| `moving_avg` | 最近 N 期简单平均 | 无明显趋势，波动较小 |
| `weighted` | 最近 N 期加权平均（越近权重越大） | 近期数据更有参考价值 |

## CSV 自动列识别

工具会自动识别列的角色：

| 角色 | 优先匹配的列名 |
|------|--------------|
| 金额 | amount, 金额, revenue, 收入, expense, 支出, cost, 成本, profit, 利润, price, 单价, actual, 实际, budget, 预算 |
| 日期 | date, 日期, time, 时间, month, 月份, year, 年份, period, 期间 |
| 类别 | category, 类别, type, 类型, name, 名称, product, 产品, department, 部门, project, 项目 |

## 法律声明

本工具提供的数据分析、比率计算和趋势预测仅供参考和辅助决策，不构成财务或投资建议。

- 预测结果基于历史数据的统计推断，实际结果可能因市场变化、政策调整、突发事件等因素与预测产生显著差异
- 财务比率的计算依赖 CSV 中列名的准确识别，使用者应验证列映射是否正确
- 建议结合专业财务知识和业务背景解读分析结果
- 工具输出不能替代专业会计师或财务顾问的意见

## 安全说明

- ✅ 纯本地运行，无网络请求
- ✅ 仅读取用户指定的文件路径
- ❌ 无任意代码执行（exec/eval）
- ❌ 无系统命令执行（subprocess/shell）
- ❌ 无数据上传或遥测

## 许可证

MIT License
