# 使用场景与示例

## 场景1：文章/博客朗读

```bash
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/tts" && mkdir -p "$OUTPUT_DIR"
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "FunAudioLLM/CosyVoice2-0.5B",
    "input": "这里填入文章正文内容，支持长篇文字...",
    "voice": "FunAudioLLM/CosyVoice2-0.5B:alex",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output "$OUTPUT_DIR/tts_$(date +%Y%m%d_%H%M%S).mp3"
```

---

## 场景2：情感化朗读

情感指令 + `<|endofprompt|>` + 正文，CosyVoice2 会以对应情感朗读：

```bash
# 高兴
"input": "你能用高兴的情感说吗？<|endofprompt|>今天真是太开心了！"

# 悲伤
"input": "请用悲伤的语气朗读：<|endofprompt|>他走了，再也不会回来了。"

# 激动
"input": "用激动兴奋的语调：<|endofprompt|>我们赢了！冠军是我们的！"

# 平静舒缓（适合冥想/睡前）
"input": "请用平静舒缓的方式：<|endofprompt|>闭上眼睛，慢慢放松..."
```

---

## 场景3：方言朗读

```bash
# 粤语
"input": "请用粤语朗读：<|endofprompt|>多保重，早休息。"

# 四川话
"input": "请用四川话说：<|endofprompt|>你好安逸哦，来耍嘛。"

# 上海话
"input": "请用上海话朗读：<|endofprompt|>侬好，欢迎来上海。"
```

---

## 场景4：双人播客对话（MOSS-TTSD）

```bash
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/tts" && mkdir -p "$OUTPUT_DIR"
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "fnlp/MOSS-TTSD-v0.5",
    "input": "[S1]大家好，欢迎收听今天的节目，我是主持人小明。[S2]我是嘉宾小红，今天我们来聊聊人工智能。[S1]是的，最近AI发展太快了，你觉得未来会怎样？[S2]我认为AI会成为每个人的助手，而不是威胁。",
    "voice": "fnlp/MOSS-TTSD-v0.5:alex",
    "response_format": "mp3",
    "speed": 1.0,
    "max_tokens": 2048
  }' \
  --output "$OUTPUT_DIR/tts_$(date +%Y%m%d_%H%M%S).mp3"
```

---

## 场景5：中英混合朗读

CosyVoice2 支持中英文自然混读：

```bash
"input": "今天我们要介绍 Machine Learning 的基础概念，也就是机器学习。首先是 Supervised Learning，监督学习..."
```

---

## 场景6：自定义声音克隆（两步操作）

**第一步：上传参考音频（一次性）**

```bash
curl --location 'https://api.siliconflow.cn/v1/uploads/audio/voice' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --form 'model="FunAudioLLM/CosyVoice2-0.5B"' \
  --form 'customName="my-voice"' \
  --form 'text="在一无所知中，梦里的一天结束了，一个新的轮回便会开始"' \
  --form 'file=@/path/to/my-voice.mp3'

# 保存返回的 uri 字段值，格式：
# speech:my-voice:cm04pf7az00061413w7kz5qxs:mjtkgbyuunvtybnsvbxd
```

**第二步：使用克隆音色朗读**

```bash
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/tts" && mkdir -p "$OUTPUT_DIR"
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "FunAudioLLM/CosyVoice2-0.5B",
    "input": "用我的声音来朗读这段文字。",
    "voice": "speech:my-voice:cm04pf7az00061413w7kz5qxs:mjtkgbyuunvtybnsvbxd",
    "response_format": "mp3"
  }' \
  --output "$OUTPUT_DIR/tts_$(date +%Y%m%d_%H%M%S).mp3"
```

---

## 音频文件播放命令

```bash
# macOS
afplay output.mp3

# Linux（需安装 mpv 或 ffmpeg）
mpv output.mp3
ffplay output.mp3

# 转换格式（需 ffmpeg）
ffmpeg -i output.mp3 output.wav

# 查看音频信息
ffprobe output.mp3
```
