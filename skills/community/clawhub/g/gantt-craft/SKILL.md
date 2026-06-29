---
name: gantt-craft
version: 1.0.0
description: 任务列表转可交互甘特图HTML，支持进度追踪和依赖关系
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

项目管理中甘特图是最常用的可视化工具之一，但 Excel 画甘特图费时费力、MS Project 学习成本太高。很多时候只需要一个轻量、可分享、无需安装的项目进度图，能看任务依赖、识别关键路径、追踪进度就够了。

本 Skill 将任务列表（名称、起止时间、负责人、依赖关系）转化为可交互的甘特图 HTML。提供 7 种视图模式——标准甘特图、里程碑导向、资源分配、依赖关系、周视图、季度概览、敏捷冲刺看板。支持时间轴缩放、进度更新、关键路径高亮等交互。

---

# Gantt Craft — 甘特图生成 Skill

> 将项目任务列表转化为可交互的甘特图 HTML，支持进度追踪和依赖关系展示。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **输入任务数据**：粘贴任务列表（名称、起止时间、负责人、进度、依赖关系）
2. **选择甘特图类型**：从映射表中选择最适合的视图
3. **选择配色方案**：选择进度状态配色主题
4. **生成甘特图**：输出交互式单文件 HTML

### 任务数据输入格式

```
任务名称,开始日期,结束日期,负责人,进度,依赖
需求分析,2024-01-01,2024-01-15,张三,100%,
UI设计,2024-01-10,2024-01-25,李四,80%,需求分析
前端开发,2024-01-20,2024-02-15,王五,60%,UI设计
后端开发,2024-01-20,2024-02-10,赵六,70%,需求分析
测试,2024-02-10,2024-02-25,张三,20%,前端开发,后端开发
```

或使用 JSON 格式：
```json
[
  {"id":"T1","name":"需求分析","start":"2024-01-01","end":"2024-01-15","owner":"张三","progress":1,"deps":[]},
  {"id":"T2","name":"UI设计","start":"2024-01-10","end":"2024-01-25","owner":"李四","progress":0.8,"deps":["T1"]}
]
```

## 场景-模式映射表

| 项目场景 | 推荐模式 | 特点 |
|---------|---------|------|
| 通用项目计划 | standard（标准） | 周/月时间轴，全部任务展示 |
| 关键节点跟踪 | milestone（里程碑） | 突出里程碑节点，弱化日常任务 |
| 人力调配 | resource（资源分配） | 按负责人着色，查看各人工作量 |
| 复杂项目 | dependency（依赖关系） | 用箭头展示任务前后依赖及关键路径 |
| 短期冲刺 | compact（周视图） | 单周/双周紧凑视图 |
| 年度规划 | quarterly（季度概览） | 季度为单位，适合高层汇报 |
| 敏捷开发 | agile-sprint（敏捷冲刺） | 类看板 + 时间轴混合 |

## 配色方案库

### 进度状态色
- **未开始**：`#9ca3af` 灰色
- **进行中**：`#3b82f6` 蓝色
- **已完成**：`#22c55e` 绿色
- **延期/风险**：`#ef4444` 红色
- **里程碑**：`#f59e0b` 金色菱形

### 负责人配色（自动分配）
```
#3b82f6 #ef4444 #22c55e #f59e0b #8b5cf6 #ec4899 #14b8a6 #f97316
```

### 4 套主题配色

#### 1. 项目蓝
```
--bg: #ffffff
--text: #1f2937
--grid: #f1f5f9
--grid-line: #e2e8f0
--weekend: #f8fafc
--today: #fef3c7
--task-border: #e2e8f0
```

#### 2. 暗色仪表盘
```
--bg: #0f172a
--text: #e2e8f0
--grid: #1e293b
--grid-line: #334155
--weekend: #1e293b
--today: #422006
--task-border: #475569
```

#### 3. 纸质计划书
```
--bg: #fefcf6
--text: #3a3a3a
--grid: #fafaf9
--grid-line: #e5e5e5
--weekend: #fefcf6
--today: #fef3c7
--task-border: #d4d4d4
```

#### 4. 极简灰白
```
--bg: #f8f9fa
--text: #212529
--grid: #ffffff
--grid-line: #dee2e6
--weekend: #f8f9fa
--today: #fff3cd
--task-border: #ced4da
```

## 交互增强包列表

### 基础交互
- 时间轴缩放（日/周/月切换）
- 任务条悬停详情
- 水平滚动查看全时间轴
- 里程碑标记

### 高级交互
- 按负责人/状态筛选任务
- 进度滑块（在线调整进度百分比）
- 关键路径高亮（最长路径任务标红边框）
- 任务依赖箭头显示/隐藏
- 导出为 PNG 图片

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **绘制方式**：时间轴和任务条使用纯 CSS/SVG 绘制
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：支持横向滚动，移动端可左右拖动查看

## 命令定义

### `/gantt-craft`
主入口命令。输入任务数据，选择甘特图类型后生成交互式甘特图 HTML。

### `/gantt-template`
生成空白甘特图模板供规划使用。包含填表示例和空行，用户可在线修改任务数据后生成。

## 文件结构

```
skills/gantt-craft/
├── SKILL.md
├── patterns/
│   ├── standard.json        # 标准甘特图
│   ├── milestone.json       # 里程碑导向
│   ├── resource.json        # 资源分配视图
│   ├── dependency.json      # 依赖关系图
│   ├── compact.json         # 紧凑周视图
│   ├── quarterly.json       # 季度概览
│   └── agile-sprint.json    # 敏捷冲刺看板
└── templates/
    ├── base.html
    ├── standard.html
    ├── milestone.html
    ├── resource.html
    ├── dependency.html
    ├── compact.html
    ├── quarterly.html
    └── agile-sprint.html
```
