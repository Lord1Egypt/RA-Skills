---
name: image-translate
description: >-
  通过 Flyelep AI 工具接口识别并翻译图片中的文字，返回翻译后的新图片地址。
  当用户要求翻译海报文字、翻译商品图文案、将图片文字改成目标语言时使用此技能。
---
# Flyelep 图片翻译
通过 Flyelep AI Tool API 对图片中的文字进行识别与翻译，并返回翻译后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`
- **超时时间**: 建议 120-300 秒

## 认证方式
所有 AI 工具接口均需在请求头中传入 `secretKey`。该密钥需由用户在 Flyelep 开放平台申请获得：https://www.flyelep.cn/controlboard 。

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：`secretKey` 必须放在请求头中，这是 AI 工具接口的统一鉴权要求。不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 请求 Body
```json
{
  "imageUrl": "https://example.com/poster_cn.jpg",
  "to": 1,
  "from": "auto"
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/translated.jpg"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为翻译后的新图片 URL

返回结果应直接展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| imageUrl | - | 待翻译的图片链接 |
| to | - | 目标语言，使用接口定义的整数枚举值 |

### 可选参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| from | `auto` | 原语言，默认自动识别 |

## 参数映射规则
### imageUrl
- 传入单张待翻译图片的公网可访问 URL
- 必须是图片直链，不要传网页地址

### from（原语言）
- 用户未指定源语言时，默认传 `"auto"`
- 用户明确指定源语言时，按用户要求原样传入

### to（目标语言）
- 文档要求传整数枚举值，而不是语言名称字符串
- 目标语言枚举如下：

| `to` | 语言 |
|------|------|
| `0` | 中文 |
| `1` | 英文 |
| `2` | 俄语 |
| `3` | 西班牙语 |
| `4` | 法语 |
| `5` | 德语 |
| `6` | 意大利语 |
| `7` | 荷兰语 |
| `8` | 葡萄牙语 |
| `9` | 越南语 |
| `10` | 土耳其语 |
| `11` | 马来语 |
| `12` | 泰语 |
| `13` | 波兰语 |
| `14` | 印度尼西亚语 |
| `15` | 日语 |
| `16` | 韩语 |
| `17` | 繁体中文 |

- 当用户以自然语言表达目标语种时，按上表映射为对应整数后传入
- 如果用户请求的语言不在上述枚举表中，应明确告知接口当前不支持该目标语言

## 调用示例
**自动识别原语言，翻译成英文：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imageUrl": "https://example.com/poster_cn.jpg",
    "to": 1,
    "from": "auto"
  }'
```

**指定原语言后翻译成日语：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imageUrl": "https://example.com/product-poster.jpg",
    "to": 15,
    "from": "zh"
  }'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `imageUrl` 无法访问 | 图片 URL 不是公网直链、已过期，或源站限制访问 |
| `to` 枚举错误 | 目标语言必须使用文档规定的整数枚举值，例如英文=`1`、日语=`15`、韩语=`16` |
| 翻译结果异常 | 原图文字过小、模糊或遮挡严重，可更换更清晰的源图后重试 |
| 请求超时 | 源图较大或识别耗时较长时，可适当增大超时时间 |

## 提示词处理
该接口不接收自然语言提示词，不需要构造额外文案。

执行时只需要：

1. 收集单张图片 URL `imageUrl`
2. 根据语言枚举表确定目标语言整数 `to`
3. 原语言未知时传 `from="auto"`
4. 在请求头中传入 `secretKey`
5. 调用接口并返回翻译后的图片 URL

如果用户只说“翻译成英文/日文/韩文”等常见语言，可直接按本技能内的枚举表映射为对应整数后调用；若用户要求的目标语言不在枚举表内，则不要硬猜，需明确告知暂不支持。
