# 可视化组件库手册

由 `apply_layout.py` 注入的 `viz_components.css` 提供。这些组件**把数据变成图形**，
是「图文并茂」的核心。组件全部用主题 CSS 变量取色，深浅主题自适应，直接拷 HTML 片段用。

> 原则：**能用组件就别用纯文字/表格**。表格只用于「确实需要逐格对照的多维数据」。

## 目录
- [大数字卡 KPI](#大数字卡-kpi) — 关键数字
- [进度条 / 进度环](#进度条--进度环) — 达成率/占比
- [横向对比条](#横向对比条) — 排名/对比（替代表格）
- [占比环形 donut](#占比环形-donut) — 构成占比
- [流程箭头](#流程箭头) — 步骤/流程
- [时间轴](#时间轴) — 节奏/里程碑
- [标签云](#标签云) — 关键词
- [信息高亮条](#信息高亮条) — 重点提示
- [VS 对比双栏](#vs-对比双栏) — 两方对比

---

## 大数字卡 KPI
关键数字别埋在文字里，做成大数字卡。
```html
<div data-role="stat-grid">
  <div class="eh-kpi">
    <span class="eh-kpi-label">月活用户</span>
    <span><span class="eh-kpi-value">1.2</span><span class="eh-kpi-unit">亿</span></span>
    <span class="eh-kpi-trend eh-up">▲ 25%</span>
  </div>
  <div class="eh-kpi">
    <span class="eh-kpi-label">GMV</span>
    <span><span class="eh-kpi-value">8.5</span><span class="eh-kpi-unit">亿</span></span>
    <span class="eh-kpi-trend eh-down">▼ 3%</span>
  </div>
</div>
```
可选迷你火花线：在 `.eh-kpi` 内加 `<svg class="eh-spark" viewBox="0 0 100 28" preserveAspectRatio="none"><path d="M0,20 L20,14 L40,16 L60,8 L80,10 L100,4"/></svg>`

## 进度条 / 进度环
```html
<!-- 横向进度条 -->
<div class="eh-progress">
  <div class="eh-pg-head"><span>目标达成</span><span>78%</span></div>
  <div class="eh-pg-track"><div class="eh-pg-fill" style="width:78%"></div></div>
</div>

<!-- 进度环（r=42 周长≈264；dasharray = 占比×264, 264）78% → 206 -->
<div class="eh-ring">
  <svg width="110" height="110" viewBox="0 0 110 110">
    <circle class="eh-ring-track" cx="55" cy="55" r="42" stroke-width="9"/>
    <circle class="eh-ring-fill" cx="55" cy="55" r="42" stroke-width="9"
            stroke-dasharray="206 264"/>
  </svg>
  <span class="eh-ring-pct">78%</span>
  <span class="eh-ring-label">目标达成</span>
</div>
```

## 横向对比条
**排名/数值对比首选**，比表格直观。**注意 `width%` 是视觉映射 ≠ 显示值**：

- **常规**：`width%` = 该项 / 最大值 ×100（最大那项填满 100%，其余按比例）。
- **小差异区间映射**（重要）：当数据集中在小区间（如出勤率都 93~97%），按上面算各条几乎等长看不出差异。改用
  `width = (值 − 区间下限) / (区间上限 − 区间下限) ×100`，把差异放大；**`eh-bar-val` 始终显示真实值**。

```html
<!-- 示例：线上 60% / 线下 40%，最大值 60% → 线上 width 100%、线下 width=40/60≈67% -->
<!-- val 显示真实占比，width 是相对最大值的视觉比例 -->
<div class="eh-bars">
  <div class="eh-bar-row"><span class="eh-bar-name">线上渠道</span>
    <div class="eh-bar-track"><div class="eh-bar-fill" style="width:100%"></div></div>
    <span class="eh-bar-val">60%</span></div>
  <div class="eh-bar-row"><span class="eh-bar-name">线下渠道</span>
    <div class="eh-bar-track"><div class="eh-bar-fill" style="width:67%"></div></div>
    <span class="eh-bar-val">40%</span></div>
</div>
```
> ⚠️ 不要把数值塞进 `eh-bar-fill` 内（会被填充色压住）；数值一律放条外 `eh-bar-val`。
> 趋势/时间序列**不要用血条**（用 Chart.js 折线/面积，见 CHARTS.md 选型表）。

## 占比环形 donut
构成占比（纯 SVG）。每段用 `stroke-dasharray="本段长 周长"` + `stroke-dashoffset` 累加偏移。
r=50 周长≈314。各段 offset = 前面所有段长之和取负。
```html
<div class="eh-donut">
  <svg width="130" height="130" viewBox="0 0 130 130">
    <circle cx="65" cy="65" r="50" fill="none" stroke="#2563EB" stroke-width="20"
            stroke-dasharray="188 314" stroke-dashoffset="0"/>
    <circle cx="65" cy="65" r="50" fill="none" stroke="#22C55E" stroke-width="20"
            stroke-dasharray="126 314" stroke-dashoffset="-188"/>
  </svg>
  <div class="eh-donut-legend">
    <div class="eh-lg-item"><span class="eh-lg-dot" style="background:#2563EB"></span>线上<span class="eh-lg-val">60%</span></div>
    <div class="eh-lg-item"><span class="eh-lg-dot" style="background:#22C55E"></span>线下<span class="eh-lg-val">40%</span></div>
  </div>
</div>
```
> 占比 donut 也可直接用 Chart.js doughnut（见 CHARTS.md），数据多时更省心。

## 流程箭头
步骤/流程，替代「1. 2. 3.」文字列表。
```html
<div class="eh-flow">
  <div class="eh-flow-step"><span class="eh-flow-num">1</span>上传 HTML 文件</div>
  <div class="eh-flow-step"><span class="eh-flow-num">2</span>注册到应用注册表</div>
  <div class="eh-flow-step"><span class="eh-flow-num">3</span>生成页面 ID + 短域名</div>
  <div class="eh-flow-step"><span class="eh-flow-num">4</span>得到可分享链接</div>
</div>
```

## 时间轴
```html
<div class="eh-timeline">
  <div class="eh-tl-item"><div class="eh-tl-time">Q1</div><div class="eh-tl-title">立项</div><div class="eh-tl-desc">完成需求评审与方案设计</div></div>
  <div class="eh-tl-item"><div class="eh-tl-time">Q2</div><div class="eh-tl-title">上线</div><div class="eh-tl-desc">核心功能灰度发布</div></div>
</div>
```

## 标签云
```html
<div class="eh-tagcloud">
  <span class="eh-tag" style="font-size:20px">高频词</span>
  <span class="eh-tag" style="font-size:15px">中频词</span>
  <span class="eh-tag" style="font-size:13px">低频词</span>
</div>
```

## 信息高亮条
重点提示/比喻/小贴士。
```html
<div class="eh-infobar"><span class="eh-infobar-icon">💡</span>
  <div>一句话记住：HTML 是骨架，CSS 是皮肤，JS 是神经。</div>
</div>
```

## VS 对比双栏
两方对比（前端 vs 后端、方案 A vs B）。
```html
<div class="eh-vs">
  <div class="eh-vs-card"><strong>前端</strong><p>跑在浏览器，HTML+CSS+JS</p></div>
  <div class="eh-vs-mid">VS</div>
  <div class="eh-vs-card"><strong>后端</strong><p>跑在服务器，存数据/调接口</p></div>
</div>
```

---

## 配色说明
组件默认用主题暴露的 `--primary` 等变量取色。donut/多色场景里写死的 hex（如图例色块）
是「数据分类色」，不属于主题皮肤，保留即可。深色主题下边框/轨道用半透明，自动适配。
