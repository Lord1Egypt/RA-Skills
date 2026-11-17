---
name: browser-cdp-connect
version: 1.0.0
description: |
  连接用户日常 Chrome 浏览器（带登录态）用于反爬严格的网站采集。
  当 headless 浏览器被网站 forbidden/反爬拦截（如贝壳 hip.ke.com/forbidden、
  自如 EdgeOne、小红书等），用此 skill 切换到用户日常 Chrome——它携带
  真实登录态和人类行为特征，不会被封。触发场景：用户提到"登录态"、
  "用我的浏览器"、"贝壳/链家被 forbidden"、"headless 被封"、
  "CDP 连接"、"反爬"、"验证码过不去"，或 browser_navigate 返回
  forbidden/hip.ke.com 时。
---

# Browser CDP Connect — 连接用户日常 Chrome

## 核心原理（为什么 headless 会被封，用户 Chrome 不会）

headless Chrome（Hermes 默认 browser 工具）有自动化指纹：
- `--headless=new` + 临时 user-data-dir → 无登录态、无 cookie
- `navigator.webdriver=true` → 被反爬识别
- 行为特征机械化 → 触发风控

用户日常 Chrome 的优势：
- 真实 user-data-dir → 携带所有网站登录态和 cookie
- 无自动化指纹 → 不被识别为机器人
- `chrome://inspect` 开的远程调试端口只接受带 UUID 路径的 WebSocket，
  不开放 HTTP `/json/*` 端点（Chrome 安全限制），比命令行
  `--remote-debugging-port` 更隐蔽

## 前提：Chrome 已开启远程调试

用户需在 Chrome 地址栏打开 `chrome://inspect/#remote-debugging`，
勾选 **"Allow remote debugging for this browser instance"**。
这会创建 `DevToolsActivePort` 文件（含端口号+wsPath UUID）。

**判断是否已开**：运行脚本（见下），若报 "chrome: not connected"
则引导用户完成上述操作，可能需重启 Chrome。

## 使用方式

### 自动连接（推荐）

```bash
bash ~/AppData/Local/hermes/skills/autonomous-ai-agents/browser-cdp-connect/scripts/connect-chrome.sh
```

脚本会：
1. 读 `DevToolsActivePort` 文件发现端口+wsPath
2. 拼接 `ws://127.0.0.1:<port>/devtools/browser/<uuid>`
3. 写入 `browser.cdp_url` 到 config.yaml（`hermes config set`）

**当前 session 立即生效**：browser 工具的 `_resolve_cdp_endpoint()` 在
**每次工具调用时**读取 `browser.cdp_url`（不是 session 启动时读一次），
所以 `hermes config set` 写入后，当前 session 的下一次 `browser_navigate`
立即用新值——无需 `/reset`。验证：`stealth_features` 应含 `cdp_override`。

> ⚠️ **坑：脚本里的 `export BROWSER_CDP_URL` 不会到达 Hermes 进程**。
> 脚本通过 `terminal` 工具运行时，`export` 发生在子 shell 里，子 shell
> 退出后环境变量就消失了，Hermes 的 Python 进程收不到。真正起作用的是
> `hermes config set browser.cdp_url`——它写 config.yaml，browser 工具
> 每次调用时读这个文件。`BROWSER_CDP_URL` 环境变量只在 Hermes 进程
> **自身**设置时才有效（如 `/browser connect` 命令在进程内设置），
> 从外部子 shell 设置无效。

### 手动连接（排查问题时）

```bash
# 1. 读 DevToolsActivePort
cat "$LOCALAPPDATA/Google/Chrome/User Data/DevToolsActivePort"
# 输出两行：端口号 / wsPath

# 2. 拼 ws URL 并设置
hermes config set browser.cdp_url "ws://127.0.0.1:<PORT>/devtools/browser/<UUID>"

# 3. 或用 /browser connect 命令（CLI 内）
```

## 验证连接成功

```bash
# 用 browser_navigate 访问之前被 forbidden 的站点
# 成功标志：stealth_features 含 "cdp_override"，页面正常加载
```

或直接用 browser 工具：
- `browser_navigate` 到 `https://sh.zu.ke.com/`（贝壳）
- 若返回正常页面（非 hip.ke.com/forbidden）→ 连接成功
- 若返回 forbidden → 仍连的是 headless，重跑 connect 脚本

## 切回 headless（完成任务后）

```bash
hermes config set browser.cdp_url ""
# 或 /reset 开新 session
```

清空 `cdp_url` 后，browser 工具回退到默认 headless Chrome。

## 已验证可用的站点（2026-07-02）

| 站点 | headless 表现 | 用户 Chrome 表现 |
|------|--------------|----------------|
| 贝壳 sh.zu.ke.com | hip.ke.com/forbidden 硬封 | 正常，搜索页+详情页均可访问 |
| 安居客 sh.zu.anjuke.com | 403 + 验证码（可点击通过） | 正常 |
| 自如 ziroom.com | EdgeOne 防护 | 待验证 |

## 技术细节

### DevToolsActivePort 文件

位置（Windows）：`%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort`
内容：两行
```
<port>
/devtools/browser/<uuid>
```
- 第一行：端口号（每次 Chrome 启动可能不同）
- 第二行：wsPath UUID（每次 Chrome 启动一定不同）

**这就是为什么要用脚本而非硬编码 config**：UUID 每次重启变化。

### 与 Codex 方案对比

Codex 的 web-access skill 用一个 Node.js HTTP 代理（cdp-proxy.mjs，
127.0.0.1:3456）把 CDP WebSocket 转 HTTP API，因为 Codex 工具不能
直连 WebSocket。

Hermes 原生 browser 工具支持 `browser.cdp_url` 直连 WebSocket，
**不需要 Node 代理**——更简单，且能用全部原生 browser 工具
（browser_click/browser_console/browser_vision 等），比 curl 调
HTTP API 强得多。

### Hermes browser 工具的 CDP 优先级

1. `BROWSER_CDP_URL` 环境变量（live override，`/browser connect` 设置）
2. `browser.cdp_url` in config.yaml
3. headless Chrome（默认回退）

源码：`tools/browser_cdp_tool.py` 的 `_resolve_cdp_endpoint()`。

## 坑与注意事项

- **wsPath UUID 每次变**：Chrome 重启后必须重跑 connect 脚本
- **同一 user-data-dir 单实例**：不能用 `--remote-debugging-port` 另起
  一个 Chrome 用同一 profile（Chrome 不允许）。`chrome://inspect` 方式
  让现有 Chrome 开调试端口，不影响正常使用
- **登录态共享**：连接后 browser 工具操作的是用户 Chrome，所有 tab
  共享。agent 创建的 tab 会出现在用户浏览器里——任务完成后记得关闭
  自己创建的 tab（`browser_navigate` 到 about:blank 或关闭 tab）
- **config 变更与 session**：`hermes config set browser.cdp_url` 写入
  config.yaml 后，browser 工具在**每次调用时**读取该值（不是 session
  启动时读一次），所以当前 session 立即生效，无需 `/reset`。新 session
  也自动读 config。`/browser connect` 命令设置 `BROWSER_CDP_URL` 环境
  变量作为 live override（优先级高于 config），但**从外部子 shell
  `export BROWSER_CDP_URL` 无法影响 Hermes 进程**——只有 Hermes 进程
  内部设置才有效。
