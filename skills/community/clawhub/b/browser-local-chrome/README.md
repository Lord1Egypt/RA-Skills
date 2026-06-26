# browser-local-chrome

本地 Chrome 调试模式浏览器自动化配置技能

## 快速开始

### 方案 A：官方 Browser（默认）

```bash
# 启动
openclaw browser --browser-profile openclaw start

# 检查状态
openclaw browser --browser-profile openclaw status

# 打开网页
openclaw browser --browser-profile openclaw open https://example.com

# 使用完成后关闭
openclaw browser --browser-profile openclaw stop
```

### 方案 B：本地 Chrome 技能（备用）

```bash
# 启动
node scripts/start-chrome.js

# 检查状态
node scripts/check-status.js

# 使用完成后关闭
node scripts/stop-chrome.js
```

### 方案 C：一键故障排查（推荐）

```bash
node scripts/troubleshoot.js
```

自动检测 + 启动可用的浏览器方案！

## 脚本说明

| 脚本 | 功能 | 参数 |
|------|------|------|
| `setup.js` | 一键配置（启动 + 配置 + 验证） | 无 |
| `start-chrome.js` | 启动 Chrome 调试模式 | `[端口]` (默认 9222) |
| `stop-chrome.js` | 关闭 Chrome 浏览器 | `[端口]` (默认 9222) |
| `configure-browser.js` | 配置 OpenClaw | `[端口]` (默认 9222) |
| `check-status.js` | 检查浏览器状态 | `[端口]` (默认 9222) |

## 配置项

在 `_meta.json` 中可自定义：

```json
{
  "config": {
    "cdpPort": 9222,
    "userDataDir": "C:\\chrome-debug-profile",
    "chromePath": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
  }
}
```

## 使用场景

- ✅ 访问需要 JavaScript 的网站（如 Google 搜索）
- ✅ 自动化网页操作
- ✅ 截图和页面分析
- ✅ 绕过 SSRF 限制

## 完整工作流程示例

```bash
# 1. 启动浏览器
node scripts/start-chrome.js

# 2. 配置 OpenClaw（首次使用时）
node scripts/configure-browser.js

# 3. 重启 Gateway（首次配置后）
openclaw gateway restart

# 4. 检查状态
node scripts/check-status.js

# === 使用浏览器工具访问网站 ===
# 在 OpenClaw 中：browser open https://example.com

# 5. 使用完成后关闭浏览器
node scripts/stop-chrome.js
```

## 故障排查

**Chrome 无法启动**
```bash
# 检查 Chrome 是否安装
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"

# 检查端口占用
netstat -ano | findstr :9222
```

**配置不生效**
```bash
# 重启 Gateway
openclaw gateway restart

# 检查配置文件
cat ~/.openclaw/openclaw.json
```

## 安全说明

此技能配置 `dangerouslyAllowPrivateNetwork: true`，允许浏览器访问私有网络地址。仅在可信环境中使用。

如需更严格的安全策略，可修改 `openclaw.json` 中的 `ssrfPolicy`：

```json
{
  "browser": {
    "ssrfPolicy": {
      "hostnameAllowlist": ["*.example.com", "example.com"]
    }
  }
}
```
