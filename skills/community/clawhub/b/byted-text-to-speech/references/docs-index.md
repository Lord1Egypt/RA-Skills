# Byted-Text-to-Speech 文档索引

以下资料主要对应火山引擎豆包语音合成 API，是本 skill 依赖的底层文档。

所有文档均位于火山引擎官网。由于官网页面为动态渲染，部分内容无法静态抓取，建议直接在浏览器中访问。

## 核心文档

| 文档 | 链接 |
|------|------|
| **HTTP Chunked/SSE 单向流式-V3**（本 skill 对应的接口） | https://www.volcengine.com/docs/6561/1598757 |
| 产品简介 | https://www.volcengine.com/docs/6561/1257543 |
| 快速入门（新版控制台） | https://www.volcengine.com/docs/6561/2119699 |

## 音色与发音人

| 文档 | 链接 |
|------|------|
| 音色列表 | https://www.volcengine.com/docs/6561/1257544 |
| SSML 标记语言（高级用法） | https://www.volcengine.com/docs/6561/1330194 |

## 鉴权

| 文档 | 链接 |
|------|------|
| API Key 管理 | https://console.volcengine.com/speech/new/setting/apikeys |
| API Key 使用说明 | https://www.volcengine.com/docs/6561/1816214 |

## 控制台入口

| 入口 | 链接 |
|------|------|
| 豆包语音控制台（API Key 管理） | https://console.volcengine.com/speech/new/setting/apikeys |

## API 关键参数速查

### 请求

```
POST https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse
Content-Type: application/json
X-Api-Key: <your-api-key>
X-Api-Resource-Id: seed-tts-2.0
```

### 请求体字段

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| user.uid | String | 是 | 用户标识 |
| req_params.text | String | 是 | 要合成的文本 |
| req_params.speaker | String | 是 | 发音人 ID |
| req_params.sample_rate | Integer | 否 | 采样率，默认 24000 |
| req_params.audio_params.format | String | 否 | 音频格式：mp3、pcm、ogg_opus |
| req_params.audio_params.speech_rate | Integer | 否 | 语速 [-50, 100] |
| req_params.audio_params.loudness_rate | Integer | 否 | 音量 [-50, 100] |
| req_params.audio_params.bit_rate | Integer | 否 | 比特率（mp3/ogg_opus），默认 64000 |
| req_params.additions | String (JSON) | 否 | 扩展参数（JSON 字符串），内部字段见下表 |

#### req_params.additions 内部字段

`additions` 的值为 JSON 字符串，序列化后的内部字段如下：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| post_process.pitch | Integer | 0 | 音调 [-12, 12] |
| disable_markdown_filter | Boolean | true | 是否禁用 markdown 过滤。`true` 保留原始 markdown 语法，`false` 过滤掉 markdown 语法（如 `**你好**` 读为"你好"） |
| enable_latex_tn | Boolean | true | 是否启用 LaTeX 公式播报 |
| latex_parser | String | "v2" | LaTeX 解析器版本 |

示例：

```json
{
  "post_process": {"pitch": 0},
  "disable_markdown_filter": true,
  "enable_latex_tn": true,
  "latex_parser": "v2"
}
```

### 响应（SSE data 行）

| 字段 | 说明 |
|------|------|
| code | 0 或 20000000 表示成功 |
| message | 错误信息 |
| data | Base64 编码的音频数据块 |

### 常见错误码

| 错误码 | 含义 |
|--------|------|
| 401 | API Key 无效或未配置 |
| 403 | 服务未开通或无权限 |
| 429 | 请求频率超限 |
| 500 | 服务端内部错误 |
