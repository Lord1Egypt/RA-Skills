# Browser Automation Skills / 浏览器自动化技能包

> **[English](#english)** | **[中文](#中文)**

Browser Automation Skills for AI models — control local Google Chrome from any AI coding assistant.

浏览器自动化技能包 — 让任何 AI 编码助手都能控制本地 Google Chrome 浏览器。

## Highlights / 亮点

- 🌐 **Navigate** — open URLs, read page content / 打开网页、读取内容
- 📸 **Screenshot** — viewport, full-page, responsive / 截图截屏
- 🖱️ **Interact** — click, type, fill forms, scroll / 点击、输入、表单
- 🕷️ **Scrape** — extract text, tables, structured data / 数据抓取
- 🔍 **Debug** — network, console, DOM inspection / 网页调试
- 🧪 **Test** — automated QA with PASS/FAIL / 自动化测试
- 🎬 **Record** — capture sessions as video / 录制操作视频
- 🚫 **No detection banner** — connects to existing Chrome via CDP / 无检测横幅

---

<a id="english"></a>

## English

A set of Skills that teach AI models how to control the local Google Chrome browser. Works with **any model** — uses `browser_subagent` on Antigravity, or the bundled Playwright CLI script on any other platform with terminal access.

### Two Backends, Same Skills

| Backend | Platform | How It Works |
|---------|----------|-------------|
| **Antigravity** | Antigravity IDE | Built-in `browser_subagent` → Chrome DevTools Protocol → Chrome |
| **Playwright CLI** | Any model with terminal access | `scripts/browser.py` → Playwright → Chrome DevTools Protocol → Chrome |

Both connect to your **existing Chrome** via CDP — no new browser instance, no "controlled by automated software" banner.

### Prerequisites

- **Google Chrome** installed locally
- For Antigravity: nothing extra (built-in)
- For other platforms: `pip install playwright` (no `playwright install` needed — we use your existing Chrome)

### Quick Start

```bash
# 1. Start Chrome with remote debugging
chrome.exe --remote-debugging-port=9222

# 2. Install dependency
pip install playwright

# 3. Try it
python scripts/browser.py status
python scripts/browser.py navigate https://example.com
python scripts/browser.py screenshot
```

### Skills

| Skill | What It Does | Invocation |
|-------|-------------|------------|
| `navigate` | Open URLs, read page content | Auto + `/navigate` |
| `screenshot` | Capture visuals (viewport, full-page, mobile) | Auto + `/screenshot` |
| `interact` | Click, type, fill forms, scroll, drag | Auto + `/interact` |
| `scrape` | Extract text, tables, structured data | Auto + `/scrape` |
| `debug` | Inspect network, console, DOM errors | Auto + `/debug` |
| `test` | Automated QA with PASS/FAIL reports | `/test` only |
| `record` | Record sessions as WebP video | `/record` only |
| `browser-context` | Backend detection + API reference | Model only |

### Installation

#### Option 1: Project-level (recommended)
```bash
cp -r browser-automation-skills/ .claude/plugins/browser-automation-skills/
```

#### Option 2: User-level (global)
```bash
cp -r browser-automation-skills/skills/* ~/.claude/skills/
```

#### Option 3: Additional directory
```bash
claude --add-dir /path/to/browser-automation-skills
```

### How It Works

```
User request (e.g., "screenshot example.com")
    │
    ▼
AI Model — matches request → Skill (e.g., screenshot)
    │
    ├─ Has browser_subagent? ──→ Antigravity backend
    │                               └→ Chrome (via CDP)
    │
    └─ Has terminal access? ──→ scripts/browser.py
                                    └→ Playwright → Chrome (via CDP)
    │
    ▼
Result → verified via screenshot → reported to user
```

### Directory Structure

```
browser-automation-skills/
├── README.md
├── scripts/
│   └── browser.py                  ← Playwright CLI adapter (universal backend)
├── docs/
│   └── api-reference.md            ← Full API reference (bilingual)
└── skills/
    ├── browser-context/SKILL.md    ← Backend detection + tool mapping
    ├── navigate/SKILL.md
    ├── screenshot/SKILL.md
    ├── interact/SKILL.md
    ├── scrape/SKILL.md
    ├── debug/SKILL.md
    ├── test/SKILL.md
    └── record/SKILL.md
```

### License

MIT

---

<a id="中文"></a>

## 中文

一组教会 AI 模型如何控制本地 Google Chrome 浏览器的技能包。适用于**任何模型** — 在 Antigravity 上使用内置工具，在其他平台上使用自带的 Playwright CLI 脚本。

### 双后端，同一套 Skills

| 后端 | 平台 | 工作方式 |
|------|------|---------|
| **Antigravity** | Antigravity IDE | 内置 `browser_subagent` → Chrome DevTools Protocol → Chrome |
| **Playwright CLI** | 任何有终端权限的模型 | `scripts/browser.py` → Playwright → Chrome DevTools Protocol → Chrome |

两种方式都连接你**已有的 Chrome** — 不启动新实例，无"正受到自动测试软件的控制"横幅。

### 前提条件

- 本地安装 **Google Chrome**
- Antigravity 环境：无需额外安装
- 其他平台：`pip install playwright`（无需 `playwright install` — 使用你已有的 Chrome）

### 快速开始

```bash
# 1. 启动 Chrome 调试模式
chrome.exe --remote-debugging-port=9222

# 2. 安装依赖
pip install playwright

# 3. 试一试
python scripts/browser.py status
python scripts/browser.py navigate https://example.com
python scripts/browser.py screenshot
```

### 技能列表

| 技能 | 功能 | 调用方式 |
|------|------|---------|
| `navigate` | 打开 URL、读取页面内容 | 自动 + `/navigate` |
| `screenshot` | 截图（视口/全页/移动端/自定义分辨率） | 自动 + `/screenshot` |
| `interact` | 点击、输入、表单填写、滚动、拖拽 | 自动 + `/interact` |
| `scrape` | 提取文本、表格、结构化数据 | 自动 + `/scrape` |
| `debug` | 检查网络请求、控制台日志、DOM 错误 | 自动 + `/debug` |
| `test` | 自动化 QA 测试，PASS/FAIL 报告 | 仅 `/test` |
| `record` | 录制浏览器操作为 WebP 视频 | 仅 `/record` |
| `browser-context` | 后端检测 + API 参考 | 仅模型 |

### 安装方法

#### 方式一：项目级（推荐）
```bash
cp -r browser-automation-skills/ .claude/plugins/browser-automation-skills/
```

#### 方式二：用户级（全局）
```bash
cp -r browser-automation-skills/skills/* ~/.claude/skills/
```

#### 方式三：额外目录加载
```bash
claude --add-dir /path/to/browser-automation-skills
```

### 工作原理

```
用户请求（如："截个图看看 example.com"）
    │
    ▼
AI 模型 — 匹配请求 → 技能（如 screenshot）
    │
    ├─ 有 browser_subagent？──→ Antigravity 后端
    │                              └→ Chrome（通过 CDP）
    │
    └─ 有终端权限？────────────→ scripts/browser.py
                                   └→ Playwright → Chrome（通过 CDP）
    │
    ▼
结果 → 通过截图验证 → 报告给用户
```

### 目录结构

```
browser-automation-skills/
├── README.md
├── scripts/
│   └── browser.py                  ← Playwright CLI 适配器（通用后端）
├── docs/
│   └── api-reference.md            ← 完整 API 参考（中英双语）
└── skills/
    ├── browser-context/SKILL.md    ← 后端检测 + 工具映射
    ├── navigate/SKILL.md           ← 导航
    ├── screenshot/SKILL.md         ← 截图
    ├── interact/SKILL.md           ← 交互
    ├── scrape/SKILL.md             ← 抓取
    ├── debug/SKILL.md              ← 调试
    ├── test/SKILL.md               ← 测试（仅手动）
    └── record/SKILL.md             ← 录制（仅手动）
```

### 许可证

MIT
