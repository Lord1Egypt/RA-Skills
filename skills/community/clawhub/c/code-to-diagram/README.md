# code-to-diagram

分析源代码逻辑，生成 Mermaid 流程图或 SVG 架构图，并渲染为高清 PNG 图片。同时生成包含代码逻辑解释的 Markdown 文档。

## 功能特性

- **双引擎渲染**：Mermaid（beautiful-mermaid）+ SVG（rsvg-convert）
- **15 种 Mermaid 主题**：github-dark、tokyo-night、dracula、nord、catppuccin-mocha 等
- **5 种 SVG 视觉风格**：Flat Icon、Dark Terminal、Blueprint、Notion Clean、Glassmorphism
- **语义图形体系**：六边形 Agent、圆柱数据库、双边框 LLM 等 12 种组件图形
- **40+ 产品图标**：OpenAI、Anthropic、PostgreSQL、Kafka、AWS 等
- **SVG 5 层自动验证**：XML 语法、标签平衡、属性引号、marker 引用、rsvg-convert 验证
- **mmdc 自动回退**：gantt、mindmap 等不支持的图表类型自动切换 mmdc 渲染

## 安装

### 前置要求

- Node.js 16+
- rsvg-convert（必需，用于 SVG → PNG 转换）

```bash
# macOS
brew install librsvg

# Debian / Ubuntu
apt-get install librsvg2-bin
```

### 安装 Skill

```bash
git clone https://github.com/zhouchang1988/code-to-diagram.git ~/.claude/skills/code-to-diagram
cd ~/.claude/skills/code-to-diagram/scripts
npm install
```

也可以克隆到任意目录后创建软链接：

```bash
git clone https://github.com/zhouchang1988/code-to-diagram.git ~/projects/code-to-diagram
ln -s ~/projects/code-to-diagram ~/.claude/skills/code-to-diagram
cd ~/projects/code-to-diagram/scripts && npm install
```

## 使用方法

### Mermaid 引擎

```bash
# 基本用法（默认 github-dark 主题）
node scripts/code_to_diagram.js render -f diagram.mmd -n output -o ./output

# 指定主题
node scripts/code_to_diagram.js render -f diagram.mmd -t tokyo-night -n output -o ./output

# 直接传入 Mermaid 源码
node scripts/code_to_diagram.js render -c 'flowchart LR\n    A --> B' -t dracula -n output

# 透明背景
node scripts/code_to_diagram.js render -f diagram.mmd --transparent -n output

# 自定义背景色
node scripts/code_to_diagram.js render -f diagram.mmd --bg "#1a1b26" -n output

# 强制使用 mmdc 渲染
node scripts/code_to_diagram.js render -f diagram.mmd --renderer mmdc -n output
```

### SVG 引擎

```bash
# 暗色终端风格
node scripts/code_to_diagram.js render -e svg -f arch.svg --style dark-terminal -n output

# Notion 简洁风格
node scripts/code_to_diagram.js render -e svg -f arch.svg --style notion-clean -n output
```

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--file` | `-f` | 输入文件（.mmd 或 .svg） | — |
| `--content` | `-c` | Mermaid 源码字符串 | — |
| `--name` | `-n` | 输出文件基础名 | diagram |
| `--output-dir` | `-o` | 输出目录 | 当前目录 |
| `--engine` | `-e` | mermaid \| svg | mermaid |
| `--theme` | `-t` | 16 个内置主题 | markdown-preview |
| `--style` | — | SVG 风格（5 种） | flat-icon |
| `--renderer` | — | auto \| beautiful-mermaid \| mmdc | auto |
| `--transparent` | — | 透明背景 | — |
| `--bg` | `-b` | 自定义背景色 | — |
| `--padding` | — | 画布内边距（px） | 40 |
| `--font` | — | 自定义字体 | 系统字体 |

### 可用主题

**暗色：** github-dark · tokyo-night · tokyo-night-storm · catppuccin-mocha · nord · dracula · one-dark · solarized-dark · zinc-dark

**亮色：** github-light · tokyo-night-light · catppuccin-latte · nord-light · solarized-light · zinc-light · markdown-preview

## 支持的图表类型

| 代码模式 | 推荐图表类型 | 引擎 |
|---------|-------------|------|
| 状态机 / 工作流 | `flowchart TD` / `stateDiagram-v2` | Mermaid |
| 类继承关系 | `classDiagram` | Mermaid |
| 接口 / 消息传递 | `sequenceDiagram` | Mermaid |
| 实体关系 | `erDiagram` | Mermaid |
| 系统架构 / 分层 | `flowchart TB` + `subgraph` | Mermaid |
| 数据趋势 / 图表 | `xychart-beta` | Mermaid |
| AI/Agent 系统图 | 语义图形 + 产品图标 | SVG |
| 需要品牌图标 | 产品图标 + 风格化 | SVG |

## 输出文件

每次渲染生成两个文件：

- `<name>.md` — 基础 Markdown 文档（仅包含图表源码，由脚本生成）
- `<name>.png` — 渲染后的高清 PNG 图片（由脚本生成）

Claude 会读取生成的 `.md` 文件，补充代码逻辑解释文字后，最终内容包含：
1. 代码逻辑解释（中文）
2. 图表源码（Mermaid 或 SVG）

终端 JSON 输出：

```json
{"md":"/path/to/diagram.md","png":"/path/to/diagram.png","engine":"mermaid","theme":"markdown-preview","renderer":"beautiful-mermaid"}
```

## 依赖

- **beautiful-mermaid** — Mermaid 渲染引擎（主要，`npm install` 安装）
- **rsvg-convert** — SVG → PNG 转换（必需，系统包）
- **mmdc** — Mermaid CLI（可选，仅回退时使用）

## License

MIT
