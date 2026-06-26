---
name: auto-subtitle
description: 视频自动字幕生成器，批量为视频生成字幕文件（SRT/VTT），结合视频帧提取和语音转文字，预览模式和撤销功能！
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "python": "3.7+", "env": ["OPENAI_API_KEY"] },
      },
  }
---

# auto-subtitle - 视频自动字幕生成器

视频自动字幕生成器，批量为视频生成字幕文件（SRT/VTT），结合视频帧提取和语音转文字，预览模式和撤销功能！

## 功能特性

- ✅ **批量提取视频音频**：从视频文件中提取音频轨道
- ✅ **语音转文字**：使用 OpenAI Whisper API 将音频转为文字
- ✅ **生成字幕文件**：支持 SRT 和 VTT 格式
- ✅ **预览模式**：不实际生成文件，只显示预览
- ✅ **撤销功能**：自动备份，支持一键撤销
- ✅ **语言支持**：支持多种语言和翻译功能
- ✅ **时间戳**：自动生成带时间戳的字幕

## 安装

```bash
# 安装依赖
pip install openai pydub
```

需要设置环境变量：
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 使用方法

### 基本用法

```bash
# 为当前目录下所有视频生成字幕
python source/auto_subtitle.py

# 指定语言（中文）
python source/auto_subtitle.py --language zh

# 翻译为英文
python source/auto_subtitle.py --task translate --language en

# 生成 VTT 格式
python source/auto_subtitle.py --format vtt

# 预览模式
python source/auto_subtitle.py --preview

# 撤销上次操作
python source/auto_subtitle.py --undo
```

### 详细参数

```
--directory DIRECTORY, -d DIRECTORY
                        要处理的目录（默认：当前目录）
--language LANGUAGE, -l LANGUAGE
                        音频语言（ISO 639-1 格式，如 zh, en, ja）
--task {transcribe,translate}, -t {transcribe,translate}
                        任务类型：transcribe（转录）或 translate（翻译）
--format {srt,vtt}, -f {srt,vtt}
                        字幕格式（默认：srt）
--prompt PROMPT, -p PROMPT
                        提示词，帮助提高识别准确率
--recursive, -r         递归处理子文件夹
--preview, -P           预览模式，不实际生成文件
--undo, -u              撤销上次操作
--output-dir OUTPUT_DIR
                        输出目录（不与视频同目录）
--extensions EXTENSIONS
                        要处理的文件扩展名，逗号分隔（默认：mp4,avi,mov,mkv,webm）
```

### 示例

```bash
# 处理单个视频文件夹，语言为中文
python source/auto_subtitle.py -d ./videos -l zh

# 翻译为英文并生成 VTT 格式
python source/auto_subtitle.py -t translate -l en -f vtt

# 递归处理所有子文件夹
python source/auto_subtitle.py -r

# 提示词提高准确率（人名、专业术语等）
python source/auto_subtitle.py -p "本视频包含以下术语：OpenAI, Codex, AgentSkills"
```

## 支持的格式

- **输入视频**：MP4, AVI, MOV, MKV, WebM
- **输出字幕**：SRT, VTT

## 注意事项

- 需要有效的 OpenAI API Key
- 大视频文件处理可能需要较长时间
- 音频提取需要 ffmpeg（如未安装会提示）
- 原始字幕文件会自动备份到 `./.video_transcriber_backup/`
- 撤销功能只能撤销最近一次操作
