
---
name: feishu-whisper-voice
description: "使用 Faster-Whisper 进行高精度的语音识别，配合 TTS 实现完整的双向语音交流！"
---

# 飞书 Whisper + TTS 语音交互技能
## 何时触发此技能


**当以下情况时使用此 Skill**:
1. 用户发送语音/音频消息需要识别和回复/语音聊天
2. 需要高精度的语音转文字（Whisper 准确率 >98%）
3. 需要将 AI 回复转换为自然语音进行交互
4. 用户提到"语音交互"、"说话"、"Faster-Whisper"、"TTS"等关键词

## Faster-Whisper + TTS 架构

```
用户语音 → 下载音频 → Faster-Whisper 识别 → AI 处理 → TTS 转换 → 语音回复
```

### 核心优势

- **Faster-Whisper**:   开源的语音识别模型，支持多语言，准确率极高
- **TTS**: 飞书内置文本转语音工具，自然流畅
- **双向交互**: 既能听懂用户说话，也能用声音回复

## 工具集成

### 1. 下载语音文件

**优先使用机器人身份（无需授权）**:
```python
feishu_im_bot_image(
    message_id="om_xxx",
    file_key="file_xxx",
    type="audio"
)
```

**用户身份（需要 OAuth 授权）**:
```python
feishu_im_user_fetch_resource(
    message_id="om_xxx",
    file_key="file_xxx",
    type="audio"
)
```

### 2. Whisper 语音识别

使用 `faster-whisper` 库进行高精度的语音转文字：

```python
from faster_whisper import WhisperModel

# 初始化模型（自动下载 base 模型）
model = WhisperModel("base", device="cpu")

# 转录音频文件
segments, info = model.transcribe(audio_file)

print(f"识别语言：{info.language}, 置信度：{info.language_probability:.4f}")
for segment in segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

**模型选项**:
- `base`: 142MB，CPU友好，推荐新手使用
- `small`: 466MB，平衡性能和准确率
- `medium`: 769MB，GPU 推荐（有 NVIDIA GPU 时使用）
- `large`: 1.5GB，最高精度

### 3. TTS 文本转语音

**使用飞书内置 tts() 工具**:
```python
await tts(text="你好，我是你的 AI 助手")
```

**返回格式**:
- 成功：音频文件路径（Base64）或 `audio_url`
- 失败：错误信息

### 4. 完整语音交互流程

```python
async def handle_voice_message(message_id: str) -> None:
    # Step 1: 下载音频文件
    audio_path = await feishu_im_bot_image(
        message_id=message_id,
        file_key=audio_file_key,
        type="audio"
    )
    
    # Step 2: Whisper 识别
    model = WhisperModel("base", device="cpu")
    segments, info = model.transcribe(audio_path)
    transcript = " ".join([seg.text for seg in segments])
    
    print(f"用户说：{transcript}")
    
    # Step 3: AI 处理（根据识别结果生成回复）
    reply_text = generate_reply(transcript)
    
    # Step 4: TTS 转换并发送语音消息
    audio_result = await tts(text=reply_text)
    
    print(f"AI 回复：{reply_text}")

```

## 依赖要求

### Python 库

- `faster-whisper` >= 1.0.0 - Whisper 语音识别引擎
- `openai-whisper` (可选) - OpenAI Whisper API

### FFmpeg (推荐安装)

用于音频格式转换和质量优化：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y ffmpeg
```

## 使用示例

### 场景 1: 语音消息识别

用户发送语音消息，AI 识别后回复文字：

```python
message_id = "om_xxx"
file_key = "file_xxx"

# 下载音频
audio_path = await feishu_im_bot_image(
    message_id=message_id,
    file_key=file_key,
    type="audio"
)

# 识别语音
model = WhisperModel("base", device="cpu")
segments, info = model.transcribe(audio_path)
transcript = " ".join([seg.text for seg in segments])

# 生成回复
reply = f"我听到了：{transcript}"

# 发送文字消息
await message.send(
    to=current_channel,
    message=reply
)
```

### 场景 2: 双向语音对话

用户说中文，AI 用语音回复：

```python
async def voice_dialogue(message_id: str):
    # 下载并识别
    audio_path = await download_audio(message_id)
    transcript = transcribe(audio_path)
    
    # AI 处理
    reply_text = generate_response(transcript)
    
    # TTS 转换
    audio_result = await tts(text=reply_text)
    
    # 发送语音消息
    await send_voice_message(
        to=current_channel,
        audio_url=audio_result["audio_url"]
    )
```

## 性能优化

### CPU vs GPU

**CPU 模式（推荐新手）**:
```python
model = WhisperModel("base", device="cpu")
# 预期速度：2-4x faster than real-time (Apple Silicon)
```

**GPU 模式（NVIDIA）**:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

```python
model = WhisperModel("medium", device="cuda")
# 预期速度：5-10x faster than real-time
```

**Apple Silicon (M1/M2/M3)**:
```python
model = WhisperModel("base", device="mps")
# Metal 加速，性能接近 GPU
```

### 模型缓存

Whisper 模型首次使用时自动下载：
- **位置**: `~/.cache/huggingface/hub/`
- **大小**: base 模型约 142MB
- **管理**: 删除后会自动重新下载

## 故障排除

### Whisper 模型下载失败

**症状**: `ConnectError: [Errno 65] No route to host`

**解决**: 设置 HuggingFace 镜像站环境变量：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

或在 Python 代码中设置：

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
```

### GPU 未检测到

**症状**: `RuntimeError: CUDA not available`

**解决**: 
1. 检查 NVIDIA 驱动安装
2. 使用 CPU 模式回退：`device="cpu"`
3. Apple Silicon 使用 MPS：`device="mps"`

## 最佳实践

1. **优先使用 base 模型** - 在 CPU 上性能足够好，启动快
2. **缓存模型文件** - 避免每次启动都下载
3. **批量处理语音消息** - 减少重复加载模型的开销
4. **设置合理的超时** - Whisper 识别可能需要几秒到几十秒

## 扩展阅读

- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [HuggingFace Whisper 模型](https://huggingface.co/systran/faster-whisper-base)
- [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)

---

**创建时间**: 2026-03-16  
**维护者**: zhou (码农zhou)  
**版本**: v1.0
