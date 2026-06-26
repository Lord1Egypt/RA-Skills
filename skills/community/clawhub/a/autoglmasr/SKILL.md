---
name: autoglm-asr-mcp
description: "AutoGLM ASR MCP 服务：长音频并发转录、上下文传递、时间戳分段。基于智谱 GLM-ASR-2512。触发词：语音识别、ASR、转录、转录音频、长音频"
---

# AutoGLM ASR MCP Server

GitHub: https://github.com/Starrylyn/autoglm-asr-mcp

一个面向 Agent 的语音转文字 MCP 服务，核心特性：
- 长音频自动分块
- 并发调用（可配置并发数）
- 上下文传递模式
- 时间戳分段输出

## 安装

```bash
# 前置依赖：ffmpeg
brew install ffmpeg  # macOS

# 运行 MCP 服务
npx autoglm-asr-mcp
```

## MCP 配置

```json
{
  "mcpServers": {
    "autoglm-asr": {
      "command": "npx",
      "args": ["-y", "autoglm-asr-mcp"],
      "env": {
        "AUTOGLM_ASR_API_KEY": "your-api-key"
      }
    }
  }
}
```

## 核心工具

### transcribe_audio

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `audio_path` | string | ✅ | - | 音频文件绝对路径 |
| `context_mode` | string | ❌ | `sliding` | 上下文模式 |
| `max_concurrency` | int | ❌ | 5 | 并发数 (1-20) |

返回：
- 完整转录文本
- 时间戳分段列表
- 运行统计（分块数、耗时、模式）

### get_audio_info

获取音频文件信息（时长、格式、预估分块数）。

---

## 核心实现解析

### 1. 并发调用机制

```python
# 使用 Semaphore 控制并发数
semaphore = asyncio.Semaphore(concurrency)

async def transcribe_with_semaphore(chunk: AudioChunk) -> None:
    async with semaphore:
        result = await self._transcribe_chunk(chunk, audio_format=audio_format)
        text_results[chunk.index] = result["text"]
        # ...

# 所有分块并行执行
tasks = [transcribe_with_semaphore(chunk) for chunk in non_silent_chunks]
await asyncio.gather(*tasks)
```

**关键点：**
- 用 `Semaphore` 限制最大并发数
- 用 `asyncio.gather()` 并行执行所有任务
- 结果存入字典 `text_results: dict[int, str]`，按分块索引排序

### 2. 上下文模式

| 模式 | 速度 | 质量 | 说明 |
|------|------|------|------|
| `sliding` | 快 | 高 | 第一个分块初始化上下文，后续并行 |
| `none` | 最快 | 中 | 各分块独立并行，无上下文传递 |
| `full_serial` | 慢 | 最佳 | 顺序执行，完整上下文链 |

**注意：** 新版 `/audio/transcriptions` API 不需要上下文传递，所有分块默认并行。

### 3. 自动分块

```python
chunks = split_audio_on_silence(
    audio,
    max_chunk_duration_ms=self.config.max_chunk_duration * 1000,  # 默认 25s
)
```

- 按静音点分割音频
- 每块最大 25 秒（可配置）
- 静音块自动跳过

### 4. 静音检测 (VAD)

```python
non_silent_chunks = [c for c in chunks if not c.is_silent]
skipped_silent = len(chunks) - len(non_silent_chunks)
```

- 使用 VAD 检测静音片段
- 静音块不调用 API，节省费用

### 5. 结果合并

```python
# 按分块顺序合并文本
full_text = "".join(text_results.get(chunk.index, "") for chunk in chunks)

# 合并时间戳分段（偏移调整）
for seg in result["segments"]:
    offset_segments.append(TranscriptionSegment(
        start=seg.start + chunk.start_ms / 1000.0,  # 加上分块起始偏移
        end=seg.end + chunk.start_ms / 1000.0,
        text=seg.text,
    ))
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AUTOGLM_ASR_API_KEY` | 必填 | 智谱 API Key |
| `AUTOGLM_ASR_API_BASE` | `https://open.bigmodel.cn/api/paas/v4/audio/transcriptions` | API 端点 |
| `AUTOGLM_ASR_MODEL` | `glm-asr-2512` | ASR 模型 |
| `AUTOGLM_ASR_MAX_CHUNK_DURATION` | 25 | 每块最大时长（秒） |
| `AUTOGLM_ASR_MAX_CONCURRENCY` | 5 | 默认并发数 |
| `AUTOGLM_ASR_CONTEXT_MAX_CHARS` | 2000 | 最大上下文字数 |
| `AUTOGLM_ASR_REQUEST_TIMEOUT` | 60 | 请求超时（秒） |
| `AUTOGLM_ASR_MAX_RETRIES` | 2 | 重试次数 |

---

## 支持的音频格式

`mp3`, `wav`, `m4a`, `flac`, `ogg`, `webm`

---

## 直接调用 API（不通过 MCP）

```bash
# 短音频
curl --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/audio/transcriptions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --form model=glm-asr-2512 \
  --form stream=false \
  --form file=@audio.wav

# 长音频：需要自己实现分块、并发、结果合并
```

---

## 最佳实践

1. **短音频（<30s）**：直接调用 API
2. **长音频**：使用 MCP 服务，自动分块 + 并发
3. **高质量需求**：用 `full_serial` 模式
4. **快速处理**：用 `none` 模式 + 高并发（10-20）
5. **平衡选择**：`sliding` 模式 + 并发 5（默认）

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `ffmpeg not found` | 未安装 ffmpeg | `brew install ffmpeg` |
| `File not found` | 路径错误 | 使用绝对路径 |
| `AUTOGLM_ASR_API_KEY environment variable is required` | 未设置 API Key | 在 MCP 配置中设置 |
| `transcriptions文件只支持单声道` | 音频是立体声 | 自动转换为单声道 |

---

## 关键代码片段（参考实现）

### Python 异步并发调用示例

```python
import asyncio
import httpx

async def transcribe_chunk(client, chunk_data, api_key):
    """转录单个音频块"""
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": ("audio.wav", chunk_data, "audio/wav")}
    data = {"model": "glm-asr-2512"}
    
    response = await client.post(
        "https://open.bigmodel.cn/api/paas/v4/audio/transcriptions",
        headers=headers,
        files=files,
        data=data,
    )
    result = response.json()
    return result.get("text", "")

async def transcribe_parallel(chunks, api_key, max_concurrency=5):
    """并发转录多个音频块"""
    semaphore = asyncio.Semaphore(max_concurrency)
    client = httpx.AsyncClient(timeout=60)
    results = {}
    
    async def limited_transcribe(chunk, index):
        async with semaphore:
            text = await transcribe_chunk(client, chunk, api_key)
            results[index] = text
    
    tasks = [limited_transcribe(chunk, i) for i, chunk in enumerate(chunks)]
    await asyncio.gather(*tasks)
    await client.aclose()
    
    # 按顺序合并
    return "".join(results.get(i, "") for i in range(len(chunks)))
```

---

## 扩展阅读

- [智谱 ASR API 文档](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-asr-2512)
- [MCP 协议规范](https://modelcontextprotocol.io)
