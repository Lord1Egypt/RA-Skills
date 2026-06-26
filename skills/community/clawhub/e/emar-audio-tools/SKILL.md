---
name: audio-tools
version: 1.0.0
description: >
  音视频处理工具集。支持以下操作：
  - 从视频文件中提取音频并保存为 WAV 格式
  - 对音频文件按指定开始时间和持续时长进行截取
  - 播放指定的视频或音频文件（调用系统默认播放器）
  - 语音识别转文字（Whisper），输出 JSON 格式（含时间戳、置信度）
  - 提取音频/视频元数据（码率、采样率、时长、编码等）
  触发词：提取音频、截取音频、音频截取、剪切音频、播放视频、播放音频、
  视频转音频、wav提取、音频剪辑、从视频提取、audio extract、clip audio、play video、play audio、
  语音转文字、音频转录、语音识别、提取文字、transcribe、STT、
  查看音频信息、提取元数据、文件信息、码率、采样率、metadata
work_dir: D:\workbuddy
runtime: python
script: scripts/audio_tools.py
---

# Audio Tools Skill

音视频处理工具集，支持三项核心功能：提取音频、截取音频片段、播放媒体文件。

## 工作目录

所有输入文件默认从 `D:\workbuddy` 读取，输出文件也保存到 `D:\workbuddy`（除非用户指定其他路径）。

## 环境要求

### Python 版本
- **要求**: Python 3.8 或更高版本
- **检查**: 运行 `python --version` 确认

### 依赖检查
执行前会自动检查以下环境，缺失时给出安装指引：
```bash
# 检查环境状态
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py --check
```

检查内容包括：
- Python 版本
- ffmpeg / ffprobe / ffplay 可用性
- moviepy 安装状态
- openai-whisper 安装状态

## 依赖说明

本 Skill 优先使用 **ffmpeg**，查找优先级如下：
1. **Skill 本地 bin 目录**（`D:\workbuddy\skills\audio-tools\bin\ffmpeg.exe`）
2. **系统 PATH** 中的 ffmpeg
3. 如均未找到，自动降级使用 **moviepy**（Python 库，首次使用时自动安装）

### 缺失依赖时的提示
如果 ffmpeg 和 moviepy 都未找到，脚本会输出：
```
[WARN] No media processing tool found!

[SOLUTION] Choose one of the following:

  Option 1 - Bundled ffmpeg (Recommended):
           Place ffmpeg.exe in: D:\workbuddy\skills\audio-tools\bin\

  Option 2 - System ffmpeg:
           Windows: winget install ffmpeg

  Option 3 - MoviePy (Python fallback):
           pip install moviepy
```

### 方式一：Bundled ffmpeg（推荐）
将 ffmpeg 放入 Skill 本地目录，实现零依赖部署：
```
D:\workbuddy\skills\audio-tools\
├── bin\
│   ├── ffmpeg.exe      ← 放入这里
│   └── ffprobe.exe     ← 可选，查时长用
├── scripts\
│   └── audio_tools.py
└── SKILL.md
```

### 方式二：系统 ffmpeg
```
# Windows - 使用 winget
winget install ffmpeg

# 或从 https://ffmpeg.org/download.html 下载，解压后将 bin 目录加入系统 PATH
```

### 方式三：moviepy（备选）
```bash
pip install moviepy
```

---

## 功能说明 & SOP

### 功能 1：提取视频音频

**用户意图识别关键词**：提取音频、视频转音频、从视频提取、wav 提取

**执行流程**：
1. 确认输入视频文件路径（相对路径自动拼接工作目录 `D:\workbuddy`）
2. 确认输出 WAV 文件路径（默认与输入同名，后缀改为 `.wav`，保存到 `D:\workbuddy`）
3. 调用脚本执行提取
4. 输出结果文件路径

**调用脚本**：
```bash
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py extract \
  --input "D:\workbuddy\video.mp4" \
  --output "D:\workbuddy\video.wav"
```

**参数说明**：
| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | ✅ | 输入视频文件路径（支持 mp4/mkv/avi/mov/flv 等） |
| `--output` | ❌ | 输出 WAV 文件路径（默认：同目录同名 .wav） |

---

### 功能 2：截取音频片段

**用户意图识别关键词**：截取音频、剪切音频、音频截取、音频剪辑、clip audio

**执行流程**：
1. 确认输入音频文件路径
2. 确认开始时间（`--start`，格式：秒数 或 `HH:MM:SS`）
3. 确认截取时长（`--duration`，单位：秒）
4. 确认输出路径（默认：原文件名加 `_clip` 后缀）
5. 调用脚本执行截取
6. 输出结果文件路径

**调用脚本**：
```bash
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py clip \
  --input "D:\workbuddy\audio.wav" \
  --start 30 \
  --duration 60 \
  --output "D:\workbuddy\audio_clip.wav"
```

**参数说明**：
| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | ✅ | 输入音频文件路径（支持 wav/mp3/flac/aac 等） |
| `--start` | ✅ | 开始时间，支持秒数（如 `30`）或时间格式（如 `00:00:30`） |
| `--duration` | ✅ | 截取时长（秒） |
| `--output` | ❌ | 输出文件路径（默认：原文件名加 `_clip` 后缀） |

---

### 功能 3：播放媒体文件

**用户意图识别关键词**：播放视频、播放音频、play video、play audio、打开播放

**执行流程**：
1. 确认媒体文件路径（相对路径自动拼接工作目录）
2. 优先使用 **ffplay**（bundled 模式）播放
3. 如 ffplay 不可用，回退到系统默认播放器
4. 输出播放状态

**播放工具优先级**：
1. **ffplay**（Skill 本地 bin/ffplay.exe）- 格式支持最全，无系统依赖
2. **系统默认播放器** - 用户习惯，界面友好

**调用脚本**：
```bash
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py play \
  --input "D:\workbuddy\video.mp4"
```

**参数说明**：
| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | ✅ | 媒体文件路径（视频或音频均可） |

---

### 功能 4：语音识别转文字（Whisper）

**用户意图识别关键词**：语音转文字、音频转录、语音识别、提取文字内容、transcribe、STT

**执行流程**：
1. 确认输入音频/视频文件路径
2. 确认 Whisper 模型大小（默认 `small`，可选 `tiny/base/small/medium/large`）
3. 确认语言（可选，默认自动检测）
4. 执行转录，生成 JSON 和 TXT 两份输出
5. 输出转录结果摘要

**调用脚本**：
```bash
# 基础用法（自动检测语言，使用 small 模型）
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py transcribe \
  --input "D:\workbuddy\lecture.wav"

# 指定语言和模型
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py transcribe \
  --input "D:\workbuddy\lecture.wav" \
  --model small \
  --language zh
```

**参数说明**：
| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | ✅ | 输入音频/视频文件路径 |
| `--output` | ❌ | 输出 JSON 路径（默认：同名.json） |
| `--model` | ❌ | Whisper 模型：`tiny/base/small/medium/large`（默认：small） |
| `--language` | ❌ | 语言代码，如 `zh`/`en`/`ja`（默认：自动检测） |

**输出文件**：
- `同名.json` - 完整 JSON，包含文字、时间戳、置信度
- `同名.txt` - 纯文本，仅文字内容

**JSON 结构示例**：
```json
{
  "text": "完整转录文字...",
  "language": "zh",
  "duration": 120.5,
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.2,
      "text": "第一段文字",
      "confidence": -0.1234,
      "no_speech_prob": 0.01
    }
  ]
}
```

---

### 功能 5：提取音频/视频元数据

**用户意图识别关键词**：查看音频信息、提取元数据、文件信息、码率、采样率、metadata

**执行流程**：
1. 确认输入文件路径
2. 优先使用 **ffprobe** 获取详细元数据
3. ffprobe 不可用时，使用 moviepy 获取基础信息
4. 输出 JSON 格式元数据（可选保存到文件）

**调用脚本**：
```bash
# 终端输出元数据
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py metadata \
  --input "D:\workbuddy\audio.wav"

# 保存到 JSON 文件
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py metadata \
  --input "D:\workbuddy\video.mp4" \
  --output "D:\workbuddy\meta.json"
```

**参数说明**：
| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | ✅ | 输入音频/视频文件路径 |
| `--output` | ❌ | 输出 JSON 路径（默认：终端输出） |

**输出信息包括**：
- 文件基础信息（大小、时长、格式）
- 音频流信息（编码、采样率、声道数）
- 视频流信息（编码、分辨率、帧率）
- 完整 ffprobe 原始数据（如可用）

---

## AI 使用规范

1. **路径处理**：用户提供相对路径时，自动补全为 `D:\workbuddy\<文件名>`
2. **工具检测**：执行前先检测 ffmpeg 是否可用，不可用则切换 moviepy
3. **错误处理**：脚本执行失败时，读取错误信息并告知用户可能的原因和解决方案
4. **输出确认**：操作完成后，明确告知用户输出文件的完整路径和文件大小

---

## 使用示例

> 用户：帮我把 D:\workbuddy\lecture.mp4 里的音频提取出来

AI 执行：
```bash
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py extract --input "D:\workbuddy\lecture.mp4"
```
输出：`✅ 提取完成：D:\workbuddy\lecture.wav（大小：12.3 MB）`

---

> 用户：把 lecture.wav 从第 30 秒开始截取 2 分钟

AI 执行：
```bash
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py clip --input "D:\workbuddy\lecture.wav" --start 30 --duration 120
```
输出：`✅ 截取完成：D:\workbuddy\lecture_clip.wav（时长：120 秒）`

---

> 用户：播放一下 lecture.mp4

AI 执行：
```bash
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py play --input "D:\workbuddy\lecture.mp4"
```
输出：`✅ 已调用系统默认播放器打开：D:\workbuddy\lecture.mp4`
