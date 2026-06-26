---
name: senseaudio-clone-wizard
description: Guided voice cloning workflow — from recording tips to first playback. Use when users want to clone their voice, create a custom voice, or ask "怎么克隆声音", "我想用自己的声音合成", "音色克隆怎么做". Walks users through recording requirements, checks audio quality before they upload, guides them to the platform for cloning, then generates a preview with their new voice.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
        - xxd
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Clone Wizard

A guided experience for voice cloning. The API itself is simple — the hard part is getting a clean recording. This skill handles that.

> Note: SenseAudio does not support cloning via API. The actual cloning happens on the platform at https://senseaudio.cn. This skill guides the user through the full process and handles the steps that can be automated.

---

## Phase 1: Before Recording

When a user says they want to clone their voice, show this guide before they record anything:

---
**录音前请注意：**

- **环境**：找一个安静的房间，关掉空调、风扇、电视
- **距离**：嘴巴距离麦克风约 20cm，不要太近（会爆音）也不要太远（声音发虚）
- **时长**：3–30 秒，朗读一段自然的文字效果最好
- **格式**：MP3、WAV 或 AAC，文件不超过 50MB
- **内容**：朗读一段话，语速自然，避免长时间停顿

推荐朗读内容（约 15 秒）：
> "大家好，我是 [你的名字]。今天天气不错，阳光明媚。我喜欢在这样的日子里出去走走，感受大自然的美好。希望每一天都能这样轻松愉快。"

录好后把文件发给我，我来帮你检测质量。

---

## Phase 2: Audio Quality Check

When the user uploads an audio file, run the quality check:

```bash
RESULT=$(curl -s -X POST https://api.senseaudio.cn/v1/audio/analysis \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -F "model=sense-asr-check" \
  -F "file=@<AUDIO_FILE>")
```

Parse the response and translate it into plain language:

**Noise score interpretation:**

| noise_score | What to tell the user |
|-------------|----------------------|
| 0.0 – 0.2 | 录音质量很好，可以直接提交克隆 |
| 0.2 – 0.4 | 录音质量不错，有轻微噪声，克隆效果可能略有影响，建议在条件允许时重录 |
| 0.4 – 0.6 | 录音噪声较明显，建议重录以获得更好的克隆效果 |
| 0.6 – 1.0 | 录音噪声严重，强烈建议重录，否则克隆出的音色可能失真 |

**Noise type translations:**

| noise_types value | 告诉用户 |
|-------------------|---------|
| background_noise | 背景噪声（周围环境声） |
| hum | 嗡嗡声（可能是空调、电器） |
| static | 静电杂音（可能是线材或设备问题） |
| wind | 风噪（话筒离嘴太近或有风） |
| echo / reverb | 回声/混响（房间太空旷，建议换小房间或靠近软装） |

**Example diagnosis output:**
```
你的录音检测结果：
- 时长：14.3 秒 ✓
- 噪声评分：0.52（中等）
- 检测到：嗡嗡声（可能是空调）

建议：关掉空调后重新录一段。如果条件不允许，可以继续提交，
但克隆出的音色可能带有轻微底噪。要继续还是重录？
```

If `has_noise` is false or score < 0.2, skip the warning and proceed directly to Phase 3.

## Phase 3: Platform Cloning

The cloning itself must be done on the SenseAudio platform — the API does not support direct cloning requests.

Guide the user:

---
**录音质量通过！接下来去平台完成克隆：**

1. 打开 https://senseaudio.cn，登录你的账号
2. 进入「音色克隆」页面
3. 点击「上传音频」，选择你刚才的录音文件
4. 系统会自动训练，通常几秒内完成
5. 训练完成后，在「我的音色」中找到新音色，复制它的 **voice_id**
6. 把 voice_id 发给我，我来帮你生成第一段试听

**注意槽位：** 每个账号有有限的克隆槽位。如果槽位已满，需要先删除旧音色才能克隆新的。

---

## Phase 4: First Playback

Once the user provides their voice_id, synthesize a welcome message so they can hear their AI voice for the first time:

Default preview text (warm and personal):
> "你好！这是我的 AI 声音。从今天起，我可以用这个声音说任何我想说的话了。"

```bash
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"SenseAudio-TTS-1.0\",
    \"text\": \"你好！这是我的 AI 声音。从今天起，我可以用这个声音说任何我想说的话了。\",
    \"stream\": false,
    \"voice_setting\": { \"voice_id\": \"<VOICE_ID>\" },
    \"audio_setting\": { \"format\": \"mp3\" }
  }" -o preview.json

jq -r '.data.audio' preview.json | xxd -r -p > my_voice_preview.mp3
```

After generating: tell the user the file is ready, and mention they can now use this voice_id with any SenseAudio TTS feature — including the `senseaudio-tts-quick` skill for quick synthesis or `senseaudio-polyglot-tts` for precise pronunciation control.
