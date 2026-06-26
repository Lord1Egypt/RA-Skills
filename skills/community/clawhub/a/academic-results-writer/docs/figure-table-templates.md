# Figure & Table Narrative Templates — Full Specification

Moved from main SKILL.md §9.

## Core Principles

1. Don't just say "see Figure X"
2. First tell the reader what question the figure answers
3. Then describe the figure structure
4. Then report the key pattern
5. Finally add statistical support
6. Statistical values invisible from the figure must not be fabricated
7. When image is unreadable, must state "based on caption / user description"

## Figure Error-Bar Terminology Rule

When user provides figure caption or chart description, strictly distinguish:

| Term | Meaning |
|------|---------|
| **SD** | Standard deviation — describes data dispersion |
| **SE** | Standard error — describes estimate precision |
| **CI** | Confidence interval — describes parameter estimate uncertainty |

**Rules:**
1. If caption says "error bars indicate ±1 SE", must NOT write "标准差参见图" or "图中显示 M ± SD"
2. If caption does NOT specify error bar type, write: "图中误差线类型未说明，需人工确认." — never assume SD/SE/CI
3. In Results text, M and SD come from user-provided data, not confused with figure error bar type

## Figure Visual-Language Source Rule

When user has NOT provided actual image screenshot — only caption, chart description, or statistics:

❌ "视觉上……" / "从图中可以明显看出……" / "图中显示出明显趋势……" / "如图所示，[trend description not from caption]"

✅ "根据用户提供的均值……" / "从均值模式看……" / "根据 caption 和统计结果……" / "若实际图像与 caption 一致，则图中应呈现……"

**Rule:** Only write "如图所示/视觉上" when user has provided image screenshot or explicitly described visual patterns.

## Figure Template

> 图 X 展示了 [变量] 在 [条件/组别/时间点] 下的变化。可以看到，[关键视觉模式]。与这一模式一致，统计分析显示……

## Table Template

> 表 X 汇总了 [分析类型] 的结果。重点来看，[变量/路径/模型] 显示……，其统计证据为……
