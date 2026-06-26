---
name: clawpaw-android-control
description: |
  Android 手机自动化控制技能。支持 Node（Gateway）和 HTTP 两种连接方式，提供点击、滑动、输入、截图、布局获取、应用打开等操作。
  （需 Java 11+、Android 10+ 手机，安装 ClawPaw App 并开启无障碍服务）
---

# ClawPaw Android 手机控制

## 📖 执行前必读

### 📱 环境要求

**手机端**：
- Android 10+（推荐 Android 11+）
- 安装 [ClawPaw App](https://github.com/klscool/ClawPaw)
- 开启无障碍服务（必需）
- 部分功能需授权额外权限（见 [权限说明](README_PERMISSIONS.md)）

**主机端**：
- Node.js 18+（运行 Gateway）
- Python 3.8+（运行 HTTP 脚本）
- 网络连通（同 WiFi 或 Tailscale）

---

**路径说明**：本文档中的 `<skill_dir>` 是占位符，代表本 skill 的实际存放路径（如 `~/.openclaw/skills/clawpaw-android-control`）。使用时请替换为实际路径。

**执行任何具体任务前，请先查阅操作指南索引：**

```
<skill_dir>/references/INDEX.md
```

该索引包含：
- ✅ 所有支持的操作场景
- ✅ 对应指南文件位置
- ✅ 快速决策流程
- ✅ 支持的应用列表

**通用流程**：
1. 确认任务场景（如"评论互动"、"搜索地点"）
2. 在 INDEX.md 中找到对应指南
3. 读取指南后执行任务
4. 优先使用获取布局的方法执行任务

---

## 方式一：Node（Gateway）

手机通过 WebSocket 连接 Gateway，通过 OpenClaw `nodes` 工具调用。

**前提**：手机端 App 显示「已连接 Gateway」

---

### 🎯 原生 Action（优先使用）

以下原生 action **直接用 `nodes action=<action>` 调用，无需 invoke**，有参数验证和统一返回格式：

| Action | 说明 | 参数 | 示例 |
|--------|------|------|------|
| `device_status` | 设备状态（电量、屏幕、WiFi、位置） | 无 | `nodes device_status --node <id>` |
| `device_info` | 设备信息（型号、厂商、Android 版本） | 无 | `nodes device_info --node <id>` |
| `device_health` | 设备健康（内存、电池详情）**仅 Node** | 无 | `nodes device_health --node <id>` |
| `device_permissions` | 权限状态 **仅 Node** | 无 | `nodes device_permissions --node <id>` |
| `location_get` | 获取位置 | 无 | `nodes location_get --node <id>` |
| `notifications_list` | 通知列表 | 无 | `nodes notifications_list --node <id>` |
| `photos_latest` | 最新照片（返回图片） | 无 | `nodes photos_latest --node <id>` |
| `status` | 列出所有节点 | 无 | `nodes status` |
| `describe` | 节点详情 | `--node <id>` | `nodes describe --node <id>` |
| `notify` | 发送通知 | `--title`, `--body` | `nodes notify --node <id> --title "标题" --body "内容"` |

**其他所有命令用 `invoke` 方式 ↓**

---

### 🔧 Invoke 命令（非原生）

**格式**：
```bash
openclaw nodes invoke --node <NODE_ID> --command <命令> --params '<JSON>'
```

**参数规则**：
- 无参数命令：`--params '{}'`
- 有参数：JSON 格式，键名与下表一致
- 带文字：传 `text`/`title`/`body` 等字段

#### 无障碍 / 界面操作（需开启无障碍服务）

| 命令 | 参数 | 说明 | 示例 |
|------|------|------|------|
| `click` | `x`, `y` | 点击坐标 | `{"x":500,"y":1000}` |
| `swipe` | `start_x`, `start_y`, `end_x`, `end_y`, `duration`(可选) | 滑动 | `{"start_x":720,"start_y":2500,"end_x":720,"end_y":500}` |
| `input_text` | `x`, `y`, `text` | 点击后输入（需 ClawPaw 输入法） | `{"x":300,"y":800,"text":"内容"}` |
| `input_text_direct` | `x`, `y`, `text` | 无障碍直接输入（无需输入法） | `{"x":300,"y":800,"text":"内容"}` |
| `long_press` | `x`, `y` | 长按 700ms | `{"x":500,"y":1000}` |
| `two_finger_swipe_same` | `start_x`, `start_y`, `end_x`, `end_y` | 两指同向滑动（放大） | `{"start_x":400,"start_y":1200,"end_x":400,"end_y":400}` |
| `two_finger_swipe_opposite` | `start_x`, `start_y`, `end_x`, `end_y` | 两指反向滑动（缩放） | `{"start_x":300,"start_y":800,"end_x":600,"end_y":800}` |
| `back` | 无 | 返回键 | `{}` |
| `get_layout` | 无 | 获取界面布局 XML | `{}` |
| `screenshot` | 无 | 截图（Base64） | `{}` |
| `open_schema` | `schema` 或 `uri` | 按包名或 schema 打开应用 | `{"schema":"com.android.chrome"}` |

#### 设备状态（无需无障碍）

| 命令 | 参数 | 返回 |
|------|------|------|
| `get_battery` | 无 | 电量百分比 0-100 |
| `get_wifi_name` | 无 | WiFi SSID |
| `get_screen_state` | 无 | `on` / `off` |
| `get_state` | 无 | 完整状态（定位+WiFi+屏幕+电量+分辨率） |

#### 硬件控制

| 命令 | 参数 | 说明 |
|------|------|------|
| `vibrate` | `duration_ms`（可选，默认 200） | 震动 |
| `camera_rear` | 无 | 后置拍照（异步） |
| `camera_front` | 无 | 前置拍照（异步） |
| `screen_on` | 无 | 点亮屏幕 |

#### 通知管理（需通知监听权限）

| 命令 | 参数 | 说明 |
|------|------|------|
| `notification.show` | `title`, `text` 或 `body` | 推送本地通知 |
| `notifications.push` | `title`, `body` | 同上（别名） |
| `system.notify` | `title`, `body` | 系统通知 |
| `notifications.actions` ⚠️ | `action`, `key` | 操作通知（dismiss/open/reply）**仅 Node** |

#### 数据访问（需相应权限）

| 命令 | 参数 | 说明 |
|------|------|------|
| `contacts.list` | `limit`（可选，默认 500） | 联系人列表 |
| `contacts.search` | `query`, `limit` | 搜索联系人 |
| `photos.latest` | `limit`（可选，默认 50） | 最近照片 |
| `calendar.list` | `limit`（可选，默认 100） | 日历事件 |
| `calendar.events` | `limit` | 同上（别名） |

#### 音量控制

| 命令 | 参数 | 说明 |
|------|------|------|
| `volume.get` | 无 | 获取音量 |
| `volume.set` | `stream`, `volume` | 设置音量（stream: `media`/`ring`） |

#### 文件操作（需存储权限）

| 命令 | 参数 | 说明 |
|------|------|------|
| `file.read_text` | `path` | 读取 UTF-8 文本 |
| `file.read_base64` | `path` | 读取二进制文件 |

#### 传感器与运动

| 命令 | 参数 | 说明 |
|------|------|------|
| `sensors.steps` | 无 | 步数 |
| `sensors.light` | 无 | 光照 lux |
| `sensors.info` | 无 | 传感器列表 |
| `motion.pedometer` ⚠️ | `startISO`, `endISO` | 计步（ISO8601 时间）**仅 Node** |
| `motion.activity` ⚠️ | 无 | 活动识别（步行/静止等）**仅 Node** |

#### 蓝牙/WiFi

| 命令 | 参数 | 说明 |
|------|------|------|
| `bluetooth.list` | 无 | 已配对设备 |
| `wifi.info` | 无 | WiFi 状态 |
| `wifi.enable` | `enabled` | 开关 WiFi（true/false） |

#### 短信/电话（需相应权限）

| 命令 | 参数 | 说明 |
|------|------|------|
| `sms.list` | `limit` | 收件箱短信 |
| `sms.send` | `address`/`to`, `body`/`text` | 发送短信 |
| `phone.dial` | `number`/`phone` | 打开拨号界面 |
| `phone.call` | `number`/`phone` | 直接拨打电话 |

#### 铃声与勿扰

| 命令 | 参数 | 说明 |
|------|------|------|
| `ringer.get` | 无 | 铃声模式（normal/silent/vibrate） |
| `ringer.set` | `mode` | 设置铃声模式 |
| `dnd.get` | 无 | 勿扰状态 |
| `dnd.set` | `enabled` | 设置勿扰（true=仅闹钟） |

---

### ⚠️ 注意事项

1. **无障碍服务**：界面操作类命令需要开启 ClawPaw 无障碍服务

2. **权限授权**：
   - 部分功能需要用户手动授权（通知、联系人、照片等）
   - 具体授权路径见 [`README_PERMISSIONS.md`](README_PERMISSIONS.md)

3. **网络连通**：
   - Gateway 模式：手机需连接到同一 Gateway
   - HTTP 模式：手机与主机需网络互通（同 WiFi 或 Tailscale）

4. **命令命名**：
   - 原生 action 用**下划线**：`device_status`
   - invoke 命令用**点号**：`device.status`、`volume.set`

5. **返回布局**：无障碍命令默认返回布局，可加 `return_layout_after: false` 关闭

---

## 🎯 快速开始

### 1. 手机端安装 ClawPaw App

1. 下载 [ClawPaw App](https://github.com/klscool/ClawPaw/releases)
2. 安装到 Android 手机（Android 10+）
3. 开启无障碍服务：
   ```
   设置 → 辅助功能 → 已下载的服务 → ClawPaw Accessibility Service → 开启
   ```
4. （可选）按需授予权限：位置、通知、联系人、照片等

---

### 2. 主机端配置

#### 方式一：Gateway（WebSocket）

```bash
# 确认 Gateway 已运行
openclaw gateway status

# 添加节点（ClawPaw App 连接到 Gateway 后自动注册）
openclaw nodes status
```

#### 方式二：本地 HTTP

```bash
# 确认手机和主机网络连通（同 WiFi 或 Tailscale）
# 手机端 ClawPaw App 端口：8765（默认）

# 使用 Python 脚本
pip3 install requests pyyaml
cd ~/.openclaw/skills/clawpaw-android-control/scripts
python3 clawpaw_controller.py device_info
```

---

### 3. 测试命令

```bash
# 查看设备信息（Gateway）
openclaw nodes device_info --node <NODE_ID>

# 获取状态（Gateway）
openclaw nodes device_status --node <NODE_ID>

# 获取最新照片（Gateway）
openclaw nodes photos_latest --node <NODE_ID>

# HTTP 方式测试
python3 clawpaw_controller.py device_info
```

---

## ⚠️ 权限说明

ClawPaw 使用 **24 项权限**，分为三类：

| 类别 | 权限数 | 说明 |
|------|--------|------|
| **基础权限** | 9 项 | 安装即授予，必需 |
| **用户授权** | 14 项 | 手动授权，可选 |
| **特殊权限** | 2 项 | 特殊授权，可选 |

**详细说明**：见 [`README_PERMISSIONS.md`](README_PERMISSIONS.md)

| 功能 | 必需权限 | 示例命令 |
|------|---------|---------|
| 点击/滑动/输入 | `BIND_ACCESSIBILITY_SERVICE` | `click`, `swipe`, `input_text` |
| 定位 | `ACCESS_FINE_LOCATION` | `location_get` |
| 通知 | `POST_NOTIFICATIONS` | `notifications_list` |
| 联系人 | `READ_CONTACTS` | `contacts.list` |
| 照片 | `READ_MEDIA_IMAGES` | `photos_latest` |
| 短信 | `READ_SMS` + `SEND_SMS` | `sms.list`, `sms.send` |
| 电话 | `CALL_PHONE` | `phone.dial`, `phone.call` |
| 文件读取 | `READ_EXTERNAL_STORAGE` | `file.read_text` |

---

[61 more lines in file. Use offset=170 to continue.]

手机端 HTTP 服务（默认端口 8765），通过 Python 脚本调用。

**前提**：手机和主机网络互通（同 WiFi 或 Tailscale）

### 配置

```yaml
# config.yaml
network_type: local  # local / tailscale / wifi
host: 127.0.0.1      # local 模式不需要
port: 8765
timeout: 10

# 百炼 API 配置（视觉分析需要）
dashscope_api_key: sk-xxx
dashscope_model: qwen3.5-plus
```

### 脚本调用

**脚本位置**：`<skill_dir>/scripts/clawpaw_controller.py`

```bash
# 基础操作
python3 clawpaw_controller.py click 500 1000
python3 clawpaw_controller.py swipe 500 1500 500 500
python3 clawpaw_controller.py input_text_direct 300 800 "内容"
python3 clawpaw_controller.py back

# 状态查询
python3 clawpaw_controller.py get_battery
python3 clawpaw_controller.py get_wifi_name
python3 clawpaw_controller.py device_info

# 视觉分析（HTTP 独有）
python3 clawpaw_controller.py analyze "找到搜索框并返回坐标"
python3 clawpaw_controller.py analyze "找到评论入口" --no-save
```

完整命令列表见脚本帮助：`python3 clawpaw_controller.py --help`

---

## 快速参考

| 需求 | 推荐方式 | 命令 |
|------|---------|------|
| 查设备状态 | 原生 action | `device_status` |
| 查设备信息 | 原生 action | `device_info` |
| 获取位置 | 原生 action | `location_get` |
| 获取通知 | 原生 action | `notifications_list` |
| 获取照片 | 原生 action | `photos_latest` |
| 点击/滑动/输入 | invoke | `click`/`swipe`/`input_text` |
| 打开应用 | invoke | `open_schema` |
| 截图/布局 | invoke | `screenshot`/`get_layout` |

---

*更新时间：2026-03-13*
