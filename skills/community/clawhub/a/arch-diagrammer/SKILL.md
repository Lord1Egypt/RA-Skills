---
name: arch-diagrammer
description: 面向架构与流程的专业制图技能。支持两种产出方式：(1) 直接生成高质量 SVG 分层架构图，提供 11+ 种风格（blue/cyber/dark/gray/green/handdrawn/mono/morandi/ocean/orange/purple/tailwind），支持精确布局与中文；(2) 使用 Mermaid / PlantUML / Graphviz 描述结构，并通过 Kroki 渲染为 SVG 或 HTML。适用于系统架构设计、方案评审与技术沟通中的可视化输出。
version: 1.0.1
author: yongsheng.hang
---

# 架构制图技能（Architecture Diagrammer）

本技能帮助在产品/前端/后端/系统等多视角下，快速产出高质量的架构图、流程图、时序图与部署图，并导出为 SVG 与 HTML。

## 产出模式

### 模式一：纯 SVG 分层架构图（推荐用于分层展示）
直接生成纯 SVG 代码，无需外部渲染，支持精确控制布局、配色、字体。

**支持 11+ 种风格**（详见 `references/svg-layered-spec.md`）：

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| blue | 深蓝商务渐变 | 企业正式 |
| cyber | 黑底霓虹色 | 科技演示 |
| dark | GitHub Dark 主题 | 开发者 |
| gray | 简约灰阶 | 文档嵌入 |
| green | 森林绿渐变 | 自然环保 |
| handdrawn | 手绘风格 | 草稿创意 |
| mono | 极简黑白直角 | 打印极简 |
| morandi | 低饱和度复古 | 设计感 |
| ocean | 海洋蓝绿 | 清新科技 |
| orange | 暖橙渐变 | 活力营销 |
| purple | 紫色渐变 | 创意高端 |
| tailwind | 多色层级区分 | 层级复杂 |

- 适用：系统分层架构、方案架构、技术全景图
- 参考：`references/svg-layered-spec.md`（风格规范、配色表、代码片段）
- 模板：`assets/svg-templates/` 目录下各风格模板

说明（重要）：
- 当用户说“生成一个 **分层架构图** / “我要的是 **svg 的分层架构图**”，默认指 **纯分层 SVG（模式一）**，而不是 “Mermaid 渲染出的 SVG”。
- 目标交付物：一个可离线打开的 `.svg` 文件（不依赖 Kroki / Mermaid CDN）。

### 模式二：Mermaid/PlantUML/Graphviz + Kroki 渲染
使用图形 DSL 描述结构，通过 Kroki 渲染为 SVG/HTML/PNG/PDF。
- 适用：流程图、时序图、C4 架构图、依赖关系图
- 参考：`references/diagram-quickstart.md`（语法速查）

## 工作流

### 画图前：先让用户选择
在开始画图前，向用户提供若干建议供选择，确认后再动手：
- **产出模式**：纯 SVG 分层图 vs Mermaid/PlantUML/Graphviz + Kroki
- **图类型**：分层架构 / 流程图 / 时序图 / C4 / 部署图 等
- **层级或复杂度**：层数按需（常见 2–5 层，不固定）、每层模块数量、是否要图例
- **风格偏好**：11+ 种风格可选（blue/cyber/dark/gray/green/handdrawn/mono/morandi/ocean/orange/purple/tailwind，见 `references/svg-layered-spec.md`）、是否图例、输出格式（.svg / .html）
用户选定或默认后，再按对应模式执行下方步骤。

### 不确定时询问
以下任一情况不确定时，**先向用户列出选项或给出建议，待确认后再动手**，不要自行假设：
- 产出模式、图类型不明确
- 层数、层级名称、每层包含哪些模块
- 配色/风格偏好、是否要图例
- 输出文件名、格式（.svg / .html）

### 纯 SVG 分层架构图
1) 按需求确定层级划分（层数不固定，常见 2–5 层，可少于 2 或多于 5）
2) 选定配色风格（11+ 种可选：blue/cyber/dark/gray/green/handdrawn/mono/morandi/ocean/orange/purple/tailwind，见 `references/svg-layered-spec.md`）
3) 基于模板绘制层级容器与子模块（画布高度、层高按层数动态调整）
4) 结构与连线（按需取舍）：
   - 只表达对沟通有价值的“直接关系/关键路径”，不必把所有区块都强行连起来
   - 允许出现不连线的独立模块/模块组（例如同层的独立域、横切能力、外部依赖清单）
   - 允许同一行放多个互不相连的大模块（并排布局），按视觉平衡与阅读顺序灵活排布
5) 添加箭头连线与标注（只画必要的流向与依赖，并用最少文字说明）
6) 添加图例
7) 对照 `references/architecture-checklist.md` 自检
8) 版式检查（避免重叠）：
   - 层级标题与子模块之间至少预留 8-12px
   - 子模块与层级容器底部至少预留 10-16px
   - 同层/同一行可并排多个独立模块组：组间留足间距，避免交叉线，必要时用小标题/分组框增强可读性
   - 图例不要贴底，必要时增加画布高度（`<svg height="...">`）并下移图例
9) 编码检查（避免中文乱码）：
   - 输出文件声明 UTF-8：`<?xml version="1.0" encoding="UTF-8"?>`
   - **推荐**：中文一律使用 XML 数字字符引用（`&#xXXXX;`），不依赖文件编码，任何 SVG 查看器都能正确显示。规则：每个汉字对应 `&#x` + 其 Unicode 码点（4 位十六进制）+ `;`，例如「权限」→ `&#x6743;&#x9650;`。详见 `references/svg-layered-spec.md` 的「中文编码与乱码修正」。
   - 若已用裸中文且出现乱码，可整体重写为数字字符引用，或用脚本按 UTF-8 重写文件（避免局部编辑混入非 UTF-8 字节）。

### Mermaid/PlantUML/Graphviz
1) 明确目标与范围：业务目标、上下文、关键约束
2) 选择图类型：C4（Context/Container/Component）、流程图、时序图、部署图
3) 起稿与迭代：从粗到细，命名统一、边界清晰
4) 渲染与导出：使用 `scripts/render_kroki.py` 生成 SVG 或 HTML
5) 质量检查：对照 `references/architecture-checklist.md` 自检

## 快速开始
- 语法速查与范例：见 `references/diagram-quickstart.md`
- 质量检查清单：见 `references/architecture-checklist.md`
- 以下命令默认假定本 skill 安装在 `~/.cursor/skills/arch-diagrammer/`

### 渲染为 SVG（Kroki）
```bash
python3 "$HOME/.cursor/skills/arch-diagrammer/scripts/render_kroki.py" \
  --type mermaid --format svg \
  --in your_diagram.mmd --out out.svg
```

### 渲染为 HTML（可直接在浏览器打开）
```bash
python3 "$HOME/.cursor/skills/arch-diagrammer/scripts/render_kroki.py" \
  --type plantuml --format html \
  --in your_diagram.puml --out out.html
```

### C4 架构图（使用 Kroki 内置 C4 支持）
```bash
python3 "$HOME/.cursor/skills/arch-diagrammer/scripts/render_kroki.py" \
  --type c4plantuml --format svg \
  --in your_c4.puml --out out.svg
```
Kroki 内置 C4-PlantUML 宏，源文件**不需要** `!includeurl` 引用 C4 库。

### JSON API 模式
当纯文本 POST 遇到特殊字符问题时，加 `--json` 切换为 JSON POST（`POST /` + JSON body）：
```bash
python3 "$HOME/.cursor/skills/arch-diagrammer/scripts/render_kroki.py" \
  --type graphviz --format svg --json \
  --in your_diagram.dot --out out.svg
```

说明：
- `--type` 支持 Kroki 全部 28 种图类型：`actdiag` | `blockdiag` | `bpmn` | `bytefield` | `c4plantuml` | `d2` | `dbml` | `ditaa` | `erd` | `excalidraw` | `graphviz` | `mermaid` | `nomnoml` | `nwdiag` | `packetdiag` | `pikchr` | `plantuml` | `rackdiag` | `seqdiag` | `structurizr` | `svgbob` | `symbolator` | `tikz` | `umlet` | `vega` | `vegalite` | `wavedrom` | `wireviz`
- 别名：`dot`→graphviz、`c4`→c4plantuml、`vega-lite`→vegalite
- `--format` 支持：`svg` | `png` | `pdf` | `jpeg` | `html`（可由 `--out` 后缀自动推断）
- `--json`：使用 JSON POST API（`POST /` + `{"diagram_source":...}`），适用于包含特殊字符的复杂图
- `--kroki-url`：指定私有 Kroki 实例；或用环境变量 `KROKI_URL`（默认 `https://kroki.io`）
- `--list-types`：列出全部支持的图类型
- 输入来源：`--in` 文件或标准输入（省略 `--in` 时从 stdin 读取）

### 渲染为 SVG（本地 Mermaid CLI，避免 Kroki 失败）
当 Kroki 返回 403/限流（常见于公共服务）时，可改用本地渲染：
```bash
npx -y @mermaid-js/mermaid-cli -i your_diagram.mmd -o out.svg
```

## 产出建议
- 命名清晰、一致：系统、服务、模块、接口、数据流命名统一
- 图例与边界：提供清晰图例；明确系统边界、外部依赖与信任区
- 分层与分视图：按 C4 层次逐步细化，避免一图承载过多信息
- 可复用：将公共元素抽为模板/片段，便于复用与演进

## 参考
- **纯 SVG 风格规范**：`references/svg-layered-spec.md`（11+ 种风格配色、布局、代码片段）
- **分层架构模板**：`assets/svg-templates/` 目录下各风格模板
- **Mermaid/PlantUML/Graphviz 语法**：`references/diagram-quickstart.md`
- **质量检查清单**：`references/architecture-checklist.md`
- **HTML 预览模板**：`assets/html/mermaid-standalone.html`

