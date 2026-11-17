---
name: "fund-analysis"
description: "火富牛综合基金分析技能，覆盖私募和公募基金的净值走势、业绩指标、持仓穿透、策略筛选与FOF组合分析。当用户需要分析基金、比较业绩、查看持仓、筛选基金或生成分析报告时调用。"
---

# 基金分析 (Fund Analysis)

## Overview

This skill enables comprehensive fund analysis covering both 私募 (private placement) and 公募 (public offering) funds.
It leverages the fof99 MCP data platform for fund data retrieval and ECharts for visualization.

## When to Use

Trigger this skill when the user asks to:

- Analyze or compare fund NAV (净值) trends
- Calculate and interpret performance metrics (Sharpe, max drawdown, Alpha, etc.)
- Review fund holdings, sector allocation, or concentration
- Screen funds by strategy, scale, or performance criteria
- Analyze FOF portfolio composition and attribution
- Generate comprehensive fund analysis reports

## Core Workflows

### Workflow 0: Fund Discovery (Always Start Here)

When the user provides a fund name (not a fund code), first resolve it:

1. Use `mcp__fof99_mcp_mall__get_fund_code` with the `fund_name` to get the `fund_code` and fund type (私募/公募).
2. If searching for a company/manager, use `mcp__fof99_mcp_mall__get_company_code` similarly.
3. Confirm the found fund with the user before proceeding with analysis.
4. For strategy-based screening, use `mcp__fof99_mcp_mall__fund_strategy_list` directly.

### Workflow 1: 净值走势分析 (NAV Trend Analysis)

**Objective:** Analyze and compare fund NAV performance over time.

**Steps:**

1. **Resolve fund codes** using Workflow 0 if the user provides fund names.
2. **Fetch NAV data:**
   - 私募: `mcp__fof99_mcp_mall__fund_company_price` (single fund) or `mcp__fof99_mcp_mall__multiple_fund_company_price` (multi-fund snapshot)
   - 公募: `mcp__fof99_mcp_mall__gm_fund_price` (single fund) or `mcp__fof99_mcp_mall__gm_multiple_fund_price` (multi-fund snapshot)
   - 自建: `mcp__fof99_mcp_mall__personal_fund_price`
   - 直投组合: `mcp__fof99_mcp_mall__fof_invest_customer_price`
   - Specify `start_date` and `end_date` if the user provides a time range.
3. **Optional:** Fetch benchmark index data for comparison using `mcp__fof99_mcp_mall__index_price` with appropriate index code.
4. **Visualize:** Use `mcp__fof99_mcp_mall__render_echarts` to render a line chart showing NAV curves. Include:
   - Multiple fund NAVs on the same chart for comparison
   - Benchmark overlay if available
   - Proper legend, axis labels, and date formatting
5. **Present:** Show the chart with a summary table of key NAV statistics (latest NAV, period return, volatility).

**ECharts Example for NAV comparison:**
```json
{
  "title": { "text": "基金净值走势对比" },
  "tooltip": { "trigger": "axis" },
  "legend": { "data": ["基金A", "基金B", "基准"] },
  "xAxis": { "type": "category", "data": ["..."] },
  "yAxis": { "type": "value", "name": "净值" },
  "series": [
    { "name": "基金A", "type": "line", "data": ["..."] },
    { "name": "基金B", "type": "line", "data": ["..."] },
    { "name": "基准", "type": "line", "data": ["..."] }
  ]
}
```

### Workflow 2: 业绩指标分析 (Performance Metrics Analysis)

**Objective:** Calculate and interpret key fund performance metrics.

**Steps:**

1. **Resolve fund codes** using Workflow 0.
2. **Fetch performance factors:**
   - 私募: `mcp__fof99_mcp_mall__get_fund_factor`
   - 公募: `mcp__fof99_mcp_mall__get_gm_fund_factor`
   - 自建: `mcp__fof99_mcp_mall__personal_fund_factor`
   - 直投组合: `mcp__fof99_mcp_mall__fof_invest_customer_factor`
   - Specify `start_date`, `end_date`, and optional `fund_index_code` as needed.
3. **Key metrics returned** (all tools return the same set):
   - 区间收益 (Period Return)
   - 年化收益 (Annualized Return)
   - 年化波动率 (Annualized Volatility)
   - 夏普比率 (Sharpe Ratio)
   - 卡玛比率 (Calmar Ratio)
   - 最大回撤 (Maximum Drawdown)
   - 下行风险 (Downside Risk)
   - 索提诺比率 (Sortino Ratio)
   - Alpha
   - 信息比率 (Information Ratio)
   - 跟踪误差 (Tracking Error)
   - 偏度 (Skewness)
   - 相关系数 (Correlation)
4. **Interpret metrics:** See `references/fund-metrics-guide.md` for detailed interpretation guidelines.
5. **Present:** Create a structured metrics table. Highlight strengths (green) and weaknesses (red) using the Chinese market convention: 红涨绿跌.
6. **Visualize:** Optionally render a radar chart for multi-dimensional comparison across funds.

### Workflow 3: 持仓分析 (Holding Analysis)

**Objective:** Analyze fund holdings, sector distribution, and concentration.

**Steps:**

1. **For FOF funds:** Use `mcp__fof99_mcp_mall__fof_sub_fund` to get underlying holdings (funds, futures, stocks with amounts and percentages).
2. **For direct portfolios:** Use `mcp__fof99_mcp_mall__fof_invest_fund_scale` to get portfolio scale and holding breakdown.
3. **For fund valuation:** Use `mcp__fof99_mcp_mall__fund_valuation_info` for valuation table info (估值日期, 估值来源, 更新时间, 解析状态).
4. **Analyze holdings:**
   - Concentration: Top 5/10 holdings percentage
   - Sector/strategy distribution
   - Position size analysis
5. **Visualize:** Use ECharts for:
   - Pie chart: holding distribution
   - Bar chart: sector/strategy allocation
   - Treemap: position hierarchy
6. **Present:** Summary table with holding details and concentration metrics.

### Workflow 4: 基金筛选 (Fund Screening)

**Objective:** Find funds matching specific criteria.

**Steps:**

1. **Strategy-based screening:** Use `mcp__fof99_mcp_mall__fund_strategy_list` with:
   - `strategy_one`: 一级策略 (期货策略, 股票对冲, 股票多头, 套利策略, 期权策略, 多资产策略, 债券策略, 组合策略, 其他)
   - `strategy_two`: 二级策略 (e.g., 主观多头, 500指增, 市场中性, etc.)
   - `strategy_three`: 三级策略 (optional)
2. **Company-based screening:** Use `mcp__fof99_mcp_mall__company_fund_list` to list all funds under a specific manager.
3. **Performance filtering:** After getting fund lists, fetch performance factors for each candidate and filter by:
   - Minimum Sharpe ratio
   - Maximum drawdown tolerance
   - Minimum annualized return
   - AUM scale requirements (use `mcp__fof99_mcp_mall__company_scale`)
4. **Present:** Ranked list with key metrics in a comparison table.

### Workflow 5: 组合分析 (Portfolio Analysis)

**Objective:** Analyze FOF/direct investment portfolio performance and attribution.

**Steps:**

1. **Get portfolio NAV:** `mcp__fof99_mcp_mall__fof_invest_customer_price`
2. **Get performance factors:** `mcp__fof99_mcp_mall__fof_invest_customer_factor`
3. **Get holding details:** `mcp__fof99_mcp_mall__fof_sub_fund` for underlying positions
4. **Get scale breakdown:** `mcp__fof99_mcp_mall__fof_invest_fund_scale`
5. **Performance attribution:**
   - Compare portfolio return vs benchmark
   - Identify top contributors and detractors
   - Analyze style factor exposure if available
6. **Risk decomposition:**
   - Concentration risk (top holdings weight)
   - Strategy/style concentration
   - Liquidity assessment
7. **Present:** Comprehensive report with charts and analysis.

## 视觉风格系统 (Visual Style System)

整体视觉遵循**火富牛**设计语言：专业、现代、红色为主视觉色调、白色底色、卡片式布局。

### 配色方案 (Color Palette)

#### 品牌色 (Brand)

| 色阶 | 色值 | 用途 |
|------|------|------|
| 品牌主红 | `#E8663C` | 主强调色、涨红色、图表主力系列、按钮、链接、KPI 高亮 |
| 深红 | `#D1442A` | Hover 态、标题点缀、警示 |
| 浅红背景 | `#FFF0EB` | 红色卡片底色、涨跌背景色 |
| 红渐变 | `#E8663C` → `#F5A623` | Banner、头部装饰、重点模块 |

#### 功能色 (Functional)

| 用途 | 色值 | 说明 |
|------|------|------|
| 涨 (Positive) | `#E8663C` | 中国股市惯例：涨为红（复用品牌色） |
| 跌 (Negative) | `#27AE60` | 中国股市惯例：跌为绿 |
| 警示/注意 | `#F5A623` | 风险提示、警告信息 |
| 信息/链接 | `#4A90D9` | 辅助信息、参考链接 |
| 中性/灰色 | `#8E8E93` | 次要信息、分割线 |

#### 中性色 (Neutral)

| 色阶 | 色值 | 用途 |
|------|------|------|
| 页面背景 | `#FFFFFF` | 全局背景（纯白） |
| 卡片/模块背景 | `#FAFBFC` | 信息卡片底色 |
| 浅灰背景 | `#F5F6FA` | 表格交替行、区块分隔 |
| 边框/分割线 | `#EBEDF0` | 卡片边框、表格线 |
| 主文字 | `#1A1A1A` | 标题、正文 |
| 次文字 | `#666666` | 辅助说明、标签 |
| 弱文字 | `#999999` | 时间戳、数据来源、注释 |

#### 图表色板 (Chart Palette)

多系列图表按以下顺序取色（红→蓝→金→紫→青→粉）：

| 序号 | 色值 | 色样 |
|------|------|------|
| 1 | `#E8663C` | 品牌红（主系列） |
| 2 | `#4A90D9` | 信息蓝 |
| 3 | `#F5A623` | 暖金 |
| 4 | `#7B68EE` | 紫罗兰 |
| 5 | `#2EB5A6` | 青绿 |
| 6 | `#E85D75` | 柔粉 |
| 7 | `#50C878` | 翠绿 |
| 8 | `#FF8C69` | 浅珊瑚 |

### 排版规范 (Typography)

| 层级 | 字号 | 字重 | 颜色 | 用途 |
|------|------|------|------|------|
| H1 页面标题 | 24px | 700 (Bold) | `#1A1A1A` | 分析报告总标题 |
| H2 模块标题 | 18px | 600 (Semi Bold) | `#1A1A1A` | 各分析模块标题 |
| H3 子标题 | 15px | 600 | `#1A1A1A` | 卡片内标题 |
| 正文 | 14px | 400 (Regular) | `#1A1A1A` | 分析文本主体 |
| 辅助说明 | 13px | 400 | `#666666` | 指标解释、图例 |
| 数据数字 | 14px | 500 (Medium) | `#1A1A1A` | 表格数据、KPI 数值 |
| 弱化信息 | 12px | 400 | `#999999` | 时间戳、数据来源 |

字体家族：`"PingFang SC", "Microsoft YaHei", "Helvetica Neue", -apple-system, sans-serif`  
数字字体：优先使用等宽/表格数字 `"SF Mono", "Menlo", "Consolas", monospace`（在 ECharts 中通过 `fontFamily` 指定）

### 布局规范 (Layout)

采用**卡片式信息层级**布局：

```
┌──────────────────────────────────────────┐
│           页面标题 + 统计区间               │
├──────────┬──────────┬──────────┬──────────┤
│  KPI 卡片 │  KPI 卡片 │  KPI 卡片 │  KPI 卡片 │
├──────────┴──────────┴──────────┴──────────┤
│            主图表区（净值走势等）             │
│           (占宽 100%，高 400px+)            │
├──────────────────────┬───────────────────┤
│   辅助图表1（饼图等）  │  辅助图表2（柱状图等） │
├──────────────────────┴───────────────────┤
│            明细数据表格                     │
├──────────────────────────────────────────┤
│            分析解读文字                     │
├──────────────────────────────────────────┤
│       数据来源 / 免责说明 / 更新时间          │
└──────────────────────────────────────────┘
```

- 卡片圆角：8px
- 卡片阴影：`0 1px 4px rgba(0,0,0,0.06)`（轻微，不过度）
- 卡片内边距：20px
- 模块间距：24px
- KPI 卡片内：数字大字号 28px + 品牌红，标签 13px 灰色
- 表格交替行底色：白色 / `#F5F6FA`

### ECharts 全局样式默认值

所有 ECharts 图表统一应用以下默认样式：

```json
{
  "backgroundColor": "#FFFFFF",
  "textStyle": {
    "fontFamily": "PingFang SC, Microsoft YaHei, sans-serif",
    "color": "#1A1A1A"
  },
  "title": {
    "textStyle": { "fontSize": 16, "fontWeight": "bold", "color": "#1A1A1A" },
    "subtextStyle": { "fontSize": 12, "color": "#999999" }
  },
  "tooltip": {
    "backgroundColor": "rgba(255,255,255,0.95)",
    "borderColor": "#EBEDF0",
    "textStyle": { "color": "#1A1A1A", "fontSize": 13 }
  },
  "legend": {
    "textStyle": { "color": "#666666", "fontSize": 12 }
  },
  "grid": {
    "left": "12%", "right": "8%", "top": "18%", "bottom": "12%"
  },
  "xAxis": {
    "axisLine": { "lineStyle": { "color": "#EBEDF0" } },
    "axisTick": { "show": false },
    "axisLabel": { "color": "#999999", "fontSize": 11 },
    "splitLine": { "show": false }
  },
  "yAxis": {
    "axisLine": { "show": false },
    "axisTick": { "show": false },
    "axisLabel": { "color": "#999999", "fontSize": 11 },
    "splitLine": { "lineStyle": { "color": "#F5F6FA", "type": "dashed" } }
  }
}
```

## Visualization Guidelines

Use `mcp__fof99_mcp_mall__render_echarts` for all chart rendering. The `option` parameter accepts a JSON string of ECharts configuration. **Always merge the global style defaults above into the chart option.**

### 数据涨跌颜色约定

遵循中国股市惯例：**红涨绿跌**，涨红色复用品牌主色。

- 涨 (Positive) → `#E8663C`（品牌红）
- 跌 (Negative) → `#27AE60`（绿）
- 基准/中性 → `#8E8E93` 或 `#4A90D9`

在 ECharts 中使用 `visualMap` 或 `itemStyle.color` 回调实现：
```javascript
// 涨跌着色回调
itemStyle: {
  color: function(params) {
    return params.value >= 0 ? '#E8663C' : '#27AE60';
  }
}
```

### Chart Types by Analysis:

| 分析场景 | 图表类型 | 用途 | 配色建议 |
|----------|---------|------|----------|
| NAV Trend | 折线图 (Line) | 多基金净值走势对比 | 基金线用色板序，基准用 `#8E8E93` 虚线 |
| Return Comparison | 柱状图 (Bar) | 区间收益对比 | 正收益 `#E8663C`，负收益 `#27AE60` |
| Risk Metrics | 雷达图 (Radar) | 多维风险指标对比 | 多基金用色板序，填充 30% 透明度 |
| Drawdown | 面积图 (Area) | 回撤走势 | 填充 `#FFF0EB`，边线 `#E8663C` |
| Holdings | 饼图/环形图 (Pie) | 持仓分布 | 色板序循环，统一饱和度 |
| Sector Allocation | 堆叠柱状图 (Stacked Bar) | 行业/策略权重 | 色板序 + 透明度分层 |
| Performance Attribution | 瀑布图/柱状图 | 收益归因拆分 | 正贡献红，负贡献绿 |
| Correlation | 热力图 (Heatmap) | 基金相关性矩阵 | `#FFF0EB`→`#FFFFFF`→`#4A90D9` 双色渐变 |

### ECharts NAV 对比示例（火富牛风格）:
```json
{
  "backgroundColor": "#FFFFFF",
  "title": {
    "text": "基金净值走势对比",
    "textStyle": { "fontSize": 16, "fontWeight": "bold", "color": "#1A1A1A" },
    "subtext": "数据来源：火富牛 | 区间：2025-01-01 ~ 2026-05-29",
    "subtextStyle": { "fontSize": 12, "color": "#999999" }
  },
  "tooltip": {
    "trigger": "axis",
    "backgroundColor": "rgba(255,255,255,0.95)",
    "borderColor": "#EBEDF0",
    "textStyle": { "color": "#1A1A1A", "fontSize": 13 }
  },
  "legend": {
    "data": ["基金A", "基金B", "沪深300"],
    "textStyle": { "color": "#666666", "fontSize": 12 }
  },
  "grid": { "left": "12%", "right": "8%", "top": "20%", "bottom": "12%" },
  "xAxis": {
    "type": "category", "data": ["..."],
    "axisLine": { "lineStyle": { "color": "#EBEDF0" } },
    "axisLabel": { "color": "#999999", "fontSize": 11 }
  },
  "yAxis": {
    "type": "value", "name": "净值",
    "splitLine": { "lineStyle": { "color": "#F5F6FA", "type": "dashed" } },
    "axisLabel": { "color": "#999999", "fontSize": 11 }
  },
  "series": [
    { "name": "基金A", "type": "line", "data": ["..."], "color": "#E8663C", "smooth": true, "lineStyle": { "width": 2.5 }, "symbol": "none" },
    { "name": "基金B", "type": "line", "data": ["..."], "color": "#4A90D9", "smooth": true, "lineStyle": { "width": 2.5 }, "symbol": "none" },
    { "name": "沪深300", "type": "line", "data": ["..."], "color": "#8E8E93", "smooth": true, "lineStyle": { "width": 1.5, "type": "dashed" }, "symbol": "none" }
  ]
}
```

## 输出排版规范 (Output Format)

整体遵循**火富牛卡片式报告**风格，信息层级：KPI 概览 → 可视化图表 → 明细数据 → 分析解读 → 数据来源。

### 1. KPI 摘要卡片

在每个分析模块顶部，用一组关键指标数字突出核心结论：

> ```
> ┌─────────────────────────────────────────────────────┐
> │  年化收益      夏普比率      最大回撤      年化波动率   │
> │  +12.35%      1.86        -8.42%       14.28%     │
> │  近一年        近一年        近一年        近一年       │
> └─────────────────────────────────────────────────────┘
> ```

正收益/好指标用 `#E8663C` 红色突出，负收益/风险指标正常黑色。

### 2. 数据表格

使用 Markdown 表格，遵循：

- 表头加粗、居中
- 数值右对齐 / 文字左对齐
- 百分比保留 2 位小数，净值保留 4 位小数
- 正收益行用 🔴 前缀，负收益行用 🟢 前缀（不强制，作为可选视觉线索）
- 排序后置顶最优/最大
- 表后附数据来源与更新日期

### 3. 可视化图表

- 图表始终在表格之前展示 —— 先看图，再看数
- 每个图表附带 1-2 句解读文字
- 图表标题清晰，含数据区间
- 左下角标注数据来源

### 4. 文字分析报告

结构化输出，层次分明：

```
## 📊 [基金名称] 分析报告

### 摘要
2-3 句话概括核心发现。

### 业绩表现
净值走势 + 关键指标解读。

### 风险分析
回撤、波动率、尾部风险评估。

### 持仓特征（如适用）
集中度、策略分布、规模分析。

### 综合评价
总结亮点与关注点，不做投资建议。

---
*数据来源：火富牛 | 更新时间：YYYY-MM-DD | 仅供参考，不构成投资建议*
```

### 5. 综合呈现

组合输出时按以下顺序排列：
1. **KPI 卡片**（快速抓重点）
2. **主图表**（净值走势 / 业绩雷达图）
3. **辅助图表**（持仓饼图 / 回撤面积图）
4. **数据表格**（详细指标对比）
5. **文字分析**（深度解读）
6. **数据来源行**（底部小字）

## Important Notes

- Always start with `get_fund_code` when the user provides fund names instead of codes.
- The fof99 tools have both regular (`mcp__fof99_mcp_mall__`) and streaming (`mcp__fof99_mcp_mall_stream__`) variants. Either can be used; they return the same data.
- For multi-fund comparison, batch calls where possible to reduce round trips.
- When the user asks about a fund without specifying time range, default to the past 1 year.
- Always cite data sources and note any data limitations or caveats.
- If a tool returns an error or empty data, inform the user clearly and suggest alternatives.
