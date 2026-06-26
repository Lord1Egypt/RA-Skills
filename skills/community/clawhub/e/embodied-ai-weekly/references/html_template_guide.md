# HTML 报告风格规范 — 具身智能周报

## 视觉风格定义

### 调色板（CSS 变量）

```css
:root {
  --bg: #0B0E14;          /* 主背景 */
  --bg2: #10141E;         /* 次背景 */
  --card: #141824;        /* 卡片背景 */
  --card2: #1A1F2E;       /* 卡片内嵌背景 */
  --border: #1E2537;      /* 边框 */
  --border2: #252D40;     /* 次级边框 */
  
  /* 主题色 */
  --indigo: #6366F1;
  --indigo-l: #818CF8;
  --cyan: #06B6D4;
  --cyan-l: #67E8F9;
  --neon: #10B981;
  --neon-l: #6EE7B7;
  --amber: #F59E0B;
  --amber-l: #FCD34D;
  --rose: #F43F5E;
  --purple: #A855F7;
  --purple-l: #D8B4FE;
  
  /* 文字 */
  --text: #E2E8F0;
  --text-2: #94A3B8;
  --text-3: #64748B;
}
```

### 字体栈

```css
font-family: -apple-system, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
```

---

## 必要动画

```css
@keyframes flow {
  0%   { background-position: 0% 50% }
  50%  { background-position: 100% 50% }
  100% { background-position: 0% 50% }
}
@keyframes pulse {
  0%, 100% { opacity: .6; transform: scale(1) }
  50%       { opacity: 1; transform: scale(1.05) }
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px) }
  to   { opacity: 1; transform: translateY(0) }
}
@keyframes scan {
  0%   { transform: translateX(-100%) }
  100% { transform: translateX(300%) }
}
```

---

## Header Hero 区

```html
<header>
  <!-- 背景光晕球 -->
  <div class="hero-orb orb-1"></div>
  <div class="hero-orb orb-2"></div>
  
  <div class="header-inner">
    <!-- 期号徽章 -->
    <div class="vol-badge">🤖 Embodied AI Weekly · Vol.<YEAR>-<WEEK></div>
    
    <!-- 渐变主标题 -->
    <h1>本周核心洞察标题<br>副标题</h1>
    
    <p class="subtitle">一句话摘要</p>
    
    <!-- 日期信息条 -->
    <div class="date-row">
      <div class="date-chip">📅 报告周期 <span><DATE_START> → <DATE_END></span></div>
      <div class="date-chip">🔬 ArXiv监测 <span>cs.RO + cs.CV</span></div>
    </div>
  </div>
  
  <!-- Executive Summary 框 -->
  <div class="exec-wrap">
    <div class="exec-label">💡 Executive Summary · 一周导读</div>
    <p class="exec-text">一周导读正文（200字内）</p>
    <!-- 关键词标签 -->
    <div class="kw-row">
      <span class="kw i">关键词1</span>
      <span class="kw c">关键词2</span>
      <span class="kw n">关键词3</span>
    </div>
  </div>
</header>
```

**Hero 光晕球 CSS：**
```css
.hero-orb { position:absolute; border-radius:50%; filter:blur(80px); pointer-events:none; }
.orb-1 { width:600px; height:600px; top:-200px; left:-150px;
  background:radial-gradient(circle,rgba(99,102,241,.18),transparent 70%);
  animation:pulse 8s ease-in-out infinite }
.orb-2 { width:500px; height:500px; top:-100px; right:-100px;
  background:radial-gradient(circle,rgba(6,182,212,.15),transparent 70%);
  animation:pulse 6s ease-in-out infinite 2s }
```

---

## Stats Cards 统计卡片区

```html
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-val sv-i">31</div>
    <div class="stat-label">ArXiv 收录论文</div>
    <div class="stat-badge sb-up">↑ 7方向覆盖</div>
  </div>
  <div class="stat-card">
    <div class="stat-val sv-c">30+</div>
    <div class="stat-label">GitHub 仓库追踪</div>
    <div class="stat-badge sb-new">本周新增 N 个</div>
  </div>
  <!-- 更多卡片... -->
</div>
```

**颜色变体：**
- `.sv-i` → indigo（论文类）
- `.sv-c` → cyan（GitHub 类）
- `.sv-n` → neon（正向数据）
- `.sv-a` → amber（金融/融资）

---

## ArXiv 分布条形图（纯 CSS 实现）

```html
<div class="trend-chart">
  <div class="tc-title">细分方向论文分布</div>
  <div class="bar-list">
    <div class="bar-item">
      <span class="bar-label">🤖 VLA / 多模态</span>
      <div class="bar-track">
        <div class="bar-fill bf-c" style="width:72%"></div>
      </div>
      <span class="bar-count">10</span>
      <span class="bar-note">代表性论文简述</span>
    </div>
    <!-- 更多条目... -->
  </div>
</div>
```

**条形颜色：**
- `.bf-i` → indigo 渐变（感知）
- `.bf-c` → cyan 渐变（VLA）
- `.bf-n` → neon 渐变（操控）
- `.bf-a` → amber 渐变（世界模型）
- `.bf-r` → rose 渐变（sim-to-real）
- `.bf-p` → purple 渐变（记忆/长视野）

**动画初始化（JS）：**
```javascript
const bars = document.querySelectorAll('.bar-fill');
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const el = e.target;
      const w = el.style.width;
      el.style.width = '0';
      requestAnimationFrame(() => setTimeout(() => { el.style.width = w }, 50));
      obs.unobserve(el);
    }
  });
}, { threshold: .3 });
bars.forEach(b => { b.style.width = '0'; obs.observe(b); });
```

---

## 论文卡片（精选深度解读）

```html
<div class="paper-card">
  <div class="paper-card-top"></div>  <!-- 顶部彩色横条 -->
  <div class="paper-card-body">
    <div class="paper-num">精选论文 01 · cs.RO · YYYY-MM-DD</div>
    <h3>论文标题（中文）</h3>
    <div class="paper-tags">
      <span class="ptag pt-i">方向标签</span>
      <span class="ptag pt-c">方法标签</span>
    </div>
    <div class="section-mini">核心问题</div>
    <p>问题描述</p>
    <div class="section-mini">技术方案</div>
    <p>方法描述</p>
    <div class="insight">
      <strong>⚡ 核心洞察：</strong>为什么这篇论文重要
    </div>
    <div class="paper-link-row">
      <a class="plink pl-i" href="https://arxiv.org/abs/XXXX" target="_blank">📄 ArXiv</a>
      <a class="plink pl-c" href="https://github.com/..." target="_blank">💾 GitHub</a>
    </div>
  </div>
</div>
```

---

## 论文完整列表（表格）

```html
<div class="paper-table-wrap">
  <div class="pt-header">
    <h3>📋 本周论文完整索引</h3>
    <span class="pt-badge">共 N 篇</span>
  </div>
  <table class="pt">
    <thead>
      <tr>
        <th>#</th>
        <th>论文标题</th>
        <th class="hide-m">方向</th>
        <th class="hide-m">核心价值点</th>
        <th>链接</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>01</td>
        <td class="td-title">论文标题</td>
        <td class="td-dir hide-m"><span class="ptag pt-i">VLA</span></td>
        <td class="td-val hide-m">50字以内核心贡献</td>
        <td class="td-link"><a href="...">→ Paper</a></td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## GitHub 热榜卡片（Top 3）

```html
<div class="hot-repos">  <!-- grid-template-columns: repeat(3, 1fr) -->
  <div class="hot-card">
    <div class="hot-rank hr-1">🥇</div>
    <h3>owner/repo-name</h3>
    <div class="repo-org">组织 · 分类</div>
    <p>仓库描述与本周亮点</p>
    <span class="star-badge">★ 13.2k</span>
    <span class="week-badge">↑ +680 本周</span>
    <a class="repo-link" href="..." target="_blank">→ github.com/...</a>
  </div>
</div>
```

---

## GitHub 仓库矩阵（3列分类网格）

```html
<div class="dim-label dl-algo">🧠 算法框架</div>
<div class="repo-matrix">  <!-- grid-template-columns: repeat(3, 1fr) -->
  <div class="matrix-card">
    <div class="mc-cat mcc-algo">算法框架</div>
    <h4>owner/repo</h4>
    <p>简介（40字内）</p>
    <span class="mc-stars">★ XXXX</span>
    <a class="mc-link" href="..." target="_blank">→ github.com/...</a>
  </div>
</div>
```

**分类标签颜色：**
- `dl-drive` / `mcc-drive` → rose（底层驱动）
- `dl-algo` / `mcc-algo` → indigo（算法框架）
- `dl-data` / `mcc-data` → neon（数据/仿真）

---

## 卡片淡入动画（JS）

```javascript
const cards = document.querySelectorAll('.paper-card, .hot-card, .matrix-card, .stat-card');
const cardObs = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
      }, i * 60);
      cardObs.unobserve(e.target);
    }
  });
}, { threshold: .1 });
cards.forEach(c => {
  c.style.opacity = '0';
  c.style.transform = 'translateY(16px)';
  c.style.transition = 'opacity .5s ease, transform .5s ease';
  cardObs.observe(c);
});
```

---

## Footer 模板

```html
<footer>
  <div class="footer-glow"></div>
  <p>
    <strong>🤖 具身智能深度周报</strong> · Vol.<YEAR>-<WEEK> ·
    报告周期：<DATE_START> 至 <DATE_END>
  </p>
  <p>
    数据来源：ArXiv (cs.RO · cs.CV) · GitHub Topics: embodied-ai ·
    行业媒体（36氪 / 晚点LatePost）
  </p>
  <p style="font-size:12px;color:var(--text-3)">
    本报告由 AI Agent 自动采集、筛选、合成生成，核心内容经过人工审核与深度加工。
    转载请注明来源。© <YEAR> Embodied AI Weekly
  </p>
</footer>
```

---

## 响应式断点

```css
@media (max-width: 900px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .hot-repos  { grid-template-columns: 1fr; }
  .repo-matrix { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .repo-matrix { grid-template-columns: 1fr; }
  table.pt .hide-m { display: none; }
  .bar-note { display: none; }
}
```

---

## 页面整体 HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>具身智能深度周报 Vol.<YEAR>-<WEEK></title>
  <style>/* 所有 CSS 内联 */</style>
</head>
<body>

<header><!-- Hero 区 --></header>

<div class="wrap">  <!-- max-width: 1180px -->
  <section id="stats"><!-- 数据概览 --></section>
  <section id="arxiv"><!-- ArXiv 论文 --></section>
  <section id="github"><!-- GitHub 项目 --></section>
  <section id="insights"><!-- 核心洞察 --></section>
</div>

<footer><!-- Footer --></footer>

<script>/* 动画脚本 */</script>
</body>
</html>
```
