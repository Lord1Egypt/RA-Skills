---
name: china-tts
description: 国内可用的文本转语音技能，基于硅基流动（SiliconFlow）API。Use when the user wants to convert text to speech in China without VPN. Supports CosyVoice2-0.5B (multilingual, emotion control, dialect support) and MOSS-TTSD-v0.5 (dual-speaker podcast style). 8 built-in voices, custom voice cloning, speed/gain control. No VPN needed — domestic access, pay via Alipay/WeChat. Requires a SiliconFlow API key.
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🔊", "requires": {"bins": ["curl"], "env": ["SILICONFLOW_API_KEY"]}, "primaryEnv": "SILICONFLOW_API_KEY"}}
---

# 国内文本转语音 China TTS

基于硅基流动（SiliconFlow）API，国内直连，无需翻墙。
支持中英日韩及粤语、四川话等方言，支持情感控制和声音克隆。

音色完整列表 → `references/voices.md`
使用场景与示例 → `references/examples.md`

## 触发时机

- "把这段文字转成语音"
- "用温柔女声朗读这段内容"
- "生成一个播客对话音频：[S1]...  [S2]..."
- "用粤语朗读这段话"
- "帮我克隆这个声音来朗读"

---

## 前置配置（首次使用）

```
1. 访问 cloud.siliconflow.cn，手机号注册（国内直连）
2. 进入「API密钥」页面，创建并复制 API Key
3. 在 OpenClaw 中配置：
   export SILICONFLOW_API_KEY="sk-xxxxxxxxxxxxxxxx"
   或写入 ~/.openclaw/.env

注意：使用自定义音色（声音克隆）需要完成实名认证
```

---

## 模型选择

```
日常朗读 / 博客配音 / 多语言    → CosyVoice2-0.5B（推荐首选）
播客对话 / 双人角色扮演          → MOSS-TTSD-v0.5
```

### CosyVoice2-0.5B（推荐）

```
模型名：FunAudioLLM/CosyVoice2-0.5B
特点：
  - 支持中文、英文、日语、韩语
  - 支持中国方言：粤语、四川话、上海话、郑州话、长沙话、天津话
  - 支持情感控制：快乐、兴奋、悲伤、愤怒等
  - 8种内置音色，支持自定义声音克隆
```

### MOSS-TTSD-v0.5（双人对话专用）

```
模型名：fnlp/MOSS-TTSD-v0.5
特点：
  - 专为对话场景设计，支持双人声音
  - 使用 [S1] [S2] 标签区分说话人
  - 支持声音克隆（通过 references 字段传入两个音色）
  - 适合 AI 播客、角色扮演、对话配音
  - 最大 128000 字符输入
```

---

## API 调用

### 基础朗读（CosyVoice2，系统预置音色）

```bash
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "FunAudioLLM/CosyVoice2-0.5B",
    "input": "你好，欢迎使用硅基流动语音合成服务。",
    "voice": "FunAudioLLM/CosyVoice2-0.5B:claire",
    "response_format": "mp3",
    "speed": 1.0,
    "gain": 0
  }' \
  --output output.mp3
```

### 情感控制朗读

```bash
# 在 input 开头加上情感指令，用 <|endofprompt|> 分隔
--data '{
  "model": "FunAudioLLM/CosyVoice2-0.5B",
  "input": "你能用高兴的情感说吗？<|endofprompt|>今天真是太开心了，马上要放假了！",
  "voice": "FunAudioLLM/CosyVoice2-0.5B:diana",
  "response_format": "mp3"
}'
```

情感指令示例：
```
"你能用高兴的情感说吗？<|endofprompt|>内容..."
"请用悲伤的语气朗读：<|endofprompt|>内容..."
"用激动兴奋的语调：<|endofprompt|>内容..."
"请用平静舒缓的方式：<|endofprompt|>内容..."
```

### 方言朗读

```bash
# 在 input 中自然指定方言，CosyVoice2 会识别
--data '{
  "model": "FunAudioLLM/CosyVoice2-0.5B",
  "input": "请用粤语朗读：<|endofprompt|>多保重，早休息。",
  "voice": "FunAudioLLM/CosyVoice2-0.5B:anna",
  "response_format": "mp3"
}'
```

支持方言：粤语、四川话、上海话、郑州话、长沙话、天津话

### 双人对话（MOSS-TTSD，播客场景）

```bash
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "fnlp/MOSS-TTSD-v0.5",
    "input": "[S1]大家好，欢迎收听今天的节目。[S2]今天我们来聊一聊人工智能的发展。[S1]是的，最近 AI 的进步真的很惊人。",
    "voice": "fnlp/MOSS-TTSD-v0.5:alex",
    "response_format": "mp3",
    "speed": 1.0,
    "gain": 0,
    "max_tokens": 2048
  }' \
  --output podcast.mp3
```

⚠️ MOSS-TTSD 对话格式规则：
```
[S1] 标签 = 说话人1
[S2] 标签 = 说话人2
两个标签必须都出现，且交替使用
单人文本请用 CosyVoice2，不要用 MOSS-TTSD
```

### 使用自定义克隆音色（需实名认证）

```bash
# 先上传参考音频（一次性操作，30秒以内的清晰录音）
curl --location 'https://api.siliconflow.cn/v1/uploads/audio/voice' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --form 'model="FunAudioLLM/CosyVoice2-0.5B"' \
  --form 'customName="my-voice"' \
  --form 'text="在一无所知中，梦里的一天结束了，一个新的轮回便会开始"' \
  --form 'file=@/path/to/reference.mp3'

# 返回 uri 字段，格式：speech:my-voice:xxxxx:xxxxx
# 将 uri 作为 voice 参数使用
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "FunAudioLLM/CosyVoice2-0.5B",
    "input": "你好，这是我的克隆声音。",
    "voice": "speech:my-voice:xxxxx:xxxxx",
    "response_format": "mp3"
  }' \
  --output cloned.mp3
```

---

## 参数说明

```
model（必填）：
  FunAudioLLM/CosyVoice2-0.5B   日常首选
  fnlp/MOSS-TTSD-v0.5            双人对话

input（必填）：
  待转换的文字，最长128000字符
  ⚠️ 不要在文字前后加多余空格
  CosyVoice2 情感控制格式：
    "情感指令<|endofprompt|>正文内容"
  MOSS-TTSD 对话格式：
    "[S1]说话人1的内容[S2]说话人2的内容"

voice（必填）：
  系统预置：FunAudioLLM/CosyVoice2-0.5B:alex 等
  自定义克隆：speech:name:xxxxx:xxxxx
  详细音色列表见 references/voices.md

response_format（可选，默认 mp3）：
  mp3    通用，默认推荐
  wav    无损，文件较大
  opus   高压缩，适合流媒体
  pcm    原始数据，需自行处理

sample_rate（可选）：
  mp3：支持 32000、44100（默认44100）
  wav/pcm：支持 8000、16000、24000、32000、44100（默认44100）
  opus：仅支持 48000

speed（可选，默认 1.0）：
  范围：0.25 ~ 4.0
  0.75 = 慢速，1.0 = 正常，1.5 = 快速

gain（可选，默认 0）：
  范围：-10 ~ 10（单位 dB）
  正值增大音量，负值减小音量

max_tokens（可选，仅 MOSS-TTSD）：
  默认 2048，最大 4096
  input + output 总计不超过 32k tokens

stream（可选，默认 true）：
  true = 流式输出（边生成边返回）
  false = 等待完整生成后返回
```

---

## 计费说明

```
计费方式：按输入文本的 UTF-8 字节数计费
  英文字母 = 1字节/字符
  中文汉字 = 3字节/字符
  
实际费用极低，新用户免费额度通常可生成数小时音频
充值方式：支付宝 / 微信，最低充值10元
```

---

## 文件保存路径

生成的音频文件保存到当前 OpenClaw 工作区（或当前子 Agent 工作区），
使用时间戳命名，保留所有历史音频。

### 路径约定

```bash
# 优先使用：当前工作区目录（$OPENCLAW_WORKSPACE 或 $PWD）
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/tts"
mkdir -p "$OUTPUT_DIR"
FILENAME="tts_$(date +%Y%m%d_%H%M%S).mp3"
OUTPUT_PATH="$OUTPUT_DIR/$FILENAME"

# 完整 curl 命令示例
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{...}' \
  --output "$OUTPUT_PATH"
```

文件命名规则：`tts_YYYYMMDD_HHMMSS.mp3`
示例：`tts_20260321_143052.mp3`

子 Agent 场景：
- 每个子 Agent 有独立工作区时，文件保存在该子 Agent 的工作区 `tts/` 子目录
- 主 Agent 调度多个子 Agent 时，各自保存各自的音频，互不干扰

---

## 输出格式

```
🔊 语音生成完成
━━━━━━━━━━━━━━━━━━━━
模型：FunAudioLLM/CosyVoice2-0.5B
音色：claire（温柔女声）
格式：MP3 / 44100Hz
文本长度：约 X 字

已保存至：{工作区}/tts/tts_20260321_143052.mp3

播放命令：
  macOS:   afplay {上方路径}
  Linux:   mpv {上方路径} / ffplay {上方路径}
  通用:    vlc {上方路径}
```

---

## 常见错误处理

```
401  → API Key 未配置或失效，重新获取
400  → 参数错误：
       - input 含前后多余空格 → 去掉空格
       - MOSS-TTSD 缺少 [S1][S2] 标签 → 检查格式
       - voice 格式错误 → 检查音色名称
429  → 请求频率超限，稍等几秒重试
403  → 使用自定义音色但未完成实名认证
```
