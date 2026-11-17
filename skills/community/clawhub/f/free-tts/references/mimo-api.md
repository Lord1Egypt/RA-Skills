# 小米 MiMo TTS API 参考（free-tts skill）

来源：https://mimo.mi.com/docs/zh-CN/quick-start/usage-guide/audio/speech-synthesis-v2.5

## Base URL 与认证

```
OpenAI 兼容: https://api.xiaomimimo.com/v1
调用路径:    POST /chat/completions
认证:        Authorization: Bearer <MIMO_API_KEY> + api-key: <MIMO_API_KEY>
Key 获取:    https://platform.xiaomimimo.com/#/console/api-keys（小米账号登录）
             格式 sk-xxxxx；Token Plan 套餐另用 tp-xxxxx + token-plan-cn.xiaomimimo.com
计费:        限时免费（控制台账单页查用量）
```

## 三个模型

| Model ID | 能力 | 音色来源 |
|----------|------|----------|
| `mimo-v2.5-tts` | 预置音色合成（支持流式、唱歌） | 预置音色列表 |
| `mimo-v2.5-tts-voicedesign` | 文本描述设计音色（不支持流式/预置/克隆） | user message 里的描述 |
| `mimo-v2.5-tts-voiceclone` | 音频样本克隆（不支持流式/预置/设计） | voice 字段传 base64 音频 |

## messages 规则（关键）

- **要合成的文本放 `role: assistant`**，不是 user！
- `role: user` 放风格指令（自然语言）或对话历史，voicedesign 模式放音色描述（必填）
- 音频标签控制内容放在 assistant content 里

## 请求体

```json
{
  "model": "mimo-v2.5-tts",
  "messages": [
    {"role": "user", "content": "风格指令（可选）"},
    {"role": "assistant", "content": "(风格标签)要合成的文本"}
  ],
  "audio": {"format": "wav|pcm16", "voice": "冰糖"}
}
```

- `audio.format`：`wav`（非流式）或 `pcm16`（流式拼接用，24kHz PCM16LE mono）
- `audio.voice`：预置音色名 / 克隆音频 `data:audio/mpeg;base64,<b64>`
- `audio.optimize_text_preview`：voicedesign 专用，true 时模型润色文本（可不传 assistant）

## 预置音色

| 音色名 | 语言 | 性别 |
|--------|------|------|
| 冰糖（中国集群默认）/ Mia（其他集群默认） | 中/英 | 女 |
| 茉莉 | 中文 | 女 |
| 苏打 | 中文 | 男 |
| 白桦 | 中文 | 男 |
| Chloe | 英文 | 女 |
| Milo / Dean | 英文 | 男 |

## 响应

```json
{"choices": [{"message": {"audio": {"data": "<base64音频>", "transcript": "..."}}}]}
```

`audio.data` base64 解码 → wav 直接写盘；pcm16 需包 wav 头（24000Hz mono 16bit）。

## 音频克隆要求

- 仅 mp3 / wav 格式；base64 后 ≤ 10MB（原文约 ≤7MB）
- MIME 前缀：`data:audio/mpeg;base64,` 或 `data:audio/wav;base64,`
- 每次请求传音频，**不保存模型**（与 Fish 持久克隆不同）

## 风格标签（放 assistant content 开头）

格式：`(风格1 风格2)文本`，支持半角/全角括号/方括号。

- 基础情绪：开心/悲伤/愤怒/恐惧/惊讶/兴奋/委屈/平静/冷漠
- 复合情绪：怅然/欣慰/无奈/愧疚/释然/嫉妒/厌倦/忐忑/动情
- 语调：温柔/高冷/活泼/严肃/慵懒/俏皮/深沉/干练/凌厉
- 音色：磁性/醇厚/清亮/空灵/稚嫩/苍老/甜美/沙哑/醇雅
- 人设：夹子音/御姐音/正太音/大叔音/台湾腔
- 方言：东北话/四川话/河南话/粤语
- 角色：孙悟空/林黛玉（也支持自定义）
- 唱歌：`(唱歌)歌词`（建议中文歌词）

文中任意位置可插细粒度标签：`[笑]` `[哽咽]` `[深呼吸]` `[叹气]` `(小声)` 等。

## 音色描述写法（voicedesign）

维度：性别年龄 + 音色质感 + 情绪语气 + 语速节奏（+角色人设/场景/年代）。1-4 句即可，避免矛盾特征、避免混响/EQ 等音质词、避免"普通的"等模糊词。

## 实测经验

- 流式接口 pcm16 用 numpy 拼接；本 skill 用 stdlib wave 模块替代（零依赖）
- voicedesign / voiceclone 的"流式"目前降级为兼容模式（推理完才返回一次）
- 兼容 OpenAI/Anthropic 双协议，可用现有 openai SDK（base_url 指向 MiMo）
