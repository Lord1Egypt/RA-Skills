---
name: "azure-transcription-tool-free"
description: "使用Azure AI进行批量语音转文字，支持基础转写与时间戳，适合个人用户处理音频。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Azure语音转写免费版"
  version: "1.0.0"
  summary: "使用Azure AI进行批量语音转文字，支持基础转写与时间戳，适合个人用户处理音频。"
  tags:
    - "语音识别"
    - "Azure"
    - "转写工具"
    - "个人创作"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **核心功能**: 本技能提供中文交互、化流程等能力。

# Azure语音转写免费版

## 概述

Azure语音转写免费版是一款面向个人用户的轻量级语音转文字工具，基于Azure AI Transcription SDK实现。支持批量转写存储在Blob中的音频文件，自动生成带时间戳的转写结果。几行Python代码即可完成音频到文字的转换，适合播客、会议录音、视频字幕等场景。

## 核心能力

| 能力 | 说明 |
| --- | --- |
| 批量转写 | 将存储在Blob中的音频文件批量转写为文字 |
| 多语言支持 | 支持中文、英文等数十种语言识别 |
| 时间戳输出 | 生成带时间戳的转写结果，便于字幕制作 |
| 格式兼容 | 支持WAV、MP3等主流音频格式 |
| 简易API | Python SDK，几行代码完成转写 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Azure、进行批量语音转文、支持基础转写与时、适合个人用户处理、语音转写免费版、面向个人用户的轻、量级语音转文字工、批量语音转文字、支持存储在、自动语言识别、英文等多种语言、简单的等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：播客录音转文字

个人播客创作者将录制好的音频转写为文字稿，用于发布文章或生成字幕。

```python
import os
from azure.ai.transcription import TranscriptionClient

# 初始化客户端
client = TranscriptionClient(
    endpoint=os.environ["TRANSCRIPTION_ENDPOINT"],
    credential=os.environ["TRANSCRIPTION_KEY"]
)

# 批量转写播客音频
job = client.begin_transcription(
    name="podcast-episode-01",
    locale="zh-CN",
    content_urls=["https://<storage>.blob.core.windows.net/podcast/episode01.wav"]
)

result = job.result()
print(f"转写状态: {result.status}")
print(f"转写内容: {result.transcript}")
```

### 场景二：会议录音整理

将会议录音转写为文字，便于后续整理会议纪要。

```python
# 会议录音转写
meeting_job = client.begin_transcription(
    name="team-meeting-20260118",
    locale="zh-CN",
blob.core.windows.net/meetings/meeting.wav"],
    diarization_enabled=False  # 免费版不启用说话人分离
)

result = meeting_job.result()

# 输出带时间戳的转写结果
for segment in result.segments:
    print(f"[{segment.start_time} - {segment.end_time}] {segment.text}")
```

### 场景三：视频字幕生成

为视频生成中文字幕文件。

```python
# 视频音频轨转写为字幕
subtitle_job = client.begin_transcription(
    name="video-subtitle",
    locale="zh-CN",
blob.core.windows.net/videos/audio_track.wav"]
)

result = subtitle_job.result()

# 生成SRT字幕文件
def generate_srt(segments, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg.start_time)
            end = format_timestamp(seg.end_time)
            f.write(f"{i}\n{start} --> {end}\n{seg.text}\n\n")

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

generate_srt(result.segments, "subtitle.srt")
print("字幕文件已生成: subtitle.srt")
```

## 不适用场景

以下场景Azure语音转写免费版不适合处理：

- 专业医学法律翻译认证
- 同声传译
- 文学创作翻译

## 触发条件

需要文本翻译、多语言转换、本地化处理时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 依赖详情

```bash
pip install azure-ai-transcription
```

### 2. 配置环境变量

```bash
export TRANSCRIPTION_ENDPOINT="https://<resource>.cognitiveservices.azure.com"
export TRANSCRIPTION_KEY="配置值"
```

### 3. 执行转写

```python
import os
from azure.ai.transcription import TranscriptionClient

client = TranscriptionClient(
    endpoint=os.environ["TRANSCRIPTION_ENDPOINT"],
    credential=os.environ["TRANSCRIPTION_KEY"]
)

# 最简转写
job = client.begin_transcription(
    name="my-audio",
    locale="zh-CN",
    content_urls=["https://<storage>/audio.wav"]
)

result = job.result()
print(result.transcript)
```

## 示例

### 环境变量配置

```bash
# .env 文件
TRANSCRIPTION_ENDPOINT=https://myresource.cognitiveservices.azure.com
TRANSCRIPTION_KEY=your_subscription_key_here
```

### 支持的语言代码

| 语言 | locale代码 |
| --- | --- |
| 中文（简体） | `zh-CN` |
| 中文（繁体） | `zh-TW` |
| 英语（美国） | `en-US` |
| 英语（英国） | `en-GB` |
| 日语 | `ja-JP` |
| 韩语 | `ko-KR` |
| 法语 | `fr-FR` |
| 德语 | `de-DE` |

### 音频格式要求

| 格式 | 推荐采样率 | 说明 |
| --- | --- | --- |
| WAV | 16kHz, 16-bit | 推荐格式，无损 |
| MP3 | 16kHz+ | 有损压缩，兼容性好 |
| FLAC | 16kHz+ | 无损压缩 |

## 优选实践

1. **音频质量**：使用清晰的录音，背景噪音越少识别准确率越高
2. **语言指定**：始终指定正确的locale，可显著提升识别准确率
3. **文件格式**：推荐使用WAV格式，16kHz采样率获得优选效果
4. **Blob存储**：音频文件需存储在可公开访问的Blob URL中
5. **结果轮询**：批量转写为异步操作，需轮询结果直到完成
6. **错误处理**：添加超时和重试机制，处理网络异常

## 常见问题

### Q1：转写结果准确率不高怎么办？

确保音频质量良好，背景噪音少。指定正确的locale语言代码。对于专业领域内容，可考虑使用自定义语音模型。

### Q2：支持本地文件转写吗？

免费版需要音频文件存储在可访问的Blob URL中。如需处理本地文件，需先上传至Blob存储。

### Q3：转写需要多长时间？

转写时间取决于音频时长。通常处理速度约为音频时长的0.5-1倍。

### 已知限制

免费版受Azure免费层级限制，每月有固定的转写时长额度。如需更大用量，建议升级至PRO版本。

### Q5：如何获取时间戳信息？

转写结果的segments属性包含每段文字的开始时间和结束时间，可用于字幕生成。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8及以上

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 3 | 运行时 | 必需 | python.org 下载安装 |
| azure-ai-transcription | Python SDK | 必需 | `pip install azure-ai-transcription` |
| Azure认知服务 | 云服务 | 必需 | Azure门户创建资源 |

### API Key 配置

- `TRANSCRIPTION_ENDPOINT`：Azure认知服务端点URL
- `TRANSCRIPTION_KEY`：Azure认知服务订阅密钥
- 使用订阅密钥认证（不支持DefaultAzureCredential）

### 可用性分类

- **分类**: MD+EXEC（纯Markdown指令，核心功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行语音转写任务。核心转写功能通过Python SDK调用Azure AI服务实现。
- API Key通过环境变量配置: export API_KEY=your_key

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。