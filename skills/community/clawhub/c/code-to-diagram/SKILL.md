---
name: "code-to-diagram"
description: "分析源代码逻辑，生成 Mermaid 流程图或 SVG 架构图并渲染为 PNG 图片。支持 15 种主题、5 种视觉风格、语义图形体系和 40+ 产品图标。"
version: "2.0.0"
tags: ["diagram", "mermaid", "svg", "flowchart", "visualization", "code-analysis", "architecture", "beautiful-mermaid"]
bindShells: ["ClaudeCode"]
---

# Code-to-Diagram Skill

分析指定目录或文件的源代码，提取控制流 / 数据流逻辑，输出两个文件：

1. **Markdown 文档**（`.md`）：包含图表源码和代码逻辑解释文字
2. **渲染后的 PNG 图片**（高清）

支持两种渲染引擎：

| 引擎 | 输入 | 渲染方式 | 适用场景 |
|------|------|----------|----------|
| **Mermaid**（默认） | `.mmd` | beautiful-mermaid → SVG → rsvg-convert → PNG | 流程图、时序图、类图、状态图、ER 图、XY 图 |
| **SVG** | `.svg` | rsvg-convert → PNG | 架构图、AI 系统图、需要品牌图标或定制风格的图表 |

> Mermaid 引擎默认使用 [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) 渲染，提供 15 种精美主题。
> 不支持的图表类型（gantt、mindmap、pie、journey、gitgraph）自动回退到 mmdc。

---

## 第一步 —— 读取并分析代码

使用 `Read`、`Glob`、`Grep` 工具理解代码结构，识别主要逻辑模式。

---

## 第二步 —— 选择引擎

### 使用 Mermaid 引擎

- 标准流程图、时序图、类图、状态图、ER 图、XY 图表
- 用户未要求特定视觉风格
- 快速、美观的主题化图表

### 使用 SVG 引擎

- 架构图需要产品图标（OpenAI、AWS、PostgreSQL 等）
- AI/Agent 系统图需要语义图形（六边形 Agent、圆柱向量库等）
- 用户要求特定风格（dark-terminal、blueprint、glassmorphism 等）
- 需要精细布局控制

---

## 第三步 A —— Mermaid 路径

### 生成 Mermaid 源码

根据分析结果编写 Mermaid 图表源码。

| 代码模式 | 推荐 Mermaid 图表类型 |
|---------|----------------------|
| 状态机 / 工作流 | `flowchart TD` 或 `stateDiagram-v2` |
| 类继承关系 | `classDiagram` |
| 接口 / 消息传递 | `sequenceDiagram` |
| 实体关系 | `erDiagram` |
| 简单流程 | `flowchart LR` |
| 系统架构 / 分层架构 | `flowchart TB` + `subgraph` |
| 微服务架构 | `flowchart TB` + `subgraph` 或 `C4Container` |
| 数据趋势 / 图表 | `xychart-beta` |

**语言规则**：节点标签、连线说明**必须使用中文**。代码标识符保留原文。

**曲线样式**：如需使用弧线（曲线）连接，在图表开头添加配置：
```
%%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
```
可选曲线类型：`basis`（平滑）、`monotoneX`、`monotoneY`、`stepBefore`、`stepAfter`。
> beautiful-mermaid 和 mmdc 都支持曲线配置，无需切换渲染器。

**换行规则**：节点文本中使用 `<br/>` 而非 `\n`。

**特殊字符规则**：
- 节点标签中**禁止使用双引号** `"`，直接移除或用单引号替代
- 节点标签中的括号 `()`、方括号 `[]`、花括号 `{}` 会被解析为节点形状，如需显示用全角符号替代
- 代码标识符中的点号 `.` 保留（如 `featurePut.SubTitle`）
- 冒号 `:` 在中文环境下通常安全，但避免在连线标签中使用
- `&` 符号使用 `&amp;` 转义

**节点文本简化原则**：
- 移除所有引号（单引号、双引号）
- 简化过长的变量名，保留关键信息
- 使用中文描述替代代码表达式（如 "创建者名 创建" 而非 `creator.Name + " 创建"`）

### 选择主题

16 个内置主题，根据场景推荐：

| 主题 | 类型 | 推荐场景 |
|------|------|----------|
| `markdown-preview`（默认） | 亮色 | Markdown预览、浅色背景、系统字体 |
| `github-dark` | 暗色 | GitHub README、技术文档 |
| `github-light` | 亮色 | 明亮文档、演示文稿 |
| `tokyo-night` | 暗色 | 优雅暗色、博客 |
| `tokyo-night-storm` | 暗色 | Tokyo Night 变体 |
| `tokyo-night-light` | 亮色 | Tokyo Night 亮色 |
| `catppuccin-mocha` | 暗色 | 温暖暗色 |
| `catppuccin-latte` | 亮色 | 温暖亮色 |
| `nord` | 暗色 | 冷色调、北欧风 |
| `nord-light` | 亮色 | 冷色调亮色 |
| `dracula` | 暗色 | 经典暗色 |
| `one-dark` | 暗色 | VS Code 风格 |
| `solarized-dark` | 暗色 | 经典 Solarized |
| `solarized-light` | 亮色 | 经典 Solarized 亮色 |
| `zinc-dark` | 暗色 | 极简暗色 |
| `zinc-light` | 亮色 | 极简亮色 |

**主题快速判断**：
- 用户说"暗色/dark/GitHub" → `github-dark`
- 用户说"亮色/light/明亮" → `github-light`
- 用户说"优雅/elegant" → `tokyo-night`
- 用户说"温暖/warm/mocha" → `catppuccin-mocha`
- 用户说"冷色/cold/北欧" → `nord`
- 用户说"紫色/dracula" → `dracula`
- 用户说"简约/minimal" → `zinc-dark` 或 `zinc-light`
- 用户说"Markdown预览/浅色/系统字体" → `markdown-preview`
- 默认 → `markdown-preview`

### 生成逻辑解释文字

在生成图表源码的同时，编写代码逻辑解释文字，包括：
- 代码的整体结构和主要功能
- 关键逻辑流程和数据流向
- 重要的设计模式和架构决策
- 图表中各组件的作用说明

### 写入 .mmd 文件并渲染

先用 `Write` 工具将 Mermaid 源码写入 `.mmd` 文件，然后调用：

```bash
node ~/.claude/skills/code-to-diagram/scripts/code_to_diagram.js render \
  --file <路径/diagram.mmd> \
  --theme <主题名> \
  --name <输出文件基础名> \
  --output-dir <保存目录>
```

脚本会生成两个文件：
1. `<name>.png` — 渲染后的高清 PNG 图片
2. `<name>.md` — 基础 Markdown 文档（仅包含图表源码）

然后用 `Read` 工具读取生成的 `.md` 文件，用 `Write` 工具补充代码逻辑解释文字，最终内容结构：
1. 代码逻辑解释文字（中文）
2. Mermaid 图表源码（代码块）

---

## 第三步 B —— SVG 路径

### 1. 选择风格

读取 `references/style-diagram-matrix.md` 快速选择风格，然后读取对应的风格参考文件：

| 风格 | 参考文件 | 适用场景 |
|------|----------|----------|
| Flat Icon（默认） | `references/style-1-flat-icon.md` | 文档、博客、演示 |
| Dark Terminal | `references/style-2-dark-terminal.md` | GitHub README、技术博客 |
| Blueprint | `references/style-3-blueprint.md` | 架构文档、RFC |
| Notion Clean | `references/style-4-notion-clean.md` | Notion 嵌入、Wiki |
| Glassmorphism | `references/style-5-glassmorphism.md` | 营销页、发布会 |

**风格快速判断**：
- 用户说"暗色/dark/terminal/GitHub" → Dark Terminal
- 用户说"蓝图/blueprint/工程" → Blueprint
- 用户说"简洁/clean/Notion" → Notion Clean
- 用户说"毛玻璃/glass/现代" → Glassmorphism
- 默认或"文档/博客" → Flat Icon

### 2. 生成 SVG

读取选定的风格参考文件和 `references/icons.md`，按照以下步骤生成 SVG：

1. 以风格参考文件中的 **SVG 模板** 为起点
2. 根据内容规划布局（节点位置、连线路径）
3. 使用 `references/icons.md` 中的 **语义图形** 表示不同类型的组件
4. 使用 **产品图标** 标识具体产品/服务
5. 使用 **箭头语义** 区分不同类型的数据流
6. 当使用 2+ 种箭头类型时，添加 **图例**
7. 所有文字标签使用中文

**关键约束**：
- **禁止 `@import url()`**——rsvg-convert 无法获取外部资源
- 字体通过内联 `<style>` 声明
- viewBox 根据实际内容调整

### 3. 生成逻辑解释文字

在生成 SVG 的同时，编写代码逻辑解释文字，包括：
- 代码的整体结构和主要功能
- 关键逻辑流程和数据流向
- 重要的设计模式和架构决策
- 图表中各组件的作用说明

### 4. 写入 SVG 文件并渲染

先用 `Write` 工具将 SVG 写入 `.svg` 文件，然后调用：

```bash
node ~/.claude/skills/code-to-diagram/scripts/code_to_diagram.js render \
  --engine svg \
  --file <路径/diagram.svg> \
  --name <输出文件基础名> \
  --style <风格名> \
  --output-dir <保存目录>
```

脚本会生成两个文件：
1. `<name>.png` — 渲染后的高清 PNG 图片
2. `<name>.md` — 基础 Markdown 文档（仅包含图表源码）

然后用 `Read` 工具读取生成的 `.md` 文件，用 `Write` 工具补充代码逻辑解释文字，最终内容结构：
1. 代码逻辑解释文字（中文）
2. SVG 图表源码（代码块）

---

## 第四步 —— 补充逻辑解释

脚本已生成基础 `.md` 文件（仅包含图表源码），现在用 `Read` 工具读取该文件，然后用 `Write` 工具补充代码逻辑解释文字，最终内容结构：
1. **代码逻辑解释**：用中文描述代码的整体结构、关键逻辑流程、设计模式和架构决策
2. **图表源码**：Mermaid 或 SVG 源码（放在代码块中）

### 告知用户文件路径

脚本最后一行输出 JSON，包含输出文件路径：

```json
{"md":"/path/to/diagram.md","png":"/path/to/diagram.png","engine":"mermaid","theme":"markdown-preview","renderer":"beautiful-mermaid"}
```

**重要：不要使用 `Read` 工具读取 PNG 文件来内联展示图片。** PNG 图片体积大，直接读取会消耗大量上下文窗口，极易导致超限。只需将生成的文件路径告知用户即可，例如：

> 已生成图表：
> - Markdown: `/path/to/diagram.md`
> - PNG: `/path/to/diagram.png`

用户可以自行打开文件查看图片。

---

## 语义图形速查表

使用 SVG 引擎时，根据组件类型选择对应图形（详见 `references/icons.md`）：

| 图形 | 含义 | 使用时机 |
|------|------|----------|
| 双边框圆角矩形 + ⚡ | LLM / 模型 | 大语言模型调用 |
| 六边形 | Agent / 编排器 | 自主代理、编排 |
| 圆柱体 + 内环 | 向量数据库 | Pinecone、Weaviate 等 |
| 圆柱体 | 传统数据库 | PostgreSQL、Redis 等 |
| 矩形 + ⚙ | 工具 / 函数 | API 调用、工具执行 |
| 菱形 | 决策点 | 条件判断 |
| 圆形 + 身体 | 用户 | 人类交互入口 |
| 虚线矩形 | 记忆节点 | 短期/长期记忆 |
| 水平管道 | 队列 / 消息流 | Kafka、RabbitMQ 等 |
| 小六边形 | API 网关 | 请求路由 |
| 红绿灯矩形 | 浏览器 | Web 客户端 |
| 折角矩形 | 文档 | 配置文件、日志 |

---

## 箭头语义速查表

| 类型 | 线型 | 含义 |
|------|------|------|
| 实线 2px | `stroke-width="2"` | 主数据流 |
| 虚线 1.5px | `stroke-dasharray="5,3"` | 记忆/缓存写入 |
| 点线 1.5px | `stroke-dasharray="4,2"` | 异步事件 |
| 曲线 1.5px | 贝塞尔曲线 | 反馈/循环 |

**颜色编码**：蓝=主数据流，红=错误/备选，绿=数据写入，紫=异步事件。

**规则**：使用 2+ 种箭头类型时，必须在左下角添加图例。

---

## 产品图标速查表

常用产品（完整列表见 `references/icons.md`）：

| 类别 | 产品 | 品牌色 |
|------|------|--------|
| AI/ML | OpenAI `#10A37F` · Anthropic `#D97757` · Gemini `#4285F4` · LLaMA `#0467DF` · Mistral `#FF7000` |
| RAG | LangChain `#1C3C3C` · LlamaIndex `#8B5CF6` · CrewAI `#EF4444` · Mem0 `#6366F1` |
| 向量库 | Pinecone `#1C1C2E` · Weaviate `#FA0050` · Qdrant `#DC244C` · Chroma `#FF6B35` |
| 数据库 | PostgreSQL `#336791` · MySQL `#4479A1` · MongoDB `#47A248` · Redis `#DC382D` |
| 消息队列 | Kafka `#231F20` · RabbitMQ `#FF6600` |
| 云平台 | AWS `#FF9900` · GCP `#4285F4` · Azure `#0089D6` · Docker `#2496ED` · K8s `#326CE5` |

---

## 命令行参数

```
node code_to_diagram.js render [选项]

通用选项：
  --file,       -f  <路径>      输入文件（.mmd 或 .svg）
  --content,    -c  <字符串>    Mermaid 源码（仅 mermaid 引擎）
  --name,       -n  <字符串>    输出文件基础名（默认：diagram）
  --output-dir, -o  <路径>      输出目录（默认：当前工作目录）
  --engine,     -e  <引擎>      mermaid | svg（默认：mermaid）
  --help,       -h              帮助信息

Mermaid 引擎（beautiful-mermaid，默认）：
  --theme,      -t  <主题>      16 个内置主题（默认：markdown-preview）
  --renderer        <渲染器>    auto | beautiful-mermaid | mmdc（默认：auto）
  --padding         <像素>      画布内边距（默认：40）
  --transparent                 透明背景
  --bg,         -b  <颜色>      自定义背景色（覆盖主题）
  --font            <字体>      自定义字体（默认：系统字体）

mmdc 回退选项：
  --width,      -W  <像素>      画布宽度（默认：2400）
  --height,     -H  <像素>      画布高度（默认：4000）
  --scale,      -s  <倍数>      缩放系数（默认：3）

SVG 引擎：
  --style       <风格>          flat-icon | dark-terminal | blueprint | notion-clean | glassmorphism

**图片尺寸说明**：beautiful-mermaid 和 SVG 引擎会根据图表内容自动计算最佳输出尺寸（viewBox 宽度 × 16，范围 2400-4800px），确保文字清晰可读。mmdc 渲染器使用固定的画布尺寸。
```

---

## 依赖说明

**Mermaid 引擎**：

- **beautiful-mermaid**（主要）：`npm install`（在 `scripts/` 目录下）
- **rsvg-convert**（必需）：将 SVG 转换为 PNG
- **mmdc**（可选，仅回退时需要）：处理 gantt、mindmap、pie、journey、gitgraph

**SVG 引擎**：依赖 `rsvg-convert`（来自 librsvg）。

**安装 rsvg-convert**：

```bash
# macOS
brew install librsvg

# Debian / Ubuntu
apt-get install librsvg2-bin
```

**安装 beautiful-mermaid**：

```bash
cd ~/.claude/skills/code-to-diagram/scripts
npm install
```
