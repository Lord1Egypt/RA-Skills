---
name: chart-craft
version: 1.0.0
description: 数据描述转柱状图/折线图/饼图等8种交互式SVG图表HTML
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

日常工作中经常需要快速展示一组数据——柱状图看对比、饼图看占比、折线图看趋势。但打开 Excel 或 PPT 来画图表太重量级，专业工具（ECharts、D3）又有学习门槛。很多时候只需要一张能嵌入文档或邮件的轻量图表，还能悬停看数值、切换图例。

本 Skill 通过自然语言描述数据 → 智能推荐图表类型 → 纯前端渲染的方式，零依赖地生成柱状图、折线图、饼图、环形图、面积图、堆叠柱状图、雷达图、组合图等交互式 SVG 图表。适合嵌入文档、邮件、汇报材料中。

---

# Chart Craft — 简易图表生成 Skill

> 将简单的数据描述转化为柱状图、饼图、折线图等交互式图表 HTML。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **描述数据**：用自然语言描述数据，或粘贴表格格式数据
2. **选择图表类型**：接受 AI 推荐或手动选择
3. **选择配色方案**：选择喜欢的配色主题
4. **生成图表**：输出交互式单文件 HTML

### 数据输入格式

```
2023年各季度营收（万元）：
Q1: 120, Q2: 180, Q3: 165, Q4: 210

或表格格式：
季度,营收
Q1,120
Q2,180
Q3,165
Q4,210
```

## 场景-模式映射表

| 数据特征 | 推荐图表 | 适用场景 |
|---------|---------|---------|
| 分类对比（≤10 类） | bar-chart（柱状图） | 各产品销量、各团队业绩 |
| 时间序列趋势 | line-chart（折线图） | 月度营收、网站访问量变化 |
| 占比构成 | pie-chart（饼图） | 市场份额、预算分配比例 |
| 占比构成（需留白） | donut-chart（环形图） | 类似饼图，更现代简洁 |
| 累积趋势 | area-chart（面积图） | 用户增长、累计销售额 |
| 总量 + 分量 | stacked-bar（堆叠柱状图） | 各产品各季度营收构成 |
| 多维度对比 | radar-chart（雷达图） | 能力评估、产品维度对比 |
| 多数据多类型 | combo-chart（组合图） | 营收（柱）+ 增长率（折线） |

## 配色方案库

### 分类配色
```
#4e79a7 #f28e2b #e15759 #76b7b2 #59a14f #edc948 #b07aa1 #ff9da7
#9c755f #bab0ac #e15759 #f28e2b #4e79a7 #76b7b2 #59a14f #edc948
```

### 渐变配色
```
蓝色渐变: #e0f2fe → #0284c7
绿色渐变: #dcfce7 → #16a34a
橙色渐变: #ffedd5 → #ea580c
紫色渐变: #e9d5ff → #7c3aed
```

### 单色配色（同一色相不同明度）
```
蓝单色: #dbeafe, #93c5fd, #60a5fa, #3b82f6, #2563eb, #1d4ed8
绿单色: #d1fae5, #6ee7b7, #34d399, #10b981, #059669, #047857
```

### 4 套主题配色

#### 1. 商业蓝
```
--bg: #ffffff
--text: #1f2937
--grid: #e5e7eb
--axis: #9ca3af
--tooltip-bg: #1f2937
--tooltip-text: #ffffff
```

#### 2. 暗色科技
```
--bg: #0f172a
--text: #e2e8f0
--grid: #334155
--axis: #64748b
--tooltip-bg: #e2e8f0
--tooltip-text: #0f172a
```

#### 3. 纸质报告
```
--bg: #fefcf6
--text: #3a3a3a
--grid: #e5e5e5
--axis: #737373
--tooltip-bg: #3a3a3a
--tooltip-text: #fefcf6
```

#### 4. 多彩活泼
```
--bg: #ffffff
--text: #1e293b
--grid: #f1f5f9
--axis: #94a3b8
--tooltip-bg: #1e293b
--tooltip-text: #ffffff
```

## 交互增强包列表

### 基础交互
- 悬停提示（显示精确数值）
- 数据标签（显示/隐藏）
- 图例切换（点击隐藏/显示数据系列）

### 高级交互
- 动画入场（数据加载动画）
- 导出为 PNG 图片（Canvas API 截图）
- 数据缩放（折线图/面积图区域缩放）
- 阈值线（添加目标值参考线）

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **图表渲染**：纯 SVG + CSS 绘制，或 Canvas API
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：自动适配容器宽度

## 命令定义

### `/chart-craft`
主入口命令。输入数据描述，选择或接受推荐的图表类型后生成交互式图表 HTML。

### `/chart-compare`
生成多数据集对比图表。支持在同一图表中叠加多组数据系列。

## 文件结构

```
skills/chart-craft/
├── SKILL.md
├── patterns/
│   ├── bar-chart.json       # 柱状图
│   ├── line-chart.json      # 折线图
│   ├── pie-chart.json       # 饼图
│   ├── donut-chart.json     # 环形图
│   ├── area-chart.json      # 面积图
│   ├── stacked-bar.json     # 堆叠柱状图
│   ├── radar-chart.json     # 雷达图
│   └── combo-chart.json     # 组合图
└── templates/
    ├── base.html
    ├── bar-chart.html
    ├── line-chart.html
    ├── pie-chart.html
    ├── donut-chart.html
    ├── area-chart.html
    ├── stacked-bar.html
    ├── radar-chart.html
    └── combo-chart.html
```
