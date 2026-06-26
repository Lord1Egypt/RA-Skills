```markdown
# 神眸智能设备控制 SDK (Cinmoore Skill Devices)

本级项目提供神眸智能摄像设备的原子能力调用和 AI 意图理解功能，支持通过自然语言组合调用多种能力完成复杂任务。

> **安全声明**：为了保护核心业务逻辑与知识产权，本项目的核心引擎（`base` 目录）已通过 PyArmor 进行字节码加密与混淆。

---

## 🚀 核心特性

- **🔌 设备基础控制**：设备发现、能力集查询、状态监控。
- **🤖 智能算法开关**：支持近 30 种算法检测（人形、车辆、宠物、包裹等）的查询与动态启停。
- **🎥 视频流与存储**：支持自动拉取设备直播流、异步 RTMP 视频录制、精准抽帧。
  > *注：为极致缩减包体积，程序在首次执行媒体相关功能时，会自动根据当前操作系统从云端高速下载并配置所需的 FFmpeg 依赖包。*
- **🕹️ PTZ 云台控制**：精准的云台方向控制、速度调节与自动校准。
- **🧠 AI 意图解析**：结合大语言模型 (LLM)，将用户的自然语言（如“不想检测到人”）精准解析并转换为对应的设备 API 调用。
- **👁️ 视觉分析 (VLM)**：结合视觉大模型，对摄像头画面进行多图异常分析与场景识别。
- **⚡ 组合技能**：支持复杂逻辑的一键执行（如：云台转动 + 边转边录 + 抽帧 + AI画面分析）。

---

## 📦 安装指南

直接下载可执行程序：

- **Linux**: [cinmoore-skill-devices-ubuntu](https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/exe/cinmoore-skill-devices-ubuntu)
- **Windows**: [cinmoore-skill-devices-windows.exe](https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/exe/cinmoore-skill-devices-windows.exe)

## ⚙️ 环境配置

在运行任何命令之前，系统需要获取身份认证和模型调用凭证。为了避免每次运行时手动输入，我们建议你在运行目录创建一个 `.env.cinmoore_skill_devices` 文件，或者直接将它们配置为系统的全局环境变量：

```env.cinmoore_skill_devices
# 日志配置
LOG_CONSOLE_LEVEL=INFO
LOG_FILE_LEVEL=DEBUG

# 存储警告阈值（GB）
STORAGE_WARNING_GB=5

# SDK 认证配置
SDK_BASE_URL=[https://sdk-api-cn.superacme.com](https://sdk-api-cn.superacme.com)
SDK_APP_KEY=your_app_key
SDK_APP_SECRET=your_app_secret
SDK_USERNAME=your_username
SDK_PASSWORD=your_password

# LLM/VLM 模型配置
OPENAI_BASE_URL=[https://openapi-cn.superacme.com](https://openapi-cn.superacme.com)
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=[https://dashscope.aliyuncs.com/compatible-mode/v1](https://dashscope.aliyuncs.com/compatible-mode/v1)
LLM_MODEL=qwen3-235b-a22b-instruct-2507
VLM_MODEL=qwen3-vl-235b-a22b-instruct
```

---

## 🛠️ CLI 快速使用

安装成功后，系统会自动注册 `cinmoore-skill-devices` 全局命令。以下是常用场景的快速调用示例：

### 1. 设备与能力查询
```bash
# 获取设备基本信息
cinmoore-skill-devices device-info <设备名称>

# 显示该设备支持的所有能力集
cinmoore-skill-devices capabilities <设备名称>
```

### 2. 算法检测控制
```bash
# 获取当前算法检测值
cinmoore-skill-devices algorithm-value <设备名称>

# 设置算法开关 (例如：关闭人形检测)
cinmoore-skill-devices set-algorithm <设备名称> PeopleDetectEnable 0
```

### 3. PTZ 云台控制
```bash
# 转动云台
cinmoore-skill-devices ptz <设备名称> LEFT --speed FAST

# 停止转动
cinmoore-skill-devices stop-ptz <设备名称>
```

### 4. 视频流与抽帧处理
```bash
# 开启直播并录制 10 秒视频
cinmoore-skill-devices record <设备名称> --duration 10 --output ./output/video.mp4

# 从录制好的视频中每秒抽 1 帧
cinmoore-skill-devices extract-frames ./output/video.mp4 ./output/frames --mode fps --fps 1
```

### 5. 🔮 AI 意图理解与自动化
```bash
# 让 AI 理解你的意图并自动调用对应的底层接口
cinmoore-skill-devices ai-intent <设备名称> "有人经过时通知我"

# VLM 多图智能分析
cinmoore-skill-devices see-analyze ./output/frames --prompt "分析画面中是否有异常情况"

# 组合技：自动转动云台录制并保存
cinmoore-skill-devices ptz-record <设备名称> LEFT --duration 30 --speed MEDIUM
```

---

## ❓ 常见问题

**Q: 运行 `record` 或 `extract-frames` 命令时卡住了怎么办？**
A: 首次运行涉及多媒体的命令时，程序会在后台自动下载 FFmpeg 依赖（支持终端进度条显示）。如果网速较慢，请耐心等待（最长限时 5 分钟）。下载完成后即可永久离线使用。如果下载一直失败，请检查网络连接或尝试手动下载放置到指定目录。

**Q: 运行时提示 `ModuleNotFoundError: No module named 'base...'`**
A: 请确保您运行的目录是**干净的测试或部署目录**，不要在含有原始未混淆 `base` 源码的开发目录中测试安装好的 whl 包，以防 Python 发生相对路径导入冲突。

**Q: 运行时提示 `httpx[h2]` 警告**
A: 这是正常的依赖回退警告（退回 HTTP/1.1）。若要追求极致的请求速度，可在当前环境中执行 `uv pip install httpx[h2]` 以启用 HTTP/2 支持。
```