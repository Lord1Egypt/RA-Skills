# Archetype · 海报 / 总结页

## 适用场景

追求**一屏视觉冲击 + 关键结论放大**的产物。读者只看 10 秒，所以必须"第一眼就看到最重要的东西"：

- 周报 / 月报的封面页
- 答辩、述职、汇报的摘要页
- 里程碑成果展示
- 一页纸（One-pager）方案摘要
- 方案对比的封面总览
- 发布 changelog 的封面

典型特征：视觉比例大、结构鲜明、关键数字/结论被放到最显眼的位置，通常一到两屏内结束。

## 核心差异：和前两种完全不一样

| 维度 | 长文 | 仪表盘 | 海报 |
|---|---|---|---|
| 阅读方式 | 从上往下通读 | 扫视 + 深挖细节 | 瞄一眼抓重点 |
| 容器宽度 | 760px 单栏 | 1280px 密布 | 1200px 开阔 |
| 视觉重量 | 克制的灰黑白 | 中性背景 + 少量色 | 允许强对比/暗色/大色块 |
| 字号跨度 | 14-36px | 12-30px | 14-64px |
| 装饰元素 | 几乎没有 | 少量 | 适度几何装饰、渐变 |

**海报是唯一允许"视觉大胆"的 archetype**，但大胆≠乱。下面讲怎么"克制地大胆"。

## 核心结构

```
┌─────────────────────────────────────────────────────┐
│                                                      │
│   ┌──────────────────────────────────────────┐       │
│   │  Hero 区（标题 + 副标题 + 元信息）         │       │
│   │  占 35-45% 高度，不留空虚                  │       │
│   └──────────────────────────────────────────┘       │
│                                                      │
│   ┌────┐ ┌────┐ ┌────┐                              │
│   │结论1│ │结论2│ │结论3│（3-6 个要点并列）          │
│   └────┘ └────┘ └────┘                              │
│                                                      │
│   ┌──────────────────────────────────────────┐       │
│   │  支撑内容（数据 / 流程 / 引用）            │       │
│   └──────────────────────────────────────────┘       │
│                                                      │
│   Footer（生成元信息）                                │
└─────────────────────────────────────────────────────┘
```

## 必备组件

### 1. Hero 区

海报的门面。关键点：

- **标题字号够大**（48-64px）
- **副标题不抢戏**（18-20px，灰度降一档）
- **元信息用极小字+字间距拉开**（12px，letter-spacing 0.1em，uppercase 英文或扁平中文）
- **允许背景色块、渐变、几何装饰**，但只做一层，不要叠

```html
<section class="hero">
  <div class="hero-badge">2026 · Q1 成果汇报</div>
  <h1 class="hero-title">从 0 到 1<br>搭建 AI 驱动的研发提效平台</h1>
  <p class="hero-subtitle">
    半年内覆盖 12 个业务线，累计节约工程师 8600 小时
  </p>
  <div class="hero-meta">
    <span>产研中心 · AI 平台团队</span>
    <span aria-hidden="true">·</span>
    <span>2026 年 5 月 10 日</span>
  </div>
</section>
```

```css
.hero {
  padding: var(--space-20) var(--space-10);
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: #f1f5f9;
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}
/* 背景装饰：一个模糊色块做"光"的感觉 */
.hero::before {
  content: "";
  position: absolute;
  top: -20%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(37,99,235,0.35), transparent 70%);
  pointer-events: none;
}
.hero > * { position: relative; z-index: 1; }
.hero-badge {
  display: inline-block;
  padding: 4px var(--space-3);
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: var(--radius-full);
  font-size: var(--fs-xs);
  letter-spacing: 0.08em;
  color: #cbd5e1;
}
.hero-title {
  margin: var(--space-5) 0 var(--space-4);
  font-size: var(--fs-5xl);
  font-weight: var(--fw-bold);
  line-height: var(--lh-tight);
  letter-spacing: -0.02em;
  color: #ffffff;
}
.hero-subtitle {
  margin: 0 0 var(--space-8);
  font-size: var(--fs-xl);
  color: #cbd5e1;
  line-height: var(--lh-normal);
  max-width: 700px;
}
.hero-meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--fs-xs);
  color: #94a3b8;
  letter-spacing: 0.05em;
}
```

**Hero 背景方案**：
- 深色渐变（上面示例，最保险）
- 浅灰 + 大号插画 SVG
- 纯白 + 一条彩色条带
- 避免用高饱和"彩虹渐变"或动态粒子

### 2. 核心数字区（Stats）

海报最重要的组件之一。和仪表盘的 KPI 卡片不同——**海报的数字要大到"视觉爆破"**：

```html
<section class="stats-hero">
  <div class="stat-big" data-metric="hours-saved" data-value="8600">
    <div class="stat-value">8,600<span class="stat-unit">小时</span></div>
    <div class="stat-label">节约工程师时间</div>
  </div>
  <div class="stat-big" data-metric="coverage" data-value="12">
    <div class="stat-value">12<span class="stat-unit">个</span></div>
    <div class="stat-label">覆盖业务线</div>
  </div>
  <div class="stat-big" data-metric="satisfaction" data-value="4.6">
    <div class="stat-value">4.6<span class="stat-unit">/5</span></div>
    <div class="stat-label">用户满意度</div>
  </div>
</section>
```

```css
.stats-hero {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-8);
  padding: var(--space-12) var(--space-8);
  margin: -40px var(--space-4) var(--space-10);
  background: var(--color-bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  position: relative;
  z-index: 2;
}
@media (max-width: 768px) {
  .stats-hero { grid-template-columns: 1fr; gap: var(--space-6); }
}
.stat-big { text-align: center; }
.stat-value {
  font-size: var(--fs-6xl);
  font-weight: var(--fw-bold);
  line-height: 1;
  color: var(--color-primary);
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
}
.stat-unit {
  margin-left: var(--space-2);
  font-size: var(--fs-xl);
  font-weight: var(--fw-regular);
  color: var(--color-text-3);
}
.stat-label {
  margin-top: var(--space-3);
  color: var(--color-text-2);
  font-size: var(--fs-base);
}
```

**上浮技巧**：`margin-top: -40px` 让 stats 卡片上浮压在 hero 下沿，增加层次感。

### 3. 要点网格（Takeaway Grid）

3-6 个并列的核心结论/亮点，每个用一个图标或数字编号：

```html
<section class="takeaways">
  <header class="takeaways-header">
    <h2>核心成果</h2>
    <p>三个维度的突破</p>
  </header>
  <div class="takeaway-grid">
    <article class="takeaway">
      <div class="takeaway-icon">01</div>
      <h3>平台化</h3>
      <p>从分散脚本整合为统一平台，沉淀可复用能力 38 项</p>
    </article>
    <article class="takeaway">
      <div class="takeaway-icon">02</div>
      <h3>可观测</h3>
      <p>建立完整的效能度量体系，决策不再靠拍脑袋</p>
    </article>
    <article class="takeaway">
      <div class="takeaway-icon">03</div>
      <h3>可扩展</h3>
      <p>开放的插件架构，业务线自行接入只需 2 天</p>
    </article>
  </div>
</section>
```

```css
.takeaways { margin-bottom: var(--space-16); }
.takeaways-header { text-align: center; margin-bottom: var(--space-10); }
.takeaways-header h2 {
  margin: 0 0 var(--space-2);
  font-size: var(--fs-3xl);
  font-weight: var(--fw-bold);
}
.takeaways-header p { margin: 0; color: var(--color-text-3); font-size: var(--fs-lg); }

.takeaway-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}
@media (max-width: 768px) { .takeaway-grid { grid-template-columns: 1fr; } }

.takeaway {
  padding: var(--space-8) var(--space-6);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-1);
  border-radius: var(--radius-lg);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}
.takeaway:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}
.takeaway-icon {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: var(--fs-xs);
  font-weight: var(--fw-semibold);
  letter-spacing: 0.1em;
  margin-bottom: var(--space-4);
}
.takeaway h3 {
  margin: 0 0 var(--space-2);
  font-size: var(--fs-xl);
  font-weight: var(--fw-semibold);
}
.takeaway p {
  margin: 0;
  color: var(--color-text-2);
  line-height: var(--lh-normal);
}
```

### 4. 时间线 / 流程带

展示"我们做了什么"的时间轴，适合复盘类海报。用纯 SVG 或 flex 布局都可以：

```html
<section class="timeline">
  <h2>里程碑</h2>
  <div class="timeline-track">
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">2025.10</div>
      <div class="timeline-title">立项</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">2025.12</div>
      <div class="timeline-title">MVP 上线</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">2026.03</div>
      <div class="timeline-title">全量推广</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot timeline-dot-active"></div>
      <div class="timeline-date">2026.05</div>
      <div class="timeline-title">阶段复盘</div>
    </div>
  </div>
</section>
```

```css
.timeline-track {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  position: relative;
  margin-top: var(--space-8);
}
.timeline-track::before {
  content: "";
  position: absolute;
  top: 7px;
  left: 5%;
  right: 5%;
  height: 2px;
  background: var(--color-border-1);
  z-index: 0;
}
.timeline-item { text-align: center; position: relative; }
.timeline-dot {
  width: 16px;
  height: 16px;
  background: var(--color-bg-card);
  border: 2px solid var(--color-border-1);
  border-radius: 50%;
  margin: 0 auto var(--space-3);
  position: relative;
  z-index: 1;
}
.timeline-dot-active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px var(--color-primary-soft);
}
.timeline-date { font-size: var(--fs-xs); color: var(--color-text-3); }
.timeline-title { margin-top: 2px; font-weight: var(--fw-semibold); }
```

### 5. 封底引用（Quote）

海报末尾常带一条"金句"或感谢语：

```html
<section class="quote-block">
  <svg width="40" height="40" viewBox="0 0 40 40" fill="#2563eb" aria-hidden="true">
    <path d="M10 25 Q10 15, 18 10 L18 14 Q13 16, 13 22 L18 22 L18 30 L10 30 Z"/>
    <path d="M24 25 Q24 15, 32 10 L32 14 Q27 16, 27 22 L32 22 L32 30 L24 30 Z"/>
  </svg>
  <p>工具不会取代人，但用好工具的人，会远远把其他人甩在后面。</p>
  <cite>—— 团队共识</cite>
</section>
```

```css
.quote-block {
  text-align: center;
  max-width: 640px;
  margin: var(--space-16) auto;
}
.quote-block svg { margin: 0 auto var(--space-4); }
.quote-block p {
  font-size: var(--fs-2xl);
  font-weight: var(--fw-medium);
  color: var(--color-text-1);
  line-height: var(--lh-normal);
}
.quote-block cite {
  display: block;
  margin-top: var(--space-4);
  color: var(--color-text-3);
  font-style: normal;
}
```

## 风格变体

海报不只一种感觉。根据内容选择合适的风格：

### 暗色商务（默认推荐，适合汇报场景）

- Hero 用深色渐变（`#0f172a` → `#1e293b`）
- 主色用蓝 `#2563eb` 或青 `#0ea5e9`
- 数字/标题用 #ffffff，正文用 `#cbd5e1`

### 浅色专业（适合产品发布、方案展示）

- 整体浅灰底 `#f8fafc`
- 强调色 `#2563eb`
- 大留白，组件之间 `--space-16` 以上
- 装饰元素极少

### 暖色人文（适合年度总结、团队故事）

- 背景米黄/暖灰（`#fef3c7` 透明度很低，或 `#faf5f0`）
- 主色琥珀 `#f59e0b` 或暖橙
- 字体行高更松（`1.85`）

## 动效（克制使用）

海报可以用一点进场动效增加质感，但范围必须极小：

```css
@keyframes hero-fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero > *          { animation: hero-fade-up 500ms ease-out both; }
.hero-badge        { animation-delay: 0ms; }
.hero-title        { animation-delay: 80ms; }
.hero-subtitle     { animation-delay: 160ms; }
.hero-meta         { animation-delay: 240ms; }

@media (prefers-reduced-motion: reduce) {
  .hero > * { animation: none; }
}
```

**禁止**：滚动视差、鼠标跟踪光标、粒子背景、typewriter 打字机效果。

## 常见失误

- **Hero 太矮**：留白不够时整个海报就塌了。padding 给足，至少 `--space-20` 上下。
- **数字没有 tabular-nums**：数字跳动/高度不齐。统一加 `font-variant-numeric: tabular-nums`。
- **takeaway 卡片太多**：超过 6 个就不是海报了，是仪表盘。
- **主色用太多**：全屏蓝色块会疲劳。主色只在 1-2 处强调（hero 按钮、stats 数字），其他位置靠灰度和留白区分。
- **忘记移动端**：海报的大字号在手机上会撑破视口。`@media (max-width: 768px)` 要把 5xl/6xl 降到 3xl/4xl。
- **文字放进图片**：别把"2026 年成果"做成 PNG，Claude 后续想修改标题就无能为力了。
