# easy-html 设计规范（DESIGN.md）

本文件是 easy-html 生成 HTML 时的**设计准则**，对齐 Refactoring UI / Apple HIG /
Anthropic frontend-design 的核心原则，并固化今天（2026-06-19）验证过的实战规范。
布局层（layout_base.css）和组件库（viz_components.css）已内置这些 token，
agent 生成骨架时按本文件选对组件 + 用对结构即可。

---

## 一、设计 token（已内置 layout_base.css `:root`）

### 间距刻度（4px 基准，杜绝散乱数值）
`--eh-s1`=4 / `--eh-s2`=8 / `--eh-s3`=12 / `--eh-s4`=16 / `--eh-s5`=24 / `--eh-s6`=32 / `--eh-s7`=48 / `--eh-s8`=64

> 规则：任何 margin/padding/gap 从刻度取值，不写 18/22/26 这种"随手数"。

### 阴影分层（双层柔阴影表达高度）
`--eh-shadow-sm`（卡片定边界）/ `--eh-shadow`（浮起）/ `--eh-shadow-lg`（弹层）

> 规则：表达"浮起/层次"用双层柔阴影，不用单层硬阴影；深色主题有 border 兜底。

### 字重层级（用字重而非字号拉层级）
`--eh-fw-normal`=400 / `--eh-fw-medium`=500 / `--eh-fw-semibold`=650 / `--eh-fw-bold`=750 / `--eh-fw-black`=850

> 规则：标题层级优先用字重对比（body 400 / 小标题 650 / 大标题 750-850），
> 字号差距控制在克制范围，避免"字号阶梯过陡"。

### 数字呈现
所有 KPI/统计/对比数值用 `font-variant-numeric: tabular-nums`（等宽数字，长短对齐）。
已内置 KPI/血条/卡片 badge/stat-value。

---

## 二、标题区规范

无版式内容（Word/Excel/Markdown）首选 `data-role="header"`：
**整宽渐变横条 + 内容居中**（图标+标题+元信息单行居中）。
不要把它做成大留白 hero 卡片（除非是内容型 landing 页）。

---

## 三、卡片规范

卡片用 `card-head`（badge+标题横排）+ `card-body`（描述）两段式，元素紧凑匀称。

**🔴 强制：card 里只要有 badge，必须把 `card-badge` + `card-title` 一起包进 `card-head`。**
否则 badge 作为 card（flex column）的直接子元素会被**拉伸成占满整行的全宽椭圆**，廉价突兀。
（layout 层已加 `align-self:flex-start` 兜底防御，但结构上仍应规范包 card-head。）

**反模式**：
- ❌ badge 不包 card-head → 全宽大椭圆色块（2026-06-19 小白科普踩过）
- ❌ badge 数字圆点孤立浮在卡片左上角、标题描述堆下方大量留白（松散不匀称）

正确结构见下方第五节示例 / DATA_ROLE.md「卡片写法」。

---

## 四、可视化选型（最重要，2026-06-19 血泪教训）

| 数据语义 | 用 | 绝不用 |
|---|---|---|
| 时间序列 / 趋势 | **Chart.js line / area** | ❌ 血条（无法表达走势）|
| 多系列时间对比 | **Chart.js 多 line** | ❌ 血条 |
| 离散对比 / 排名（≤6项）| **雅致血条 eh-bars** | ❌ Chart.js bar（粗实色不雅致）|
| 单/少量关键数字 | KPI 大数字卡 | — |
| 1-2 项达成率 | 进度条 / 进度环 | — |
| 2-4 段构成占比 | donut / Chart.js doughnut | — |
| 多维对比 | Chart.js radar | — |

**核心三原则**：
1. **趋势 → 折线/面积图**，永远不用血条画时间维度。
2. **排名 → 雅致血条**，不用 Chart.js 柱状图（柱状粗笨）。
3. **小差异血条做「区间映射」**：值都在 93~97% 时，width 按 `(值-下限)/(上限-下限)` 放大差异，
   真实值标注在条外。

详见 references/CHARTS.md（图表）+ references/VIZ_COMPONENTS.md（CSS 组件）。

---

## 五、雅致血条标准结构（不做"游戏血条"）

细轨道(10px) + 渐变填充 + 末端高光圆点 + 数值在条外独立列：

```html
<div class="eh-bars">
  <div class="eh-bar-row">
    <span class="eh-bar-name">综合职能部</span>
    <div class="eh-bar-track"><div class="eh-bar-fill" style="width:72.5%"></div></div>
    <span class="eh-bar-val">95.9%</span>
  </div>
</div>
```

**严禁**把数值塞进 `eh-bar-fill` 内（会被填充色压住）；轨道别用 22px 粗条。

---

## 六、Chart.js CDN

`chart_helper.js` 的 `CDN_SOURCES` 依次尝试 jsdelivr / cloudflare / unpkg / fastly
四个公网源，单源失败自动切到下一个，全失败时显示占位而非整页空白。
离线或私有网络环境，在引入脚本前设 `window.EH_CHART_CDN = ["https://你的镜像/chart.umd.min.js"]`
即可换成自建源。

---

## 七、特色主题特色字体（已在 html-golive 主题侧实现）

部分主题配了特色字体（非 Inter），选样式时可据此推荐：

| 主题 | 字体 | 气质 |
|---|---|---|
| newspaper | Playfair Display | 杂志衬线 |
| ink / palace | Noto Serif SC / Ma Shan Zheng（毛笔）| 中式书法 |
| steampunk | Cinzel | 复古罗马衬线 |
| cyberpunk | Rajdhani | 科技几何 |
| bloomberg | IBM Plex Mono | 金融等宽 |
| 其余 | Inter | 通用现代 |

> 字体走 fonts.font.im 公网 CDN，中文字体（Noto Serif SC/Ma Shan Zheng）首屏可能略慢。

---

## 八、不做（来自 Anthropic frontend-design 的反 AI-slop 警示，按数据报告场景取舍）

- 数据报告**不追求**自定义光标 / grain overlay / 激进不对称布局（牺牲可读性）。
- 但**避免**：纯灰平铺无层次、字号阶梯过陡、间距随手填、单层硬阴影。
- 克制 > 堆砌：质感来自间距/阴影/字重/对齐的精确，而非装饰元素的数量。
