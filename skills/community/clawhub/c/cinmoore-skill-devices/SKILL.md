---
name: "cinmoore-skill-devices"
description: "神眸智能设备控制技能：整合设备控制、视频录制、事件查询、VLM分析等原子能力，支持AI意图理解与自动化组合。Invoke when user wants to control devices, analyze video, query events, or understand device capabilities."
homepage: "http://192.168.8.60/system/algorithm/cinmoore-skill-devices"
metadata:
  openclaw:
    emoji: "🏠"
    install:
      - id: exe-install-linux
        kind: command
        command: |
          echo "🚀 正在下载独立可执行程序 (Ubuntu/Linux)..."
          curl -L -o cinmoore-skill-devices https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/exe/cinmoore-skill-devices-ubuntu
          curl -L -o .env.cinmoore_skill_devices https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/env/env.cinmoore_skill_devices
          mkdir -p tools/linux
          curl -L -o tools/linux/ffmpeg https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/ffmpeg/linux/ffmpeg
          chmod +x cinmoore-skill-devices
        label: "下载独立程序并初始化配置 (Linux)"
        platform: ["Linux"]

      - id: exe-install-windows
        kind: command
        command: |
          echo 🚀 正在下载独立可执行程序 (Windows)...
          curl -L -o cinmoore-skill-devices.exe https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/exe/cinmoore-skill-devices-windows.exe
          curl -L -o .env.cinmoore_skill_devices https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/env/env.cinmoore_skill_devices
          mkdir -p tools/windows
          curl -L -o tools/windows/ffmpeg.exe https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/ffmpeg/windows/ffmpeg.exe
        label: "下载独立程序并初始化配置 (Windows)"
        platform: ["Windows"]
---

# 神眸智能设备控制技能 (CLI Agent Reference)

> **🔴 AI Agent 核心行为约束 (STRICT INSTRUCTIONS FOR LLM):**
> 1. **严禁越界**：本技能是一个已经编译好的独立二进制程序（无需 Python 环境），你**绝对不可**尝试使用 `cat`、`read` 等命令查看其内容，也**绝对不可**尝试编写 Python 脚本去调用它。
> 2. **唯一交互方式**：你必须且只能使用下方的 **CLI 命令**来完成用户任务。所有的操作都必须通过直接运行该可执行文件来实现。
> 3. **变量检查**：在执行任何设备控制命令前，如果发现当前目录存在新建的 `.env.cinmoore_skill_devices` 且包含 `your_app_key_here` 等默认值，必须先提醒用户补充完整真实的认证信息，或在执行命令时动态拼接全局参数（如 `--app-key xxx`）。

---

## 核心 CLI 指令字典

*注：以下示例使用 Linux 格式 (`./cinmoore-skill-devices`)。如果您在 Windows 下执行，请替换为 `.\cinmoore-skill-devices.exe`。所有命令均需在配置好 `.env.cinmoore_skill_devices` 或带有全局认证参数的前提下执行。*

### 1. 设备基础查询与控制
* **获取设备信息**: `./cinmoore-skill-devices device-info <设备名称>`
* **获取设备列表**: `./cinmoore-skill-devices all-group-device-list`
* **查询设备能力集**: `./cinmoore-skill-devices capabilities <设备名称>`
* **获取算法当前值**: `./cinmoore-skill-devices algorithm-value <设备名称>`
* **设置算法开关**: `./cinmoore-skill-devices set-algorithm <设备名称> <identifier> <value>` 
    *(例: 关闭人形检测 `... set-algorithm 5500... PeopleDetectEnable 0`)*

### 2. 云台 (PTZ) 控制
* **转动云台**: `./cinmoore-skill-devices ptz <设备名称> <动作> [--speed SLOW|MEDIUM|FAST]`
    *(动作支持: LEFT / RIGHT / UP / DOWN / UP_LEFT 等)*
* **停止云台**: `./cinmoore-skill-devices stop-ptz <设备名称>`
* **校准云台**: `./cinmoore-skill-devices ptz-calibrate <设备名称>`

### 3. 事件与视频媒体处理
* **查询报警事件**: `./cinmoore-skill-devices query-events <设备名称> [--begin 时间戳] [--end 时间戳]`
* **开启直播流**: `./cinmoore-skill-devices start-live <设备序列号>`
* **录制视频**: `./cinmoore-skill-devices record <设备序列号> [--duration 秒数] [--output 输出路径]`
* **视频抽帧**: `./cinmoore-skill-devices extract-frames <视频路径> <输出目录> [--mode fps|frame_count] [--fps 帧率] [--frame-count 帧数]`
* **VLM 多图视觉分析**: `./cinmoore-skill-devices see-analyze <抽帧目录> [--prompt 分析提示词]`

### 4. 复合型 AI 自动化指令
* **自然语言意图直达**: `./cinmoore-skill-devices ai-intent <设备名称> "<自然语言指令>"`
    *(例: `... ai-intent SN123 "不想检测到人"`，自动解析并执行对应的算法开关)*
* **云台转动+录制组合**: `./cinmoore-skill-devices ptz-record <设备名称> <动作> [--speed SLOW|MEDIUM|FAST] [--duration 秒数] [--output 输出路径] [--stop-duration 秒数]`