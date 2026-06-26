---
name: feishu-voice
description: 当用户发来语音消息时, 使用此 feishu-voice SKILL以语音消息回复。version: "1.0.2"
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["ffmpeg（仅 MiniMax 链路需要）"],"env":["MINIMAX_API_KEY（可选）"]}}}
---

# feishu-voice

## 接收：语音 → 文字

飞书自动为语音消息生成转写，消息体中自带 `Transcript` 字段，直接读取即可，无需任何 API 调用。

---

## 发送：文字 → 语音

## 流程

**Step 1.** 调用脚本生成语音文件：

```
python scripts/reply.py "<文字内容>"
```

输出文件路径（格式为 `.opus` 或 `.ogg`）。

**Step 2.** 通过飞书发送语音：

```
message(action=send, channel=feishu, media=<filepath>, contentType="audio/opus")
```

注：Edge TTS 输出的 `.ogg` 文件同样使用 `audio/opus` contentType。

---

## MiniMax 语气词（配置了 MINIMAX_API_KEY 时）

在生成回复文本时主动嵌入以下标记，可让语音更自然：

| 标记 | 含义 | 使用场景 |
|------|------|---------|
| `<#0.3#>` | 停顿 0.3 秒 | 逗号后、句子中间 |
| `(breath)` | 自然呼吸 | 长句中间、句末 |
| `(sighs)` | 叹气 | 感叹、无奈时 |
| `(emm)` | 思考语气 | 问句结尾、停顿后继续 |
| `(clear-throat)` | 清嗓 | 转折、开始说话 |
| `(laughs)` | 笑声 | 开心、幽默内容 |
| `(chuckle)` | 轻笑 | 轻松调侃 |
| `(sniffs)` | 吸鼻子 | 轻微情绪 |
| `(humming)` | 哼唱 | 愉快、自言自语 |

**规则：**
- 标记插入两个有发音文本之间，不可连续叠加
- 问句句尾加 `(emm)`
- 感叹句插 `(laughs)` 或 `(sighs)`
- 句号前无自然停顿时加 `(breath)`
- 长叙述每隔 20-30 字符插一次 `(breath)` 或 `<#0.3#>`

**示例：**
```
模型生成文本：好的，那我们出发吧。
应生成：好的<#0.3#>，那我们出发吧(laughs)。

模型生成文本：等等，让我想想，这个怎么做来着？
应生成：等等<#0.3#>，让我想想(emm)<#0.4#>，这个怎么做来着？

模型生成文本：唉，今天真是太累了。
应生成：唉(sighs)，今天真是太累了(breath)。
```

---

## 链路降级

```
MiniMax T2A (mp3) → ffmpeg → opus  [优先]
    ↓ 超时/无 key
Edge TTS (ogg 直出)                  [降级]
    ↓ 失败
返回纯文字（不走语音）
```

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `MINIMAX_API_KEY` | 否 | 有则优先 MiniMax；无则 Edge TTS |
| `EDGE_TTS_VOICE` | 否 | Edge TTS 音色，默认 `zh-CN-XiaoxiaoNeural` |

---

## 快速参考

```
# 生成语音并发送
python scripts/reply.py "<文字>"  →  输出文件路径  →  message(media=路径, contentType="audio/opus")
```
