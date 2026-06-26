---
name: ecommerce-voice-cs
description: 电商 AI 语音技能。用于在 OpenClaw 或类似技能宿主中，按不同触发词独立启用两套互不干扰的能力：(1) 售后客服模式，将售后文本咨询按预设退款规则生成客服回复并输出 TTS 音频；(2) 电话推销模式，按产品名称、功能、优势和优惠范围生成推销话术并输出 TTS 音频。适用于需要模式切换、配置确认、音色选择和语音落盘的场景。
---

# Ecommerce Voice CS

实现一个最小可集成的电商售后语音客服 skill。

## Trigger

识别触发词：

- `我需要你现在当一个客服机器人`
- `我需要你现在当一个推销员`

这两个模式必须完全独立运行，不能共享会话状态、配置或业务逻辑。用户触发哪个模式，就只进入哪个模式。

## 售后模式

收到售后触发词后，不要立刻进入客服模式。先收集并确认这些配置：

- `api_key`（可选；若未设置环境变量 `SENSEAUDIO_API_KEY` 时再提供）
- `refund_policy`
- `unboxing_allowed`
- `shipping_fee_by`
- `audio_output_path`
- `voice_id`（可选，默认 `child_0001_b`）

配置收集完整后，先给用户一份确认摘要。只有用户明确回复“确认进入”，才正式进入售后模式。

进入售后模式后，每次处理客户消息时都必须：

1. 先生成文本客服回复
2. 再生成 TTS 音频文件
3. 在文本结尾附上“`TTS 已生成成功，文件已保存到：<path>`”

## 电话推销模式

收到推销触发词后，不要立刻进入推销模式。先收集并确认这些配置：

- `api_key`（可选；若未设置环境变量 `SENSEAUDIO_API_KEY` 时再提供）
- `audio_output_path`
- `product_name`
- `product_features`
- `product_advantages`
- `discount_range`
- `voice_id`（可选，默认 `child_0001_b`）

配置收集完整后，先给用户一份确认摘要。只有用户明确回复“开始”或确认进入，才正式进入电话推销模式。

进入电话推销模式后，每次处理客户消息时都必须：

1. 先生成电话推销文本话术
2. 再生成 TTS 音频文件
3. 在文本结尾附上“`TTS 已生成成功，文件已保存到：<path>`”

## Runtime Inputs

调用方应提供这些字段：

- `session_id`: 会话标识。多轮配置和客服模式都依赖同一个 `session_id`
- `message`: 用户输入文本
- `api_key`: SenseAudio API Key，可选；优先通过环境变量 `SENSEAUDIO_API_KEY` 提供，未设置时再由调用方传入
- `voice_id`: 已确认可用的 SenseAudio voice_id
- `refund_policy`: 退款政策文本
- `unboxing_allowed`: 是否支持拆封退货
- `shipping_fee_by`: 运费承担方
- `audio_output_path`: 音频输出目录
- `product_name`: 电话推销产品名称
- `product_features`: 电话推销产品功能
- `product_advantages`: 电话推销产品优势
- `discount_range`: 电话推销可优惠范围
- `audio_format`: 可选，默认 `.mp3`

## Playback Protocol

当 skill 成功生成音频时，返回结果除 `audio_file` 外，还会带一个 `playback` 字段，供宿主直接播放：

```json
{
  "playback": {
    "action": "play_audio",
    "auto_play": true,
    "source_type": "local_file",
    "path": "tts_output\\cs_reply_20260315_210818.mp3",
    "format": "mp3",
    "mime_type": "audio/mpeg",
    "retain_file": true
  }
}
```

宿主约定：

- 当 `playback` 不为 `null` 且 `playback.action == "play_audio"` 时，立即播放 `playback.path`
- 播放完成后不要删除文件，因为 `retain_file` 固定为 `true`
- 如果宿主不支持自动播放，至少保留 `audio_file` 和 `playback.path` 供后续手动播放

## Confirmed Voice IDs

只使用这 3 个已确认可用的 voice_id：

- `child_0001_b`
- `male_0004_a`
- `male_0018_a`

如果调用方未指定 `voice_id`，默认使用 `child_0001_b`。

## Files

- `helper.py`: 对外调用入口，包含售后模式和电话推销模式两套独立状态机
- `src/ecommerce_voice_cs/`: 底层实现，包括状态管理、规则引擎、SenseAudio TTS 适配层

## Notes

- 当前仅接入公开可验证的 SenseAudio TTS 接口
- 音色克隆上传接口未公开时，不实现 `upload_sample` 真正上传；直接使用现有 `voice_id`
- TTS 接口文档：`https://senseaudio.cn/docs/voice_api`
