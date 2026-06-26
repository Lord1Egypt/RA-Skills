# Chrome 145+ App-Bound Encryption 技术方案总结

## 问题背景

**Chrome 126+** 引入了 **App-Bound Encryption**：所有 Cookie 使用 DPAPI（Data Protection API）加密，绑定到原始 user-data-dir 路径。

**Chrome 130+** 加强了限制：  
`--remote-debugging-port` 强制要求使用**非默认的 user-data-dir**，否则浏览器内部会静默忽略该参数，远程调试端口无法启用。

这导致之前常见的 `--remote-debugging-port=9222 --user-data-dir=<默认路径>` 方案在 Chrome 130+ 失效。

---

## 解决方案

### 1. **Profile 复制绕过（核心方案）**

将 Chrome 默认 profile 从：
```
%LOCALAPPDATA%\Google\Chrome\User Data
```
复制到自定义路径（如 `<CHROME_PROFILE_DIR>`，通过环境变量配置）。

**原理**：
- 复制后的路径是"非默认"，Chrome 会允许 `--remote-debugging-port` 启用
- 同时复制 `Local State`（加密密钥元数据），保证 DPAPI 能解密现有 Cookie
- 首次使用可能登录态丢失（DPAPI 绑定原路径），需在浏览器手动登录一次
- 之后所有新 Cookie 会存储到新路径，每次启动都能保持登录

### 2. **启动参数关键设置**

```bash
chrome.exe \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="<CHROME_PROFILE_DIR>" \
  --profile-directory=Default \
  --no-first-run \
  --no-default-browser-check
```

**参数说明**：
- `--remote-debugging-port=9222`：开启 CDP 调试端口
- `--remote-allow-origins=*`：允许本地连接（Chrome 116+ 需要）
- `--user-data-dir=<非默认路径>`：**必须**是非默认路径，否则 Chrome 130+ 会忽略（用环境变量 `CHROME_PROFILE_DIR` 配置）
- `--profile-directory=Default`：指定使用 Default profile
- `--no-first-run`：跳过首次运行提示
- `--no-default-browser-check`：跳过默认浏览器检查

### 3. **连接流程**

```
┌──────────────────────────────────────┐
│ 1. 复制 Profile 到自定义目录           │
│    - 复制 Local State（加密元数据）   │
│    - 复制 Default profile（包含Cookie）│
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 2. 以 CDP 参数启动 Chrome              │
│    - 指定复制后的 profile 路径        │
│    - 启用 --remote-debugging-port    │
│    （通过 CHROME_PROFILE_DIR 环境变量）│
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 3. 等待 CDP 就绪（检查 9222 端口）    │
│    - GET http://localhost:9222/...   │
│    - 获取 WebSocket URL                │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 4. 连接 WebSocket                     │
│    - Playwright: connect_over_cdp()  │
│    - browser-use: BrowserProfile()   │
│    - 获取页面引用并操作                 │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 5. 首次登录状态丢失处理                 │
│    - 在浏览器中手动登录一次            │
│    - Cookie 会加密保存到新 profile     │
│    - 之后每次都能直接使用              │
└──────────────────────────────────────┘
```

---

## 技术细节

### Cookie 加密与 DPAPI

**Chrome 126+** 开始使用 DPAPI 加密所有 Cookie：

| Chrome 版本 | 加密方案 | 绑定方式 | 影响 |
|---|---|---|---|
| < 126 | 无加密（纯文本） | - | 可直接读取 Cookie |
| 126-129 | DPAPI | 原始 user-data-dir | Profile 复制后需重新登录 |
| 130+ | DPAPI + App-Bound | 原始 user-data-dir | 同时要求 `--remote-debugging-port` 用非默认路径 |
| 145（当前） | DPAPI + App-Bound | 原始 user-data-dir + 强制检查 | 版本行为稳定 |

**DPAPI 绑定的影响**：
- 当你在 `C:\Users\user\AppData\Local\Google\Chrome\User Data` 登录
- Cookie 会被加密并存储
- 如果复制到其他路径（如 `C:\custom\chrome-profile`）
- DPAPI 无法解密旧 Cookie（密钥绑定原路径）
- 需要在新路径的 Chrome 中重新登录一次
- 新登录的 Cookie 使用新路径的加密密钥

**解决方案**：只需登录一次，之后自动保持

---

## 实践工作流

### 初始化（一次性）

```bash
# 1. 启动 Chrome 以 CDP 模式
python scripts/start_chrome.py

# 2. Chrome 窗口打开后，如果登录态丢失
#    手动完成登录（用你的登录方式）

# 3. 登录成功后，Cookie 会保存到自定义 profile
#    关闭浏览器，重新启动——登录态已保存！
```

### 日常使用

```bash
# 启动 Chrome CDP 模式
python scripts/start_chrome.py

# 查询 CDP 连接信息
python scripts/query_cdp.py

# 用 Playwright 直连操作（确定性任务）
python scripts/playwright_connect.py --url https://example.com --screenshot output.png

# 用 browser-use Agent 执行自然语言任务（AI 驱动）
python scripts/run_agent.py --task "打开网站，列出所有商品" --model qwen3.5:9b
```

---

## 关键发现

1. **Chrome 版本锁定很重要**：145 版本稳定，建议生产环境固定此版本
2. **Profile 复制成本**：首次可能需要 2-5 分钟（取决于 Cookie/缓存大小）
3. **多实例共享 Profile**：不支持，每个 Chrome 进程需要独占一个 profile 副本
4. **Port 冲突**：如需多个 Chrome 实例，修改 `--remote-debugging-port` 为不同值

---

## 故障排查

### 1. "DevTools remote debugging requires a non-default data directory"

✅ **解决**：确认 `--user-data-dir` 不是默认路径

```bash
# 错误 ❌ - 使用默认路径
--user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data"

# 正确 ✅ - 使用自定义路径（设置环境变量）
$env:CHROME_PROFILE_DIR = "C:\custom\chrome-profile"
python start_chrome.py
```

### 2. CDP 端口 9222 仍然不通

✅ **检查清单**：
- Chrome 进程是否真的启动了：`tasklist | grep chrome`
- Profile 是否有读写权限
- 防火墙是否阻止本地 9222：`netstat -ano | grep 9222`
- 是否有另一个 Chrome 进程已占用该端口

### 3. 登录态在新 profile 中丢失

✅ **预期行为**：首次复制 profile 后，DPAPI 无法解密旧 Cookie，需手动重新登录一次

✅ **解决**：
```bash
# 在浏览器中手动完成登录
# 用你的登录方式（App 扫码、验证码等）登录

# 完成后关闭 Chrome，重新启动
python scripts/start_chrome.py

# 此后登录态会自动保存
```

### 4. Playwright 连接失败："WebSocket connection failed"

✅ **检查**：
```bash
# 确认 CDP 在线
python scripts/query_cdp.py

# 确认 WebSocket URL 可访问
curl http://localhost:9222/json/version
```

---

## 参考资源

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Playwright Chrome 连接文档](https://playwright.dev/python/docs/browsers#connect-to-an-existing-browser-instance)
- [browser-use Agent 文档](https://docs.browser-use.com/)
- [Chrome App-Bound Encryption 说明](https://developers.google.com/privacy-sandbox/3pcd)
