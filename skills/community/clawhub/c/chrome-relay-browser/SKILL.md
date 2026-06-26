---
name: chrome-relay-browser
description: 通过 Chrome Extension relay 控制浏览器。用于控制用户已在 Chrome 中打开并 attach 的标签页，无需启动新浏览器，用户可直接看到操作界面。触发条件：(1) 用户让我操作浏览器 (2) 需要复用用户已打开的页面 (3) 需要截图/填表/点击等操作
metadata: {"openclaw":{"emoji":"🌐","requires":{"env":["RELAY_TOKEN","RELAY_PORT"],"config":["~/.openclaw/secrets/browser-relay.env"]}}}
---

# chrome-relay-browser

通过 Chrome Extension relay 控制已 attach 的浏览器标签页。

## 前置条件

0. **配置 openclaw.json**（确保 browser 部分已配置）：
   ```json
   "browser": {
     "enabled": true,
     "defaultProfile": "chrome-relay",
     "attachOnly": true
   }
   ```

1. **安装 Chrome 扩展**：
   ```bash
   openclaw browser extension install
   openclaw browser extension path  # 获取安装路径
   ```
   然后在 Chrome 中加载：打开 `chrome://extensions`，开启开发者模式，加载上述路径

2. **配置扩展**（安装后需配置一次）：
   - 点击扩展图标 → 设置
   - Relay port: 从 `~/.openclaw/secrets/browser-relay.env` 读取 `RELAY_PORT`
   - Gateway token: 从 `~/.openclaw/secrets/browser-relay.env` 读取 `RELAY_TOKEN`

3. **Attach 标签页**：
   - 在 Chrome 打开任意页面
   - 点击扩展图标 attach

## 使用方法

运行 scripts/ctl.js 控制浏览器：

```bash
cd ~/.openclaw/workspace/skills/chrome-relay-browser/scripts
node ctl.js <command> [args]
```

### 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `navigate <url>` | 打开 URL | `node ctl.js navigate https://baidu.com` |
| `screenshot [path]` | 截图 | `node ctl.js screenshot /tmp/abc.png` |
| `title` | 获取页面标题 | `node ctl.js title` |
| `url` | 获取当前 URL | `node ctl.js url` |
| `evaluate <js>` | 执行 JS | `node ctl.js evaluate "document.title"` |

### 配置

Token 和 Port 存储在 `~/.openclaw/secrets/browser-relay.env`，脚本自动读取：
- `RELAY_TOKEN` - Gateway token
- `RELAY_PORT` - Relay 端口号

## 故障排除

- **Unauthorized**: 检查扩展设置的 Gateway token 是否与 secrets 中的 RELAY_TOKEN 一致
- **No tabs**: 提醒用户先在 Chrome 中 attach 标签页
- **Connection refused**: 重启 Gateway 或检查 RELAY_PORT 配置