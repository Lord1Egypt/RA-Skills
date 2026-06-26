---
name: chrome-attach
description: 使用 Chrome Session Attach 功能控制用户的浏览器标签页。包括安装 Chrome 扩展、配置连接、Attach/Detach 标签页、截图、导航、填表等操作。
version: 1.0.0
---

# Chrome Session Attach

让 Agent 控制用户已有的 Chrome 标签页，无需在 OpenClaw 管理的浏览器中登录。

## 前置条件

1. Gateway 必须运行在本地（127.0.0.1）
2. Chrome 扩展已加载

## 安装步骤

### 1. 获取扩展路径并复制到桌面

```bash
openclaw browser extension path
# 输出: ~/.openclaw/browser/chrome-extension
```

复制到桌面以便访问：
```bash
cp -r ~/.openclaw/browser/chrome-extension ~/Desktop/OpenClaw-Extension
```

### 2. 在 Chrome 中加载扩展

1. 打开 Chrome → `chrome://extensions`
2. 启用 "Developer mode"（右上角）
3. 点击 "Load unpacked"
4. 选择 `~/Desktop/OpenClaw-Extension`

### 3. 配置扩展

点击工具栏的 OpenClaw 扩展图标，配置：

- **Port**: Gateway 端口（默认 18789，可在 `openclaw gateway status` 查看）
- **Token**: Gateway token

获取 Token：
```bash
cat ~/.openclaw/openclaw.json | jq -r '.gateway.auth.token'
```

### 4. Attach 标签页

1. 在想要控制的标签页点击扩展图标
2. 点击 "Attach to this tab"
3. 图标显示 ON = 已连接

## 可用命令

| 命令 | 说明 |
|------|------|
| `openclaw browser snapshot` | 获取页面快照 |
| `openclaw browser navigate <url>` | 导航到 URL |
| `openclaw browser click <ref>` | 点击元素 |
| `openclaw browser type <ref> "text"` | 输入文字 |
| `openclaw browser screenshot` | 截图 |
| `openclaw browser tabs` | 列出标签页 |
| `openclaw browser close <target>` | 关闭标签页 |

## Detach

点击扩展图标 → 再次点击 "Attach to this tab" 即可断开连接。

## 故障排除

- 扩展图标显示红色 ! → Gateway 未运行或端口错误
- `openclaw gateway status` 查看 Gateway 状态
- 确保 Gateway 绑定在 127.0.0.1（非远程模式）
