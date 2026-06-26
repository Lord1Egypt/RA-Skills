---
name: excel-finance
description: Excel 财务模型技能 - Excel 财务模型模板、自动化报表生成
author: 滚滚家族 🌪️
version: "1.0.0"
homepage: https://aigogoai.com
triggers:
  - "Excel 财务"
  - "财务模型"
  - "Excel 模板"
  - "报表生成"
  - "财务表格"
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins:
        - python3
        - pip
    config:
      env: {}
---

# 📊 Excel 财务模型技能

**Excel 财务模型模板与自动化工具**

**作者：** 滚滚家族 🌪️  
**版本：** 1.0.0  
**主页：** https://aigogoai.com

---

## 🎯 技能描述

**一个帮助财务人快速创建 Excel 财务模型的工具。**

**核心功能：**
- 📊 Excel 财务模型模板
- 📈 自动化报表生成
- 💰 财务预测模型
- 📉 敏感性分析
- 🎯 图表自动生成

---

## 🛠️ 使用方法

### 1. 创建财务模型

```python
from excel_finance import create_financial_model

# 创建三表模型
model = create_financial_model(
    company_name="XX 公司",
    forecast_years=5,
    output_file="financial_model.xlsx"
)

# 输出：Excel 文件路径
```

### 2. 生成财务报表

```python
from excel_finance import generate_reports

# 生成财务报表
reports = generate_reports(
    stock_code="600519.SH",
    report_types=["balance_sheet", "income_statement", "cash_flow"],
    output_file="reports.xlsx"
)
```

### 3. 敏感性分析

```python
from excel_finance import sensitivity_analysis

# 敏感性分析
result = sensitivity_analysis(
    base_case={"revenue_growth": 0.15, "margin": 0.5},
    scenarios={
        "bull": {"revenue_growth": 0.20, "margin": 0.55},
        "bear": {"revenue_growth": 0.10, "margin": 0.45}
    },
    output_file="sensitivity.xlsx"
)
```

---

## 📋 模板列表

### 财务模型模板

| 模板 | 描述 | 适用场景 |
|------|------|----------|
| **三表模型** | 资产负债表 + 利润表 + 现金流量表 | 全面财务分析 |
| **DCF 估值** | 现金流折现模型 | 股票估值 |
| **预算模型** | 年度预算编制 | 企业预算管理 |
| **盈利预测** | 未来 3-5 年盈利预测 | 投资研究 |

### 分析报表模板

| 模板 | 描述 | 适用场景 |
|------|------|----------|
| **财务比率分析** | 盈利能力/偿债能力/营运能力 | 财务健康诊断 |
| **趋势分析** | 3-5 年财务数据趋势 | 成长性分析 |
| **同业对比** | 同行业多公司对比 | 竞争地位分析 |
| **杜邦分析** | ROE 分解分析 | 盈利能力深度分析 |

---

## 📚 参考文档

- [Excel 财务模型教程](https://aigogoai.com/knowledge/excel-models)
- [财务预测方法](https://aigogoai.com/knowledge/financial-forecasting)
- [敏感性分析指南](https://aigogoai.com/knowledge/sensitivity-analysis)

---

## 🌪️ 滚滚的话

**"你只管 do it，Excel 模型交给滚滚！"**

**这个技能是滚滚家族为财务人打造的 Excel 自动化利器，**
**希望能帮助你更高效地完成财务建模工作！**

**如有问题或建议，欢迎反馈！**

**翻滚的地球人，一直在！** 🌪️💚

---

**创建人：** 滚滚 6 号（数据分析师）  
**创建时间：** 2026-03-28  
**状态：** ✅ 完成
