# 模板：下钻分析报告（Drill-Down）

**尺寸**：1200×auto（自适应高度） | **风格**：Neo-Brutalism

> 用于展示逐层深入的分析过程：全局概览 → 维度拆解 → 交叉下钻 → 根因建议。
> 每层之间用引导条连接，说明"发现了什么 → 接下来分析什么"。

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; background: #F5E6D3;
  padding: 40px; font-family: "PingFang SC", Arial, sans-serif;
}

/* ── 报告标题 ── */
.report-header {
  text-align: center; margin-bottom: 36px;
}
.report-title {
  font-size: 28px; font-weight: 900; color: #1A1A1A;
  letter-spacing: 2px;
}
.report-subtitle {
  font-size: 14px; color: #888; margin-top: 6px;
}

/* ── 层级标签 ── */
.level-section { margin-bottom: 0; }
.level-tag {
  display: inline-block;
  background: #1A1A1A; color: #FFD700;
  padding: 4px 14px; border-radius: 6px;
  font-size: 13px; font-weight: 800;
  margin-bottom: 10px; letter-spacing: 1px;
}

/* ── 卡片容器 ── */
.section-card {
  background: #FFFDF7; border: 4px solid #1A1A1A;
  border-radius: 12px; padding: 28px;
  box-shadow: 6px 6px 0 #1A1A1A;
}
.section-title {
  font-size: 20px; font-weight: 800; color: #1A1A1A;
  margin-bottom: 18px;
}

/* ── 下钻引导条 ── */
.drilldown-connector {
  display: flex; align-items: center; justify-content: center;
  padding: 18px 0; position: relative;
}
.connector-line {
  width: 4px; height: 30px; background: #E17055;
  position: absolute; top: 0; left: 50%;
}
.connector-arrow {
  width: 0; height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 12px solid #E17055;
  position: absolute; bottom: 24px; left: calc(50% - 6px);
}
.connector-text {
  background: #E17055; color: #FFFDF7;
  padding: 6px 20px; border-radius: 20px;
  font-size: 13px; font-weight: 700;
  position: relative; top: 16px;
  box-shadow: 3px 3px 0 #1A1A1A;
}

/* ── L0: KPI 卡片行 ── */
.kpi-row { display: flex; gap: 16px; }
.kpi-card {
  flex: 1; text-align: center; padding: 18px 12px;
  border: 2px solid #E8E0D8; border-radius: 10px;
  background: #FDFAF5;
}
.kpi-value { font-size: 36px; font-weight: 900; }
.kpi-label { font-size: 13px; color: #888; margin-top: 4px; }
.kpi-change { font-size: 12px; margin-top: 2px; }
.c-coral { color: #E17055; }
.c-mint  { color: #45B7AA; }
.c-gold  { color: #D4A017; }
.c-olive { color: #5B8C5A; }
.up   { color: #4CAF50; }
.down { color: #FF3B4F; }

/* ── L1: 维度柱状图区 ── */
.dim-chart-area {
  display: flex; gap: 20px; margin-top: 12px;
}
.dim-chart {
  flex: 1; background: #FDFAF5; border: 2px solid #E8E0D8;
  border-radius: 10px; padding: 18px;
}
.dim-chart-title {
  font-size: 14px; font-weight: 700; color: #1A1A1A;
  margin-bottom: 12px;
}
.bar-row {
  display: flex; align-items: center; margin-bottom: 8px;
  font-size: 13px;
}
.bar-label { width: 80px; color: #555; text-align: right; padding-right: 10px; }
.bar-track { flex: 1; height: 22px; background: #F0E8DD; border-radius: 4px; overflow: hidden; position: relative; }
.bar-fill  { height: 100%; border-radius: 4px; }
.bar-value { width: 60px; text-align: right; font-weight: 700; padding-left: 8px; }
.fill-coral { background: #E17055; }
.fill-mint  { background: #45B7AA; }
.fill-gold  { background: #D4A017; }
.fill-olive { background: #5B8C5A; }
/* 异常标注 */
.anomaly-badge {
  display: inline-block;
  background: #FF3B4F; color: #fff;
  font-size: 11px; font-weight: 700;
  padding: 1px 6px; border-radius: 3px;
  margin-left: 4px;
}

/* ── L2: 交叉分析热力格 ── */
.cross-grid {
  display: grid; gap: 3px; margin-top: 12px;
}
.cross-cell {
  padding: 10px; text-align: center; font-size: 13px;
  font-weight: 700; border-radius: 4px; color: #1A1A1A;
}
.cross-header {
  background: #1A1A1A; color: #FFD700;
  font-size: 12px; font-weight: 800;
}
.heat-1 { background: #FDE8E1; }
.heat-2 { background: #F9C4B4; }
.heat-3 { background: #F09E87; }
.heat-4 { background: #E17055; color: #fff; }
.heat-5 { background: #C0392B; color: #fff; }

/* ── L3: 根因诊断卡 ── */
.root-cards { display: flex; gap: 16px; margin-top: 12px; }
.root-card {
  flex: 1; border: 3px solid #1A1A1A; border-radius: 10px;
  overflow: hidden; box-shadow: 4px 4px 0 #1A1A1A;
}
.root-header { padding: 12px 16px; font-size: 15px; font-weight: 800; }
.root-header-red   { background: #FF3B4F; color: #fff; }
.root-header-green { background: #4CAF50; color: #fff; }
.root-header-blue  { background: #45B7AA; color: #fff; }
.root-body { background: #FFFDF7; padding: 16px; }
.root-body li {
  font-size: 13px; color: #333; line-height: 1.9;
  list-style: none; padding: 4px 0;
  border-bottom: 1px solid #F0E8DD;
}
.root-body li:last-child { border-bottom: none; }
.cause-tag {
  display: inline-block; background: #1A1A1A; color: #FFD700;
  padding: 1px 8px; border-radius: 3px;
  font-size: 11px; font-weight: 700; margin-right: 4px;
}
</style>
</head>
<body>

<!-- ═══════════ 报告标题 ═══════════ -->
<div class="report-header">
  <p class="report-title">营销渠道 ROI 下钻分析</p>
  <p class="report-subtitle">数据范围：2025-07 ~ 2025-12 ｜ 数据源：MySQL + PostgreSQL + Excel</p>
</div>

<!-- ═══════════ Level 0: 全局概览 ═══════════ -->
<div class="level-section">
  <span class="level-tag">L0 全局概览</span>
  <div class="section-card">
    <p class="section-title">核心 KPI</p>
    <div class="kpi-row">
      <div class="kpi-card">
        <p class="kpi-value c-coral">¥228万</p>
        <p class="kpi-label">总营收</p>
        <p class="kpi-change up">↑ 34% MoM</p>
      </div>
      <div class="kpi-card">
        <p class="kpi-value c-mint">5,000</p>
        <p class="kpi-label">总订单</p>
        <p class="kpi-change up">↑ 22%</p>
      </div>
      <div class="kpi-card">
        <p class="kpi-value c-gold">2.8</p>
        <p class="kpi-label">整体 ROI</p>
        <p class="kpi-change up">↑ 0.3</p>
      </div>
      <div class="kpi-card">
        <p class="kpi-value c-olive">¥732</p>
        <p class="kpi-label">客单价</p>
        <p class="kpi-change down">↓ 5%</p>
      </div>
    </div>
  </div>
</div>

<!-- ── 下钻引导 ── -->
<div class="drilldown-connector">
  <div class="connector-line"></div>
  <div class="connector-arrow"></div>
  <span class="connector-text">发现：整体 ROI 2.8，但各渠道差异大 → 按渠道拆解</span>
</div>

<!-- ═══════════ Level 1: 维度拆解 ═══════════ -->
<div class="level-section">
  <span class="level-tag">L1 维度拆解</span>
  <div class="section-card">
    <p class="section-title">各渠道 ROI 对比</p>
    <div class="dim-chart-area">
      <!-- 左图：渠道 ROI -->
      <div class="dim-chart">
        <p class="dim-chart-title">ROI 排名</p>
        <div class="bar-row">
          <span class="bar-label">短视频</span>
          <div class="bar-track"><div class="bar-fill fill-coral" style="width:92%"></div></div>
          <span class="bar-value c-coral">4.6 <span class="anomaly-badge">↑ 最高</span></span>
        </div>
        <div class="bar-row">
          <span class="bar-label">直播带货</span>
          <div class="bar-track"><div class="bar-fill fill-mint" style="width:74%"></div></div>
          <span class="bar-value">3.7</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">社交媒体</span>
          <div class="bar-track"><div class="bar-fill fill-gold" style="width:60%"></div></div>
          <span class="bar-value">3.0</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">内容种草</span>
          <div class="bar-track"><div class="bar-fill fill-olive" style="width:52%"></div></div>
          <span class="bar-value">2.6</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">搜索引擎</span>
          <div class="bar-track"><div class="bar-fill fill-coral" style="width:44%"></div></div>
          <span class="bar-value">2.2</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">邮件营销</span>
          <div class="bar-track"><div class="bar-fill fill-mint" style="width:30%"></div></div>
          <span class="bar-value">1.5</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">线下活动</span>
          <div class="bar-track"><div class="bar-fill fill-gold" style="width:22%"></div></div>
          <span class="bar-value down">1.1 <span class="anomaly-badge">↓ 最低</span></span>
        </div>
      </div>
      <!-- 右图：渠道获客成本 -->
      <div class="dim-chart">
        <p class="dim-chart-title">获客成本 (CAC)</p>
        <div class="bar-row">
          <span class="bar-label">线下活动</span>
          <div class="bar-track"><div class="bar-fill fill-coral" style="width:95%"></div></div>
          <span class="bar-value down">¥320 <span class="anomaly-badge">↑ 最高</span></span>
        </div>
        <div class="bar-row">
          <span class="bar-label">邮件营销</span>
          <div class="bar-track"><div class="bar-fill fill-mint" style="width:72%"></div></div>
          <span class="bar-value">¥245</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">搜索引擎</span>
          <div class="bar-track"><div class="bar-fill fill-gold" style="width:55%"></div></div>
          <span class="bar-value">¥186</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">内容种草</span>
          <div class="bar-track"><div class="bar-fill fill-olive" style="width:42%"></div></div>
          <span class="bar-value">¥142</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">社交媒体</span>
          <div class="bar-track"><div class="bar-fill fill-coral" style="width:35%"></div></div>
          <span class="bar-value">¥118</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">直播带货</span>
          <div class="bar-track"><div class="bar-fill fill-mint" style="width:25%"></div></div>
          <span class="bar-value">¥85</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">短视频</span>
          <div class="bar-track"><div class="bar-fill fill-gold" style="width:18%"></div></div>
          <span class="bar-value up">¥62 <span class="anomaly-badge">↓ 最低</span></span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ── 下钻引导 ── -->
<div class="drilldown-connector">
  <div class="connector-line"></div>
  <div class="connector-arrow"></div>
  <span class="connector-text">发现：短视频 ROI 最高(4.6)、线下活动最低(1.1) → 交叉渠道×地区深入</span>
</div>

<!-- ═══════════ Level 2: 交叉下钻 ═══════════ -->
<div class="level-section">
  <span class="level-tag">L2 交叉下钻</span>
  <div class="section-card">
    <p class="section-title">渠道 × 地区 ROI 热力图</p>
    <div class="cross-grid" style="grid-template-columns: 100px repeat(5, 1fr);">
      <!-- 表头 -->
      <div class="cross-cell cross-header"></div>
      <div class="cross-cell cross-header">华东</div>
      <div class="cross-cell cross-header">华南</div>
      <div class="cross-cell cross-header">华北</div>
      <div class="cross-cell cross-header">西南</div>
      <div class="cross-cell cross-header">华中</div>
      <!-- 短视频 -->
      <div class="cross-cell cross-header">短视频</div>
      <div class="cross-cell heat-5">5.8</div>
      <div class="cross-cell heat-4">4.9</div>
      <div class="cross-cell heat-3">3.8</div>
      <div class="cross-cell heat-4">4.5</div>
      <div class="cross-cell heat-3">4.0</div>
      <!-- 直播带货 -->
      <div class="cross-cell cross-header">直播带货</div>
      <div class="cross-cell heat-4">4.2</div>
      <div class="cross-cell heat-3">3.5</div>
      <div class="cross-cell heat-3">3.6</div>
      <div class="cross-cell heat-2">2.8</div>
      <div class="cross-cell heat-3">3.1</div>
      <!-- 社交媒体 -->
      <div class="cross-cell cross-header">社交媒体</div>
      <div class="cross-cell heat-3">3.4</div>
      <div class="cross-cell heat-3">3.2</div>
      <div class="cross-cell heat-2">2.5</div>
      <div class="cross-cell heat-2">2.6</div>
      <div class="cross-cell heat-2">2.8</div>
      <!-- 线下活动 -->
      <div class="cross-cell cross-header">线下活动</div>
      <div class="cross-cell heat-1">1.4</div>
      <div class="cross-cell heat-1">1.2</div>
      <div class="cross-cell heat-1">0.8</div>
      <div class="cross-cell heat-1">0.9</div>
      <div class="cross-cell heat-1">1.0</div>
    </div>
  </div>
</div>

<!-- ── 下钻引导 ── -->
<div class="drilldown-connector">
  <div class="connector-line"></div>
  <div class="connector-arrow"></div>
  <span class="connector-text">发现：短视频×华东 ROI 达 5.8，线下×华北仅 0.8 → 分析根因与建议</span>
</div>

<!-- ═══════════ Level 3: 根因与建议 ═══════════ -->
<div class="level-section">
  <span class="level-tag">L3 根因 &amp; 建议</span>
  <div class="section-card">
    <p class="section-title">诊断结论与行动建议</p>
    <div class="root-cards">
      <div class="root-card">
        <div class="root-header root-header-red">根因分析</div>
        <div class="root-body">
          <ul>
            <li><span class="cause-tag">主因</span>短视频渠道年轻用户占比 72%，复购率高</li>
            <li><span class="cause-tag">主因</span>线下活动场地成本占预算 60%，转化周期长</li>
            <li><span class="cause-tag">辅因</span>华东地区电商渗透率领先，线上渠道天然优势</li>
          </ul>
        </div>
      </div>
      <div class="root-card">
        <div class="root-header root-header-blue">数据佐证</div>
        <div class="root-body">
          <ul>
            <li><span class="cause-tag">数据</span>短视频渠道 18-30 岁用户占 72%，高于均值 45%</li>
            <li><span class="cause-tag">数据</span>线下活动 CPA ¥320，是短视频的 5.2 倍</li>
            <li><span class="cause-tag">数据</span>华东短视频转化率 8.3%，全国均值 5.1%</li>
          </ul>
        </div>
      </div>
      <div class="root-card">
        <div class="root-header root-header-green">行动建议</div>
        <div class="root-body">
          <ul>
            <li><span class="cause-tag">P0</span>短视频预算上调 30%，重点投华东、西南</li>
            <li><span class="cause-tag">P1</span>线下活动缩减至一线城市，预算降 40%</li>
            <li><span class="cause-tag">P2</span>直播带货复制短视频打法，测试华东市场</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

</body>
</html>
```

---

## 适用场景

- 需要逐层深入的分析报告（营销归因、异常排查、业绩复盘）
- 需要展示"发现 → 深入 → 结论"的分析逻辑链
- 演示 AI 的分析推理过程

---

## 结构说明

| 层级 | 标签 | 用途 | 典型图表 |
|------|------|------|----------|
| L0 全局概览 | `level-tag` | 顶层 KPI，一眼看全貌 | KPI 卡片 |
| L1 维度拆解 | `level-tag` | 按单一维度拆解，标注异常 | 柱状图 + `anomaly-badge` |
| L2 交叉下钻 | `level-tag` | 两个维度交叉，定位热点 | 热力格 / 分组柱状图 |
| L3 根因建议 | `level-tag` | 根因诊断 + 行动计划 | 诊断三栏卡片 |

层与层之间用 `drilldown-connector` 连接，`.connector-text` 写明下钻依据。

---

## 使用方法

1. 复制 HTML 代码
2. 根据实际分析结果替换每一层的数据
3. **重点修改** `.connector-text`：写清每一步的下钻发现和理由
4. L1 的 `anomaly-badge` 标注值得深入的异常点
5. L2 的热力格颜色用 `heat-1` ~ `heat-5`（浅到深）
6. L3 的 `cause-tag` 标注根因权重（主因/辅因/数据/P0-P2）
7. 合成到总报告后截图

---

## 自定义层数

不是所有分析都需要 4 层。可以灵活裁剪：

| 场景 | 推荐层数 | 说明 |
|------|----------|------|
| 简单趋势查询 | L0 + L1 | 概览 + 维度拆解即可 |
| 多维对比分析 | L0 + L1 + L2 | 加交叉下钻 |
| 完整归因分析 | L0 ~ L3 | 四层全用 |
| 问题排查 | L0 + L1 + L3 | 跳过 L2，直接定位根因 |
