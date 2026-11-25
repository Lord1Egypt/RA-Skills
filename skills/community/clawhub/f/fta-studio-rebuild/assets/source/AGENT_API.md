# FTA Studio — WorkBuddy 调用手册

> 本文档是 **给 AI Agent（WorkBuddy）调用本工具的接口规范**。
> 目标：让 WorkBuddy 能在对话中直接描述故障树，拿到完整分析结果与报告。

---

## 1. 三种调用方式

| 方式 | 入口 | 适用场景 |
|---|---|---|
| **Node.js API** | `import { fta } from './src/api.mjs'` | WorkBuddy 在本地脚本中批量调用 |
| **CLI** | `node src/cli.mjs <cmd> <file>` | 生成报告文件、SVG、JSON |
| **HTTP REST** | `http://127.0.0.1:8777/api/*` | 图形编辑器 + 外部程序集成 |

三者共用同一计算引擎，**结果完全一致**。

---

## 2. 最快路径：DSL → 报告

### 2.1 Node.js API（推荐给 WorkBuddy）

```js
import { fta } from './src/api.mjs';

const dsl = `
meta title: 冷却系统失效
meta missionTime: 8760

TOP 冷却能力丧失
  OR
    INTER 冷却回路失效
      AND
        BASIC 泵停转 p=0.002 ref=FM-01 comp=冷却泵
        BASIC 管道堵塞 p=0.001 ref=FM-02 comp=管路
    BASIC 主电源失效 p=0.0002 ref=FM-05 comp=电源
`;

const r = fta.analyzeDSL(dsl, { report: 'markdown' });

console.log(r.metrics.topProb);      // 顶事件概率
console.log(r.cutSets.total);        // 割集数
console.log(r.importance[0]);       // 首要风险事件
console.log(r.report);              // 完整 Markdown 报告
```

### 2.2 CLI

```bash
# 生成 Markdown 报告
node src/cli.mjs analyze tree.fta --out report.md

# 同时导出矢量图
node src/cli.mjs analyze tree.fta --out report.md --svg tree.svg

# 输出结构化 JSON
node src/cli.mjs json tree.fta --out result.json

# 割集阶数限制 + 概率截断
node src/cli.mjs analyze tree.fta --order 3 --truncation 1e-10

# HTML 报告
node src/cli.mjs report tree.fta --html --out report.html
```

### 2.3 HTTP REST

```bash
# 启动服务
node src/cli.mjs serve --port 8777

# 分析
curl -X POST http://127.0.0.1:8777/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"dsl":"TOP 顶事件\n  OR\n    BASIC A p=0.01"}'

# Markdown 报告
curl -X POST http://127.0.0.1:8777/api/report \
  -H "Content-Type: application/json" \
  -d '{"dsl":"...","options":{"format":"markdown"}}'

# SVG 图形
curl -X POST http://127.0.0.1:8777/api/svg \
  -H "Content-Type: application/json" -d '{"dsl":"..."}'
```

---

## 3. DSL 语法速查

### 3.1 基本结构

```
meta <key>: <value>          # 元信息（可选）

<事件类型> <名称> [key=value ...]
  <逻辑门>                    # 缩进一级，紧跟事件
    <子事件>                  # 缩进两级
```

**缩进即层级**，每级 2 空格。

### 3.2 事件类型

| 关键字 | 类型 | 形状 |
|---|---|---|
| `TOP` | 顶事件 | 矩形 |
| `INTER` / `INT` | 中间事件 | 矩形 |
| `BASIC` | 基本事件 | 圆 |
| `UNDEV` | 未开发事件 | 菱形 |
| `HOUSE` | 房屋事件 | 五边形 |
| `COND` / `CONDITION` | 条件事件 | 圆角矩形 |
| `EXT` / `EXTERNAL` | 外部事件 | 带对角线矩形 |
| `TIN` / `TOUT` | 传输符号 | 三角形 |
| `COMMENT` | 注释 | 虚线框 |

未标注类型时：**顶层默认为 TOP，子节点默认为 BASIC**。

### 3.3 逻辑门

`AND`（与） `OR`（或） `XOR`（异或） `PAND`（优先与）
`INHIBIT`（禁门，条件为最后一个输入） `NOT`（非门）
`VOTE k/n`（表决门，至少 k/n 成立）

> ⚠ **门必须单独占一行**，且位于其作用事件之下：
> ```
> TOP 顶事件
>   AND          ← 作用于 TOP
>     BASIC A
>     BASIC B
> ```

### 3.4 事件属性

| 属性 | 含义 | 示例 |
|---|---|---|
| `p` / `prob` | 固定概率 q | `p=1e-3` `p=0.5%` |
| `lambda` / `lam` | 失效率 (/h) | `lambda=3e-9` |
| `beta` / `shape` | 威布尔形状参数 | `beta=2` |
| `n` / `demands` | 需求次数 | `n=1000` |
| `dp` | 单次需求失效率 | `dp=1e-6` |
| `tmr` | 平均修复时间 (h) | `tmr=8` |
| `ti` | 监控周期 (h) | `ti=100` |
| `ref` | 追溯编号（FMEA/需求） | `ref=FMEA-001` |
| `comp` | 所属部件 | `comp=制动泵` |
| `fm` | 失效模式 | `fm=卡滞` |
| `desc` | 描述（需引号） | `desc="主缸压力不足"` |
| `owner` | 责任人 | `owner=张工` |

**概率模型自动推断**：写了 `tmr` → 可修复；写了 `ti` → 周期监控；
写了 `n`/`dp` → 需求型；写了 `lambda` → 指数分布；否则固定概率。

### 3.5 meta 字段

```
meta title: 故障树标题
meta project: 项目名称
meta standard: ISO 26262
meta missionTime: 100      # 任务时间(h)
meta author: 分析师
meta date: 2026-10-15
meta description: 分析说明
```

---

## 4. 分析结果结构

```jsonc
{
  "ok": true,
  "meta": { "title": "...", "missionTime": 8760 },
  "validation": { "ok": true, "errors": [], "warnings": [] },
  "metrics": {
    "topProb": 2.035e-4,        // 顶事件概率（主结果）
    "topProbMethod": "BDD 精确解",
    "topProbUpper": 2.1e-4,     // MCUB 上界
    "reliability": 0.99980,
    "rareEventSum": 2.1e-4,     // 稀有事件近似
    "mcub": 2.1e-4,
    "missionTime": 8760,
    "nonCoherent": false,       // 是否含非相干门
    "bddSize": 5,
    "truncated": false,         // 割集是否被截断
    "cutSets": { "total": 3, "byOrder": {"1":1,"2":2}, "singlePoints": 1 }
  },
  "cutSets": {
    "total": 3,
    "items": [
      { "index": 1, "order": 1, "events": ["N005"], "names": ["主电源失效"], "probability": 2e-4 }
    ]
  },
  "importance": [
    {
      "rank": 1, "id": "N005", "name": "主电源失效", "component": "电源",
      "probability": 2e-4,
      "birnbaum": 0.9998,        // ∂Q(TOP)/∂q
      "criticality": 0.9828,     // q·B/Q 关键重要度
      "fussellVesely": 0.9828,   // 消除该事件的风险降幅
      "raw": 1.0,                // Q(q=1)/Q
      "rrw": null,               // 消除风险倍数 (Infinity 时为 null)
      "structureImportance": 1.0,
      "heat": 1.0                // 0~1 热力图值
    }
  ],
  "heatmap": { "N005": 1.0, "N002": 0.01 },
  "outline": [ { "depth": 0, "id": "N001", "name": "顶事件", "type": "top" } ],
  "report": "…Markdown/HTML…",   // 仅当 report 选项开启
  "svg": "<svg…>",               // 仅当 includeSVG 开启
  "timing": { "computeMs": 3 }
}
```

---

## 5. 高级功能

### 5.1 What-if 敏感度模拟

```js
fta.simulate(tree, { 'N005': 0 });   // 假设主电源零失效
// → { before, after, delta, deltaPct }
```

### 5.2 时间相关分析

```js
fta.timeCurve(tree, 20, 8760);
// → [{ t: 0, q: 0, reliability: 1 }, { t: 438, q: … }, …]
```

### 5.3 模型校验

```js
const { validation } = fta.fromDSL(dsl);
validation.errors    // 环路、缺顶事件、类型非法…
validation.warnings  // 名称为空、未设概率…
```

### 5.4 规范化 DSL

```js
fta.toDSL(tree);   // 输出标准化 DSL 文本
```

---

## 6. 计算方法与精度

| 方法 | 用途 | 说明 |
|---|---|---|
| **BDD 精确解** | 主结果（默认） | 二叉决策图，对相干/非相干树均精确 |
| **稀有事件近似** | 对比参考 | Q ≈ Σ 各最小割集概率；q 很小时误差可忽略 |
| **MCUB 上界** | 可靠性上界 | 各割集概率之和作为上界 |
| **MOCUS** | 定性割集 | Fussell-Vesely 算法，位掩码优化实现 |

**重要度**：Birnbaum、关键重要度、Fussell-Vesely、RAW、RRW、结构重要度
—— 全部通过 BDD 精确求值（将事件概率置 0/1 重算），**含非相干树**。

**已知边界**：MOCUS 在宽 OR 树上存在组合爆炸（与 KUREAS / SAPHIRE 等专业工具一致）。
超出规模时自动标记 `truncated: true`，**顶事件概率仍由 BDD 精确给出**。

---

## 7. 跨页 / 多图功能

对标 medini analyze 的 *"handle large fault trees by multiple diagrams"*。

### 7.1 设计原则

**分页是显示层概念，定量计算始终基于完整原树。**

这一点至关重要：若把节点真的"搬到"另一页，该子树会与父节点断开，
导致割集丢失（实测概率会从 8e-9 变成 6e-9）。
因此本实现中：
- `paginate()` 只产出**分页方案**（哪些节点属于哪页），不改模型
- `buildPageView(tree, pag, i)` 产出**第 i 页的视图树**，仅用于渲染/导出
- 页边界用**传输符号**（三角形）标注跳转关系，但概率恒为 0 且被排除在割集外

### 7.2 用法

```js
import { paginate, buildPageView } from './src/paginate.mjs';

const pag = paginate(tree, { maxNodes: 24, maxDepth: 5 });
// pag.pages     → [{index, title, nodes:Set, roots, continuedFrom, continuesTo}, ...]
// pag.references→ 跨页引用列表

const view = buildPageView(tree, pag, 2);   // 第 2 页的视图树
const svg  = renderSVG(view);                 // 渲染该页
```

### 7.3 HTTP API

```bash
# 计算分页方案
curl -X POST http://127.0.0.1:8777/api/paginate \
  -H "Content-Type: application/json" \
  -d '{"dsl":"...","options":{"maxNodes":24}}'

# 渲染指定页
curl -X POST http://127.0.0.1:8777/api/page-svg \
  -H "Content-Type: application/json" \
  -d '{"dsl":"...","options":{"pageIndex":2,"maxNodes":24}}'
```

---

## 8. 与 medini analyze 的格式互操作

medini 原生支持导入 **Isograph FaultTree+ 结构 XML** 与 **CAFTA XML**，
且与 FaultTree+ 之间可双向交换。因此导出 FaultTree+ XML 即可在 medini 中打开。

### 8.1 支持的格式

| 格式 | 导入 | 导出 | 说明 |
|---|---|---|---|
| **FaultTree+ XML** | ✅ | ✅ | medini 首选交换格式 |
| **CAFTA XML** | ✅ | ✅ | 核工业标准（NRC）格式 |
| **medini 交换 JSON** | ✅ | ✅ | 含追溯信息与分析结果 |
| 内部 JSON | ✅ | ✅ | 完整模型 |
| 紧凑 DSL | ✅ | ✅ | 文本，便于版本管理 |

### 8.2 往返一致性已验证

```
原始      Q=1.2644e-6  割集 10
FaultTree+ Q=1.2644e-6  割集 10   ✓ 完全一致
CAFTA      Q=5.020e-4   割集 3    ✓ 完全一致
```

### 8.3 用法

```js
import { toFaultTreePlusXML, fromFaultTreePlusXML,
         toCAFTA, fromCAFTA, importAny } from './src/interchange.mjs';

// 导出（medini 可直接 Import）
const xml = toFaultTreePlusXML(tree);          // → medini: Import from Isograph FaultTree+
const cafta = toCAFTA(tree);                    // → medini: Import CAFTA

// 导入（自动识别格式）
const r = importAny(fileContent, 'tree.xml');
// r.format → 'faulttreeplus' | 'cafta' | 'json' | 'dsl'
// r.tree, r.validation
```

### 8.4 HTTP API

```bash
# 导出
curl -X POST http://127.0.0.1:8777/api/export \
  -H "Content-Type: application/json" \
  -d '{"dsl":"...","options":{"format":"faulttreeplus"}}'

# 导入（自动识别）
curl -X POST http://127.0.0.1:8777/api/import \
  -H "Content-Type: application/json" \
  -d '{"content":"<?xml ...>","filename":"tree.xml"}'
```

### 8.5 在 medini 中打开本工具导出的文件

1. 本工具：导出 → **FaultTree+ XML**
2. medini analyze：`File → Import → Import from Isograph FaultTree+`
3. 选择该 `.xml` 文件，即可看到完整故障树结构

反向：本工具「导入」按钮支持 FaultTree+ XML / CAFTA XML，
可读取从 medini 导出的这两种格式。

> **说明**：medini 自有的工程包（`.mdb` / 项目目录）为专有数据库格式，
> 需在 medini 中先导出为 FaultTree+ XML 才能被本工具读取。
> 这是格式的客观限制，不是实现缺陷。

---

## 9. 符号规范

门与事件符号严格遵循 **IEC 61025:2006 Annex A** 几何定义，
集中在 `src/symbols.mjs`，前后端共用，保证屏幕显示与导出图形一致。

| 符号 | 几何特征 |
|---|---|
| 与门 AND | 平顶 + 半圆底 |
| 或门 OR | 弧顶 + 凹底（盾形） |
| 异或门 XOR | 或门 + 背面附加弧线 |
| k/n 表决门 | 矩形 + k/n 标签 |
| 禁门 INHIBIT | 或门 + 底部悬垂线 |
| 优先与门 PAND | 与门 + 内部横线 |
| 基本事件 | 圆 |
| 中间/顶事件 | 矩形 |
| 未开发事件 | 菱形 |
| 房屋事件 | 五边形 |
| 外部事件 | 圆 + 内部叉 |
| 传输符号 | 三角形 |

---

## 10. 图形编辑器

```bash
node src/cli.mjs serve --port 8777
```

浏览器打开 `http://127.0.0.1:8777/`

功能：
- 符号面板（7 种事件 + 6 种逻辑门，IEC 61025 标准形状）
- 拖拽节点、拖拽连线
- 自动布局（有序树算法）
- **跨页视图**：工具栏「分页」按钮，可设置每页节点数、上下翻页
- **导入**：支持 .fta / .json / .xml（自动识别 FaultTree+ / CAFTA）
- **导出**：FaultTree+ XML / CAFTA / medini JSON / SVG / JSON / DSL
- 大纲视图、子树折叠/展开
- 定量热力图（绿→黄→红，按 Birnbaum 重要度着色）
- 实时计算：最小割集、重要度排名、What-if
- 一键生成 Markdown / HTML 报告

---

## 11. WorkBuddy 集成建议

在对话中做 FTA 时，按以下流程调用：

1. **澄清建模假设** — 任务时间、基本事件概率来源（手册数据？现场统计？）、
   是否为相干树、是否需考虑共因失效
2. **生成 DSL** — 按第 3 节语法输出，先确认结构再计算
3. **校验** — `fta.fromDSL(dsl)` 检查 errors/warnings
4. **分析** — `fta.analyzeDSL(dsl, { report: 'markdown' })`
5. **解读** — 重点说明：
   - 顶事件概率与目标值的差距
   - **单一失效点**（1 阶割集）→ 系统性风险
   - 关键重要度前 3 → 改进优先级
   - 被截断时明确告知完整性限制
6. **交付** — Markdown 报告 + SVG 图形

**示例 DSL 模板**：

```js
const dsl = `meta title: ${topEvent}
meta standard: ${standard}
meta missionTime: ${t}

TOP ${topEventName}
  OR
${causes.map(c => `    BASIC ${c.name} p=${c.p} ref=${c.ref} comp=${c.component}`).join('\n')}`;
```