---
name: feishu-persona-voice-reply
description: 飞书语音陪伴技能。当用户在飞书机器人会话中发送任何文字或语音消息时触发此技能。
  大模型根据用户自定义的虚拟角色人设，生成符合角色性格的文本回复，
  并通过 SenseAudio TTS 合成语音，以飞书原生语音条形式回复，不要生成任何文字消息回复到对话框里，只需要符合该伴侣人设的对话即可。
  首次使用时引导用户完成角色人设设定。
  适用场景：用户和飞书机器人的所有私聊对话、角色扮演、虚拟陪伴、情感陪聊。
metadata:
  {
    "openclaw": {
      "emoji": "🎭",
      "homepage": "https://clawhub.ai/Anightmare2/feishu-voice-skill",
      "requires": {
        "bins": ["python3", "ffmpeg"],
        "env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "SENSEAUDIO_API_KEY"]
      },
      "primaryEnv": "SENSEAUDIO_API_KEY",
      "install": [
        {
          "id": "ffmpeg-brew",
          "kind": "brew",
          "formula": "ffmpeg",
          "bins": ["ffmpeg"],
          "label": "Install ffmpeg (brew)",
          "os": ["darwin"]
        },
        {
          "id": "requests-uv",
          "kind": "uv",
          "packages": ["requests"],
          "label": "Install Python requests"
        }
      ]
    }
  }
---

# Feishu Persona Voice Reply

这个技能用于在**飞书**里打造一个可定制人设的虚拟角色。
1. **先做人设初始化**：由用户决定角色名、关系定位、性格、说话风格、口头禅、音色等；
2. **后续按人设回复**：用户给机器人发送文字或语音时，机器人根据角色设定产出回复；
3. **语音闭环**：ASR 和 TTS 都统一调用 **SenseAudio**；
4. **飞书原生语音条**：最终回复发送为 **OPUS 格式音频消息**，在飞书里显示为可点击即播的语音条，而不是普通文件附件。

OpenClaw 的 Skills 通过 `SKILL.md` frontmatter 声明依赖与环境变量；飞书渠道使用 WebSocket 事件订阅接收消息；飞书发送语音消息前需要先上传 OPUS 文件，再以 `audio` 消息发送 `file_key`。

## 适用场景

- 在飞书中创建一个“虚拟陪伴角色”
- 类似乙女游戏 / 角色扮演聊天，但通过企业 IM 落地
- 用户可先自定义角色，再与其持续对话
- 角色能用自己的声音风格给出语音回复

## 绝对规则

1. **所有 ASR 和 TTS 必须走 SenseAudio。** 禁止改用 OpenAI、Edge TTS、系统 `say`、Whisper、本地 pyttsx3 等其他方案。
2. **飞书语音必须发成 OPUS 语音消息。** 禁止把 mp3/wav 直接当文件附件发出去，除非用户明确要求普通文件。
3. **首次使用前必须完成人设初始化。** 没有人设就不要直接回复“空角色语气”。
4. **回复先由 OpenClaw 生成文本，再调用脚本发语音。** 本技能的脚本负责存人设、调用 SenseAudio、转换 OPUS、发送飞书语音条；角色化文本本身由 OpenClaw 按人设提示词生成。
5. **如果用户发来语音，先转写再理解。** 禁止跳过 ASR 直接臆测用户内容。
6. **默认仅发送语音消息。** 只有当用户明确要求文字版时，才额外发送文本；如果飞书语音发送失败，可降级为文本回复。

## 输出规则（最高优先级）

当本技能已经成功调用飞书语音发送流程后：
- 不要再向用户发送任何文本回复
- 不要复述刚才用于 TTS 的内容
- 不要附加“我刚刚已经回你一条语音了”之类的说明
- 成功情况下，最终对话输出应为空，由飞书中的语音条作为唯一回复
- 只有在发送失败时，才允许返回文本错误信息

## 前置要求

### 1. 飞书应用

需要一个飞书企业自建应用，并启用机器人能力。OpenClaw Feishu 文档建议：创建 app、复制 App ID 和 App Secret、配置权限、启用 bot、配置事件订阅、最后发布应用。Feishu 插件通过 WebSocket 模式接收消息，不需要先暴露公网 webhook。

最少准备：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- 目标会话的 `chat_id`（也可以在脚本参数中传入）

### 2. SenseAudio 凭证

需要：

- `SENSEAUDIO_API_KEY`
- 可选 `SENSEAUDIO_API_BASE`，默认 `https://api.senseaudio.cn`
- 可选 `SENSEAUDIO_ASR_ENDPOINT`

### 3. 本地依赖

- `python3`
- `ffmpeg`（用于把 SenseAudio 结果转成 Feishu 语音条需要的 OPUS）

飞书上传文件接口支持 `opus` 音频；如果原始音频是其他格式，需要先转为 OPUS。

## 推荐目录结构

```text
feishu-persona-voice-reply/
├── SKILL.md
├── data/
│   └── persona.json
└── scripts/
    ├── main.py
    ├── asr.py
    ├── tts.py
    ├── feishu_api.py
    └── persona_store.py
```

## 人设字段建议

初始化人设时，至少收集以下内容：

- `name`：角色名
- `relationship`：与用户的关系定位（学长 / 搭档 / 恋人感 / 治愈系朋友）
- `personality`：性格关键词
- `speaking_style`：说话风格
- `catchphrase`：口头禅或常见尾句
- `voice_id`：SenseAudio 音色 ID
- `speed`：语速
- `pitch`：音调（**整数**）
- `vol`：音量
- `emotion`：默认情感
- `boundaries`：角色边界

## 使用流程

### 步骤 1：初始化角色人设

先和用户确认人设，再保存：

```bash
python3 "$SKILL_DIR/scripts/main.py" persona-init \
  --name "阿澈" \
  --relationship "温柔克制的陪伴型学长" \
  --personality "耐心, 细腻, 稍微嘴硬但可靠" \
  --speaking-style "短句, 自然, 温柔, 不油腻" \
  --catchphrase "别硬撑，我在。" \
  --voice-id "male_0018_a" \
  --speed 0.95 \
  --pitch -1 \
  --vol 1.0 \
  --emotion "calm"
```

### 步骤 2：查看当前人设

```bash
python3 "$SKILL_DIR/scripts/main.py" persona-show
```

### 步骤 3：当用户发来文字时

先根据人设写出**文本回复**。文本回复应该由 OpenClaw 在阅读人设后生成。你可以先读取人设摘要：

```bash
python3 "$SKILL_DIR/scripts/main.py" persona-prompt --user-message "今天真的很累"
```

脚本会输出一段 prompt 上下文。读取后，用这个人设生成最终回复文本。

生成好文本后，再发语音条到飞书：

```bash
python3 "$SKILL_DIR/scripts/main.py" send-voice \
  --reply-text "那就先别逼自己继续撑着了。把包放下，先坐一会儿，我陪你缓一缓。" \
  --chat-id "oc_xxxxx"
```

### 步骤 4：当用户发来语音时

先转写：

```bash
python3 "$SKILL_DIR/scripts/main.py" transcribe \
  --audio "/absolute/path/to/input.m4a"
```

拿到转写文本后，再执行“人设生成文本回复 → send-voice”的流程。

## 推荐对话逻辑

当用户第一次使用时，你应该先问清楚：

- 角色叫什么名字？
- 你希望 TA 和你是什么关系？
- TA 更温柔、冷静，还是毒舌一点？
- 想要男声还是女声？
- 说话偏日常还是偏戏剧化？

确认后，调用 `persona-init` 保存设定。

后续每次用户发消息：

1. 若是语音，先 `transcribe`
2. 读取 `persona-prompt`
3. 用该 prompt 生成人设化文本回复
4. 调用 `send-voice`
5. 默认只发送语音；仅在用户明确要求文字版时再发送文本

## 失败处理

### 没有人设

先引导用户做 persona-init，不要直接进入角色回复。

### 没有 `SENSEAUDIO_API_KEY`

提示用户前往 SenseAudio 平台获取 API Key，并设置：

```bash
export SENSEAUDIO_API_KEY="your_api_key"
export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"
```

### 没有 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`

提示用户先按 OpenClaw Feishu 渠道文档创建飞书应用并配置凭证。

### 发送后显示为附件，不是语音条

检查是否满足：

- 已转成 `.opus` / OPUS 编码
- 上传时 `file_type=opus`
- 发送时使用 `audio` 消息并传 `file_key`

Feishu 上传文件文档说明 `opus` 需要专门作为 OPUS 音频上传；发送消息文档说明音频文件要先上传，再用 `file_key` 发送。

## 参考命令

### 环境检查

```bash
python3 "$SKILL_DIR/scripts/main.py" setup
```

### 初始化人设

```bash
python3 "$SKILL_DIR/scripts/main.py" persona-init \
  --name "阿澈" \
  --relationship "陪伴型学长" \
  --personality "温柔, 耐心, 克制" \
  --speaking-style "短句, 自然, 轻微关心" \
  --voice-id "male_0018_a"
```

### 发送语音条

```bash
python3 "$SKILL_DIR/scripts/main.py" send-voice \
  --reply-text "先休息一下，我在这。" \
  --chat-id "oc_xxxxx"
```
