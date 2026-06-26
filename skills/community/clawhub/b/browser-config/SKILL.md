---
name: Browser Config
description: 配置和管理 OpenClaw-CN 浏览器模式（openclaw/chrome），解决浏览器连接问题
metadata: {"clawdbot":{"requires":{"bins":["openclaw-cn"]}}}
---

# Browser Config - 浏览器配置技能

## 描述

配置和管理 OpenClaw-CN 浏览器模式。支持两种浏览器模式：
- **openclaw** - OpenClaw 独立管理的浏览器（推荐，稳定）
- **chrome** - Chrome 扩展中继模式（需要扩展连接）

## 触发词

- 配置浏览器
- 切换浏览器模式
- 浏览器打不开
- 浏览器配置
- 设置浏览器

## 两种模式对比

| 特性 | openclaw 模式 | chrome 模式 |
|------|---------------|-------------|
| 依赖扩展 | ❌ 不需要 | ✅ 需要 OpenClaw Browser Relay 扩展 |
| 稳定性 | ⭐⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中（依赖扩展连接） |
| 登录状态 | 独立保存 | 使用 Chrome 现有登录 |
| 适用场景 | 长期稳定使用、需要登录的网站 | 临时使用、想共用 Chrome 书签 |
| 启动命令 | `openclaw-cn browser --browser-profile openclaw start` | `openclaw-cn browser --browser-profile chrome start` |

## 配置方法

### 切换到 openclaw 模式（推荐）

编辑 `C:\Users\Administrator\.openclaw\openclaw.json`，添加或修改：

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "headless": false,
    "noSandbox": false,
    "attachOnly": false,
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      }
    }
  }
}
```

然后重启网关：
```bash
openclaw-cn gateway restart
```

启动浏览器：
```bash
openclaw-cn browser --browser-profile openclaw start
```

### 切换到 chrome 模式

编辑 `C:\Users\Administrator\.openclaw\openclaw.json`：

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "chrome",
    "headless": false,
    "noSandbox": false,
    "attachOnly": false
  }
}
```

重启网关后，需要：
1. 打开 Chrome 浏览器
2. 点击 OpenClaw Browser Relay 扩展图标
3. 确保扩展连接到当前标签页（图标显示 ON）

## 常见问题排查

### 问题 1：浏览器服务连不上

**错误信息：** `Can't reach the OpenClaw-CN browser control service`

**解决方案：**
1. 检查浏览器状态：`openclaw-cn browser --browser-profile <profile名> status`
2. 如果 `运行中：false`，启动它：`openclaw-cn browser --browser-profile <profile名> start`
3. 如果是 chrome 模式，确保扩展已连接

### 问题 2：chrome 扩展模式一直连不上

**原因：** 扩展中继服务通信问题

**解决方案：** 改回 openclaw 模式（更稳定）

### 问题 3：网关重启后浏览器没了

**解决方案：** 重新运行启动命令：
```bash
openclaw-cn browser --browser-profile openclaw start
```

## 使用示例

### 打开网页
```bash
openclaw-cn browser --browser-profile openclaw open https://www.xiaohongshu.com
```

### 查看状态
```bash
openclaw-cn browser --browser-profile openclaw status
```

### 截图
通过 browser 工具调用：
```
browser: screenshot, targetId=<标签页 ID>
```

## 注意事项

1. **登录状态保存** - openclaw 模式的登录数据保存在 `C:\Users\Administrator\.openclaw\browser\openclaw\user-data`
2. **不要混用模式** - 频繁切换模式可能导致登录状态丢失
3. **推荐 openclaw 模式** - 更稳定，不依赖扩展，适合长期使用
4. **发小红书/微博等** - 登录一次后会话会保持，不需要每次都登录

## 配置文件位置

- 主配置：`C:\Users\Administrator\.openclaw\openclaw.json`
- 浏览器数据：`C:\Users\Administrator\.openclaw\browser\openclaw\user-data`
- 网关日志：`C:\Users\Administrator\.openclaw\logs\gateway.log`
