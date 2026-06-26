---
name: image-enlarge
description: >-
  通过 Flyelep AI 工具接口对图片进行无损放大，支持单张或批量处理。
  当用户要求提升清晰度、放大图片尺寸、做超清增强、批量增强商品图时使用此技能。
---
# Flyelep 无损放大
通过 Flyelep AI Tool API 对图片进行无损放大处理，并返回增强后的图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge`
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
  "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg",
  "scalingRatio": 2
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/enlarged1.jpg,https://example.com/enlarged2.jpg"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为放大后的图片地址
- 多张图片时，`data` 中多个 URL 以英文逗号 `,` 分隔

返回结果应按逗号拆分后逐个展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| imgUrls | - | 图片链接字符串，多张时使用英文逗号分隔 |
| scalingRatio | - | 增强强度：`1=轻度增强`、`2=标准增强`、`3=强力增强` |

## 参数映射规则
### imgUrls
- 接口要求传字符串，不是数组
- 单张图片时直接传一个 URL 字符串
- 多张图片时，用英文逗号 `,` 按顺序拼接
- 每个链接都应为公网可访问的图片直链，不要传网页地址

### scalingRatio
- `1`：轻度增强，适合原图质量较好、只需温和提清晰度
- `2`：标准增强，适合作为默认值
- `3`：强力增强，适合原图较糊或需要更明显提升

推荐默认规则：

- 用户未指定增强强度时，默认传 `2`
- 用户强调“轻微增强、尽量自然”时，传 `1`
- 用户强调“尽可能清晰、强力修复”时，传 `3`

> **说明**：PDF 文档额外提示“AI 超清有较严格的图片规格限制，文档中已注明”，但当前可提取页面未包含该规格细则。因此调用前应优先使用常见、清晰、可公开访问的图片直链；若接口报规格错误，应以 Flyelep 最新文档或控制台提示为准。

## 调用示例
**单张图片标准增强：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imgUrls": "https://example.com/img1.jpg",
    "scalingRatio": 2
  }'
```

**批量图片强力增强：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg",
    "scalingRatio": 3
  }'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `imgUrls` 格式错误 | 该字段必须是字符串，多张图用英文逗号分隔，不是 JSON 数组 |
| 图片 URL 无法访问 | 传入的链接不是公网直链、已过期，或源站限制访问 |
| `scalingRatio` 非 1/2/3 | 增强强度只支持 `1`、`2`、`3` |
| 接口提示图片规格不符合要求 | Flyelep AI 超清对源图可能有限制，换用更规范的图片尺寸或格式后重试 |
| 请求超时 | 批量图片较多或增强强度较高时，可适当增大超时时间 |

## 提示词处理
该接口不接收自然语言提示词，不需要构造额外文案。

执行时只需要：

1. 收集一张或多张图片 URL
2. 将多张 URL 用英文逗号拼接为 `imgUrls`
3. 根据用户意图确定 `scalingRatio`
4. 在请求头中传入 `secretKey`
5. 调用接口并将返回的结果按逗号拆分后逐个展示

如果用户只是说“帮我变清晰一点”，优先使用默认的 `scalingRatio=2`；如果用户特别强调“不要过度锐化”，则使用 `1`。
