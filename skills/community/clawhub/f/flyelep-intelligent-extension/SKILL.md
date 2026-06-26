---
name: intelligent-extension
description: >-
  通过 Flyelep AI 工具接口对图片进行智能延展，支持批量处理并指定目标比例。
  当用户要求扩图、延展图片边缘、补全画布、适配 16:9/1:1 等比例时使用此技能。
---
# Flyelep 图片智能延展
通过 Flyelep AI Tool API 对一张或多张图片进行智能延展。
**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**
## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`
- **超时时间**: 建议 120-300 秒（批量图片处理可能耗时更长）

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
  "imgUrlList": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "ratio": "16:9"
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    "https://example.com/result1.jpg",
    "https://example.com/result2.jpg"
  ]
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为延展后的图片 URL 数组，与 `imgUrlList` 的输入顺序一致

返回结果应逐个展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| imgUrlList | - | 源图片 URL 列表，支持批量传入多张图片 |
| ratio | - | 目标延展比例 |

## 参数映射规则
### ratio（目标比例）
仅支持以下比例：

- `1:1`
- `2:3`
- `3:2`
- `3:4`
- `4:3`
- `9:16`
- `16:9`
- `21:9`

当用户明确指定目标比例时，原样传入 `ratio`。

当用户仅表达“改成横版”或“适配视频封面”等模糊需求时，可按上下文推断最合理的比例：

- 横版内容优先考虑 `16:9`
- 方图内容优先考虑 `1:1`
- 竖版内容优先考虑 `9:16`

如果上下文不足以安全推断，先向用户确认目标比例。

## 调用示例
**单张图片延展为横版 16:9：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imgUrlList": [
      "https://example.com/image1.jpg"
    ],
    "ratio": "16:9"
  }'
```

**批量图片延展为方图 1:1：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imgUrlList": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ],
    "ratio": "1:1"
  }'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入密钥 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `imgUrlList` 为空 | 至少传入一张待处理图片 URL |
| 比例不支持 | `ratio` 只能使用接口支持的固定枚举值 |
| 处理超时 | 批量图片较多或源图较大时可适当增大超时时间 |
| 返回数组数量异常 | 先核对源图 URL 是否可访问，再重试请求 |

## 提示词处理
该接口不接收自然语言提示词，不需要构造额外文案。

执行时只需要：

1. 收集用户提供的图片 URL 列表
2. 确定目标比例 `ratio`
3. 在请求头中传入 `secretKey`
4. 调用接口并按输入顺序展示返回的图片 URL

保留用户原始图片顺序，不要擅自重排 `imgUrlList`。
