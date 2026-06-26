# Archetype · 仪表盘 / 数据风

## 适用场景

以**数据密度和对照**为主的产物，读者用来"扫"和"比"，不是用来"读"：

- 数据分析结果、业务指标汇总
- 项目进度看板、健康度监控
- A/B 测试结果、方案对比矩阵
- 用户反馈分类、问题归因汇总

典型特征：统计卡片 + 表格 + 图表 + 列表并置，关键数字需要一眼捕捉，细节放二级视觉层。

## 核心结构

仪表盘的灵魂是**栅格 + 信息密度**。左右不留过多空白，但组件之间要有清晰间距。

```
┌──────────────────────────────────────────────────────────┐
│  标题栏（页面标题 + 时间范围 + 说明）                      │
├──────────────────────────────────────────────────────────┤
│  核心指标区（4 个统计卡片一行）                           │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐                           │
│  │ KPI│ │ KPI│ │ KPI│ │ KPI│                           │
│  └────┘ └────┘ └────┘ └────┘                           │
├──────────────────────────────────────────────────────────┤
│  图表区（通常 2 列，大图可跨列）                          │
│  ┌───────────┐ ┌───────────┐                            │
│  │  Chart 1  │ │  Chart 2  │                            │
│  └───────────┘ └───────────┘                            │
├──────────────────────────────────────────────────────────┤
│  明细区（表格、排行榜、列表）                              │
│  ┌────────────────────────────────────────┐              │
│  │ 表格                                   │              │
│  └────────────────────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

容器宽度 `max-width: 1280px`，两侧 padding `--space-6`。

## 必备组件

### 1. 顶部标题栏

包含页面标题、生成时间、数据范围。注意别和长文的 Cover 一样厚重——仪表盘要尽快进入数据：

```html
<header class="dash-header">
  <div>
    <h1 class="dash-title">Q1 产品数据概览</h1>
    <p class="dash-subtitle">2026-01-01 至 2026-03-31 · 所有渠道</p>
  </div>
  <div class="dash-meta">
    <span class="dash-tag">已完成</span>
    <span>更新于 2026-05-10</span>
  </div>
</header>
```

```css
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: var(--space-10) 0 var(--space-6);
  border-bottom: 1px solid var(--color-border-1);
  margin-bottom: var(--space-8);
  gap: var(--space-6);
  flex-wrap: wrap;
}
.dash-title {
  margin: 0 0 var(--space-2);
  font-size: var(--fs-3xl);
  font-weight: var(--fw-bold);
  line-height: var(--lh-tight);
}
.dash-subtitle {
  margin: 0;
  color: var(--color-text-3);
  font-size: var(--fs-sm);
}
.dash-meta {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  color: var(--color-text-3);
  font-size: var(--fs-sm);
}
.dash-tag {
  padding: 2px var(--space-2);
  background: var(--color-success-soft);
  color: var(--color-success);
  border-radius: var(--radius-sm);
  font-weight: var(--fw-medium);
}
```

### 2. KPI 统计卡片（核心组件）

仪表盘的灵魂。设计要点：

- **大数字第一眼可见**（28-36px，字重 600）
- **标签在上，数字在下**（符合扫视习惯）
- **变化趋势用颜色 + 小三角**（上升绿色、下降红色、持平灰色）
- **不要把卡片做得太花哨**，保持克制

```html
<section class="kpi-row">
  <div class="kpi-card" data-metric="mrr" data-value="1280000">
    <div class="kpi-label">月度经常性收入</div>
    <div class="kpi-value">¥128<span class="kpi-unit">万</span></div>
    <div class="kpi-delta kpi-delta-up">
      <svg width="10" height="10" viewBox="0 0 10 10"><path d="M5 1 L9 7 L1 7 Z" fill="currentColor"/></svg>
      <span>+12.4%</span>
      <span class="kpi-delta-note">环比上月</span>
    </div>
  </div>
  <!-- 重复 3 个 -->
</section>
```

```css
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}
@media (max-width: 1024px) { .kpi-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px)  { .kpi-row { grid-template-columns: 1fr; } }

.kpi-card {
  padding: var(--space-5);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-lg);
}
.kpi-label {
  color: var(--color-text-3);
  font-size: var(--fs-sm);
  margin-bottom: var(--space-2);
}
.kpi-value {
  font-size: var(--fs-3xl);
  font-weight: var(--fw-semibold);
  color: var(--color-text-1);
  line-height: var(--lh-tight);
  letter-spacing: -0.01em;
}
.kpi-unit {
  font-size: var(--fs-lg);
  font-weight: var(--fw-regular);
  color: var(--color-text-3);
  margin-left: 2px;
}
.kpi-delta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: var(--space-3);
  font-size: var(--fs-sm);
}
.kpi-delta-up   { color: var(--color-success); }
.kpi-delta-down { color: var(--color-danger); }
.kpi-delta-flat { color: var(--color-text-3); }
.kpi-delta-note {
  margin-left: var(--space-2);
  color: var(--color-text-3);
}
```

**关键**：`data-metric` 和 `data-value` 属性非常重要——下一轮 AI 读取这份 HTML 时，可以直接抽取指标名和数值，不用从视觉文字里反推。

### 3. 图表

**静态图表优先用内联 SVG**，真实需要交互时才上 ECharts/Chart.js。

#### 简单柱状图（纯 SVG）

```html
<article class="chart-card">
  <header class="chart-header">
    <h3>近 7 天订单量</h3>
    <span class="chart-meta">单位：单</span>
  </header>
  <svg class="chart-svg" viewBox="0 0 480 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="近 7 天订单量柱状图">
    <!-- 网格线 -->
    <g stroke="#e2e8f0" stroke-width="1">
      <line x1="40" y1="40"  x2="460" y2="40"/>
      <line x1="40" y1="100" x2="460" y2="100"/>
      <line x1="40" y1="160" x2="460" y2="160"/>
      <line x1="40" y1="200" x2="460" y2="200"/>
    </g>
    <!-- Y 轴标签 -->
    <g fill="#94a3b8" font-family="Inter" font-size="11" text-anchor="end">
      <text x="34" y="44">300</text>
      <text x="34" y="104">200</text>
      <text x="34" y="164">100</text>
      <text x="34" y="204">0</text>
    </g>
    <!-- 柱子 -->
    <g fill="#2563eb">
      <rect x="60"  y="120" width="40" height="80"  rx="2"/>
      <rect x="120" y="90"  width="40" height="110" rx="2"/>
      <rect x="180" y="70"  width="40" height="130" rx="2"/>
      <rect x="240" y="110" width="40" height="90"  rx="2"/>
      <rect x="300" y="60"  width="40" height="140" rx="2"/>
      <rect x="360" y="50"  width="40" height="150" rx="2"/>
      <rect x="420" y="30"  width="40" height="170" rx="2"/>
    </g>
    <!-- X 轴标签 -->
    <g fill="#64748b" font-family="Inter" font-size="11" text-anchor="middle">
      <text x="80"  y="222">周一</text>
      <text x="140" y="222">周二</text>
      <text x="200" y="222">周三</text>
      <text x="260" y="222">周四</text>
      <text x="320" y="222">周五</text>
      <text x="380" y="222">周六</text>
      <text x="440" y="222">周日</text>
    </g>
  </svg>
</article>
```

#### 需要真实交互时用 ECharts

CDN 只在确实需要的情况下引入：

```html
<!-- head -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>

<!-- body -->
<article class="chart-card">
  <header class="chart-header"><h3>用户增长趋势</h3></header>
  <div id="chart-growth" class="chart-svg"></div>
</article>

<script>
  const chart = echarts.init(document.getElementById('chart-growth'));
  chart.setOption({
    color: ['#2563eb', '#10b981'],
    tooltip: { trigger: 'axis' },
    legend: { data: ['新用户', '活跃用户'], textStyle: { color: '#64748b' } },
    grid: { left: 40, right: 20, top: 40, bottom: 30 },
    xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May'] },
    yAxis: { type: 'value' },
    series: [
      { name: '新用户', type: 'line', data: [120, 200, 150, 280, 320], smooth: true },
      { name: '活跃用户', type: 'line', data: [800, 920, 1050, 1200, 1380], smooth: true }
    ]
  });
</script>
```

图表颜色**强制从 `--chart-1` 到 `--chart-8` 按顺序取**，保证整份 HTML 里所有图表观感一致。

#### 图表卡片样式

```css
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}
@media (max-width: 900px) { .chart-grid { grid-template-columns: 1fr; } }

.chart-card {
  padding: var(--space-5);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-lg);
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}
.chart-header h3 {
  margin: 0;
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
}
.chart-meta {
  font-size: var(--fs-xs);
  color: var(--color-text-3);
}
.chart-svg { width: 100%; height: 240px; }
```

### 4. 数据表格

和长文表格类似，但仪表盘里的表格通常行数更多，也常带状态 tag：

```html
<section class="data-table-section">
  <header class="section-header">
    <h2>明细数据</h2>
    <span class="section-note">共 128 条</span>
  </header>
  <div class="table-wrapper">
    <table class="data-table">
      <thead>
        <tr>
          <th>订单号</th>
          <th>客户</th>
          <th>产品</th>
          <th style="text-align:right">金额</th>
          <th>状态</th>
          <th>时间</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>#A20260510-001</code></td>
          <td>北京智造</td>
          <td>企业套餐</td>
          <td style="text-align:right">¥12,800</td>
          <td><span class="tag tag-success">已付款</span></td>
          <td>2026-05-10 09:42</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

状态 tag 样式：

```css
.tag {
  display: inline-block;
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  font-size: var(--fs-xs);
  font-weight: var(--fw-medium);
  line-height: 1.5;
}
.tag-success { background: var(--color-success-soft); color: var(--color-success); }
.tag-warning { background: var(--color-warning-soft); color: var(--color-warning); }
.tag-danger  { background: var(--color-danger-soft);  color: var(--color-danger); }
.tag-info    { background: var(--color-info-soft);    color: var(--color-info); }
.tag-muted   { background: var(--color-bg-muted);     color: var(--color-text-3); }
```

### 5. 排行榜 / 进度列表

比表格更轻量的展示方式，适合 top 10 类数据：

```html
<div class="rank-list">
  <div class="rank-item">
    <div class="rank-index">1</div>
    <div class="rank-name">企业 SaaS 套餐</div>
    <div class="rank-bar">
      <div class="rank-bar-fill" style="width: 92%"></div>
    </div>
    <div class="rank-value">92%</div>
  </div>
</div>
```

```css
.rank-item {
  display: grid;
  grid-template-columns: 28px 140px 1fr 60px;
  gap: var(--space-3);
  align-items: center;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-2);
}
.rank-index {
  width: 24px; height: 24px;
  background: var(--color-bg-muted);
  color: var(--color-text-2);
  border-radius: var(--radius-sm);
  text-align: center;
  line-height: 24px;
  font-size: var(--fs-sm);
  font-weight: var(--fw-semibold);
}
.rank-item:nth-child(1) .rank-index { background: var(--color-primary); color: white; }
.rank-bar {
  height: 8px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.rank-bar-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--radius-full);
}
.rank-value {
  text-align: right;
  font-variant-numeric: tabular-nums;
  color: var(--color-text-2);
  font-size: var(--fs-sm);
}
```

### 6. Section 分区标题

数据密度高时，子分区标题要比长文的 h2 克制：

```html
<header class="section-header">
  <h2>图表分析</h2>
  <span class="section-note">近 7 天</span>
</header>
```

```css
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin: var(--space-8) 0 var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-1);
}
.section-header h2 {
  margin: 0;
  font-size: var(--fs-xl);
  font-weight: var(--fw-semibold);
}
.section-note { font-size: var(--fs-sm); color: var(--color-text-3); }
```

## 常见变体

### 单列窄仪表盘

如果数据量不多，用 `max-width: 960px` 单列排列，更像"数据摘要"而不是"控制台"。

### 多维度对比表

A/B 测试结果这种场景，把卡片做成"方案 A vs 方案 B"并排：

```html
<div class="compare-grid">
  <div class="compare-card compare-a">
    <div class="compare-tag">方案 A · 新流程</div>
    <div class="compare-metrics">...</div>
  </div>
  <div class="compare-vs">vs</div>
  <div class="compare-card compare-b">
    <div class="compare-tag">方案 B · 对照组</div>
    <div class="compare-metrics">...</div>
  </div>
</div>
```

## 常见失误

- **数字没有单位或千分位**：12800000 要写成 `¥1,280,000` 或 `¥128 万`，中文场景"万/亿"单位更友好。
- **图表颜色乱配**：每张图都换一套颜色，整体看起来像拼贴画。**一律从 `--chart-1` 按顺序取**。
- **Mock 数据太假**：不要全是 100, 200, 300。真实感来自参差不齐的小数和偶尔的异常值。
- **KPI 卡片太多**：一行 4 个已是上限，超过就拆成两行或移到明细表格。
- **图表没标题和单位**：图表卡片必须有标题，Y 轴需要时要有单位说明。
- **忘了给下轮 AI 留 data-* 属性**：仪表盘最大的价值就是"数据被结构化"，千万别让数字只存在于文字里。
