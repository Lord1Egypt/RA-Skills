---
name: Financial Industry Data Analysis Expert
slug: finance-data-analytics
description: AI-powered financial data analysis expert — covers financial statement analysis, KPI tracking, trend analysis, data visualization, and automated reporting. Built for financial analysts, CFO offices, and data-driven decision making. Keywords: financial data analysis, KPI dashboard, data visualization, financial reporting, Python analysis, SQL queries, 金融数据分析, 财务分析, KPI追踪, 数据可视化, Python分析, 数据看板, 经营分析, 业务分析, Excel分析, Pandas分析.
version: "5.0.2"
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - code-examples-reference
---

# Financial Industry Data Analysis Expert / 金融数据分析专家
> **⚠️ SECURITY NOTICE**
> - **Type:** Educational reference / analytical framework ONLY
> - **技能本身不包含可执行代码**，文中Python代码为教学示例
> - **No persistent storage, background execution, or credential collection**
> - **No credential collection, PII processing, or system access**
> - **All outputs require human review before real-world application**
> - **NOT financial, legal, or insurance advice**
>
> **⚠️ 数据安全警告**
> - 本技能仅提供金融数据分析的方法论参考框架，**不执行任何代码或脚本**
> - 文中提到的市场数据查询、资金流向分析为**教学方法论展示**，不涉及实际的API调用或数据采集
> - 不会自动访问、存储或处理用户的任何数据或个人信息
> - 所有分析结果仅供参考，不构成投资建议



> **English:** AI-powered financial data analysis — covers financial statements, KPIs, visualization, and automated reporting.
>
> **中文:** 金融数据分析——覆盖财务报表、KPI、可视化、自动化报告。

---


### 金融监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 金融监管 | 2026年Q1：金融数据合规要求提升 | 数据分析框架需纳入合规和信披新标准 |
| 金融监管 | 理财信息披露'三清'推进，数据分析需关注新标准 | 数据分析框架需纳入合规和信披新标准 |
| 金融监管 | 反洗钱数据监控要求加强 | 数据分析框架需纳入合规和信披新标准 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **数据分散** | 数据源多，整合耗时 | 统一数据模型 |
| **手工报表多** | 月报/季报重复劳动 | 自动报告生成 |
| **分析浅** | 只看表面数字 | 深度归因分析 |
| **可视化差** | 图表不直观 | 专业可视化模板 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** financial data analysis, KPI dashboard, data visualization, financial reporting, Python analysis

**中文触发词：** 数据分析 / 财务分析 / KPI追踪 / 数据可视化 / 自动化报告 / Python分析 / SQL查询 / 数据看板 / 经营分析 / 业绩分析 / 同比环比

---

## Core Capabilities / 核心能力

### 1. Financial Analysis Templates / 财务分析模板

> **示例代码（仅供学习参考，非本技能自动执行）**：
```python
class FinancialAnalyzer:
    """财务分析引擎"""
    
    def income_statement_analysis(self, data: dict) -> dict:
        """损益表分析"""
        return {
            "收入趋势": self._trend_analysis(data["revenue"]),
            "毛利率分析": self._gross_margin_analysis(data),
            "费用结构": self._expense_breakdown(data),
            "利润质量": self._profit_quality_analysis(data)
        }
    
    def ratio_analysis(self, financial_data: dict) -> dict:
        """比率分析"""
        ratios = {
            "盈利能力": {
                "毛利率": data["gross_profit"] / data["revenue"],
                "净利率": data["net_profit"] / data["revenue"],
                "ROE": data["net_profit"] / data["equity"]
            },
            "运营效率": {
                "存货周转": data["cogs"] / data["inventory"],
                "应收账款周转": data["revenue"] / data["ar"]
            },
            "偿债能力": {
                "流动比率": data["current_assets"] / data["current_liabilities"],
                "资产负债率": data["total_liabilities"] / data["total_assets"]
            }
        }
        return ratios
```

### 2. Dashboard Templates / 数据看板模板

```python
DASHBOARD_TEMPLATES = {
    "CFO驾驶舱": {
        "widgets": [
            {"type": "kpi_card", "metrics": ["营收", "利润", "ROE"]},
            {"type": "line_chart", "data": "收入趋势"},
            {"type": "bar_chart", "data": "各业务线收入"},
            {"type": "waterfall", "data": "利润变动归因"},
            {"type": "gauge", "data": "KPI完成率"}
        ]
    },
    "业务分析看板": {
        "widgets": [
            {"type": "funnel", "data": "转化漏斗"},
            {"type": "heat_map", "data": "客户活跃度"},
            {"type": "pie_chart", "data": "客户分布"},
            {"type": "trend", "data": "关键指标趋势"}
        ]
    }
}
```

---

## Disclaimer

This skill provides data analysis tools for educational purposes.
