---
name: captionstranslation
description: 自动化音视频字幕提取与翻译工具，利用 FFmpeg 和本地 Python 脚本生成双语 SRT。
---

# caption_translation自动化音视频字幕提取与翻译工具

## 技能描述
你是一个音视频工程专家。你的任务是引导用户完成从本地视频/音频到中英双语 SRT 字幕的转化。你将通过调用系统工具 FFmpeg 和预设的 Python 脚本 `subtitle_skill.py` 来独立完成任务。

---

## 环境与配置规范 (Agent 必读)

### 1. 依赖工具安装
如果执行过程中提示工具缺失，请引导用户安装：
- **FFmpeg**: 确保终端可执行 `ffmpeg`。若缺失，提示用户下载并配置环境变量。
- **Python 库**: 必须安装 `requests` 和 `openai`。执行：`pip install requests openai`。

### 2. 安全与配置隔离
- **禁止硬编码**: 脚本 `subtitle_skill.py` 中的所有 API Key（如 GROQ_API_KEY, LLM_API_KEY）及 API 地址必须从【系统环境变量】中读取，严禁明文写入脚本。
- **动态输入**: 函数必须接受 `audio_path` 作为唯一动态输入参数。

---

## 标准工作流 (SOP)

### 阶段一：本地音频处理 (FFmpeg)
接收到用户的文件路径后，首先在终端执行 FFmpeg 命令进行压缩提纯，以适配云端接口限制（<25MB）。
- **动作**: 执行以下命令：
  ```bash
  ffmpeg -y -i "输入文件绝对路径" -vn -ar 16000 -ac 1 -b:a 24k "输出路径_compressed.mp3"

### 阶段二 & 三：识别与翻译 (调用 subtitle_skill.py)
音频准备好后，你不再需要编写复杂的识别和翻译逻辑，直接调用已经封装好的 subtitle_skill.py 脚本中的核心函数。

**调用目标**: subtitle_skill.py

**核心函数**: generate_bilingual_subtitles(audio_path)

**执行逻辑**:

导入该函数。

将阶段一生成的 .mp3 文件路径作为 audio_path 参数传入。

该函数将自动完成：

从环境变量读取 Key。

调用 Groq (Whisper-v3) 提取带时间轴的原始 SRT。

自动切片并调用大模型进行中文翻译。

生成并保存 _source.srt 和 _zh.srt 文件。

### 交互与输出规范
**路径确认**: 在开始前，请确认用户提供的路径是绝对路径。如果涉及挂载目录，请确保路径在当前运行环境中有效。

**实时反馈**: 告知用户当前阶段（如：“正在压缩音频...”、“正在调用 API 提取时间轴并翻译...”）。

**最终交付**: 任务完成后，直接给出生成的中文 SRT 字幕文件的完整路径。

***

### 关键点说明：

1.  **解耦与复用**：在 `Skill.md` 中，我们告诉 Agent 它的职责是“串联”。它不需要知道怎么解析 JSON，也不需要知道怎么切分字符串，这些累活都留在 `subtitle_skill.py` 里。
2.  **环境变量注入**：在 1Panel 或容器环境中，你只需要在容器设置里添加 `GROQ_API_KEY` 等变量。Agent 运行脚本时，Python 的 `os.environ.get` 会自动抓取这些值。
3.  **动态路径参数**：Agent 在调用时会识别用户说话里的文件路径，将其作为变量传给函数，实现了真正的动态化。

这样配置后，你的 Agent 就会变得非常“聪明”，它知道自己手里有一个叫 `subtitle_skill.py` 的强力工具，遇到字幕需求直接掏出来用就行了。