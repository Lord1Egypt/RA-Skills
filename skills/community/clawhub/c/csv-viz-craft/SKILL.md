---
name: csv-viz-craft
version: 1.0.0
description: CSV数据转可筛选、排序、搜索的交互式数据表格HTML
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

团队成员之间传递数据时，Excel 表格需要安装软件、手机端体验差、分享出去容易版本混乱。更关键的是，静态表格无法筛选、排序、搜索，大量数据时定位困难。

本 Skill 将 CSV 数据转化为可交互的 HTML 数据表格，支持列排序、全局搜索、列筛选、分页、行选择、统计摘要等交互功能。提供 7 种展示模式——从标准表格到卡片网格、从简易透视到筛选面板，让数据分享变得简单、直观、可交互。

---

# CSV Viz Craft — CSV 可视化 Skill

> 将 CSV 数据转化为可筛选、排序、搜索的交互式数据表格 HTML。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **粘贴 CSV 数据**：直接粘贴 CSV 文本内容（支持逗号/制表符/Tab 分隔）
2. **自动解析**：AI 自动识别列名、列类型（文本/数字/日期/分类）
3. **选择展示模式**：从映射表中选择最适合的展示方式
4. **选择配色方案**：选择数据可视化配色主题
5. **生成表格**：输出交互式单文件 HTML

### 输入格式建议

```csv
姓名,年龄,城市,月收入
张三,28,北京,15000
李四,35,上海,22000
```

支持标准 CSV、TSV（制表符分隔）、以及带 BOM 的 UTF-8 编码。

## 场景-模式映射表

| 数据类型 | 推荐模式 | 特点 |
|---------|---------|------|
| 结构化数据表 | data-table（标准表格） | 列排序、筛选、分页、可定制列宽 |
| 产品/人员展示 | card-grid（卡片网格） | 卡片式布局，适合图文展示 |
| 分类汇总 | pivot-lite（简易透视） | 按维度分组汇总，支持计数/求和/均值 |
| 多维度分析 | filter-dashboard（筛选面板） | 多维度联动筛选，适合探索式分析 |
| 选项对比 | comparison（对比视图） | 选中多行并排对比，适合产品/方案对比 |
| 趋势数据 | chart-embed（内嵌图表） | 表格内嵌迷你柱状图/折线图 |
| 报告输出 | export-ready（打印优化） | 打印友好，去掉交互元素，保留结构 |

## 配色方案库

### 数据可视化配色

**分类色**（用于类别区分）
```
#4e79a7 #f28e2b #e15759 #76b7b2 #59a14f #edc948 #b07aa1 #ff9da7
```

**连续色**（用于数值渐变）
```
#c7e9c0 → #74c476 → #238b45
```

**发散色**（用于正负对比）
```
#d73027 → #f7f7f7 → #1a9642
```

### 4 套主题配色

#### 1. 清爽蓝白（通用）
```
--bg: #ffffff
--text: #1f2937
--header-bg: #1a73e8
--header-text: #ffffff
--row-even: #f8fafc
--row-hover: #e0f2fe
--border: #e2e8f0
```

#### 2. 暗色数据
```
--bg: #1e293b
--text: #e2e8f0
--header-bg: #0f172a
--header-text: #94a3b8
--row-even: #1e293b
--row-hover: #334155
--border: #475569
```

#### 3. 商务灰
```
--bg: #f8f9fa
--text: #343a40
--header-bg: #495057
--header-text: #ffffff
--row-even: #ffffff
--row-hover: #e9ecef
--border: #dee2e6
```

#### 4. 暖色报表
```
--bg: #fefcf6
--text: #3a3a3a
--header-bg: #ea580c
--header-text: #ffffff
--row-even: #fff7ed
--row-hover: #ffedd5
--border: #fed7aa
```

## 交互增强包列表

### 基础交互
- 列排序（升序/降序/恢复默认）
- 全局搜索（实时过滤所有列）
- 列筛选（下拉选择唯一值和范围）
- 分页（可配置每页行数）

### 高级交互
- 行选择（多选/全选，选中行统计）
- 统计面板（列最小值/最大值/均值/计数）
- 列类型切换（日期格式化、数字精度控制）
- 导出 CSV（当前筛选结果）
- 打印优化

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **CSV 解析**：纯 JS 实现，支持引号转义、换行符、BOM 头
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：支持横向滚动和卡片自适应

## 命令定义

### `/csv-viz`
主入口命令。粘贴 CSV 数据，选择展示模式后生成交互式数据表格 HTML。

### `/csv-dashboard`
生成带图表的仪表盘视图。自动识别数值列和分类列，生成统计图表 + 数据表格的组合视图。

## 文件结构

```
skills/csv-viz-craft/
├── SKILL.md
├── patterns/
│   ├── data-table.json      # 标准数据表格
│   ├── card-grid.json       # 卡片网格
│   ├── pivot-lite.json      # 简易透视表
│   ├── filter-dashboard.json# 多维度筛选面板
│   ├── comparison.json      # 对比视图
│   ├── chart-embed.json     # 内嵌迷你图表
│   └── export-ready.json    # 打印/导出优化
└── templates/
    ├── base.html
    ├── data-table.html
    ├── card-grid.html
    ├── pivot-lite.html
    ├── filter-dashboard.html
    ├── comparison.html
    ├── chart-embed.html
    └── export-ready.html
```
