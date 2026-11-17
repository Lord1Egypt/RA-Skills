# data-role 标注规范（吃样式的接口）

19 种 CSS 用 `[data-role="xxx"]` 属性选择器匹配元素。`apply_style.py` 会自动调
html-golive 的 tagger 给常见元素打标（从 class / 标签名推断），但**手写 HTML 时主动按
语义打标，命中率最高、样式最准**。

## 两层 CSS 分工（务必理解）

- **布局层**（easy-html `assets/layout_base.css`，由 `apply_layout.py` 注入）：
  居中容器、卡片网格、模块间距、留白、圆角、表格排版、响应式。**只管布局，不碰配色**。
- **皮肤层**（19 套主题 CSS，由 `apply_style.py` 注入）：
  配色、字体、边框色、阴影、渐变。**只管视觉属性，明文禁止写布局**。

两层都靠 `data-role` 匹配元素，各管一层、不冲突。**生成骨架后两步都要做**：
先 `apply_layout.py`（布局）→ 再 `apply_style.py`（皮肤）。漏了布局层 = 页面贴边无留白。

## 核心原则（生成 HTML 骨架时遵守）

1. **只产语义结构 + data-role，不写死配色/背景** —— 配色交给皮肤层，布局交给布局层。
   - ❌ 不要 `style="background:#fff;color:#333"`
   - ✅ 用 `<div data-role="card">`、`<section data-role="section">` 等语义标注
   - 用对 data-role，布局层和皮肤层会自动套上间距与配色
2. **能用语义标签就用**：`h1/h2`、`table/thead/tr/td`、`section`、`blockquote` 等
   tagger 会自动识别，但显式 `data-role` 更稳。
3. **深色样式安全**：不写死浅背景深字色，避免和 bloomberg/palace 等深色皮肤打架。

## 常用 data-role 速查（高频）

| data-role | 语义 | 用在哪 |
|-----------|------|--------|
| `container` | 页面最外层容器 | 最外 div |
| `header` | 标题条（整宽渐变横条，内容居中）| 无版式内容首选标题区 |
| `header-logo` | 标题条徽标 | emoji/图标 |
| `header-title` | 标题条主标题 | — |
| `header-meta` | 标题条元信息 | 日期/范围等 |
| `hero` | 英雄区 / Banner | 顶部大标题区（内容型大块）|
| `page-title` | 页面主标题 | h1 |
| `page-subtitle` | 副标题/描述 | 标题下说明 |
| `section` | 内容区块 | 每个章节 |
| `card-grid` | 卡片容器 | 卡片外层 |
| `card` | 单张卡片 | 卡片 |
| `card-head` | 卡片顶部行（badge+标题并排）| 让卡片元素匀称的关键 |
| `card-badge` | 卡片角标/数字徽章 | 排名/数值锚点 |
| `card-title` | 卡片标题 | — |
| `card-body` | 卡片正文 | — |
| `stat-block` | 统计卡片容器 | KPI 数字卡 |
| `stat-value` | 统计数值 | 大数字 |
| `stat-trend` | 趋势指示 | ↑↓ 同比 |
| `data-table` | 数据表格容器 | table |
| `table-header` | 表头 | thead/th |
| `table-row` | 表格行 | tr |
| `table-cell` | 单元格 | td |
| `tag-group` / `tag-item` | 标签组 / 标签 | 关键词标签 |
| `callout` | 提示/高亮块 | 重点提醒 |
| `quote` | 引用块 | blockquote |
| `progress-bar` | 进度条 | 达成率 |
| `timeline` | 时间轴 | 节奏/里程碑 |
| `step-item` | 步骤条项目 | 流程步骤 |
| `divider` | 分割线 | hr |
| `footer` | 页脚 | 底部 |

> 完整 60+ role 清单见 html-golive 的 `golive/resources/data_role_reference.md`。

## 标题区写法（header，无版式内容首选）

从 Word/Excel/Markdown 等无版式内容生成 HTML 时，标题用 `header`（整宽渐变横条 + 内容居中）：

```html
<div data-role="header">
  <span data-role="header-logo">📊</span>
  <span data-role="header-title">报告标题</span>
  <span data-role="header-meta">2025H2 ~ 2026H1 · 共 6 个月</span>
</div>
```

布局层会让横条贯穿整宽、背景渐变（主题色），内部图标+标题+元信息单行居中。

## 卡片写法（card-head 让元素匀称）

卡片把 badge + 标题包进 `card-head` 横排，下方放 body，元素紧凑匀称（不要 badge 孤立浮顶部）：

```html
<div data-role="card">
  <div data-role="card-head">
    <div data-role="card-badge">24</div>
    <div data-role="card-title">AI研发部</div>
  </div>
  <div data-role="card-body">疑似旷工 24 天，6 个月汇总最多</div>
</div>
```

## 自动推断（无需手打标的情况）

tagger 会从这些 class/标签自动推断 data-role：
- `.wrapper`/`#app`/`#root` → container
- `h1` → page-title，`.card`/`.item` → card，`table` → data-table
- `.kpi`/`.metric-card` → stat-block，`.value` → stat-value
- `blockquote` → quote，`.tag` → tag-item …

所以即使骨架用语义化 class 命名，apply_style 也能自动吃上样式。
显式 data-role 是「保险」，二者不冲突（已有 data-role 不会被覆盖）。
