# 架构与算法

## 1. 数据模型（`src/model.mjs`）

```js
tree = {
  meta:        { title, missionTime, asil?, ... },
  settings:    { missionTime, cutSetOrder, method, probabilityCutoff? },
  nodes: [
    {
      id,                  // 自动编号 N001 / FMEA-001 ...
      type,                // 见下表
      name,                // 显示名
      ref,                 // 可选，外部追溯编号（FMEA-xxx）
      component,           // 可选，所属部件
      gate,                // 逻辑门（仅可挂门的节点）
      voteK, voteN,        // VOTE 门 k/n
      prob,                // 固定概率
      probModel,           // fixed | exponential | weibull | demand | repairable | periodic
      lambda, beta, eta,   // 模型参数
      collapsed            // 前端折叠状态
    }
  ],
  connections: [{ from, to }]      // 有向，from 为上层
}
```

事件类型：`top` `intermediate` `basic` `undeveloped` `house` `condition` `external` `comment` `transfer_in` `transfer_out`
逻辑门：`AND` `OR` `XOR` `NOT` `PAND` `INHIBIT` `VOTE`

## 2. 符号几何（`src/symbols.mjs` ↔ `public/app.js`）

门体半宽 `WG=16`、半高 `HG=11`。**medini 风格：平底 + 拱顶，操作符写在门体内。**

| 门 | 路径要点 | 门内符号 |
|---|---|---|
| AND / PAND | `M -w h L -w 0 A w h 0 0 1 w 0 L w h Z` | `&` |
| OR | `M -w h L -w 0 Q 0 -h*1.62 w 0 L w h Z` | `≥1` |
| XOR | OR + 内侧平行拱 `M -w*0.62 h*0.2 Q 0 -h*1.05 w*0.62 h*0.2` | `=1` |
| INHIBIT | AND + 底部悬垂线 `M 0 h L 0 h*1.7` | `&` |
| VOTE | 矩形 2w×2h | `k/n` |
| NOT | 三角形 `M -w -h L w -h L 0 h Z` | — |

事件（节点框固定 152×44，符号按类型）：
- `top` / `intermediate` → 矩形
- `basic` → 圆（宽高比 0.8 的椭圆，保证名称可读）
- `undeveloped` → 菱形
- `house` → 五边形
- `condition` → 扁椭圆（`ry = h*0.76`）
- `external` → 圆 + 交叉线
- `transfer_in/out` → 三角形
- `comment` → 虚线矩形

> 改几何时**必须两处同步改**：`src/symbols.mjs`（导出用）和 `public/app.js`（画布用）。

## 3. 定性分析：MOCUS（`src/mocus.mjs`）

自顶向下把每个门展开成割集族，然后极小化。

- **OR 门**：子割集族取**并集**
- **AND 门**：子割集族做**笛卡尔积**（两两合并成更大割集）
- **NOT / 非相干门**：不适用纯 MOCUS，退化到 BDD
- 每步按 `settings.cutSetOrder` 剪枝：阶数超过上限的割集直接丢弃（medini 的 "Restrict cut set order up to n"）
- 极小化：若割集 A ⊆ B，则删除 B

输出：`[{ order, events: [ids], prob }]`

## 4. 定量分析：BDD（`src/bdd.mjs`）

Shannon 展开：`f = (x ∧ f|x=1) ∨ (¬x ∧ f|x=0)`，节点按 id 排序保证唯一化。
BDD 用于**精确概率**与**非相干门**（XOR/NOT/INHIBIT），先序计算：

```
P(node) = P(x)*P(high) + (1-P(x))*P(low)
```

大树上 BDD 可能膨胀，因此提供"割集近似"作为备选方法（`settings.method = auto|mocus|bdd`）。

## 5. 量化公式（`src/quantify.mjs`）

设子事件概率为 `Qi`：

| 门 | 公式 |
|---|---|
| OR | `1 - Π(1-Qi)` |
| AND | `ΠQi` |
| XOR（2 输入） | `Q1(1-Q2) + Q2(1-Q1)` |
| NOT | `1 - Q1` |
| VOTE k/n | 恰好 k 个以上发生的组合求和；近似用二项分布 |
| INHIBIT | `Q_child * Q_condition` |
| PAND | 按 AND 处理（顺序语义仅作提示，保守取值） |

事件概率模型：

| 模型 | 公式 |
|---|---|
| `fixed` | `Q = prob` |
| `exponential` | 不可靠度 `F(t) = 1 - e^{-λt}` |
| `weibull` | `F(t) = 1 - e^{-(t/η)^β}` |
| `demand` | `Q = PFD`（每次需求） |
| `repairable` | 不可用度 `Q = λT / (1 + λT)`（T 为平均修复时间） |
| `periodic` | 按监控周期折算平均不可用度 |

重要度（`importanceMeasures`）：
- **Birnbaum** `∂Q_top/∂Q_i`
- **FV（Fussell-Vesely）** `Q_i/Q_top · ∂Q_top/∂Q_i`
- **RAW** `∂Q_top/∂Q_i / Q_top`
- **RRW** `1 / (1 - FV)`

每个节点的概率汇总在 `nodeProbs: { [id]: Q }`，前端用它画 `Q=…` 标签。

## 6. 统一入口（`src/api.mjs`）

```js
analyze(tree, options) → {
  ok, topProb, cutSets, nodeProbs, heatmap,
  importance, meta, method, warnings
}
```

**易漏点**：`nodeProbs` 必须在 API 层显式透传，否则前端拿不到（曾因此调试很久）。

## 7. HTTP 契约（`src/server.mjs`）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/capabilities` | 能力自描述。**启动器的就绪探测与单实例识别都依赖它**，必须返回 `{name|product|ok|capabilities}` 之一 |
| GET | `/api/examples` | 示例列表 |
| GET | `/api/example/:name` | 示例树 + 预计算分析 |
| POST | `/api/analyze` | 定量分析 |
| POST | `/api/svg` | 服务端 SVG 导出 |
| POST | `/api/svg-a4` | A4 分页 HTML（每页一张纸，可直接打印 / 另存 PDF） |
| POST | `/api/paginate` | 分页切分；`options.mode='band'` 走手动分页点，返回 `pages/pageOf/extraOf/contOf` |
| POST | `/api/report` | Markdown / HTML 报告 |
| POST | `/api/import` | 多格式导入 |
| POST | `/api/export` | 多格式导出 |

静态资源响应头必须含：

```
Cache-Control: no-store, must-revalidate
Pragma: no-cache
Expires: 0
```

## 8. 导入导出格式（`src/interchange.mjs`）

- **DSL**：缩进表示层级，`TOP 名称` / `OR` / `BASIC A p=0.01`，便于版本管理
- **FaultTree+ XML**：medini analyze 可直接导入（首选交换格式）
- **CAFTA XML**：核工业标准
- **medini JSON**：含追溯与分析结果
- **内部 JSON**：完整模型

往返转换要保证：节点类型、门类型、概率模型、追溯编号不丢。

## 9. 分页（`src/paginate.mjs`）

分页是**显示层**能力，任何定量计算都必须基于完整原树（否则被搬走的子树会丢掉割集）。

### 9.1 `paginateBanded(tree, { budget })` —— 导出的主算法

前沿推进（ISOGRAPH 风格）：自上而下逐层展开，页底那层只画框不展开，下一页顶事件 = 本页页底事件。

手动分页点（`node.pageBreak`）走**递归切分**：

```js
function expandPage(tops, contFrom) {
  // 1) 本页逐层展开，遇到分页点：整层留在本页，分页点不展开
  // 2) 本页命中的分页点按 DFS 先序排序，逐个 expandPage([分页点], 本页页号)
  // 3) 没有命中分页点时，页底整层作为下一页顶事件（自动分页）
}
```

要点：

- **每个分页点各开一页**，绝不合并；
- `dfsIndex` 先序遍历决定同页多个分页点的先后（= 图中从左到右）；
- 页对象字段：`{ index, tops, nodes, bottom, breakNodes, continuedFrom, topNames, title, manual }`；
- 一旦本页命中手动分页点，预算限制对该页剩余部分失效（由画图人负责分页）。

### 9.2 `buildBandedView(tree, pag, index)` —— 页面视图

只含本页节点，不补祖先、不加存根（兄弟天然齐全），并在 `meta` 里给出：

```js
{ continuedFromPages: [父页号], continuedFromNames, breakMarkerIds, contMarkerIds }
```

`breakMarkerIds` = 本页页底虚线框；`contMarkerIds` = 本页页顶承接框（`index > 1`）。渲染层据此画虚线与页码胶囊。

### 9.3 `renderA4HTML(tree, { budget })`

A4 @96dpi = 794×1123，每页一张 `<section class="sheet">`，`@page { size: A4 }` + `page-break-after: always`。等比缩放 `min(1.6, cw/w, ch/h)`。虚线框旁印真实目标页（逐 id 查 `pageOf`）。

### 9.4 历史算法（保留但非默认）

`paginate()` 子树分页 / `paginateByDepth()` 层带分页 / `buildFlatView()` + 存根 —— 均为早期方案：横向并排、页间无纵向关系、存根虚线易被误读为"底事件虚线"。新代码不要再基于它们扩展。
