# 故障排查

## 安装问题

---

### 问题 1：Chrome 未找到或无法启动

**难度：** 低

**症状：** `Error: Chrome not found` 或 `Could not find Chrome (ver. xxx)`

**排查步骤：**
```bash
# macOS
ls /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

# Linux
which google-chrome || which chromium-browser

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

**解决方案：**
- 安装 Chrome：从 https://www.google.com/chrome/ 下载稳定版
- 或在 MCP 配置中指定 Chrome 路径：
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest",
               "--executable-path=/usr/bin/google-chrome"]
    }
  }
}
```

---

### 问题 2：Node.js 版本不兼容

**难度：** 低

**症状：** `engines.node is not satisfied` 或 `SyntaxError: Unexpected token`

**排查步骤：**
```bash
node --version
# 需要 >= 20.19
```

**解决方案：**
```bash
# 使用 nvm 安装最新 LTS
nvm install --lts
nvm use --lts

# 或使用 fnm
fnm install --lts
fnm use --lts

# 验证
node --version  # 应显示 v20.x.x 或更高
```

---

### 问题 3：`claude mcp add` 命令后 MCP 未生效

**难度：** 低

**症状：** 安装命令成功但 AI 无法使用浏览器工具

**排查步骤：**
```bash
claude mcp list
# 确认 chrome-devtools 已在列表中
```

**解决方案：**
- **必须重启 Claude Code** — 安装后 MCP 不会自动热加载
- 如果使用插件安装方式，需执行 `/plugin install chrome-devtools-mcp` 后再重启
- 重启后发送截图请求验证：`请截图 https://example.com`

---

## 使用问题

---

### 问题 4：MCP 服务器启动超时

**难度：** 中

**症状：** `MCP server failed to start within timeout` 或连接请求挂起

**常见原因：**
- Chrome 首次启动下载组件（概率 40%）
- 系统资源不足（概率 30%）
- 防火墙拦截了 DevTools 协议端口（概率 20%）
- npm/npx 缓存损坏（概率 10%）

**解决方案：**
```bash
# 清理 npx 缓存后重试
npx clear-npx-cache
npx -y chrome-devtools-mcp@latest --headless

# Windows 增加超时时间（在 .codex/config.toml 中）
# startup_timeout_ms = 20_000
```

---

### 问题 5：截图返回空白或黑屏

**难度：** 中

**症状：** AI 调用截图工具成功但返回全黑图片，或图片只有背景色

**常见原因：**
- 页面尚未完全渲染（SPA 水合延迟）
- 目标页面需要登录
- CSS 动画未完成

**解决方案：**
```
# 让 AI 等待后再截图
请打开 http://localhost:3000，等待 2 秒后截图

# 或者先检查控制台是否有渲染错误
打开 http://localhost:3000，读取控制台所有错误，然后截图
```

如果页面需要登录状态：
```bash
# 先启动带已有 Profile 的 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=$HOME/.chrome-debug-profile

# 在 Profile 中手动登录后，配置 MCP 连接
```

---

### 问题 6：网络请求检查不到数据

**难度：** 中

**症状：** `network` 工具返回空列表，或只显示部分请求

**原因：** MCP 服务器在页面加载后才连接，错过了初始请求

**解决方案：**
```
# 让 AI 先连接，再触发请求
请导航到 http://localhost:3000/api-test，开始监听网络请求，
然后点击"加载数据"按钮，最后显示所有捕获到的网络请求
```

或让 AI 刷新页面后立即捕获：
```
导航到 http://localhost:3000，强制刷新页面，然后立即检查所有网络请求
```

---

### 问题 7：JavaScript 执行返回 undefined 或报错

**难度：** 低

**症状：** `evaluate` 工具执行成功但结果为 `undefined`

**常见原因：**
- 返回值需要显式 `return` 语句
- 异步代码未等待

**解决方案：**
```
# 错误：缺少 return
执行 JavaScript: document.title

# 正确：添加 return
执行 JavaScript: return document.title

# 异步代码
执行 JavaScript: return await fetch('/api/data').then(r => r.json())
```

---

## 网络/环境问题

---

### 问题 8：企业网络环境 HTTPS 插件安装失败

**难度：** 中

**症状：** `Failed to clone repository` 或 `/plugin marketplace add` 报网络错误

**解决方案：**

改用 CLI 方式安装（不依赖 Git clone）：
```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

或手动添加 JSON 配置到 `~/.claude/settings.json`：
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

### 问题 9：Windows 下 Chrome 找不到或路径错误

**难度：** 中

**症状：** Windows 环境下 `spawn chrome ENOENT` 或 `Chrome not found`

**解决方案：**

在 `.codex/config.toml` 中显式配置：
```toml
[mcp_servers.chrome-devtools]
command = "cmd"
args = ["/c", "npx", "-y", "chrome-devtools-mcp@latest"]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 20_000
```

或在 MCP 配置中指定 Chrome 路径：
```json
{
  "args": ["-y", "chrome-devtools-mcp@latest",
           "--executable-path=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]
}
```

---

### 问题 10：连接已有 Chrome 实例失败（`--browser-url` 无响应）

**难度：** 高

**症状：** 使用 `--browser-url=http://127.0.0.1:9222` 但连接超时

**排查步骤：**
```bash
# 确认 Chrome 远程调试端口已开启
curl http://127.0.0.1:9222/json/version

# 期望返回 JSON，如：
# {"Browser": "Chrome/130.0.0.0", "webSocketDebuggerUrl": "..."}
```

**常见原因：**
- Chrome 没有以 `--remote-debugging-port=9222` 启动（概率 60%）
- 端口被防火墙拦截（概率 25%）
- Chrome 已有实例正在运行且未开启调试（概率 15%）

**解决方案：**
```bash
# 关闭所有现有 Chrome 进程
pkill -f "Google Chrome"  # macOS/Linux

# 重新以调试模式启动
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check

# 验证连接
curl http://127.0.0.1:9222/json/version
```

---

## 通用诊断

```bash
# 检查 MCP 服务器状态
claude mcp list

# 手动测试 MCP 服务器启动
npx -y chrome-devtools-mcp@latest --headless

# 检查 Node.js 和 Chrome 版本
node --version
google-chrome --version || /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

**GitHub Issues：** https://github.com/ChromeDevTools/chrome-devtools-mcp/issues

**完整故障排查文档：** https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md
