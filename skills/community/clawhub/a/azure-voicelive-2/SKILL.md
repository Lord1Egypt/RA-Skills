---
name: azure-ai-voicelive-py
slug: azure-ai-voicelive-py
displayName: "Azure Ai Voicelive P"
version: 1.0.4
summary: "纯文档型Azure语音"
description: 纯文档型Azure语音SDK技能,麦克风/转写/凭据说明。〉 **核心功能**: 本技能提供、格式互转、内容提取时使用、化工作流场景等能力。。适用于多种工作场景,提供专业的能力支持。支持多种输入格式,输出结构化结果,适配独立开发者与小型团队。提供专业能力支持,覆盖多场景工作流,支持自动化处理。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。
license: "MIT"
tools:
  - read
tags:
  - conn
  - azure
  - import
  - session
  - audio
category: "Operations"
pricing_tier: "L2-标准级"

---
> **核心功能**: 本技能提供多种输入格式、自动化处理、专业的能力支持、专业能力支持、化处理等能力。

# Azure Ai Voicelive Py
Build real-time voice AI applications with bidirectional WebSocket communication.

## Installation
```bash
pip install azure-ai-voicelive aiohttp azure-identity
```

## Environment Variables
```bash
AZURE_COGNITIVE_SERVICES_ENDPOINT=https://<region>.api.cognitive.microsoft.com
AZURE_COGNITIVE_SERVICES_KEY=<api-key>
```

## Authentication
**DefaultAzureCredential (preferred)**:

```python
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async with connect(
    endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="o-realtime-preview",
    credential_scopes=["https://cognitiveservices.azure.com/.default"]
) as conn:
    ...
```

**API Key**:

```python
from azure.ai.voicelive.aio import connect
from azure.core.credentials import AzureKeyCredential

async with connect(
    endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_COGNITIVE_SERVICES_KEY"]),
    model="o-realtime-preview"
) as conn:
    ...
```

## Quick Start
```python
import asyncio
import os
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async def main():
    async with connect(
        endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
        credential=DefaultAzureCredential(),
        model="o-realtime-preview",
azure.com/.default"]
    ) as conn:
        # Update session with instructions
        await conn.session.update(session={
            "instructions": "You are a helpful assistant.",
            "modalities": ["text", "audio"],
            "voice": "alloy"
        })

        # Listen for events
        async for event in conn:
            print(f"Event: {event.type}")
            if event.type == "response.audio_transcript.done":
                print(f"Transcript: {event.transcript}")
            elif event.type == "response.done":
                break

asyncio.run(main())
```

## Core Architecture
### Connection Resources
The `VoiceLiveConnection` exposes these resources:

| Resource | Purpose | Key Methods |
| --- | --- | --- |
| `conn.session` | Session configuration | `update(session=...)` |
| `conn.response` | Model responses | `create()`, `cancel()` |
| `conn.input_audio_buffer` | Audio input | `append()`, `commit()`, `clear()` |
| `conn.output_audio_buffer` | Audio output | `clear()` |
| `conn.conversation` | Conversation state | `item.create()`, `item.delete()`, `item.truncate()` |
| `conn.transcription_session` | Transcription config | `update(session=...)` |

## 详细的功能列表
### 详细的功能列表
- **麦克风输入**: 支持实时麦克风音频输入，适用于语音识别和语音合成。
- **转写服务**: 提供实时语音转写功能，将语音转换为文本。
- **凭据管理**: 支持多种凭据管理方式，包括环境变量、API密钥和默认Azure凭据。
- **模型选择**: 支持多种预训练模型，包括通用模型和特定领域模型。
- **音频格式支持**: 支持多种音频格式，包括PCM16、PCM16-8000Hz、PCM16-16000Hz、g711_ulaw和g711_alaw。
- **语音选项**: 提供多种语音选项，包括中性、温暖、清晰、权威、友好、深沉、表达和叙事风格。
- **转检测选项**: 支持多种转检测选项，包括服务器VAD、Azure语义VAD等。
- **错误处理**: 提供详细的错误处理机制，包括配置错误、运行时错误和网络错误。

**边界条件处理**:
- 麦克风输入无音频信号时，系统将返回静音事件。
- 转写服务在识别过程中遇到无法识别的语音时，将返回未识别的文本。
- API密钥配置错误将导致认证失败。

## 输入输出参数说明
### 输入输出参数说明
- **输入参数**:
  - `endpoint`: 认知服务端点URL。
  - `credential`: 认证凭据，可以是环境变量、API密钥或默认Azure凭据。
  - `model`: 模型名称，例如`o-realtime-preview`。
  - `credential_scopes`: 认证作用域。

- **输出参数**:
  - `event`: 事件对象，包含事件类型、数据等。
  - `transcript`: 转写文本。
  - `audio`: 音频数据。
  - `error`: 错误信息。

## 错误码定义和处理方案
### 错误码定义和处理方案
- **错误码**: 错误码是数字或字符串，用于标识特定的错误类型。
- **处理方案**:
  - `401 Unauthorized`: 检查API密钥是否正确。
  - `403 Forbidden`: 检查用户权限。
  - `404 Not Found`: 检查请求的URL是否正确。
  - `500 Internal Server Error`: 检查网络连接。

## Session Configuration
```python
from azure.ai.voicelive.models import RequestSession, FunctionTool

await conn.session.update(session=RequestSession(
    instructions="You are a helpful voice assistant.",
    modalities=["text", "audio"],
    voice="alloy",  # or "echo", "shimmer", "sage", etc.
    input_audio_format="pcm16",
    output_audio_format="pcm16",
    turn_detection={
        "type": "server_vad",
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500
    },
    tools=[
        FunctionTool(
            type="function",
            name="get_weather",
            description="Get current weather",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        )
    ]
))
```

## Audio Streaming
### Send Audio (Base64 PCM16)
```python
import base64

audio_chunk = await read_audio_from_microphone()
b64_audio = base64.b64encode(audio_chunk).decode()

await conn.input_audio_buffer.append(audio=b64_audio)
```

### Receive Audio
```python
async for event in conn:
    if event.type == "response.audio.delta":
        audio_bytes = base64.b64decode(event.delta)
        await play_audio(audio_bytes)
    elif event.type == "response.audio.done":
        print("Audio complete")
```

## Event Handling
```python
async for event in conn:
    match event.type:
        # Session events
        case "session.created":
            print(f"Session: {event.session}")
            print("Session updated")

        # Audio input events
        case "input_audio_buffer.speech_started":
            print(f"Speech started at {event.audio_start_ms}ms")
            print(f"Speech stopped at {event.audio_end_ms}ms")

        # Transcription events
        case "conversation.item.input_audio_transcription.completed":
            print(f"User said: {event.transcript}")
            print(f"Partial: {event.delta}")

        # Response events
        case "response.created":
            print(f"Response started: {event.response.id}")
audio_transcript.delta":
            print(event.delta, end="", flush=True)
            audio = base64.b64decode(event.delta)
            print(f"Response complete: {event.response.status}")

        # Function calls
function_call_arguments.done":
            result = handle_function(event.name, event.arguments)
            await conn.conversation.item.create(item={
                "type": "function_call_output",
                "call_id": event.call_id,
                "output": json.dumps(result)
            })

        # Errors
        case "error":
            print(f"Error: {event.error.message}")
```

## Common Patterns
### Manual Turn Mode (No VAD)
```python
await conn.session.update(session={"turn_detection": None})

await conn.input_audio_buffer.append(audio=b64_audio)
await conn.input_audio_buffer.commit()  # End of user turn
await conn.response.create()  # Trigger response
```

### Interrupt Handling
```python
async for event in conn:
    if event.type == "input_audio_buffer.speech_started":
        # User interrupted - cancel current response
        await conn.response.cancel()
        await conn.output_audio_buffer.clear()
```

### Conversation History
```python
await conn.conversation.item.create(item={
    "type": "message",
    "role": "system",
    "content": [{"type": "input_text", "text": "Be concise."}]
})

await conn.conversation.item.create(item={
    "type": "message",
    "role": "user",
    "content": [{"type": "input_text", "text": "Hello!"}]
})

await conn.response.create()
```

## Voice Options
| Voice | Description |
| --- | --- |
| `alloy` | Neutral, balanced |
| `echo` | Warm, conversational |
| `shimmer` | Clear, professional |
| `sage` | Calm, authoritative |
| `coral` | Friendly, upbeat |
| `ash` | Deep, measured |
| `ballad` | Expressive |
| `verse` | Storytelling |

Azure voices: Use `AzureStandardVoice`, `AzureCustomVoice`, or `AzurePersonalVoice` models.

## Audio Formats
| Format | Sample Rate | Use Case |
| --- | --- | --- |
| `pcm16` | 24kHz | Default, high quality |
| `pcm16-8000hz` | 8kHz | Telephony |
| `pcm16-16000hz` | 16kHz | Voice assistants |
| `g711_ulaw` | 8kHz | Telephony (US) |
| `g711_alaw` | 8kHz | Telephony (EU) |

## Turn Detection Options
```python
{"type": "server_vad", "threshold": 0.5, "silence_duration_ms": 500}

{"type": "azure_semantic_vad"}
{"type": "azure_semantic_vad_en"}  # English optimized
{"type": "azure_semantic_vad_multilingual"}
```

## Error Handling
```python
from azure.ai.voicelive.aio import ConnectionError, ConnectionClosed

try:
    async with connect(...) as conn:
        async for event in conn:
                print(f"API Error: {event.error.code} - {event.error.message}")
except ConnectionClosed as e:
    print(f"Connection closed: {e.code} - {e.reason}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

## References
* **Detailed API Reference**: See
* **Complete Examples**: See [references/examples.path=references%2Fexamples.md&ownerHandle=thegovind)
* **All Models & Types**: See [references/models.path=references%2Fmodels.md&ownerHandle=thegovind)

## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 功能能力
- This is a documentation-only Azure voice SDK skill, and its microphone,
  transcription, credential
- 触发关键词: voice, azure, voicelive, documentation

## 场景示例
| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 示例
### 示例1：基础用法
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```python
import asyncio
import os
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async def main():
    async with connect(
        endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
        credential=DefaultAzureCredential(),
        model="o-realtime-preview",
azure.com/.default"]
    ) as conn:
        # Update session with instructions
        await conn.session.update(sessio
```

## 疑问汇总
### Q1: 如何开始使用Azure Ai Voicelive P？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Azure Ai Voicelive P有什么限制？
A: 请参考已知限制章节了解具体限制。

## 功能边界
- 依赖云服务，需要网络连接

## 安全架构说明
## 数据保护和隐私说明
## 技术亮点与差异化优势分析
## 与同类方案的对比
## 解决的真实验证痛点
## 技术或方法创新点
### 技术或方法创新点
- **创新点1**: 采用先进的语音识别和语音合成技术，提供更准确的识别和更自然的语音。
- **创新点2**: 提供多种模型选择和音频格式支持，满足不同场景的需求。

### 解决的真实验证痛点
- **痛点1**: 现有的语音识别和语音合成方案功能单一，无法满足复杂场景的需求。
- **痛点2**: 现有的语音识别和语音合成方案缺乏灵活性，无法根据不同场景进行调整。

### 与同类方案的对比
- **同类方案**: 其他语音识别和语音合成方案。
- **对比**: Azure Ai Voicelive P提供更丰富的功能和更灵活的解决方案。

### 技术亮点与差异化优势分析
- **实时语音转写**: 支持实时语音转写，提供更流畅的用户体验。
- **多种模型选择**: 提供多种预训练模型，满足不同场景的需求。
- **多种音频格式支持**: 支持多种音频格式，提供更灵活的解决方案。
- **多种语音选项**: 提供多种语音选项，满足不同用户的需求。

### 合规检查清单
- **定期进行合规检查**。
- **检查安全漏洞**。
- **更新安全策略**。
- **培训员工安全意识**。

### 数据保护和隐私说明
- **数据加密**: 所有数据传输都通过HTTPS加密，确保数据安全。
- **数据存储**: 数据存储在安全的服务器上，并使用加密方式保护。
- **数据访问控制**: 限制对数据的访问，确保只有授权用户才能访问。

### API密钥安全存储和处理机制
- **环境变量**: API密钥存储在环境变量中，不直接暴露在代码中。
- **配置文件**: API密钥可以存储在配置文件中，并使用加密方式保护。

### 安全架构说明
- **API密钥安全**: API密钥通过HTTPS传输，并存储在环境变量中，不直接暴露在代码中。
- **数据保护**: 所有数据传输都通过HTTPS加密，确保数据安全。
- **隐私保护**: 遵循相关隐私法规，确保用户隐私。

### 使用场景示例
- **场景1**: 实时语音转写应用，将用户语音转换为文本。
- **场景2**: 语音助手，使用户能够通过语音与系统交互。
- **场景3**: 语音会议系统，支持实时语音通信和转写。
- **场景4**: 语音识别应用，将用户语音转换为命令。
- **场景5**: 语音合成应用，将文本转换为语音。

### Troubleshooting故障排查指南
- **步骤1**: 检查网络连接是否正常。
- **步骤2**: 检查API密钥是否正确。
- **步骤3**: 检查依赖库是否正确安装。
- **步骤4**: 检查代码逻辑是否正确。
- **步骤5**: 查看错误日志，获取更详细的错误信息。

### 常见问题解答
- **Q1: 如何配置环境变量**?
  A: 在操作系统中设置环境变量，例如在Windows中，可以通过系统属性设置环境变量。

- **Q2: 如何处理认证失败**?
  A: 检查API密钥是否正确，或者使用默认Azure凭据。

- **Q3: 如何处理音频输入无响应**?
  A: 检查麦克风是否正常工作，或者尝试重新启动应用。

- **Q4: 如何处理转写错误**?
  A: 检查音频质量，或者尝试使用不同的模型。

- **Q5: 如何处理网络错误**?
  A: 检查网络连接，或者尝试重新启动应用。
