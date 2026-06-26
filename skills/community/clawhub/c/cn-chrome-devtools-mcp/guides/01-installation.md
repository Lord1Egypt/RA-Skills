# 安装指南

## 适用场景

- 在 Claude Code 中安装 chrome-devtools-mcp
- 在 VS Code / Cursor 等其他 AI 工具中配置
- 验证 MCP 服务器正常连接

---

## Claude Code 安装（推荐两种方式）

### 方式一：CLI 安装（仅 MCP）

> **AI 可自动执行**

```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

`--scope user` 表示对当前用户全局生效（所有项目可用）。

### 方式二：插件安装（MCP + Skills，功能更完整）

在 Claude Code 会话中执行：

```
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
/plugin install chrome-devtools-mcp
```

**安装完成后必须重启 Claude Code**，然后用 `/skills` 验证 Skills 已加载。

> 若出现 `Failed to clone repository` 错误（企业网络 HTTPS 受限），改用方式一 CLI 安装。

---

## VS Code / Copilot 安装

### CLI 一键安装

```bash
# macOS / Linux
code --add-mcp '{"name":"io.github.ChromeDevTools/chrome-devtools-mcp","command":"npx","args":["-y","chrome-devtools-mcp"],"env":{}}'

# Windows PowerShell
code --add-mcp '{"""name""":"""io.github.ChromeDevTools/chrome-devtools-mcp""","""command""":"""npx""","""args""":["""-y""","""chrome-devtools-mcp"""]}'
```

### 手动配置

在 VS Code MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

---

## Cursor 安装

进入 `Cursor Settings → MCP → New MCP Server`，使用以下配置：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

---

## Windows 特殊配置（Codex）

Windows 下需要指定 Chrome 路径和增加超时时间，在 `.codex/config.toml` 中：

```toml
[mcp_servers.chrome-devtools]
command = "cmd"
args = ["/c", "npx", "-y", "chrome-devtools-mcp@latest"]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 20_000
```

---

## 验证安装

安装并重启 AI 工具后，在对话中发送：

```
请截图 https://example.com 的当前状态
```

**期望结果：** AI 打开浏览器，导航到 example.com，并返回截图。

或检查 MCP 服务器列表：

```bash
# Claude Code
claude mcp list
```

---

## 隐私设置（可选）

禁用 Google 使用统计收集：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]
    }
  }
}
```

或通过环境变量：
```bash
export CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=1
```

---

## 完成确认检查清单

- [ ] MCP 服务器配置已添加到对应 AI 工具
- [ ] AI 工具已重启
- [ ] 发送截图请求，AI 成功控制浏览器并返回截图
- [ ] （可选）`claude mcp list` 显示 chrome-devtools 已注册

---

## 下一步

- [快速开始](02-quickstart.md) — 调试工作流、性能分析、网络检查
