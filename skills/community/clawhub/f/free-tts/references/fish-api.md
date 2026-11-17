# Fish Audio API 参考（free-tts skill）

来源：https://docs.fish.audio · https://fish.audio/zh-CN/blog/s2-1-pro-free-api/

## Base URL 与认证

```
Base URL: https://api.fish.audio
认证:     Authorization: Bearer <FISH_API_KEY>
Key 获取: https://fish.audio/app/api-keys/（注册免费、无需信用卡）
TTS 模型通过 header `model: <model-string>` 指定（不是 body）
```

## 免费层事实（重要）

- 模型字符串 `s2.1-pro-free`，与付费层同一端点，仅 header 不同
- **有效期 2026-08-31**（官方两次延期：7-24 → 7 月底 → 8-31，变动会提前通知）
- 无硬性字符上限，受公平使用政策约束；无 SLA/延迟保证
- 请求数据可能被用于模型改进；ARR > $1M 商用需联系官方
- 声音克隆在免费层同样可用
- 83 种语言，同一模型同一端点

## Endpoint 1：TTS 合成

```
POST /v1/tts
Content-Type: application/json
Header: model: s2.1-pro-free
```

Body 字段：

| 字段 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `text` | ✅ | — | 合成文本 |
| `reference_id` | ❌ | — | 持久化 voice_id（克隆模型） |
| `references` | ❌ | — | 即时克隆 `[{audio: <裸base64>, text: <字幕>}]`（不是 data URI） |
| `format` | ❌ | mp3 | mp3 / wav / pcm / opus |
| `mp3_bitrate` | ❌ | 128 | 64 / 128 / 192 |
| `sample_rate` | ❌ | — | wav/pcm 采样率 |
| `prosody.speed` | ❌ | 1.0 | 0.5-2.0 |
| `prosody.volume` | ❌ | 0 | dB |
| `temperature` | ❌ | 0.7 | 越低越稳定 |
| `top_p` | ❌ | 0.7 | |
| `chunk_length` | ❌ | 200 | 100-300 |
| `latency` | ❌ | balanced | balanced(~300ms TTFA) / normal(稳但慢) |
| `normalize` | ❌ | true | 数字/日期归一化 |

响应：成功直接返回音频二进制（不是 JSON）。错误返回 JSON `{message, status}`。

错误码：400 参数错 / 401 key 无效 / 402 余额不足（换 s2.1-pro-free）/ 403 无权限 / 429 限流（等 30s）。

## Endpoint 2：创建声音克隆模型

```
POST /model
Content-Type: multipart/form-data（文件上传必须 multipart）
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `type` | ✅ | 固定 `tts` |
| `title` | ✅ | 模型标题 |
| `train_mode` | ✅ | `fast`（秒级可用，推荐）/ `full` |
| `voices` | ✅ | 1-20 个音频文件（.wav/.mp3/.m4a/.opus） |
| `visibility` | ❌ | private(默认) / unlist / public |
| `description` | ❌ | 描述 |
| `texts` | ❌ | 与 voices 对应的转写（最多 20 条，重复字段形式） |
| `enhance_audio_quality` | ❌ | 默认 true，自动降噪 |

响应 201：`{_id: voice_id, state: created|training|trained|failed, title, ...}`
fast 模式几乎立即 `trained`。

样本要求：单人、无背景音乐/混响、≥10 秒（推荐 1-2 分钟）。

## Endpoint 3：列出模型

```
GET /model?pageSize=50
```

响应：`{items: [...]}`（兼容 list）。

## Endpoint 4：删除模型

```
DELETE /model/{voice_id}
```

200/204 成功。

## 实测经验

- 裸 HTTP（urllib）比官方 SDK 稳，本 skill 全部 stdlib 实现
- 即时克隆 `references[].audio` 是**裸 base64**，不带 `data:...;base64,` 前缀
- 克隆 multipart 的 `texts` 是重复字段（多个同名 part），不是 JSON 数组
- 海外 API：直连失败设 `HTTPS_PROXY=http://127.0.0.1:7897`
- OpenAPI schema: https://api.fish.audio/openapi.json
