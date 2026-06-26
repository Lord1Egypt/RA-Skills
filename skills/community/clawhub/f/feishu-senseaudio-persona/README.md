# Feishu Persona Voice Reply

一个基于 OpenClaw 的场景化 skill：

- 先为虚拟角色定制人设
- 后续根据用户消息生成符合人设的文本回复
- 使用 **SenseAudio ASR** 转写用户语音
- 使用 **SenseAudio TTS** 合成角色语音
- 自动把音频转成 **OPUS** 并发送为飞书原生语音条

## 目录

```text
feishu_persona_voice_skill/
├── SKILL.md
├── README.md
├── data/
│   └── persona.json
└── scripts/
    ├── main.py
    ├── asr.py
    ├── tts.py
    ├── feishu_api.py
    └── persona_store.py
```

## 环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"           # 可选，也可通过命令传 --chat-id
export SENSEAUDIO_API_KEY="your_key"
export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"
export SENSEAUDIO_ASR_ENDPOINT="https://api.senseaudio.cn/v1/asr"   # 如果你们实际路径不同，请替换
```

## 飞书配置

1. 在飞书开放平台创建企业自建应用
2. 启用机器人能力
3. 配置事件订阅（WebSocket 模式）
4. 至少确保应用具备消息相关权限并已发布版本
5. 在 OpenClaw 中添加 Feishu 渠道：

```bash
openclaw channels add
```

选择 Feishu，然后填写 `App ID` 和 `App Secret`。

## 安装依赖

```bash
python3 -m pip install requests
brew install ffmpeg   # macOS
```

## 快速开始

### 检查环境

```bash
python3 scripts/main.py setup
```

### 初始化角色

```bash
python3 scripts/main.py persona-init \
  --name "阿澈" \
  --relationship "温柔克制的陪伴型学长" \
  --personality "耐心, 细腻, 稍微嘴硬但可靠" \
  --speaking-style "短句, 自然, 温柔, 不油腻" \
  --catchphrase "别硬撑，我在。" \
  --voice-id "male_0018_a" \
  --speed 0.95 \
  --pitch -1 \
  --vol 1.0 \
  --emotion calm
```

### 查看当前角色

```bash
python3 scripts/main.py persona-show
```

### 让 OpenClaw 生成角色 prompt

```bash
python3 scripts/main.py persona-prompt --user-message "今天真的很累"
```

把输出的 prompt 交给 OpenClaw / LLM 生成最终文本回复。

### 发送飞书语音条

```bash
python3 scripts/main.py send-voice \
  --reply-text "那就先别逼自己继续撑着了。把包放下，先坐一会儿，我陪你缓一缓。" \
  --chat-id "oc_xxxxx"
```

### 转写用户语音

```bash
python3 scripts/main.py transcribe --audio /absolute/path/to/input.m4a
```

## 推荐 OpenClaw 工作流

1. 首次对话时，先收集用户希望的角色设定
2. 调用 `persona-init` 保存人设
3. 后续用户发消息：
   - 文字：直接读取 `persona-prompt` 生成回复
   - 语音：先 `transcribe`，再读取 `persona-prompt`
4. 让 OpenClaw 生成最终回复文本
5. 调用 `send-voice` 把文本合成为飞书语音条
6. 同时把文本也发送给用户
