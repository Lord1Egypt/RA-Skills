# 真图表（Chart.js）使用指南

由 `apply_layout.py` 注入的 `chart_helper.js` 提供。**数据密集 / 需要真坐标轴的场景**
（趋势折线、多系列柱状、占比饼图、雷达对比）用真图表，比 CSS 组件更省心、更准确。

## 用法：放一个 canvas + data-eh-chart

在 HTML 里放 `<canvas>`，用 `data-eh-chart` 属性写配置 JSON。助手会自动渲染。
**canvas 必须放在一个有高度的容器里**（否则 Chart.js 高度塌陷）。

```html
<div style="height:320px;margin:20px 0">
  <canvas data-eh-chart='{
    "type": "line",
    "title": "近 6 个月 DAU 趋势",
    "labels": ["1月","2月","3月","4月","5月","6月"],
    "datasets": [{"label":"DAU(万)","data":[120,135,128,150,162,180]}]
  }'></canvas>
</div>
```

## 支持的 type
| type | 用途 |
|------|------|
| `line` | 趋势 |
| `area` | 趋势（带填充，视觉更重） |
| `bar` | 对比/排名（多系列分组） |
| `doughnut` / `pie` | 占比构成 |
| `radar` | 多维对比 |

## 多系列示例（柱状）
```html
<div style="height:340px">
  <canvas data-eh-chart='{
    "type":"bar",
    "labels":["Q1","Q2","Q3","Q4"],
    "datasets":[
      {"label":"线上","data":[60,65,70,75]},
      {"label":"线下","data":[40,35,30,25]}
    ]
  }'></canvas>
</div>
```

## 占比饼图
```html
<div style="height:300px">
  <canvas data-eh-chart='{
    "type":"doughnut",
    "labels":["写死HTML","TemplateAPI","Supabase","BIData"],
    "datasets":[{"data":[15,35,30,20]}]
  }'></canvas>
</div>
```

## 关键约束
- **JSON 必须合法**：用单引号包 `data-eh-chart`，内部用双引号；数字不加引号。
- **容器要有高度**：用 `<div class="eh-chart-box">`（默认 300px，`.eh-chart-sm`=240px / `.eh-chart-lg`=360px），由 viz_components.css 提供；或自己包 `<div style="height:XXXpx">`。
- **配色自动**：助手从主题 `--primary` 取主色 + 一组和谐辅助色，深浅主题自适应，**不要在配置里写死颜色**（除非数据分类必须固定色）。
- **CDN 多源兜底**：`chart_helper.js` 的 `CDN_SOURCES` 依次尝试 jsdelivr / cloudflare / unpkg / fastly 四个公网源，单源失败自动切换；全失败时显示「图表加载失败」占位，不整页空白。
  > 💡 离线/私有网络环境可在引入脚本前设 `window.EH_CHART_CDN = ["https://你的镜像/chart.umd.min.js"]` 指定自建源。
- **截图安全**：图表渲染不依赖滚动/入场动画，puppeteer fullPage 截图正常。
  > ⚠️ 部分容器化浏览器对 canvas 截图有捕获延迟，截图偶发空白≠渲染失败；用浏览器 `evaluate` 查 `canvas.width>0 && window.Chart` 确认真实渲染状态。

## 🎯 可视化选型决策表（重要）
| 场景 | 选 | 不要用 |
|------|-----|--------|
| 单个/少量关键数字 | CSS 大数字卡（KPI）| — |
| 1-2 项达成率/占比 | CSS 进度条/环 | — |
| **离散对比/排名（≤6 项）** | **CSS 雅致血条（eh-bars）** | ❌ Chart.js bar（粗实色柱不雅致）|
| 2-4 段构成占比 | CSS donut 或 Chart.js doughnut | — |
| **时间序列趋势** | **Chart.js line/area** | ❌ 血条（血条是离散排名语义，画趋势是错的）|
| **多系列时间对比** | **Chart.js 多 line** | ❌ 血条 |
| 多维雷达 | Chart.js radar | — |
| 数据点多（>6）的占比 | Chart.js | — |

**核心规则**：
1. **时间维度（趋势）→ 折线/面积图**，绝不用血条（血条无法表达"走势"，只能表达"谁大谁小"）。
2. **离散对比（排名）→ 雅致血条**，不用 Chart.js bar（血条更精致，柱状图粗笨）。
3. **小差异数据用血条时做「区间映射」**：如出勤率都在 93~97%，直接按 95% 算 width 四条几乎一样长；应映射到 `(值-下限)/(上限-下限)` 放大视觉差异（width 标注真实值在条外）。

## CSS 组件 vs 真图表怎么选
| 场景 | 选 |
|------|-----|
| 单个/少量关键数字 | CSS 大数字卡（VIZ_COMPONENTS.md）|
| 1-2 项达成率/占比 | CSS 进度条/环 |
| 少量排名对比（≤6项） | CSS 横向对比条 |
| 2-4 段构成占比 | CSS donut 或 Chart.js doughnut |
| **多点趋势（折线/面积）** | **Chart.js line/area** |
| **多系列分组柱状** | **Chart.js bar** |
| **多维雷达** | **Chart.js radar** |
| **数据点多（>6）的占比/对比** | **Chart.js** |

> 经验：静态、少量、强调「设计感」→ CSS 组件；动态坐标、多数据点、强调「准确读数」→ Chart.js。
> 一个页面两者可混用，但同页图表类型别堆太多（≤5 种，保持可读）。
