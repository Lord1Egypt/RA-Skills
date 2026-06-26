---
name: android-adb-skill
description: Android 开发调试技能，通过系统 ADB 工具操作 Android 设备。以下场景必须触发此技能：(1) 直接 ADB 操作——安装 APK、查看设备列表、抓取 logcat 日志、查看已安装应用、清除应用数据、截图、重启设备、拉取/推送文件、查看 CPU/内存/电池信息、adb shell 操作；(2) Android 开发编码任务——编写或修改 Android/Flutter/HarmonyOS 代码、修复 Android 端 Bug、实现 Android 功能、调整 AndroidManifest、修改 Gradle 配置等一切涉及安卓端的开发工作，编码完成后必须主动提示用户通过 ADB 部署验证修改成果；(3) 验证与测试——用户说"试一下""看看效果""测试一下""跑一下""装到手机上"等语句，只要上下文是 Android 项目，立即触发设备检测并引导安装验证。即使用户只说"帮我装一下"或"看看日志"，只要上下文涉及 Android 设备或 Android 项目，也必须触发此技能。
---

# Android ADB 调试技能

## 概述

此技能通过调用系统环境变量中的 `adb` 命令操作 Android 设备。执行任何 ADB 操作前，必须先执行「设备检测流程」。

---

## 编码完成后的验证流程

**每当完成 Android 端代码修改（包括 Flutter Android、原生 Android 等），必须在回复末尾主动附上以下提示：**

> 📱 **代码已修改，建议通过 ADB 验证效果：**
> 1. 构建 APK：`flutter build apk --debug` / `./gradlew assembleDebug`
> 2. 检测设备并安装：（执行设备检测流程 → 自动安装）
> 3. 查看运行日志：`adb logcat --pid=$(adb shell pidof <包名>)`
>
> 需要我帮你执行安装和日志监控吗？

**不要等用户主动询问，编码任务完成即触发此提示。**

---

## 核心流程：设备检测

**每次执行 ADB 操作前必须先运行设备检测。**

```bash
# 检测 adb 是否可用
which adb || echo "ADB_NOT_FOUND"

# 获取已连接设备列表
adb devices
```

### 设备数量判断逻辑

| 情况 | 处理方式 |
|------|---------|
| adb 命令不存在 | 提示用户安装 Android SDK Platform Tools，并给出下载地址 |
| 0 台设备 | 提示用户连接设备或开启 USB 调试，给出排查步骤 |
| 1 台设备 | **直接执行**，无需用户确认 |
| 多台设备 | **展示设备列表**，让用户选择目标设备，所有后续命令加 `-s <serial>` 参数 |

### 设备列表展示格式（多设备时）

```
检测到 N 台已连接的 Android 设备：

序号  设备序列号           状态    设备信息
 1   emulator-5554        online  [模拟器]
 2   R3CT90BFXXX         online  [获取型号]
 3   192.168.1.100:5555   online  [无线连接]

请输入序号选择目标设备：
```

获取设备型号：
```bash
adb -s <serial> shell getprop ro.product.model
```

---

## 功能模块

### 1. 安装 APK

```bash
# 单设备
adb install -r <apk_path>

# 指定设备
adb -s <serial> install -r <apk_path>

# 常用参数说明：
# -r  允许覆盖安装（保留数据）
# -d  允许降级安装
# -g  自动授予所有运行时权限（Android 6.0+）
# -t  允许安装测试 APK
```

**安装结果判断**：
- `Success` → 安装成功，显示包名
- `INSTALL_FAILED_*` → 解析错误码并给出中文说明和解决方案

常见错误码对照表见 `references/install-errors.md`

---

### 2. 抓取 Logcat 日志

```bash
# 清除旧日志
adb [-s <serial>] logcat -c

# 按包名过滤（需先获取 PID）
PID=$(adb [-s <serial>] shell pidof <package_name>)
adb [-s <serial>] logcat --pid=$PID

# 按 Tag 过滤
adb [-s <serial>] logcat -s <TAG>:V

# 按级别过滤（V/D/I/W/E/F）
adb [-s <serial>] logcat *:E

# 保存到文件
adb [-s <serial>] logcat --pid=$PID > logcat_$(date +%Y%m%d_%H%M%S).log

# 实时过滤关键词
adb [-s <serial>] logcat | grep <keyword>
```

**用户输入包名时的标准流程**：
1. 先用 `pidof` 获取 PID
2. 若 PID 为空（应用未运行），提示用户先启动应用，或改用包名关键词 grep
3. 提供实时输出与保存文件两个选项

---

### 3. 查看已安装应用列表

```bash
# 所有应用
adb [-s <serial>] shell pm list packages

# 只看第三方应用（用户安装的）
adb [-s <serial>] shell pm list packages -3

# 只看系统应用
adb [-s <serial>] shell pm list packages -s

# 包含 APK 路径
adb [-s <serial>] shell pm list packages -f

# 搜索关键词（如 "wechat"）
adb [-s <serial>] shell pm list packages | grep <keyword>

# 获取应用详细信息
adb [-s <serial>] shell dumpsys package <package_name>
```

**输出格式化**：去掉 `package:` 前缀，每行一个包名，按字母排序后展示。

---

### 4. 卸载应用

```bash
# 卸载（保留数据）
adb [-s <serial>] shell pm uninstall -k <package_name>

# 完全卸载
adb [-s <serial>] uninstall <package_name>
```

---

### 5. 清除应用数据

```bash
adb [-s <serial>] shell pm clear <package_name>
```

---

### 6. 启动/停止应用

```bash
# 启动应用（需要知道 MainActivity）
adb [-s <serial>] shell monkey -p <package_name> -c android.intent.category.LAUNCHER 1

# 强制停止
adb [-s <serial>] shell am force-stop <package_name>

# 启动指定 Activity
adb [-s <serial>] shell am start -n <package_name>/<activity_name>
```

---

### 7. 截图与录屏

```bash
# 截图并拉取到本地
adb [-s <serial>] shell screencap /sdcard/screenshot.png
adb [-s <serial>] pull /sdcard/screenshot.png ./screenshot_$(date +%Y%m%d_%H%M%S).png

# 录屏（最长3分钟，Ctrl+C 停止）
adb [-s <serial>] shell screenrecord /sdcard/record.mp4
adb [-s <serial>] pull /sdcard/record.mp4 ./record_$(date +%Y%m%d_%H%M%S).mp4
```

---

### 8. 文件操作

```bash
# 推送文件到设备
adb [-s <serial>] push <local_path> <device_path>

# 从设备拉取文件
adb [-s <serial>] pull <device_path> <local_path>
```

---

### 9. 设备信息查询

```bash
# 设备型号
adb [-s <serial>] shell getprop ro.product.model

# Android 版本
adb [-s <serial>] shell getprop ro.build.version.release

# API Level
adb [-s <serial>] shell getprop ro.build.version.sdk

# 电池信息
adb [-s <serial>] shell dumpsys battery

# CPU 信息
adb [-s <serial>] shell cat /proc/cpuinfo

# 内存信息
adb [-s <serial>] shell cat /proc/meminfo

# 应用内存占用
adb [-s <serial>] shell dumpsys meminfo <package_name>

# 设备 IP 地址
adb [-s <serial>] shell ip addr show wlan0
```

---

### 10. 无线 ADB 连接

```bash
# USB 连接后，开启 TCP 模式（Android 11 以下）
adb [-s <serial>] tcpip 5555
adb connect <device_ip>:5555

# Android 11+ 无线配对（设置 → 开发者选项 → 无线调试）
adb pair <ip>:<port>   # 输入配对码
adb connect <ip>:5555
```

---

### 11. 重启设备

```bash
# 正常重启
adb [-s <serial>] reboot

# 重启到 Recovery
adb [-s <serial>] reboot recovery

# 重启到 Bootloader
adb [-s <serial>] reboot bootloader
```

---

## 输出规范

1. **始终显示实际执行的命令**，让用户知道运行了什么
2. **命令输出用代码块包裹**，保持原始格式
3. **中文解释结果**，不要让用户自己看英文错误
4. **多步骤操作**给出进度提示（如"正在安装... 安装完成 ✓"）
5. **失败时**给出具体原因和解决步骤，不只是报错

---

## ADB 环境排查

若 `adb` 命令找不到：

```bash
# macOS / Linux 检查
echo $ANDROID_HOME
ls $ANDROID_HOME/platform-tools/adb

# Windows 检查
echo %ANDROID_HOME%
where adb
```

**下载地址**：https://developer.android.com/studio/releases/platform-tools

**PATH 配置**（以 macOS/Linux 为例）：
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk   # macOS
export PATH=$PATH:$ANDROID_HOME/platform-tools
```