---
name: fta-studio-rebuild
description: 从零重建 FTA Studio（对标 Ansys medini analyze 的故障树 FTA 绘图与分析工具）的完整工程方法与踩坑记录。当用户说"重新做这个 FTA 软件""换电脑了要重建这个工具""把故障树工具再做一遍""做个 medini 风格的 FTA 工具"，或需要给该工具加功能/修 bug（双击折叠、撤销、门符号、事件符号、底事件红点、A4 分页与分页点跳转、便携打包、.bat 打不开）时使用。内含可直接还原的源码快照、模块规格、medini 操作对齐清单、分页与打印契约、Windows 启动器与便携包规范、可执行的验证脚本。
---

# FTA Studio 重建指南

零依赖（仅 Node 内置模块）的故障树分析工具：浏览器图形编辑器 + MOCUS/BDD 精算引擎 + 多格式导入导出 + 报告生成 + 可携带打包。

## 0. 先判断走哪条路

| 用户诉求 | 走法 |
|---|---|
| "重建 / 还原这个软件" | **路径 A**：从 `assets/source/` 复制恢复，再按需修改 |
| "真的从零写一遍" | **路径 B**：按第 2 节顺序逐个模块实现 |
| "加功能 / 修 bug" | 先路径 A 还原，再改；改完必须过第 5 节验证 |
| "换个电脑继续用" | 路径 A + 第 6 节打包 |

## 1. 路径 A：直接还原（最快、最可靠）

```bash
cp -r <skill>/assets/source/*  <新项目目录>/
cd <新项目目录>
node src/launch.mjs --selftest     # 应打印 "服务就绪，自检通过"
node test/run-tests.mjs            # 应 62/62 通过
node test/test-new-features.mjs    # 应 91/91 通过
node test/_jump.mjs                # 分页/跳转契约，应"全部通过"
```

零依赖，**不需要 npm install**。Node ≥ 18（实测 24.14）。

## 2. 路径 B：从零实现的顺序与验收

按依赖顺序做，每步都能独立验证，不要跳步。

| # | 文件 | 职责 | 验收 |
|---|---|---|---|
| 1 | `src/model.mjs` | 树数据结构、节点/连接规范化、ID 生成、校验 | 能解析 DSL 得到 nodes/connections |
| 2 | `src/mocus.mjs` | 最小割集（定性，含割集阶数限制） | 2 个基本事件 OR → 2 个 1 阶割集 |
| 3 | `src/bdd.mjs` | BDD 精确概率 | 与解析解一致 |
| 4 | `src/quantify.mjs` | 门概率聚合（AND/OR/XOR/NOT/PAND/INHIBIT/VOTE）、指数/威布尔/需求型、`nodeProbs` | NOT 门 p = 1 − p_child |
| 5 | `src/api.mjs` | 统一 `analyze()` 入口，聚合上述结果 | 返回 topProb / cutSets / nodeProbs / heatmap |
| 6 | `src/interchange.mjs` | DSL / FaultTree+ XML / CAFTA / medini JSON 双向 | 往返一致 |
| 7 | `src/symbols.mjs` + `src/svg.mjs` | 门与事件几何 + 服务端 SVG 导出 | 与前端 `SYMBOLS` 几何完全一致 |
| 8 | `src/layout.mjs` + `src/paginate.mjs` | 纵向树布局、跨页拆分 | 页面切分不丢节点；分页行为符合第 4 节契约 |
| 9 | `src/report.mjs` | Markdown / HTML 报告 | 含割集表与概率 |
| 10 | `src/server.mjs` + `src/launch.mjs` | 静态服务 + `/api/*` + 启动器 | `--selftest` 通过 |
| 11 | `public/` | 前端编辑器 | 见 `references/frontend.md` |

数据模型与算法细节见 `references/architecture.md`。

## 3. 五条不可违反的硬约束

1. **前后端符号几何同源**：`public/app.js` 的 `SYMBOLS` / `eventShapePath` 与 `src/symbols.mjs` 必须几何一致，否则"屏幕上看到的"和"导出的"不是同一个东西。
2. **零依赖**：只用 Node 内置模块。不要引入 express / svg.js 之类，否则便携包还得带 node_modules。
3. **`.bat` 必须纯 ASCII + CRLF**；含中文的 `.ps1` / `.txt` 必须 UTF-8 **带 BOM**。详见 `references/windows-packaging.md`。
4. **静态资源带版本号 + 服务端 `Cache-Control: no-store`**，否则改完代码用户仍看到旧页面，会反复报"没生效"。
5. **改完必须同步到用户实际运行的那一份**：用户跑的是 `%LOCALAPPDATA%\FTA Studio\app`，不是你改的源码目录。跑 `scripts/sync-installed.ps1 -SourceDir <项目> -Restart`，否则一切努力都白费（见 `pitfalls.md` §9）。

## 4. 分页与打印契约（用户强约定，改分页前必读）

分页是**纯显示层**概念：定量计算永远基于完整原树，不存在"搬到别的页导致割集丢失"。

**① 分页点由画图人决定。** 右键事件 →「分页：从此事件另起一页」（`node.pageBreak = true`）。工具**不得**因为"本页节点少/一页装得下"就自动取消分页点。

**② 每个分页点各开一页**（用户原话："每次分页都是从新的一页开始"）。

- 同一页触发的多个分页点，按 **DFS 先序**（图中从左到右、自上而下的阅读顺序）依次分配页号；
- 分页点的子树内部若还有分页点，继续往后顺延开页；
- **绝不能**把同页的多个分页点合并进同一个下一页（这是历史 bug）；
- `continuedFrom` 记的是**真正承接的父页页号**，不是机械的"上一页"。

**③ 页间记号（ISOGRAPH / medini 惯例）**

| 记号 | 含义 |
|---|---|
| 虚线框 + `⤓ 分页 · 第 N 页` | 本页页底，该事件子树翻到第 N 页 |
| 虚线框 + `↑ 续上页 · 第 N 页` | 本页页顶事件，来自第 N 页 |
| 实线框 | 本页正常事件（**底事件绝不画虚线**） |

**④ 子事件必须齐全**：同一事件的兄弟整层一起走，不追祖先链；页首事件靠上面那条虚线说明出处。

**⑤ 跳转**：虚线标签本身就是可点胶囊（`gotoPage(N)`）；分页导航条有 `↪ 第 N 页`；右键菜单有「跳转到第 N 页」。目标页算法：页底分页点 → `pageOf[id]`（向后）；页顶承接事件 → 反查 `extraOf`（向前）。

**⑥ A4 打印导出**：逐分页点查 `pageOf` 印真实目标页（`⤓ 分页 → 第 2 页` / `↑ 续自第 1 页`），**不能统一写 `index + 1`**；标注画在框上方，需要 `topPad` 把几何整体下移，否则首行标注被 viewBox 裁掉。

数据契约见 `references/frontend.md` §9、`references/architecture.md` §9。

## 5. 验证门槛（每次改动后必跑）

```bash
node --check public/app.js
node --check src/<改动的文件>
node test/run-tests.mjs            # 62 项
node test/test-new-features.mjs    # 91 项
node test/_jump.mjs                # 分页点/跳转三场景（双分页点→3 页、单分页点回归、自动分页）
```

**渲染 / 交互类改动必须再过浏览器验证**——纯逻辑测试覆盖不到 DOM 与事件：

```bash
node <skill>/scripts/verify-ui.mjs http://127.0.0.1:8777/
node test/_ui_jump.mjs             # 设分页点 → 分页 → 点胶囊翻页 → 承接页跳回（11 项）
node test/_dot_shot.mjs            # 底事件红点：画布 + A4 导出各 7 个
```

该脚本用 `Input.dispatchMouseEvent` 产生**真实鼠标序列**（含 `clickCount=2` 的双击）。见 `references/pitfalls.md` 第 1 条：用 `dispatchEvent(new MouseEvent('dblclick'))` 会**假通过**。

## 6. 打包成可携带工具（换电脑直接用）

```powershell
powershell -ExecutionPolicy Bypass -File <skill>/scripts/build-portable.ps1 -SourceDir <项目目录> -OutDir <输出目录>
```

产出 `FTA Studio\`（内置 `runtime\node.exe`）+ zip。目标机器**免装 Node、免联网、免管理员权限**。
规范见 `references/windows-packaging.md`，启动器模板在 `assets/launchers/`。

## 7. 参考文件索引

| 文件 | 何时读 |
|---|---|
| `references/architecture.md` | 要理解数据模型、API 契约、MOCUS / BDD / 量化算法、分页 API |
| `references/frontend.md` | 要改画布渲染、布局、分页视图、拖拽、连线、撤销/重做、折叠 |
| `references/medini-parity.md` | 要对齐 medini 的图形与操作行为（含底事件红点、分页记号） |
| `references/windows-packaging.md` | 要做 .bat 启动器、便携包、安装/卸载脚本 |
| `references/pitfalls.md` | **遇到诡异现象先看这里**：已踩过的坑及根因 |

## 8. 换电脑时怎么带走

```text
# 旧机器：把整个 skill 文件夹打成 zip 带走
# 新机器：解压到  C:\Users\<用户名>\.workbuddy\skills\fta-studio-rebuild\
```

重启 WorkBuddy 后，新机器上就能凭这个 skill 直接还原软件。源码在 `assets/source/`，即使没有网络也能重建。
