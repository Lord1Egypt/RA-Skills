# 前端：渲染与交互

## 1. 结构

```html
<main class="canvas-wrap">
  <div class="canvas-scroll" id="scroll">
    <svg id="canvas"><g class="zoom"> … </g></svg>
  </div>
  <!-- 浮层（图例、计数）放 canvas-wrap 下，不随内容滚动 -->
</main>
```

缩放通过 `svg.width/height = L.w * zoom` + 固定 `viewBox` 实现；`svgPoint(ev)` 用 `getBoundingClientRect` 反算坐标，天然兼容缩放。

## 2. 布局（`computeLayout`）

```js
const LAY = { w: 152, h: 44, rowGap: 84, colGap: 22 };
```

1. `index(tree)` → `{ map, kids, hasKids }`（`kids` 由 connections 派生）
2. 找根：优先 `type === 'top'`，其次无入边节点
3. `widthOf(id)`：叶子宽 = `LAY.w`；否则子树宽之和
4. `place(rootId, 0, 0)`：先序遍历，子节点水平居中排布
5. 归一化到左内边距 `PAD = 36`，叠加 `state.offsets` 的手动拖拽偏移（钳制 ≥ 2）
6. 计算：
   ```js
   p.outY  = p.y + LAY.h;          // 事件框底边 = 连线起点
   p.gateY = p.outY + HG + 3;      // 门体中心：框下方，留间隙（medini 风格）
   p.gateX = p.x + LAY.w / 2;
   ```
   门的位置**不要**贴在框底边上，否则符号会压在边框上。

**折叠**在布局层处理：

```js
const collapsed = new Set(t.nodes.filter((n) => n.collapsed).map((n) => n.id));
```

⚠️ 不要写成 `n.collapsed && n.id !== rootId` —— 那会让"双击顶事件无效"（历史 bug）。

## 3. 渲染顺序（`render()`）

```
清空 → <defs><marker id="arw"> → g.zoom
  → 连线（含 link-hit 透明加粗层）
  → 节点（形状 / 底事件红点 / 文本 / 编号 / Q 值 / 折叠徽标 / 分页胶囊 / 连线端口）
  → 门（仅当该节点有出边）
  → 选中虚线框 → 新节点橙色高亮环
  → 分页页眉（可选）
  → 设置 svg width/height/viewBox
  → 历史快照 histPush()
```

连线：`p.gateX` 与 `q.cx` 差值 < 1 时画直线，否则走折线，拐点 `my = p.gateY + HG + 7`（**在门体下方**，避免横线穿过门）。

编号装饰：`state.showIds`（默认 `true`，medini 默认显示），矩形下方的编号小框；关闭时 Q 标签居中到节点下方。

折叠徽标：节点右下角 `+N`（N = 全部后代数，`countDescendants` 递归）。

## 4. 事件绑定（关键）

```js
shapeEl.addEventListener('pointerdown', (ev) => startDrag(ev, id));
shapeEl.addEventListener('contextmenu', (ev) => openCtx(ev, id));
// 不要绑 dblclick —— 见下
```

### 双击折叠必须手写判定

`startDrag` 会立即 `render()`，而 `render()` 执行 `svg.innerHTML = ''` **重建整个画布**，第一次点击的 DOM 被销毁 → 第二次点击落在新元素上 → **浏览器不会触发原生 `dblclick`**。

```js
let lastDown = { id: null, t: 0 };

function startDrag(ev, id) {
  const now = performance.now();
  if (lastDown.id === id && now - lastDown.t < 420) {
    lastDown = { id: null, t: 0 };
    state.dragging = null;
    toggleCollapse(id);      // 双击 → 折叠/展开
    return;                  // 不进入拖拽
  }
  lastDown = { id, t: now };
  … 正常拖拽 …
}
```

门（`.gate-hit`）可以保留原生 `dblclick`：点门不触发 render，DOM 未重建。

## 5. 撤销 / 重做

快照式，不逐个改造调用点：

```js
const HIST = { stack: [], idx: -1, max: 150, restoring: false };
histSnapshot() = JSON.stringify({ tree: state.tree, offsets: state.offsets });
```

- 在 `render()` **末尾**调用 `histPush()`：与上一快照不同才压栈 → 所有改动自动被记录
- `state.dragging` / `state.linking` 期间跳过；拖拽只在 `pointerup` 记一次
- 初始化完成（含自动载入示例）后调 `histReset()` 把当前状态设为唯一基线，否则"刚打开就能撤销到空树"
- 快捷键 `Ctrl+Z` / `Ctrl+Y` / `Ctrl+Shift+Z`；输入框内不拦截（`isTextEditing`）

## 6. 交互清单

| 操作 | 行为 |
|---|---|
| 拖动节点 | 写 `state.offsets[id]`，叠加在自动布局上 |
| 右侧圆点拖出 | `startLink` → `pointerup` 命中目标节点 → `addConnection` |
| 右键节点 | 上下文菜单：插入子事件 / 设门 / 计算概率 / 评估故障树 / 折叠子树 / 整理子树 / 布尔表达式 / 删除 |
| 双击节点或门 | 折叠 / 展开子树（叶子节点则打开属性） |
| Delete | 删除选中节点 |
| 滚轮 / 按钮 | 缩放 |

`addConnection` 必须拦截：自身连接、重复连接、**成环**（`isInSubtree(to, from)`）。

## 7. 样式要点

```css
:root{
  --ev-text:#1a1a1a;   /* medini 黑字 */
  --ev-bd:#333333;     /* 细黑边框 */
  --canvas:#ffffff;
}
.nshape{fill:#fff;stroke:var(--ev-bd);stroke-width:1.1}
```

- 静态资源引用带版本号：`app.js?v=NN`，每次改动 +1
- 服务端同时下发 `no-store`，双保险

底事件红点（medini 风格）：

```css
.basic-dot{fill:#e01b24;stroke:#9c1a1a;stroke-width:.7}
```

绘制规则：**只有 `type === 'basic'`** 的节点画红点，位置在椭圆左缘（`cx - w*0.4 + 9`, `cy`），半径 3.5；该节点的文字改为 `text-anchor:start` 从红点右侧起排，用 `fitCanvasLabel(name, 可用宽度, 11.5)` 截断。其余事件类型文字仍居中。

导出端（`src/svg.mjs`）必须同规则同比例（`r=4`、`fill="#e01b24"`），否则画布与 A4 打印件不一致。

## 8. 左侧调色板

事件 7 类 + 门 7 种，**图标必须互不相同**且与画布几何一致：

| 类型 | 图标 |
|---|---|
| 顶事件 / 中间事件 | 矩形（顶事件描边更粗，便于区分） |
| 基本事件 | 圆形 |
| 未开发事件 | 菱形 |
| 房屋事件 | 五边形 |
| 条件事件 | 扁椭圆 |
| 外部事件 | 圆 + 交叉线 |
| AND / OR / XOR / PAND / INHIBIT / VOTE / NOT | 拱顶门体 + 门内操作符（`&` / `≥1` / `=1` / `k/n`） |

## 9. 分页视图（画布）

分页规则本身在 `src/paginate.mjs`（见 `SKILL.md` §4），前端只负责"按页过滤 + 画记号 + 提供跳转"。

### 9.1 数据契约

`POST /api/paginate`（`options.mode = 'band'`）返回：

```js
{
  total, pages: [{ index, title, nodeCount }],
  pageOf,    // { id: 页号 }           —— 后写的页胜出：分页点取"真正展开"的那一页
  extraOf,   // { 页号: [id…] }       —— 归下一页、但本页仍要虚线画出的分页点
  contOf,    // { 页号: [id…] }       —— 本页页顶承接事件（来自上一页的分页点）
  breakCount,
}
```

前端把这些标记注入视图树，不修改原树：

```js
extra.has(id) → { ...n, __pbMarker: true, __pbExtra: true, collapsed: true }
cont.has(id)  → { ...n, __pbMarker: true, __pbCont: true }
```

### 9.2 记号

| 状态 | 画法 |
|---|---|
| `__pbExtra` | 形状 `stroke-dasharray="5 4"` + 框上方虚线 + 胶囊 `⤓ 分页 · 第 N 页` |
| `__pbCont` | 同上，胶囊文字 `↑ 续上页 · 第 N 页` |
| 普通节点 | 实线（**底事件永远不画虚线**） |

### 9.3 跳转

```js
function jumpTargetFor(id) {
  const home = state.pagination.pageOf?.[id];
  if (home && home !== state.pagination.pageIndex) return home;  // 页底分页点 → 向后
  for (const [k, ids] of Object.entries(state.pagination.extraOf || {}))
    if (Number(k) !== state.pagination.pageIndex && ids.includes(id)) return Number(k); // 页顶 → 向前
  return 0;
}
```

胶囊即按钮（`drawJumpChip()`）：有目标页时画圆角底、`cursor:pointer`、`pointerdown` 阻止冒泡（否则会触发拖拽），`click → gotoPage(N)`。另有 `#pg-jump` 导航条按钮与右键菜单「跳转到第 N 页」。

⚠️ 分页视图下 `computeLayout()` 要给所有节点 `y += 30`：胶囊画在事件框上边缘之上，首行不留白会被页眉盖住。

### 9.4 导出侧

`renderA4HTML()` 为每页生成 `pageNotes = { id: '⤓ 分页 → 第 N 页' }`，透传给 `renderSVG({ pageNotes, topPad: 16 })`；`topPad` 用 `<g transform="translate(0,topPad)">` 包住几何，避免首行标注被 viewBox 裁掉。
