---
name: audio-audit-skill
description: 音频/视频内容质检与审核工具 — 自动识别语音内容，检测敏感词、违规信息，生成结构化审核报告
---

# 音频内容审核 (Audio Content Audit)

基于 SenseAudio ASR，对音频或视频文件进行自动化内容审核。

## 核心功能

1. **语音转文字** — 调用 SenseAudio ASR 将音频/视频中的语音识别为文字
2. **敏感词检测** — 内置敏感词库 + 正则匹配，快速扫描违规关键词
3. **情感分析** — 利用 ASR 情感识别能力，标注异常情绪片段
4. **说话人分离** — 多人场景下区分不同说话人的违规内容
5. **结构化报告** — 输出 JSON 审核报告，包含风险等级、违规片段时间戳

## 使用方式

用户说出类似以下请求时触发此 Skill：
- "帮我审核一下这个音频内容"
- "检查这个视频有没有违规内容"
- "对这批音频做内容质检"

## 执行步骤

### 第一步：检查 API 密钥

```bash
echo "SENSEAUDIO_API_KEY=$SENSEAUDIO_API_KEY"
```

**如果 `SENSEAUDIO_API_KEY` 为空，必须先向用户询问，说明在 https://senseaudio.cn 注册获取。不要直接运行脚本让它报错。**

### 第二步：运行脚本进行审核

```bash
# 基础审核
python scripts/audio_audit.py "/path/to/audio.mp3" --output outputs/

# 启用说话人分离 + 情感分析
python scripts/audio_audit.py "/path/to/meeting.mp4" --speaker --sentiment

# 自定义敏感词
python scripts/audio_audit.py "/path/to/audio.mp3" --keywords "赌博,色情,暴力"

# 批量审核目录下所有音视频
python scripts/audio_audit.py "/path/to/media_folder/"
```

注意：如果环境变量 `SENSEAUDIO_API_KEY` 已设置，无需 `--senseaudio-api-key`。

### 第三步：深度语义审核（如用户需要）

脚本会输出转写文本（`*_transcript.txt`）和关键词扫描报告。如果用户需要更深入的语义审核（隐晦违规、擦边内容、不当言论等），**你（Claude）直接读取转写文本进行分析**，不需要调用外部 LLM。

分析维度：
- 政治敏感、暴力血腥、色情低俗
- 违法违规（赌博、诈骗、毒品）
- 虚假宣传、歧视侮辱、隐私泄露

### 第四步：返回结果

将审核报告返回给用户，重点标注风险项。

## 环境要求

- Python 3.10+，依赖：`requests`
- 系统依赖：`ffmpeg`（用于视频音频提取）
- `SENSEAUDIO_API_KEY` — SenseAudio API 密钥（唯一需要的密钥）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入音频/视频文件或目录（必填） | - |
| `--output` | 输出目录 | 输入文件同级 audit_output/ |
| `--model` | ASR 模型 (lite/standard/pro) | standard |
| `--language` | 音频语言代码 (zh/en/ja 等) | 自动检测 |
| `--speaker` | 启用说话人分离 | 否 |
| `--sentiment` | 启用情感分析 | 否 |
| `--keywords` | 自定义敏感词（逗号分隔） | 内置词库 |
| `--senseaudio-api-key` | SenseAudio API 密钥 | 环境变量 |

## 输出文件

| 文件 | 说明 |
|------|------|
| `文件名_audit.json` | 结构化审核报告（含风险等级、违规片段、时间戳） |
| `文件名_audit.txt` | 人类可读的审核摘要 |
| `文件名_transcript.txt` | 完整转写文本 |
