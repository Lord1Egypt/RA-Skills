# Coze TTS API 参考文档

## 接口信息

- **接口地址**: `POST https://api.coze.cn/v1/audio/speech`
- **认证方式**: Bearer Token (`Authorization: Bearer {COZE_API_KEY}`)
- **Content-Type**: `application/json`

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| input | string | 是 | 要转换为语音的文本内容 |
| voice_id | int64 | 否 | 音色ID，默认为1 |
| response_format | string | 否 | 输出格式：mp3/ogg_opus/wav/pcm，默认为mp3 |
| speed | float | 否 | 语速，范围0.5-2.0，默认为1.0 |

## 响应

成功时返回音频文件二进制数据。

错误时返回JSON格式错误信息。

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 认证失败，API Key无效 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## 音色列表

| voice_id | 音色名称 | 描述 |
|----------|----------|------|
| 1 | 默认音色 | 标准女声 |
| 2 | 男声 | 标准男声 |

> 注：具体可用音色请参考 Coze 官方文档

## 输出格式说明

| 格式 | 说明 | 适用场景 |
|------|------|----------|
| mp3 | 压缩音频格式 | 通用播放 |
| ogg_opus | Ogg封装的Opus编码 | 即时通讯 |
| wav | 无损音频格式 | 高质量需求 |
| pcm | 原始音频数据 | 专业音频处理 |

## 使用限制

- 文本长度限制：单次请求文本长度有限制
- 频率限制：根据账号等级有不同限制
- 并发限制：注意并发请求数量

## 官方文档

https://www.coze.cn/docs/developer_guides/audio_speech
