# BrightData 搜索与抓取能力配置

本文档说明如何为当前环境配置 BrightData 的搜索和网页抓取能力。有两种方式可用：MCP 服务器集成（推荐用于 Claude Code）和独立 CLI 工具。

## 方式一：MCP 服务器集成（推荐）

将 BrightData 作为 MCP 服务器接入 Claude Code，使 agent 可直接调用搜索和抓取工具。

### 前置条件

1. 已安装并配置 Claude Code
2. 拥有 BrightData 账户（新用户可获得免费测试额度）
3. 从 BrightData 用户设置页面获取 API 密钥

### 安装步骤

**1. 添加 MCP 服务器**

```bash
claude mcp add --transport sse brightdata "https://mcp.brightdata.com/sse?token=<your-api-token>"
```

将 `<your-api-token>` 替换为实际 API 令牌。

**2. 验证连接**

```bash
claude mcp list
```

预期输出：
```
brightdata: https://mcp.brightdata.com/sse?token=<yourapikey>(SSE) - ✓ Connected
```

### MCP 提供的工具

| 工具类别 | 用途 | 示例工具名 |
|----------|------|-----------|
| 搜索引擎 | 发现候选平台 | `search_engine`, `search_engine_batch`, `discover` |
| 网页抓取 | 抓取官网、docs、pricing 等页面正文 | `scrape_as_markdown`, `scrape_batch` |
| 结构化数据 | 快速读取 GitHub 等平台结构化数据 | `web_data_github_repository_file` |
| 远程浏览器 | 导航、点击、截图、读取需 JS 渲染的页面 | `scraping_browser_navigate`, `scraping_browser_snapshot` |

### 检测 MCP 是否可用

在 skill 的 preflight 阶段：
- 检查当前环境是否有以 `mcp__brightdata__` 为前缀的工具可用
- 如果有 `search_engine` 工具 → 搜索能力可用
- 如果有 `scrape_as_markdown` 工具 → 抓取能力可用

## 方式二：BrightData CLI（独立命令行工具）

BrightData 也提供独立的 CLI 工具，可在终端中直接使用搜索、抓取、结构化数据提取等功能。适用于不依赖 MCP 的场景，或作为 MCP 的补充。

### 安装

```bash
npm install -g @brightdata/cli
```

验证安装：
```bash
brightdata --version
```

安装后也可使用简写别名 `bdata`。

### 认证

**方式 A：浏览器 OAuth（推荐）**
```bash
brightdata login
```
自动打开浏览器完成认证。登录一次后所有后续命令自动认证。

**方式 B：无浏览器环境（SSH/服务器）**
```bash
brightdata login --device
```
打印一个 URL 和验证码，在任意设备上打开 URL 输入验证码即可。

**方式 C：直接 API Key（CI/CD 场景）**
```bash
brightdata login --api-key YOUR_API_KEY
```

**方式 D：环境变量**
```bash
export BRIGHTDATA_API_KEY=YOUR_API_KEY
```

### 验证配置

```bash
brightdata config   # 查看配置
brightdata budget   # 查看额度
brightdata scrape https://example.com   # 测试抓取
```

### 常用命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `brightdata scrape <url>` | 抓取网页为 Markdown | `brightdata scrape https://example.com` |
| `brightdata search "<query>"` | 搜索引擎查询 | `brightdata search "OpenAI compatible API gateway"` |
| `brightdata discover "<query>"` | AI 驱动的意图搜索 | `brightdata discover "AI API relay" --intent "找中转平台"` |
| `brightdata pipelines <type> <url>` | 结构化数据提取 | `brightdata pipelines github_repo "<url>"` |
| `brightdata browser open <url>` | 远程浏览器控制 | `brightdata browser open https://example.com` |
| `brightdata add mcp` | 将 BrightData MCP 添加到 coding agent | `brightdata add mcp` |

### 交互式初始化向导

首次使用也可运行引导式设置：
```bash
brightdata init
```

### 配置文件位置

| 系统 | 路径 |
|------|------|
| macOS | `~/Library/Application Support/brightdata-cli/` |
| Linux | `~/.config/brightdata-cli/` |
| Windows | `%APPDATA%\brightdata-cli\` |

## MCP vs CLI 选择建议

| 场景 | 推荐方式 |
|------|----------|
| Claude Code 中使用本 skill | MCP（agent 可直接调用工具） |
| 终端中手动搜索/抓取 | CLI |
| CI/CD 自动化流水线 | CLI |
| 两者都已安装 | 优先用 MCP（agent 调用更直接），CLI 作补充 |

## 自动修复

如果 BrightData 能力未配置：

**MCP 未配置时：**
1. 告知用户需要配置 BrightData MCP
2. 提供安装命令：`claude mcp add --transport sse brightdata "https://mcp.brightdata.com/sse?token=<your-api-token>"`
3. 提醒用户需要自行替换 API token
4. 安装完成后需要重启 Claude Code 会话才能生效

**CLI 未安装时：**
1. 可自动尝试安装：`npm install -g @brightdata/cli`
2. 安装后提示用户运行 `brightdata login` 完成认证

**注意：** API token / 账户认证属于用户私密操作，skill 不应尝试自动获取或存储。必须由用户手动完成。

## 完整文档索引

BrightData 完整文档索引：`https://docs.brightdata.com/llms.txt`
可用于查找所有可用功能页面。
