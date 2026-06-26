---
name: browser-extension-enabler
description: Auto-detect and enable OpenClaw Browser Relay Chrome extension when disconnected. Uses native mouse control to click the extension icon.
version: 1.0.0
author: OpenClaw Community
keywords: [browser, extension, chrome, automation, mouse, click, enable, relay]
license: MIT
dependencies:
  - win-mouse-native
---

# Browser Extension Enabler

自动检测并启用 OpenClaw Browser Relay Chrome 扩展。当扩展未连接时，自动移动鼠标点击扩展图标。

## 功能

- ✅ 自动检测 Browser Relay 连接状态
- ✅ 鼠标自动移动到扩展图标位置
- ✅ 自动点击启用扩展
- ✅ 验证连接是否成功
- ✅ 可配置的图标坐标

## 前置依赖

必须先安装 `win-mouse-native` skill：
```bash
clawhub install win-mouse-native
```

## 安装

```bash
clawhub install browser-extension-enabler
```

## 使用方法

### 命令行方式

```powershell
# 使用默认坐标 (1920x1080 屏幕)
.\enable-browser-extension.ps1

# 指定自定义坐标
.\enable-browser-extension.ps1 -IconX 1800 -IconY 70

# 测试模式（不实际点击）
.\enable-browser-extension.ps1 -TestMode
```

### 在 Agent 中使用

当 Agent 检测到扩展未连接时，可以自动调用：

```javascript
// 检测扩展状态
browser: { action: "tabs", profile: "chrome" }

// 如果未连接，自动启用
exec: {
  command: "powershell -File \"$env:USERPROFILE\\.openclaw\\workspace\\skills\\browser-extension-enabler\\scripts\\enable-browser-extension.ps1\"",
  pty: false
}
```

## 配置

### 校准扩展图标坐标

不同屏幕分辨率和浏览器配置下，扩展图标位置不同。请按以下步骤校准：

1. **找到当前坐标**
   ```powershell
   # 把鼠标移到扩展图标上，记录位置
   win-mouse abs 1850 60
   ```

2. **手动测试**
   ```powershell
   # 测试候选坐标
   win-mouse abs 1850 60   # 移动
   win-mouse click left    # 点击
   ```

3. **更新默认值**
   编辑脚本中的 `$IconX` 和 `$IconY` 默认值，或使用时传入参数

### 推荐坐标

| 屏幕分辨率 | 图标坐标 (X, Y) |
|-----------|----------------|
| 1920x1080 | (1850, 60) |
| 2560x1440 | (2490, 70) |
| 3840x2160 | (3770, 90) |

## 工作流程

```
1. 检测 Browser Relay 连接状态
   ↓ 未连接
2. 激活 Chrome 窗口
   ↓
3. 移动鼠标到扩展图标
   ↓
4. 点击左键
   ↓
5. 等待 5 秒
   ↓
6. 验证连接成功 (最多重试3次)
```

## 测试方法

1. 关闭 OpenClaw Browser Relay 扩展（点击扩展图标断开）
2. 运行脚本：`enable-browser-extension.ps1`
3. 观察鼠标移动和点击
4. 验证扩展是否重新连接

## 故障排除

### 扩展仍未连接

- 检查坐标是否正确：`win-mouse abs X Y` 测试
- 确保 Chrome 窗口可见（未最小化）
- 检查是否已安装 OpenClaw Browser Relay 扩展
- 增加等待时间或重试次数

### 鼠标移动但无响应

- 确保 Chrome 在操作时是前台窗口
- 增加点击前的等待时间
- 检查扩展图标是否被其他图标遮挡

### 检测失败但扩展已连接

脚本通过 `openclaw browser tabs` 命令检测。如果输出格式变化，可能需要更新匹配模式。

## 安全提示

⚠️ 此 skill 会控制真实鼠标移动和点击，请确保：
- 了解脚本将点击的位置（先用 TestMode 验证）
- 在测试模式下先验证坐标
- 不要在重要工作时运行（可能干扰操作）

## 版本历史

- v1.0.0 - 初始版本，支持基本的自动启用功能

## 许可证

MIT

## 作者

OpenClaw Community
