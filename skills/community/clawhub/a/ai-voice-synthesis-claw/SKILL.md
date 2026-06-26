---
name: ai-voice-synthesis-claw
description: |
  AI智能配音合成专家。将文案/脚本转换为高拟真语音音频，支持多种音色、情感控制、SSML标注和后期处理。
  触发场景：用户说"配音"、"语音合成"、"TTS"、"旁白"、"播客音频"、"有声读物"、"AI配音"、"朗读"、"音频生成"，
  或要求"用XX声音读这段文案"、"生成播客音频"、"把文章转成有声版"等。
  支持 ElevenLabs、OpenAI TTS、Azure TTS 等引擎，输出 MP3/WAV 格式音频文件。
---

# 智能配音合成虾 (ai-voice-synthesis-claw)

将文字转化为有温度的声音。

## 工作流程

### 步骤 1：理解需求

收集以下信息（未提供时使用默认值）：
- **文本内容**：待配音的文案/脚本
- **音色风格**：参考 `references/voice-style-guide.md` 选择合适音色
- **语速**：slow / normal（默认）/ fast
- **情感**：calm / warm / professional / energetic
- **输出格式**：mp3（默认）/ wav

### 步骤 2：文本预处理

在调用 TTS 前对文本进行处理：
- 分句断句（按标点符号）
- 数字转中文（100 → 一百）
- 多音字标注（如"重要"的"重"）
- 添加停顿标记

### 步骤 3：选择 TTS 引擎

按优先级选择可用引擎：
1. **ElevenLabs**（推荐）：最自然，支持情感控制，需 `ELEVENLABS_API_KEY`
2. **OpenAI TTS**：质量稳定，需 `OPENAI_API_KEY`
3. **Azure TTS**：多语言支持，需 `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION`
4. **系统 TTS**（兜底）：使用 `tts` 工具直接合成（无需 API key，质量较低）

检查环境变量确认可用引擎：
```bash
echo "ElevenLabs: $ELEVENLABS_API_KEY" && echo "OpenAI: $OPENAI_API_KEY"
```

### 步骤 4：生成 SSML（可选，精细控制时使用）

参考 `references/ssml-guide.md` 为文本添加 SSML 标注。
简单场景可跳过，直接传纯文本。

### 步骤 5：调用合成脚本

```bash
# 单段文本合成
python3 scripts/synthesize-voice.py \
  --text "你好，欢迎收听本期节目" \
  --voice warm-female \
  --speed normal \
  --output ./output.mp3

# 从文件合成
python3 scripts/synthesize-voice.py \
  --script ./script.txt \
  --voice professional-male \
  --speed fast \
  --output ./output.mp3

# 添加背景音乐
python3 scripts/synthesize-voice.py \
  --script ./script.txt \
  --bgm ./bgm/light-jazz.mp3 \
  --bgm-volume 0.1 \
  --output ./output.mp3
```

### 步骤 6：后期处理

参考 `references/audio-processing-guide.md`，脚本自动完成：
- 降噪处理
- 音量标准化（-14 LUFS）
- 背景音乐混音（可选）
- 格式转换

### 步骤 7：交付

将生成的音频文件发送给用户：
```
合成完成！这是你的配音文件。
MEDIA:./output.mp3
```

## 音色快速参考

| 场景 | 推荐音色 |
|------|---------|
| 知识科普 | professional-male / professional-female |
| 情感故事 | warm-female |
| 商业广告 | magnetic-male |
| 轻松娱乐 | young-energetic |

详细音色库见 `references/voice-style-guide.md`。

## 环境依赖

```bash
pip install elevenlabs openai pydub requests
brew install ffmpeg  # macOS
```

## 注意事项

- 单次合成建议不超过 10 分钟音频
- 音色克隆需至少 1 分钟清晰样本音频
- 使用他人声音克隆需获得授权
- 无 API key 时降级使用系统 `tts` 工具
