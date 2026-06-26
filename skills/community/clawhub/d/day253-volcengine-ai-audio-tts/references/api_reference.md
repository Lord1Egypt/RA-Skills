# Volcengine TTS API 参考

本文档对应 **在线语音合成 API - HTTP 一次性合成（非流式）**。

## 接口地址

- `POST https://openspeech.bytedance.com/api/v1/tts`

## 鉴权

- Header: `Authorization: Bearer;${token}`
- 其中 `token` 为控制台获取的应用 Token（与请求体 `app.token` 一致）。

## 请求体结构（JSON）

| 层级 | 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| app | | dict | ✓ | 应用配置 |
| app | appid | string | ✓ | 应用 ID，控制台获取 |
| app | token | string | ✓ | 应用 Token |
| app | cluster | string | ✓ | 业务集群，如 `volcano_tts`（标准音色） |
| user | | dict | ✓ | 用户配置 |
| user | uid | string | ✓ | 用户标识，可任意非空 |
| audio | | dict | ✓ | 音频配置 |
| audio | voice_type | string | ✓ | 音色，见 [发音人参数列表](https://www.volcengine.com/docs/6561/79824) |
| audio | rate | int | | 采样率 8000/16000/24000，默认 24000 |
| audio | encoding | string | | wav / pcm / ogg_opus / mp3，默认 pcm；wav 不支持流式 |
| audio | speed_ratio | float | | 语速 [0.2, 3]，默认 1.0 |
| audio | volume_ratio | float | | 音量 [0.1, 3]，默认 1.0 |
| audio | pitch_ratio | float | | 音高 [0.1, 3]，默认 1.0 |
| audio | language | string | | 语言，见发音人列表 |
| audio | emotion | string | | 情感/风格 |
| request | | dict | ✓ | 请求配置 |
| request | reqid | string | ✓ | 每次请求唯一，建议 UUID |
| request | text | string | ✓ | 合成文本，UTF-8，建议 ≤1024 字节 |
| request | text_type | string | | plain / ssml，默认 plain |
| request | operation | string | ✓ | 非流式固定为 `query` |
| request | silence_duration | int | | 句尾静音 ms，默认 125 |

## 响应（成功时 code=3000）

| 字段 | 类型 | 说明 |
|------|------|------|
| reqid | string | 与请求一致 |
| code | int | 3000 表示成功 |
| message | string | 状态信息 |
| sequence | int | 负数表示合成完毕（如 -1） |
| data | string | 音频 Base64 编码 |
| addition | object | duration（ms）、frontend（时间戳）等 |

## 错误码

| code | 说明 |
|------|------|
| 3000 | 成功 |
| 3001 | 无效请求、参数非法 |
| 3003 | 并发超限 |
| 3005 | 后端服务忙 |
| 3010 | 文本长度超限 |
| 3011 | 无效文本（空、与语种不匹配等） |
| 3030 | 处理超时 |
| 3031 | 处理错误 |
| 3050 | 音色查询失败（检查 voice_type/cluster） |

## 脚本归一化请求字段（本 skill）

- `text` → request.text
- `voice_type` 或 `voice` → audio.voice_type
- `encoding` → audio.encoding
- `rate` → audio.rate
- `speed_ratio`, `volume_ratio`, `pitch_ratio` → audio 同名
- `language`, `emotion` → audio 同名
- `app_id`, `token`, `cluster` 可由环境变量注入，不写入请求文件时可省略
