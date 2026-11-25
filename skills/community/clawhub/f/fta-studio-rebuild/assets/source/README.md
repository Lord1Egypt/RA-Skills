# FTA Studio

**故障树分析工具 — 对标 Ansys medini analyze FTA 模块**

零依赖（仅需 Node.js ≥18），提供图形编辑器 + 精算引擎 + 程序化调用接口。
计算引擎已对照 **NRC FTA Handbook 标准算例**与数学解析解验证（62 项测试全部通过）。

---

## 快速开始

```bash
# 1. 启动图形编辑器（浏览器打开 http://127.0.0.1:8777/）
node src/cli.mjs serve

# 2. 分析内置示例
node src/cli.mjs example brake

# 3. 生成报告
node src/cli.mjs analyze examples/brake-system.fta --out report.md --svg tree.svg

# 4. 运行测试
node test/run-tests.mjs
```

---

## 功能对照（vs. Ansys medini analyze）

| medini analyze 能力 | FTA Studio | 说明 |
|---|---|---|
| 定性/定量 FTA 图形编辑器 | ✅ | SVG 画布，7 种事件 + 6 种逻辑门 |
| 顶级/中间/基本/房屋/未开发/条件事件 | ✅ | 全部支持 |
| AND / OR / XOR / k-n 表决门 | ✅ | 另加 PAND、INHIBIT、NOT |
| 自动布局 | ✅ | 有序树算法 |
| **跨页 / 多图（multiple diagrams）** | ✅ | 画图人设分页点，每个分页点各开一页；页底虚线 + 页码胶囊可点跳转 |
| **A4 分页打印导出** | ✅ | 每页一张 A4，页底/页顶虚线标注「第 N 页」，可直接另存 PDF |
| **事件符号细节** | ✅ | 底事件左缘红色圆点 + 文字左对齐（与 medini 一致） |
| 最小割集（阶数可调） | ✅ | MOCUS + 位掩码优化 |
| 概率截断 | ✅ | `--truncation` |
| BDD 精确概率 | ✅ | 非相干树精确解 |
| 稀有事件近似 / MCUB 上界 | ✅ | 对比与校核 |
| 时间相关计算 | ✅ | 指数/威布尔/维修/监控模型 |
| 多种概率模型 | ✅ | fixed/exponential/weibull/demand/repairable/monitored |
| Birnbaum / Criticality / FV | ✅ | BDD 精确求值 |
| RAW / RRW / 结构重要度 | ✅ | 完整六项 |
| 定量热力图 | ✅ | 绿→黄→红，按重要度着色 |
| 路径分析 / 大纲视图 | ✅ | 含子树折叠 |
| 与 FMEA 追溯 | ✅ | `ref=FMEA-001` 字段 |
| 单点失效识别 | ✅ | 1 阶割集自动标注警告 |
| 自动分页 FTA 报告 | ✅ | Markdown / HTML，含图形 |
| 敏感度分析 | ✅ | What-if 模拟 |
| 图形导出 | ✅ | SVG（IEC 61025 符号） |
| **导入 Isograph FaultTree+ XML** | ✅ | medini 原生支持格式 |
| **导入/导出 CAFTA** | ✅ | 核工业标准交换格式 |
| **medini 双向交换** | ✅ | 导出后可在 medini 直接 Import |
| SysML / FMEDA / DOORS 集成 | ❌ | 本工具聚焦 FTA 内核 |
| RBD 可靠性方块图 | ❌ | 未实现 |
| medini 专有工程包（.mdb）直读 | ❌ | 需 medini 先导出 XML |
| 项目版本管理 / 团队协作 | ❌ | 单机工具 |

---

## 架构

```
fta-studio/
├── src/
│   ├── model.mjs      数据模型 + DSL 解析/序列化 + 校验
│   ├── symbols.mjs    IEC 61025 Annex A 符号几何（前后端共用）
│   ├── mocus.mjs      MOCUS 最小割集（BigInt 位掩码）
│   ├── bdd.mjs        BDD 精确概率 + BDDSession 增量求值
│   ├── quantify.mjs   定量分析 + 重要度 + 概率模型
│   ├── paginate.mjs   跨页/多图 + 传输符号
│   ├── layout.mjs     自动布局 + 大纲
│   ├── svg.mjs        SVG 渲染 + 热力配色
│   ├── interchange.mjs FaultTree+ / CAFTA / medini 格式互操作
│   ├── report.mjs     Markdown / HTML 报告生成
│   ├── api.mjs        统一调用门面（FTAStudio）
│   ├── cli.mjs        命令行入口
│   └── server.mjs     HTTP 服务（零依赖）
├── public/            图形编辑器前端
├── examples/          工程示例
├── test/              62 项引擎测试 + 78 项新功能测试
└── AGENT_API.md       WorkBuddy 调用手册
```

**性能**：4×4×4 嵌套树（85 节点 / 1024 割集）MOCUS 约 7 ms；
BDD 单次构建 + N 次增量求值，避免重要度分析的 O(N) 重复建树。

---

## 符号规范

门与事件符号严格遵循 **IEC 61025:2006 Annex A**：

| 符号 | 几何特征 |
|---|---|
| 与门 AND | 平顶 + 半圆底 |
| 或门 OR | 弧顶 + 凹底（盾形） |
| 异或门 XOR | 或门 + 背面附加弧线 |
| k/n 表决门 | 矩形 + k/n 标签 |
| 禁门 INHIBIT | 或门 + 底部悬垂线 |
| 优先与门 PAND | 与门 + 内部横线 |
| 基本事件 | 圆 |
| 未开发事件 | 菱形 |
| 房屋事件 | 五边形 |
| 外部事件 | 圆 + 内部叉 |
| 传输符号 | 三角形 |

几何定义集中在 `src/symbols.mjs`，前后端共用 —— 屏幕上看到的与导出报告的完全一致。

---

## 跨页 / 多图

对标 medini analyze 的 *"handle large fault trees by multiple diagrams"*。

**核心设计原则：分页是显示层概念，定量计算始终基于完整原树。**

若把节点真的"搬到"另一页，该子树会与父节点断开导致割集丢失
（实测概率会从 8e-9 变成 6e-9）。因此分页只产出"页面视图树"，不改模型。

### 分页规则（画图人决定）

右键任意事件 →「分页：从此事件另起一页」，设定 `node.pageBreak`。工具栏「分页」按这些分页点切分：

- **每个分页点各开一页**；同一页的多个分页点按图中从左到右的阅读顺序依次开页
- 上一页页底保留该事件（**虚线框**）表示"此处分页"，标注 `⤓ 分页 · 第 N 页`
- 下一页页首同一事件同样虚线，标注 `↑ 续上页 · 第 N 页`
- 同一事件的子事件永远整层一起出现在同一页，不追祖先链

### 跳转

虚线标签本身就是按钮，点一下跳到该事件所在的那一页；分页导航条有 `↪ 第 N 页`；右键菜单也有「跳转到第 N 页」。

### A4 打印

「导出 → A4 分页图」，每页一张 A4（794×1123 @96dpi），虚线框旁印真实目标页（`⤓ 分页 → 第 2 页` / `↑ 续自第 1 页`），浏览器 `Ctrl+P` 另存 PDF 即可。

```js
const pag = paginateBanded(tree, { budget: 14 });
const view = buildBandedView(tree, pag, 2);   // 第 2 页
```

---

## 与 medini analyze 的互操作

medini 原生支持 **Isograph FaultTree+ 结构 XML** 与 **CAFTA XML**，
且与 FaultTree+ 可双向交换。因此：

| 方向 | 做法 |
|---|---|
| 本工具 → medini | 导出 **FaultTree+ XML**，medini 中 `Import from Isograph FaultTree+` |
| medini → 本工具 | 本工具「导入」按钮，支持 FaultTree+ XML / CAFTA XML |

**往返一致性已验证**：
```
原始       Q=1.2644e-6  割集 10
FaultTree+ Q=1.2644e-6  割集 10   ✓ 完全一致
CAFTA      Q=5.020e-4   割集 3    ✓ 完全一致
```

> **限制说明**：medini 自有工程包（`.mdb` / 项目目录）为专有数据库格式，
> 需在 medini 中先导出为 FaultTree+ XML 才能被本工具读取。
> 这是格式的客观限制。

---

## 计算方法

- **定性**：MOCUS 算法（Fussell & Vesely, 1972），位掩码加速，
  按最低置位分桶做 O(1) 子集判定与吸收剪枝
- **定量**：BDD（二叉决策图）唯一表 + apply 记忆化，对相干/非相干树均给出精确解
- **重要度**：将事件概率置 0/1 重算 BDD，得到精确敏感度

### 已验证算例

| 算例 | 期望 | 结果 |
|---|---|---|
| 串联系统 | q₁q₂q₃ | ✅ |
| 并联系统 | 1−(1−q₁)(1−q₂)(1−q₃) | ✅ |
| NRC 双泵冗余 | 8E−4 量级 | ✅ 8.2E−4 |
| 2oo3 表决 | 3q²−2q³ | ✅ |
| 3oo3 表决 | q³ | ✅ |
| XOR 非相干 | q₁(1−q₂)+(1−q₁)q₂ | ✅ |
| 吸收律 A∧(A∨B)=A | 1 个割集 | ✅ |
| 分配律 (A∨B)∧(A∨C) | {A}, {B,C} | ✅ |
| Birnbaum（串联） | q_B·q_C | ✅ |
| FV / RAW（串联） | 1.0 / 10 | ✅ |

---

## 许可

MIT