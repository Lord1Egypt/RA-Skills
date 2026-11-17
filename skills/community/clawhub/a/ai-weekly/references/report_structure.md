# AI 周报结构规范

## 报告整体结构（按顺序）

```
1. Cover / 封面
2. KPI 仪表盘（5个核心指标）
3. 市场数据图表（6个 Chart.js 图表）
4. 重大新闻（10条，按时间倒序）
5. 并购与融资亮点（表格 + 图表）
6. 大模型排行榜（Top 10，标注数据来源与排名标准）
7. 趋势深度解析（6大趋势卡片）
8. 下周期待（时间线）
9. Footer / 页脚
```

## 各节详细规范

### 1. 封面 (Cover)

- **背景**：渐变紫色/蓝色（`#1e3a8a → #7c3aed`）
- **内容**：
  - 标签：`📊 行业周报 · 第XX周`
  - 主标题：`AI 行业周报`
  - 副标题：`YYYY年MM月DD日 — MM月DD日 | 全球人工智能行业动态与数据分析`
  - 元信息：报告日期、覆盖区域、数据来源

### 2. KPI 仪表盘

固定5个指标（如数据源无更新，使用上次有效数据并标注估算）：

| # | 指标名称 | 数据来源 |
|---|---------|---------|
| 1 | 全球AI市场规模（当年） | Resourcera / Companies History |
| 2 | 本周AI融资总额 | AI Funding / StartupHub |
| 3 | ChatGPT市场份额 | 市场份额追踪网站 |
| 4 | 企业AI采用率 | Gartner / Stanford AI Index |
| 5 | 本周重大并购金额 | 新闻搜索汇总 |

每个 KPI 卡片包含：标签、数值、同比/环比变化箭头、**周环比（WoW）对比**。

**周环比对比**：
- 数据来源：`tools/accumulate_data.py` 维护的 `data/history.csv`
- 展示格式：`.kpi-wow` 区域显示 "vs 上周 +X.X%" 或 "持平"
- 颜色：`.wow-up`（绿色）、`.wow-down`（红色）、`.wow-flat`（灰色）
- Agent 在生成报告时应先读取 `data/history.csv` 的上一周数据，计算差值后填入

### 3. 市场数据图表（6个）

| # | 图表标题 | 图表类型 | canvas ID | 数据来源 |
|---|---------|---------|-----------|---------|
| 1 | 全球AI市场规模 (2024-2033F) | 柱状图 Bar | marketSizeChart | Resourcera / Statista |
| 2 | AI融资季度趋势 (2023Q1-最新) | 折线图 Line | fundingChart | Crunchbase / AI Funding |
| 3 | 企业AI应用场景分布 (Top 10) | 饼图 Doughnut | adoptionChart | Gartner / Stanford AI Index |
| 4 | AI聊天机器人市场份额 (当年) | 饼图 Doughnut | marketShareChart | 市场份额数据 |
| 5 | 并购交易规模对比 | 柱状图 Bar | maChart | 新闻搜索汇总 |
| 6 | AI智能体市场预测 | 柱状图 Bar | agentMarketChart | 行业研究报告 |

Chart.js 配置规范：
- `borderRadius: 6`（柱状图）
- `fill: true, tension: 0.3`（折线图）
- `borderWidth: 2`（饼图，白色边框）
- 配色：使用 CSS 变量色系（见模板）

### 4. 重大新闻（10条）

**选取标准**（优先级从高到低）：
1. 重大并购/融资（$1B以上）
2. 前沿模型发布/重大更新
3. 重要政策/监管动态
4. 技术突破（基准测试刷新）
5. 大公司战略转型

**格式规范**：
```html
<li class="news-item">
  <div class="news-date [color-class]">MM/DD</div>
  <div class="news-body">
    <h4>新闻标题</h4>
    <p>2-3句摘要（含关键数字和背景）</p>
    <span class="tag [color]">分类标签</span>
    <!-- 最多3个标签 -->
  </div>
</li>
```

**日期标签颜色规范**：
- `.news-date`（默认蓝色）：一般新闻
- `.news-date.red`：政策监管
- `.news-date.orange`：并购/芯片/硬件
- `.news-date.purple`：产品发布/模型更新
- `.news-date.green`：中国AI动态/融资

### 5. 并购与融资亮点

**表格列**：日期 | 类型（并购/融资） | 收购方/领投方 | 标的 | 金额 | 领域

**类型标签**：
- `.badge.acq`（蓝色）：并购
- `.badge.fund`（绿色）：融资
- `.badge.ipo`（紫色）：IPO

**图表**：并购交易规模对比（柱状图，单位 $B）

### 6. 大模型排行榜（Top 10，标注数据来源与排名标准）

**评分来源**（按可用性排序）：
1. Artificial Analysis Intelligence Index
2. SWE-bench Pro / Pro 2.0
3. Terminal-Bench 2.1
4. 官方基准测试数据

**每款模型展示**：
- 排名徽章（金/银/铜/普通）
- 模型名称 + 开发方 + 开源/闭源标注
- 关键基准测试分数
- 数值化评分（用于排序）

### 7. 趋势深度解析（6大趋势）

从以下维度选取本周最显著的6个趋势：
- 监管政策方向
- 资本流向变化
- 技术范式转移
- 市场竞争格局
- 产业链变动
- 地缘政治影响

每个趋势卡片格式：
```html
<div class="trend-card">
  <div class="arrow">[emoji]</div>
  <h4>趋势标题</h4>
  <p>2-3句分析（基于事实，不过度推测）</p>
</div>
```

### 8. 下周期待

时间线格式，包含：
- 已确认事件（日期 + 事件描述）
- 预计事件（月份 + 事件描述）
- 值得关注的动态

### 9. 页脚

```
数据来源：[列出所有使用的来源]
免责声明：本报告由 AI 辅助编制，数据仅供参考
```

## Chart.js 数据格式参考

详见 `SKILL.md` 中的"图表数据格式"章节。

## 视觉设计规范

| 元素 | 规范 |
|------|------|
| 主色 | `#2563eb`（蓝色） |
| 辅助色 | `#7c3aed`（紫色）、`#059669`（绿色） |
| 警告色 | `#dc2626`（红色）、`#ea580c`（橙色） |
| 圆角 | `12px`（卡片）、`10px`（图表区）、`8px`（标签） |
| 阴影 | `0 1px 3px rgba(0,0,0,0.08)` |
| 字体 | PingFang SC / Microsoft YaHei / sans-serif |
| 响应式断点 | `700px` |
| 暗色模式 | `[data-theme="dark"]` + `@media (prefers-color-scheme: dark)` 自动跟随系统 |
| 主题切换 | 右上角圆形按钮，点击切换明/暗主题，Chart.js 网格线颜色同步更新 |
| 打印优化 | `@media print`：隐藏交互元素、固定图表高度、`page-break-inside: avoid`、封面单独一页 |
