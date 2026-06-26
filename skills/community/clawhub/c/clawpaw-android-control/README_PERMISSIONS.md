# ClawPaw 权限说明（发布版 README）

> 本文档适用于 `clawpaw-android-control` Skill 发布版

---

## 📖 权限说明概览

ClawPaw 使用 **24 项权限**，分为三类：

- ✅ **基础权限**（安装即授予，必需）
- 🔐 **用户授权权限**（需手动开启，可选）
- ⚠️ **特殊权限**（需特殊授权）

---

## ✅ 一、基础功能（无需额外授权）

这些功能**仅需安装 ClawPaw App 并开启无障碍服务**即可使用：

| 功能 | 说明 | 必需权限 |
|------|------|---------|
| **界面操作** | | |
| 点击坐标 | 在指定位置点击 | `BIND_ACCESSIBILITY_SERVICE` |
| 滑动 | 滑动操作（单指/双指） | `BIND_ACCESSIBILITY_SERVICE` |
| 输入文字 | 在指定位置输入文本 | `BIND_ACCESSIBILITY_SERVICE` |
| 获取布局 | 获取当前界面 XML | `BIND_ACCESSIBILITY_SERVICE` |
| 截图 | 截取当前屏幕 | `BIND_ACCESSIBILITY_SERVICE` |
| 返回键 | 执行返回操作 | `BIND_ACCESSIBILITY_SERVICE` |
| 打开应用 | 按包名/URI 打开应用 | `BIND_ACCESSIBILITY_SERVICE` |
| **设备信息** | | |
| 设备信息 | 型号、厂商、Android 版本 | 无 |
| 电量查询 | 当前电量百分比 | 无 |
| WiFi 名称 | 当前 WiFi SSID | `ACCESS_WIFI_STATE` |
| 屏幕状态 | 亮/灭 | 无 |
| 震动 | 震动反馈 | `VIBRATE` |
| 唤醒屏幕 | 点亮屏幕 | `WAKE_LOCK` |
| 拍照 | 前/后置拍照 | `CAMERA` |
| 音量控制 | 获取/设置音量 | `MODIFY_AUDIO_SETTINGS`、`CHANGE_WIFI_STATE` |
| WiFi 开关 | 开/关 WiFi | `CHANGE_WIFI_STATE` |

### 🔧 开启无障碍服务步骤

1. 打开 ClawPaw App
2. 点击「无障碍服务」卡片
3. 进入系统设置页面
4. 选择「ClawPaw Accessibility Service」并开启
5. 勾选「允许辅助功能服务访问所有应用数据」

---

## 🔐 二、高级功能（需要用户授权）

以下功能需要在系统设置中手动授予相应权限：

### 📍 1. 位置权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `ACCESS_FINE_LOCATION` | `location_get` | 设置 → 应用 → 权限 → 位置 |

### 📱 2. 通知权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `POST_NOTIFICATIONS` | `notifications_list`, `notification.show` | 设置 → 应用 → 权限 → 通知 |

### 👥 3. 联系人权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `READ_CONTACTS` | `contacts.list`, `contacts.search` | 设置 → 应用 → 权限 → 通讯录 |

### 📅 4. 日历权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `READ_CALENDAR` | `calendar.list`, `calendar.events` | 设置 → 应用 → 权限 → 日历 |

### 📸 5. 照片权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `READ_MEDIA_IMAGES` | `photos_latest` | 设置 → 应用 → 权限 → 照片 |

### 📝 6. 短信权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `READ_SMS` | `sms.list` | 设置 → 应用 → 权限 → 短信 |
| `SEND_SMS` | `sms.send` | 设置 → 应用 → 权限 → 短信 |

### 📞 7. 电话权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `CALL_PHONE` | `phone.dial`, `phone.call` | 设置 → 应用 → 权限 → 电话 |

### 🎵 8. 步数与活动

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `ACTIVITY_RECOGNITION` | `sensors.steps`, `motion.pedometer` | 设置 → 应用 → 权限 → 健康与活动 |
| `BLUETOOTH_CONNECT` | `bluetooth.list` | 设置 → 应用 → 权限 → 蓝牙 |

### 📂 9. 存储权限

| 权限 | 对应命令 | 授权路径 |
|------|---------|---------|
| `READ_EXTERNAL_STORAGE` | `file.read_text`, `file.read_base64` | 设置 → 应用 → 权限 → 其他权限 |
| `WRITE_EXTERNAL_STORAGE` (≤Android 12) | `file.read_text`, `file.read_base64` | 设置 → 应用 → 权限 → 其他权限 |

---

## ⚠️ 三、特殊权限（需特殊授权）

### 🔍 1. 查询所有应用（`QUERY_ALL_PACKAGES`）

- **用途**：查询所有已安装应用包名，用于 `open_schema` 命令
- **风险**：可扫描用户安装的所有应用
- **授权方式**：
  ```
  设置 → 应用 → 所有应用列表 → ClawPaw → 权限管理
  ```

### 📁 2. 全局文件管理（`MANAGE_EXTERNAL_STORAGE`）

- **用途**：读取大文件
- **风险**：可访问用户所有文件
- **授权方式**：
  ```
  设置 → 存储 → 更多设置 → 存储访问权限
  ```

### 🚫 3. 勿扰策略（`ACCESS_NOTIFICATION_POLICY`）

- **用途**：修改铃声/勿扰模式
- **风险**：可绕过用户设置修改系统行为
- **授权方式**：
  ```
  设置 → 声音 → 勿扰 → 应用控制
  ```

---

## 🛠 权限授予完整指南

### 方法一：通过 ClawPaw App 引导

1. 打开 ClawPaw App
2. 进入「初始化」页面
3. 逐项检查并授权：
   - ✅ 无障碍服务（必选）
   - ✅ 输入法（建议）
   - ✅ 各项权限（按需授权）

### 方法二：手动授权

| 权限 | 授权路径 |
|------|---------|
| 无障碍服务 | 设置 → 辅助功能 → 已下载的服务 → ClawPaw Accessibility Service |
|输入法 | 设置 → 语言和输入法 → 当前键盘 |
|通知 | 设置 → 应用 → 推送与通知 |
|位置 | 设置 → 位置信息 → 应用权限 |
|通讯录 | 设置 → 隐私 → 项目访问权限 → 通讯录 |
|日历 | 设置 → 隐私 → 项目访问权限 → 日历 |
|照片 | 设置 → 隐私 → 项目访问权限 → 照片 |
|短信 | 设置 → 隐私 → 项目访问权限 → 短信和彩信 |
|电话 | 设置 → 隐私 → 项目访问权限 → 电话 |
|健康/活动 | 设置 → 隐私 → 项目访问权限 → 健康 |
|蓝牙 | 设置 → 蓝牙 → 应用蓝牙权限 |
|存储 | 设置 → 存储 → 更多设置 → 存储访问权限 |

---

## 📊 权限最小集（推荐配置）

### 🎯 基础使用（必备）

```
✅ ACCESS_FINE_LOCATION（可选）
✅ ACCESS_WIFI_STATE（安装即授）
✅ VIBRATE（安装即授）
✅ WAKE_LOCK（安装即授）
✅ MODIFY_AUDIO_SETTINGS（安装即授）
✅ CHANGE_WIFI_STATE（安装即授）
✅ BIND_ACCESSIBILITY_SERVICE（必需）
```

### 👍 推荐配置（完整功能）

```
✅ ACCESS_FINE_LOCATION（定位）
✅ POST_NOTIFICATIONS（通知）
✅ READ_CONTACTS（联系人）
✅ READ_CALENDAR（日历）
✅ READ_MEDIA_IMAGES（照片）
✅ READ_SMS（短信读取）
✅ SEND_SMS（短信发送）
✅ CALL_PHONE（电话）
✅ ACTIVITY_RECOGNITION（步数）
✅ BLUETOOTH_CONNECT（蓝牙）
✅ READ_EXTERNAL_STORAGE（文件读取）
✅ ACCESS_NOTIFICATION_POLICY（铃声/勿扰）
```

### 🚫 避免授权的权限

- `MANAGE_EXTERNAL_STORAGE`（除非需要读取大文件）
- `QUERY_ALL_PACKAGES`（除非需要精确识别应用包名）

---

## ❓ 常见问题

### Q1: 为什么需要无障碍服务？

**A**: 无障碍服务是实现点击、滑动、输入等界面操作的核心。没有它，ClawPaw 无法与应用界面交互。

### Q2: 位置权限会泄露我的位置吗？

**A**: 定位权限仅在执行 `location_get` 命令时获取位置信息，且仅返回 lat/lon 坐标，不包含详细地址。

### Q3: 如何只授权必要的权限？

**A**: 根据使用需求选择性授权：
- 仅做界面操作 → 仅需无障碍服务
- 需要通知 → 额外授权通知权限
- 需要通讯录/日历 → 按需授权

### Q4: 迁移手机后权限丢失怎么办？

**A**: 重新开启无障碍服务和必要的权限授权即可。

### Q5: 权限在 Android 13+ 有什么变化？

**A**: Android 13+ 使用 `READ_MEDIA_IMAGES` 代替 `READ_EXTERNAL_STORAGE` 访问照片。

---

## 📝 权限变更历史

| 版本 | 变更内容 |
|------|---------|
| v1.0.0 | 初次发布，包含 24 项权限 |

---

**最后更新**：2026-03-14  
**适用版本**：v1.0.0
