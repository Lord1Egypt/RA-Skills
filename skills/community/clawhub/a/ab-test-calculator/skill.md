# 📊 ab-test-calculator

**输入两组数据，一句白话告诉你该不该上线。不做数据科学家也能看懂 A/B 测试。**
**Feed it two data sets — one plain-language verdict on whether to ship. No stats PhD required.**

## 三种数据类型 · Three Data Types

| 类型 Type | 检验方法 Test | 场景 Use Case | 输入 Input |
|-----------|--------------|---------------|------------|
| 连续型 Continuous | Welch's t + Cohen's d | 加载时间、停留时长、评分<br>Load time, session duration, ratings | 两组数字 或 均值±标准差<br>Raw values or mean±std |
| 二项型 Binary | Chi-square + Cohen's h | 转化率、点击率、留存率<br>Conversion rate, CTR, retention | 转化数 / 总数<br>Conversions / total |
| 计数型 Count | Mann-Whitney U | 每日事件数、购买件数<br>Daily events, items purchased | 两组事件计数<br>Per-user event counts |

## 输出什么 · Output

```
📊 A/B Test Report

Group A:  12.50% conversion (120/1000)
Group B:  16.50% conversion (165/1000)

Difference:  +4.50pp   [+1.44pp, +7.56pp]
Relative:    +37.50%

χ² = 8.286   p = 0.004 **   Cohen's h = 0.13

⚠️ Significant but small effect.
   Real uplift, but modest magnitude.
```

一句话结论，不用猜 p 值啥意思。One-line verdict — no decoding p-values required.

## 技术亮点 · Tech Highlights

- **纯 Python 自实现**：正态 CDF/PPF、不完全 Beta、不完全 Gamma → 精确的 p 值和置信区间，零依赖
  *Pure Python from scratch: normal CDF/PPF, incomplete Beta, incomplete Gamma → exact p-values & CIs, zero external deps*
- **Welch's t-test**：不假设两组方差相等，比标准 t 检验更稳健
  *No equal-variance assumption — more robust than standard Student's t*
- **效应量 + 统计功效**：不只告诉你「是否显著」，还告诉你「差得值不值」和「样本量够不够」
  *Effect size + statistical power — not just "is it real?" but "does it matter?" and "did we test enough people?"*
- **白话结论引擎**：把 p 值、效应量、功效组合成一句人话
  *Plain-language verdict engine: synthesizes p-value, effect size, and power into one actionable sentence*

## 触发词 · Triggers

「A/B测试」「AB测试」「显著性检验」「实验对比」「哪个版本更好」「转化率对比」「t检验」「卡方检验」「统计功效」「ab test」
