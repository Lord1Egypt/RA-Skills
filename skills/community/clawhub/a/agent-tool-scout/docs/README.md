<h1 align="center"><img src="assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM: 给 AI 装上控制 Mac 的手</h1>

<p align="center">
  <a href="https://pypi.org/project/clam-mac/"><img src="https://img.shields.io/pypi/v/clam-mac?color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/clam-mac/"><img src="https://img.shields.io/pypi/pyversions/clam-mac" alt="Python"></a>
  <a href="https://github.com/mileszhang001-boom/cli-on-mac/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/clam-mac" alt="License"></a>
</p>

<p align="center">
  <strong>你的 Mac 上有几十个应用，但 AI 一个都碰不到。<br>
  CLAM 自动扫描、生成 CLI 接口，让任何 AI Agent 用原生方式操控一切。</strong>
</p>

<p align="center">
  <a href="#-openclaw--lobster">OpenClaw Skill</a> · <a href="#-claude-code--mcp">Claude Code MCP</a> · <a href="#-30-秒上手人类版">命令行直接用</a> · <a href="#-为什么需要-clam">对比其他方案</a>
</p>

安装后，AI Agent 能调用应用原生能力播放音乐、操作 Word、发邮件、绘制 3D 模型——无需依赖 API，无需手动写一行适配代码。

## 🆚 为什么需要 CLAM？

现有方案让 AI 控制 Mac 应用，要么**覆盖面窄**，要么**根本做不到**：

| 现有方案 | 问题 |
|---------|------|
| 手写专用接口 (MCP/Skill) | 每个应用都要有人单独开发，大多数应用根本没有 |
| 浏览器自动化 | 只能控制网页，碰不到 Music、Finder、Word 等原生应用 |
| 让 AI 直接写 AppleScript | 语法诡异，生成的脚本经常报错，输出非结构化 |

**CLAM 一次性解决了这些问题：**

| CLAM 能力 | 效果 |
|-----------|------|
| `clam scan` | AI 自动发现你 Mac 上所有可控应用 |
| `clam install <app>` | 10 秒生成完整 CLI，零配置，不需要有人提前开发 |
| `--json` 输出 | 所有命令返回结构化 JSON，AI 可直接用于推理决策 |
| `clam doctor` | 提前告诉 AI 哪些命令可靠，避免盲试出错 |

## 🦀 给你的 AI 装上虾钳

```bash
pip install clam-mac                    # 从 PyPI 安装
```

或者从源码安装：

```bash
git clone https://github.com/mileszhang001-boom/cli-on-mac.git
cd cli-on-mac
pip install -e .                        # 开发模式
```

然后根据你使用的 AI Agent 选择集成方式：

### 🦞 OpenClaw / Lobster

CLAM 生成的每个 `clam-<app>` 都是标准 shell 命令，可直接作为 Lobster pipeline step：

```yaml
# focus-mode.lobster — 一键进入专注模式
steps:
  - run: clam-music set-sound-volume 20
  - run: clam-music play
  - run: clam-finder open ~/Projects/current
```

也可以作为 OpenClaw Skill 使用——AI 自动调用 `clam scan` 发现能力、`clam install` 安装、`clam-<app>` 执行。

### 🤖 Claude Code / MCP

```bash
claude mcp add clam -- clam-mcp         # 注册 MCP Server
```

完成了。去 Claude Code 里说一句：

> "帮我把音量调到 50，然后告诉我现在在放什么歌"

AI 自动扫描应用、安装 wrapper、执行命令——你不需要输入任何命令。

### 🔧 其他 Agent 框架

CLAM 生成的是标准 CLI 工具，任何能调用 shell 命令的 Agent 都可以直接使用：

```python
# LangChain / AutoGPT / 任何框架
import subprocess, json
result = subprocess.run(["clam-music", "--json", "get-current-track"], capture_output=True, text=True)
track = json.loads(result.stdout)  # 结构化 JSON，直接用
```

## 🖐 30 秒上手（人类版）

```bash
clam scan                              # 看看有什么
clam install music                     # 装一个试试
clam-music play                        # 播放
clam-music next-track                  # 下一首
clam-music set-sound-volume 80         # 音量 80
clam-music get-current-track           # 当前曲目全部信息（JSON）
```

## 🔧 三种模式，覆盖几乎所有应用

| 模式 | 原理 | 典型应用 | 能力 |
|------|------|---------|------|
| **完整模式** | 解析 .sdef 脚本定义 | Music、Finder、Chrome、Word | 几十到几百个命令 |
| **UI Scripting** | 通过菜单点击控制 | Figma、Slack、VS Code、Spotify | 菜单里能点的都能控 |
| **基础模式** | macOS 标准套件 | 钉钉、WPS、微信 | 前置/退出/打开文件/查版本 |

安装时自动选择最佳模式，不需要手动指定。

## 📖 完整命令

```bash
clam scan              # 扫描可控应用
clam install <app>     # 安装 CLI（模糊匹配：chrome → google-chrome）
clam info <app>        # 查看能力详情
clam doctor <app>      # 检查命令可靠性
clam list              # 查看已安装
clam remove <app>      # 卸载

clam-<app>             # 能力概览
clam-<app> api         # 完整 API 列表
```

## ❓ 常见问题

**找不到 `clam-xxx`？** — `source .venv/bin/activate`

**"permission denied"？** — 系统设置 > 隐私与安全性 > 自动化，允许终端控制目标应用

**UI Scripting 报权限错误？** — 系统设置 > 隐私与安全性 > 辅助功能，允许终端

**只有基础命令？** — 取决于应用开发者，国产应用大多没有脚本化接口，只能基础模式
