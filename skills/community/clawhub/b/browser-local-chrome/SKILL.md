# 浏览器自动化配置技能

配置 OpenClaw 使用本地 Chrome 调试模式进行浏览器自动化。

## 功能

- ✅ 一键启动 Chrome 调试模式
- ✅ 自动配置 OpenClaw 浏览器设置
- ✅ 启用 SSRF 白名单（允许访问任意网站）
- ✅ 检查浏览器状态

## 使用方法

### 一键配置（推荐）

```bash
node scripts/setup.js
```

这会自动完成所有步骤：启动 Chrome → 配置 OpenClaw → 验证状态

### 分步配置

### 1. 启动浏览器

```bash
node scripts/start-chrome.js
```

### 2. 配置 OpenClaw

```bash
node scripts/configure-browser.js
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

### 4. 检查状态

```bash
node scripts/check-status.js
```

### 5. 关闭浏览器（使用完成后）

```bash
node scripts/stop-chrome.js
```

## 配置说明

### CDP 端口
默认：`9222`

### 用户数据目录
默认：`C:\chrome-debug-profile`

### SSRF 策略
- `dangerouslyAllowPrivateNetwork: true` - 允许访问任意网站
- 如需更严格的安全策略，可改用 `hostnameAllowlist`

## 故障排查

### Chrome 无法启动
- 检查 Chrome 是否已安装：`C:\Program Files\Google\Chrome\Application\chrome.exe`
- 检查端口 9222 是否被占用

### 浏览器工具不可用
- 确认 Gateway 已重启
- 检查 CDP 连接：`curl http://127.0.0.1:9222/json/version`

### SSRF 错误
- 确认 `openclaw.json` 中已配置 `ssrfPolicy`
- 重启 Gateway 使配置生效

## 适用场景

- 访问需要 JavaScript 渲染的网站
- 自动化网页操作（点击、填写表单等）
- 截图和页面分析
- 绕过 curl 无法处理的动态内容

## 注意事项

- Chrome 调试模式需要保持运行
- **使用完成后请关闭浏览器**：`node scripts/stop-chrome.js`
- 重启后需要重新启动 Chrome
- 建议将启动脚本添加到开机自启
