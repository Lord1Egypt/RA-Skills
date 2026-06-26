# 🐾 ClawPaw - Android Phone Control

Turn your Android phone into an OpenClaw node and control it remotely to automate taps, swipes, text input, and more.

> **Note**: Requires [ClawPaw App](https://github.com/klscool/ClawPaw) installed on your phone.

---

## 🎯 What This Skill Does

**📱 Turn Phone into OpenClaw Node**
- Connect phone to OpenClaw Gateway as a node
- Query node status and device info anytime

**🖥️ Screen Operations**
- Tap, swipe, long press, gestures, text input

**ℹ️ Get Information**
- Screenshot, layout XML, device status, battery, location

**🚀 App Control**
- Open apps, back button

**🔐 Advanced Features** (requires permission)
- Notification list, photos, contacts, calendar, SMS, etc.

---

## 📱 Requirements

**Phone Side**:
- Android 10+ (Android 11+ recommended)
- Install [ClawPaw App](https://github.com/klscool/ClawPaw)
- Grant permissions as needed (enable only what you need)

**Host Side**:
- Node.js 18+ (for Gateway)
- Python 3.8+ (for HTTP scripts)
- Network connectivity (same WiFi or Tailscale)

---

## 🚀 How to Use with OpenClaw

### 1. Install ClawPaw App

Install and configure ClawPaw App on your phone:
```
https://github.com/klscool/ClawPaw
```

### 2. Configure Connection

**Option 1: Gateway (Recommended)**

Phone connects to OpenClaw Gateway via WebSocket, using `nodes` tool.

**Setup Steps**:
1. Configure Gateway address in ClawPaw App
2. Confirm App shows "Connected to Gateway"
3. OpenClaw auto-detects the node

**Option 2: HTTP Direct**

Call phone API directly via Python script.

**Setup Steps**:
1. Ensure phone and host are on same network
2. Configure phone IP and port in `config.yaml`
3. Use `clawpaw_controller.py` script

### 3. Use in OpenClaw

After setup, just tell OpenClaw what you want to do, for example:

```
"Open maps and search for nearby coffee shops"
"Take a screenshot and analyze what's on the screen"
"Check my notifications"
"Order food delivery for me"
"Scroll through Xiaohongshu for me"
```

OpenClaw will automatically call this Skill to execute.

---

## 📖 Detailed Documentation

| Document | Description |
|----------|-------------|
| [`SKILL.md`](SKILL.md) | Complete command list and parameters |
| [`README_PERMISSIONS.md`](README_PERMISSIONS.md) | 24 permissions detailed explanation |
| [`references/INDEX.md`](references/INDEX.md) | Operation guide index (read this first) |
| [`references/apps/app-list.md`](references/apps/app-list.md) | Supported apps list |
| [`references/guides/basic-example.md`](references/guides/basic-example.md) | Basic integration example |

---

## 📦 File Structure

```
clawpaw-android-control/
├── README.md              # This file
├── SKILL.md               # OpenClaw Skill definition
├── README_PERMISSIONS.md  # Permissions documentation (24 permissions)
├── config.yaml            # Configuration file (template)
├── scripts/
│   └── clawpaw_controller.py  # HTTP control script
└── references/
    ├── INDEX.md           # Operation guide index
    ├── apps/
    │   └── app-list.md    # Supported apps list
    └── guides/
        └── basic-example.md # Basic integration example
```

---

## ❓ FAQ

**Q: Connection failed?**  
A: Check if phone and host are on same network, verify Gateway address or IP is correct.

**Q: Tap not working?**  
A: Make sure Accessibility Service is enabled, try re-authorizing permissions.

**Q: Which apps are supported?**  
A: See `references/apps/app-list.md` for a list of app package names.

---

## 🔗 Related Links

- [ClawPaw App](https://github.com/klscool/ClawPaw)
- [OpenClaw Docs](https://docs.openclaw.ai)

---

**Last Updated**: 2026-03-14  
**Version**: v1.0.0

---

---

# 🐾 ClawPaw Android 手机控制

将你的 Android 手机变成 OpenClaw 节点，远程控制并自动执行点击、滑动、输入等操作。

> **提示**：需要在手机上安装 [ClawPaw App](https://github.com/klscool/ClawPaw)。

---

## 🎯 这个 Skill 能做什么

**📱 手机变身为 OpenClaw 节点**
- 手机连接 Gateway，成为 OpenClaw 的一个节点
- 随时查询节点状态和设备信息

**🖥️ 界面操作**
- 点击、滑动、长按、手势、输入文字

**ℹ️ 获取信息**
- 截图、界面布局 XML、设备状态、电量、位置

**🚀 应用控制**
- 打开应用、返回键

**🔐 高级功能**（需授权）
- 通知列表、照片、联系人、日历、短信等

---

## 📱 环境要求

**手机端**：
- Android 10+（推荐 Android 11+）
- 安装 [ClawPaw App](https://github.com/klscool/ClawPaw)
- 按需授权权限（用哪个功能开哪个）

**主机端**：
- Node.js 18+（运行 Gateway）
- Python 3.8+（运行 HTTP 脚本）
- 网络连通（同 WiFi 或 Tailscale）

---

## 🚀 如何让 OpenClaw 使用

### 1. 安装 ClawPaw App

在手机端安装并配置 ClawPaw App：
```
https://github.com/klscool/ClawPaw
```

### 2. 配置连接方式

**方式一：Gateway（推荐）**

手机通过 WebSocket 连接 OpenClaw Gateway，使用 `nodes` 工具调用。

**配置步骤**：
1. 在 ClawPaw App 中配置 Gateway 地址
2. 确认 App 显示「已连接 Gateway」
3. OpenClaw 自动识别节点

**方式二：HTTP 直连**

通过 Python 脚本直接调用手机 API。

**配置步骤**：
1. 确保手机和主机在同一网络
2. 在 `config.yaml` 中配置手机 IP 和端口
3. 使用 `clawpaw_controller.py` 脚本调用

### 3. 在 OpenClaw 中使用

配置完成后，直接告诉 OpenClaw 你要做什么，例如：

```
"帮我打开地图，搜索附近的咖啡店"
"截取当前手机屏幕，分析上面有什么内容"
"看看我有什么通知"
"帮我点个外卖"
"帮我刷刷小红书"
```

OpenClaw 会自动调用这个 Skill 执行操作。

---

## 📖 详细文档

| 文档 | 说明 |
|------|------|
| [`SKILL.md`](SKILL.md) | 完整命令列表和参数 |
| [`README_PERMISSIONS.md`](README_PERMISSIONS.md) | 24 项权限详细说明 |
| [`references/INDEX.md`](references/INDEX.md) | 操作指南索引（执行任务前先看） |
| [`references/apps/app-list.md`](references/apps/app-list.md) | 支持的应用列表 |
| [`references/guides/basic-example.md`](references/guides/basic-example.md) | 基础集成示例 |

---

## 📦 文件结构

```
clawpaw-android-control/
├── README.md              # 本文档
├── SKILL.md               # OpenClaw Skill 定义
├── README_PERMISSIONS.md  # 权限说明（24 项权限详细文档）
├── config.yaml            # 配置文件（模板）
├── scripts/
│   └── clawpaw_controller.py  # HTTP 控制脚本
└── references/
    ├── INDEX.md           # 操作指南索引
    ├── apps/
    │   └── app-list.md    # 支持的应用列表
    └── guides/
        └── basic-example.md # 基础集成示例
```

---

## ❓ 常见问题

**Q: 连接失败怎么办？**  
A: 检查手机和主机是否在同一网络，确认 Gateway 地址或 IP 正确。

**Q: 点击不生效？**  
A: 确认无障碍服务已开启，尝试重新授权权限。

**Q: 支持哪些应用？**  
A: 见 `references/apps/app-list.md` 包名列表。

---

## 🔗 相关链接

- [ClawPaw App](https://github.com/klscool/ClawPaw)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

**最后更新**：2026-03-14  
**适用版本**：v1.0.0
