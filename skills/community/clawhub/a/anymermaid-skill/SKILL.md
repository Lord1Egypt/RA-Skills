---
name: anymermaid
description: |
  使用 Mermaid 语法生成图表，并通过 mmdc CLI 渲染为 SVG/PNG/PDF 文件。当用户要求创建流程图、时序图、类图、状态图、ER 图、甘特图、饼图、思维导图、时间线、Git 图、架构图、看板、象限图，或任何 Mermaid 支持的图表类型时使用此技能。当用户提到 "mermaid"、"anymermaid"、".mmd"、"mmdc"，或希望将关系、流程、架构、数据流等可视化为图表时也触发。即使用户只是说"画个图"、"画个流程图"、"画个时序图"、"做个图"而未指定工具，也应主动使用。
---

# AnyMermaid 画图技能

使用 Mermaid 的文本语法创建图表，并通过 `mmdc` CLI 工具渲染为图片文件（SVG/PNG/PDF）。

覆盖 26 种官方图表类型的完整语法参考、跨平台（macOS / Linux / Windows）命令、以及 puppeteer 沙箱、headless 环境、stdin 直渲、干跑校验等实战经验。

## 工作流程

1. **识别图表类型**：根据用户需求对照[图表类型表](#图表类型)
2. **查阅语法参考**：仅读取 `references/syntax.md` 中对应类型的章节（详见[查阅语法参考](#查阅语法参考)）
3. **决定是否落文件**：
   - **图 ≤ 15 行 且 用户不需要保留源**：直接用 [stdin heredoc](#stdin-直渲小图) 一步渲染，不落中间文件
   - **图 > 15 行 或 用户需要保留源**：将内容写入当前工作目录下的 `.mmd` 文件
4. **渲染前干跑校验**（可选但推荐，见[干跑校验](#干跑校验)）
5. **渲染为指定格式**：用 `mmdc` 命令渲染（见[渲染输出](#渲染输出)）
6. **打开结果**：见[打开结果](#打开结果)，headless 环境自动跳过
7. **保留 `.mmd` 文件**：渲染成功后保留 `.mmd` 文件，便于用户不满意时修改重渲
8. **删除中间文件**：仅当用户明确确认满意后，才删除 `.mmd` 文件

## 图表类型

根据用户意图选择图表类型。确定类型后，仅从 `references/syntax.md` 读取对应章节的语法，不需要加载其他章节。

| 用户意图 | 图表类型 | Mermaid 关键字 |
|---------|---------|----------------|
| 流程、决策、工作流 | 流程图 | `graph` / `flowchart` |
| 参与者之间的时序交互 | 时序图 | `sequenceDiagram` |
| 类/对象结构、继承关系 | 类图 | `classDiagram` |
| 状态转换、生命周期 | 状态图 | `stateDiagram-v2` |
| 数据库表与关系 | ER 图 | `erDiagram` |
| 项目排期、里程碑、任务 | 甘特图 | `gantt` |
| 占比、百分比 | 饼图 | `pie` |
| Git 分支/合并历史 | Git 图 | `gitGraph` |
| 用户体验步骤（含满意度打分） | 用户旅程图 | `journey` |
| 围绕中心主题的层级结构 | 思维导图 | `mindmap` |
| 按时间排列的事件/路线图 | 时间线图 | `timeline` |
| 2x2 战略定位 | 象限图 | `quadrantChart` |
| 软件架构（上下文/容器/组件） | C4 图 | `C4Context` 等 |
| 需求追溯 | 需求图 | `requirementDiagram` |
| 流量/能量流向 | 桑基图 | `sankey-beta` |
| 柱状图 / 折线图 | XY 图表 | `xychart-beta` |
| 分列/嵌套架构块 | 块图 | `block-beta` |
| 网络协议数据包字段 | 数据包图 | `packet-beta` |
| 任务看板（列 + 卡片） | 看板图 | `kanban` |
| 云原生系统架构 | 架构图 | `architecture-beta` |
| 多维度对比 | 雷达图 | `radar-beta` |
| 事件驱动设计 | 事件建模图 | `eventmodeling` |
| 层级占比矩形 | 树状图 | `treemap-beta` |
| 集合交集 | 韦恩图 | `venn-beta` |
| 根因分析（鱼骨图） | 石川图 | `ishikawa-beta` |
| 战略演化映射 | Wardley 地图 | `wardley-beta` |

## 查阅语法参考

`references/syntax.md` 收录了完整的图表语法，文件较长（>400 行）。为节省上下文，只加载当前需要的章节，不要整文件读入。

推荐的区间加载方法（以"用户旅程图"为例）：

1. 用 grep 定位目标章节起始行：
   ```bash
   grep -n "^## 用户旅程图" references/syntax.md
   ```
2. 用 grep 列出所有 `## ` 标题行，找到紧随目标章节之后的下一个标题，得到结束行：
   ```bash
   grep -n "^## " references/syntax.md
   ```
3. 用 read 的 `offset` / `limit` 只读取该区间：
   - `offset` = 目标章节起始行
   - `limit` = 下一章节起始行 - 目标章节起始行

`references/syntax.md` 顶部已提供目录，可先读取前 ~25 行了解章节命名，再按上述方法精确定位。

## 选择输出格式

根据用户请求判断：

- `画个流程图` / 未指定格式 → 默认 **SVG**
- `png 流程图` / `导出为 png` → PNG
- `画个甘特图，要 pdf` → PDF

SVG 为默认格式：可缩放、清晰、适合文档嵌入。

| 格式 | 扩展名 | 适用场景 |
|------|--------|---------|
| SVG | `.svg` | 默认。可缩放，任意分辨率都清晰，适合文档 |
| PNG | `.png` | 幻灯片 / 不支持 SVG 的文档场景 |
| PDF | `.pdf` | 打印场景 |

## 渲染输出

### 前置检测

渲染前必须先检测 CLI 是否已安装。**按当前操作系统选用对应命令**：

```bash
# macOS / Linux / WSL / Git Bash
command -v mmdc || which mmdc
```

```powershell
# Windows PowerShell
Get-Command mmdc -ErrorAction SilentlyContinue
```

```cmd
:: Windows cmd
where mmdc
```

- **已安装**：返回可执行路径，直接进入下一步渲染
- **未安装**：命令无输出或返回非零。此时**不要**自行执行 `npm install` 等安装命令，应停止流程并提示用户：

  > 未检测到 `mmdc`（Mermaid CLI）。请先安装后再使用本技能。任选一种：
  >
  > ```bash
  > # 全局安装（三平台通用，需要 Node.js ≥ 18）
  > npm install -g @mermaid-js/mermaid-cli
  >
  > # 免安装单次运行（每次会临时下载）
  > npx  -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.svg
  > pnpm dlx @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.svg
  > bunx @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.svg
  > ```
  >
  > 安装完成后告知我，我会继续渲染。

  等待用户确认安装完成后再继续，避免擅自改动用户环境。

> 仓库：<https://github.com/mermaid-js/mermaid-cli> ；官方文档：<https://mermaid.nodejs.cn/>

### 基本命令（跨平台）

**推荐默认参数**：渲染时始终使用 `-w 1600 -s 3`，确保输出清晰度与布局宽度。仅在用户明确指定其他值时覆盖。

> `-s`（Puppeteer 缩放）只影响位图（PNG/PDF），对 SVG 无效；`-w` 对 SVG **依然生效**——它会影响初始布局宽度，长链流程图（`flowchart LR`）尤其明显。因此 SVG 也建议带 `-w 1600`。

以下命令**在 macOS / Linux / Windows 三平台完全一致**（`mmdc` 是跨平台 Node CLI，参数与调用方式相同）：

```bash
# SVG（推荐带 -w 控制布局宽度）
mmdc -i diagram.mmd -o diagram.svg -w 1600

# PNG（推荐默认参数，确保清晰度）
mmdc -i diagram.mmd -o diagram.png -w 1600 -s 3 -b white

# PDF（自动适配图表大小）
mmdc -i diagram.mmd -o diagram.pdf -f
```

> Windows 用 PowerShell 或 cmd 都可，命令原样输入即可。仅路径分隔符需按各自 shell 惯例（PowerShell 支持 `/` 与 `\`，cmd 用 `\`）。

### stdin 直渲（小图）

图小于 ~15 行、且用户不需要保留 `.mmd` 源时，从 stdin 输入可省去创建/清理文件的开销。**shell 语法各异，选一种**：

```bash
# macOS / Linux / WSL / Git Bash（heredoc）
mmdc -i - -o diagram.svg -w 1600 <<'EOF'
graph TD
    A[客户端] --> B[负载均衡]
    B --> C[服务 1]
    B --> D[服务 2]
EOF
```

```powershell
# Windows PowerShell（here-string @'...'@ 逐字量，避免变量插值）
@'
graph TD
    A[客户端] --> B[负载均衡]
    B --> C[服务 1]
    B --> D[服务 2]
'@ | mmdc -i - -o diagram.svg -w 1600
```

```cmd
:: Windows cmd 无原生 heredoc，退回落文件的常规方式
:: 建议直接写 .mmd 文件后 `mmdc -i diagram.mmd -o diagram.svg`
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-i, --input` | 输入 `.mmd` 文件（`-` 表示从 stdin 读取） | `-i diagram.mmd` |
| `-o, --output` | 输出文件路径 | `-o diagram.svg` |
| `-t, --theme` | 主题：`default`、`forest`、`dark`、`neutral` | `-t dark` |
| `-b, --backgroundColor` | 背景色（仅 PNG/SVG） | `-b transparent` |
| `-w, --width` | 页面宽度 px（CLI 默认 800，**本技能默认 1600**） | `-w 1600` |
| `-H, --height` | 页面高度 px（默认 600） | `-H 900` |
| `-s, --scale` | Puppeteer 缩放因子（仅位图，CLI 默认 1，**本技能默认 3**） | `-s 3` |
| `-c, --configFile` | Mermaid JSON 配置文件 | `-c config.json` |
| `-C, --cssFile` | 自定义 CSS 文件 | `-C style.css` |
| `-p, --puppeteerConfigFile` | Puppeteer 启动参数（沙箱等） | `-p puppeteer-config.json` |
| `-q, --quiet` | 静默模式，不输出日志 | `-q` |
| `-f, --pdfFit` | PDF 自动缩放以适应图表（仅 PDF） | `-f` |

### 示例

```bash
# 渲染为 SVG（默认）
mmdc -i flowchart.mmd -o flowchart.svg -w 1600

# 渲染为 PNG，推荐默认参数（宽 1600，3 倍缩放）
mmdc -i flowchart.mmd -o flowchart.png -b white -w 1600 -s 3

# 渲染为 PDF，自动缩放适配
mmdc -i gantt.mmd -o gantt.pdf -f

# 静默模式，保持终端整洁
mmdc -q -i diagram.mmd -o diagram.svg
```

### 干跑校验

写完 `.mmd` 后正式渲染前，可先跑一次到临时路径快速验证语法。**注意各平台的临时目录**：

```bash
# macOS / Linux
mmdc -q -i diagram.mmd -o /tmp/anymermaid-dryrun.svg && echo OK || echo FAIL
```

```powershell
# Windows PowerShell
mmdc -q -i diagram.mmd -o "$env:TEMP\anymermaid-dryrun.svg"; if ($?) { "OK" } else { "FAIL" }
```

```cmd
:: Windows cmd
mmdc -q -i diagram.mmd -o "%TEMP%\anymermaid-dryrun.svg" && echo OK || echo FAIL
```

- `OK`：语法正确，继续用正式参数渲染
- `FAIL`：查看错误信息定位行号，修正 `.mmd` 后重跑

### 高级配置

需要自定义主题变量、布局选项或时序图设置时，创建 JSON 配置文件：

```json
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#4A90D9",
    "lineColor": "#888"
  },
  "flowchart": { "curve": "basis" }
}
```

```bash
mmdc -c config.json -i diagram.mmd -o diagram.svg
```

完整配置项见 [Mermaid 配置 Schema](https://mermaid.nodejs.cn/config/schema-docs/config.html)。

### Puppeteer 沙箱配置（Docker / CI / Linux / WSL 必备）

在 Docker、CI 或部分 Linux/WSL 环境下，Puppeteer 会因缺少沙箱权限报错：
`Failed to launch the browser process` / `No usable sandbox`。macOS 与 Windows 桌面环境**通常不需要**这项配置。

创建 `puppeteer-config.json`：

```json
{
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
```

调用时通过 `-p` 传入（三平台命令一致）：

```bash
mmdc -p puppeteer-config.json -i diagram.mmd -o diagram.svg
```

字体缺失导致中文乱码时：

- **Linux / Docker**：`apt-get install -y fonts-wqy-zenhei fonts-liberation`
- **WSL**：同 Linux，或直接使用 Windows 字体挂载
- **macOS / Windows**：系统自带中文字体，无需处理

### 处理 Markdown 文件

如果 Markdown 文件中包含 ```mermaid 代码块，`mmdc` 可以一次性提取并渲染其中所有图表：

```bash
mmdc -i document.md -o document-rendered.md
```

## 打开结果

渲染完成后打开预览。**headless / 远程环境自动跳过，仅打印绝对路径**。

### macOS / Linux / WSL（bash / zsh）

```bash
FILE=diagram.svg
if [ -n "$SSH_CONNECTION" ] || [ ! -t 1 ]; then
    echo "[headless] $(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
else
    case "$(uname -s)" in
        Darwin) open "$FILE" ;;
        Linux)  xdg-open "$FILE" 2>/dev/null || realpath "$FILE" ;;
        MINGW*|MSYS*|CYGWIN*) start "" "$FILE" ;;
    esac
fi
```

WSL2 打开 Windows 端应用时用：

```bash
cmd.exe /c start "" "$(wslpath -w diagram.svg)"
```

### Windows PowerShell

```powershell
$File = "diagram.svg"
if ([Environment]::UserInteractive -and -not $env:SSH_CONNECTION) {
    Invoke-Item $File
} else {
    Write-Host "[headless] $((Resolve-Path $File).Path)"
}
```

### Windows cmd

```cmd
start "" "diagram.svg"
```

### 平台命令速查

| 环境 | 命令 |
|------|------|
| macOS | `open <文件>` |
| Linux（有 GUI） | `xdg-open <文件>` |
| WSL2 → Windows 打开 | `cmd.exe /c start "" "$(wslpath -w <文件>)"` |
| Windows PowerShell | `Invoke-Item <文件>` 或 `ii <文件>` |
| Windows cmd | `start "" <文件>` |
| SSH / CI / 无 GUI | **跳过打开**，仅打印绝对路径 |

无论是否打开，都要打印输出文件的绝对路径，便于用户手动定位。

## 文件命名

- 基于图表内容的有意义命名：`login-flow`、`database-schema`、`deployment-architecture`
- 多词名称使用小写加连字符
- 扩展名反映格式：`login-flow.svg`、`gantt-chart.png`

## 渲染前校验

Mermaid 对语法要求严格。写入 `.mmd` 文件前先检查：

- 第一行是合法的图表关键字（`graph`、`sequenceDiagram`、`classDiagram` 等）
- 节点 ID 不含空格（用方括号/引号包裹的 label 来显示文本）
- 标签中的特殊字符用引号包裹：`A["节点 (含括号)"]`
- 箭头类型合法（`-->`、`->>`、`-->>`、`-.->`、`==>`、`-)`、`--x`）
- 流程图关键字后需跟方向（`TD`、`LR`、`BT`、`RL`）

如果 `mmdc` 报解析错误，根据错误信息定位行号、修正 `.mmd` 文件后重试；或先跑一次[干跑校验](#干跑校验)。

## 主题

用 `-t` 切换视觉主题，无需修改图表内容：

| 主题 | 适用场景 |
|------|---------|
| `default` | 默认，清爽文档风格，多数场景适用 |
| `forest` | 绿色调，自然/环保主题 |
| `dark` | 暗色幻灯片 / 夜间模式文档 |
| `neutral` | 灰度，正式 / 印刷报告 |

## 排错

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 解析错误 / unknown error | Mermaid 语法不合法 | 阅读错误信息，修正 `.mmd` 文件后重试 |
| 输出空白 | 图表关键字缺失或拼写错误 | 第一行必须以合法关键字开头 |
| 含特殊字符的标签出错 | 字符未转义 | 用引号包裹标签：`A["节点 (文本)"]` |
| 节点 ID 含空格失败 | ID 必须是单个标识符 | 用 camelCase 或下划线做 ID，文本放在 label 中 |
| Puppeteer/Chrome 启动报错 | 无头浏览器沙箱不可用 | 见 [Puppeteer 沙箱配置](#puppeteer-沙箱配置docker--ci--linux--wsl-必备) |
| 大图被截断 | 默认页面过小 | 增大 `-w` / `-H`，或用 `-s` 缩放（仅位图） |
| SVG 布局压缩变形 | 未设 `-w` | 加 `-w 1600` 提供足够画布宽度 |
| 中文乱码（Docker / Linux CI） | 无中文字体 | 安装 `fonts-wqy-zenhei` 或类似字体包 |
| Windows `mmdc` 不识别 | PATH 未更新 | 关闭当前终端重开；或用 `npx @mermaid-js/mermaid-cli` |
| Windows PowerShell 报"脚本被禁止" | 执行策略限制 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 后重试 |
