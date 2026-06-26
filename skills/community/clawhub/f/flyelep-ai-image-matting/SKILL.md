---
name: ai-image-matting
description: >-
  通过 Flyelep AI 工具接口自动去除图片背景，支持单张或批量处理。
  当用户要求抠图、去背景、提取商品主体、生成透明底素材时使用此技能。
---
# Flyelep AI抠图
通过 Flyelep AI Tool API 自动去除图片背景，并返回抠图后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting`
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
  "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg"
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/matted1.png,https://example.com/matted2.png"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为抠图后图片地址
- 多张图片时，`data` 中多个 URL 以英文逗号 `,` 分隔

返回结果应按逗号拆分后逐个展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| imgUrls | - | 图片链接字符串，多张时使用英文逗号分隔 |

## 参数映射规则
### imgUrls
- 接口要求传字符串，不是数组
- 单张图片时直接传一个 URL 字符串
- 多张图片时，用英文逗号 `,` 按顺序拼接
- 每个链接都应为公网可访问的图片直链，不要传网页地址

### 结果格式
- 抠图结果通常更适合返回透明背景图片
- 文档示例中返回的是 `.png`，因此应优先预期结果为支持透明底的图片格式
- 若接口实际返回其他格式，按接口返回值原样展示即可

## 调用示例
**单张图片抠图：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imgUrls": "https://example.com/img1.jpg"
  }'
```

**批量图片抠图：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "imgUrls": "https://example.com/img1.jpg,https://example.com/img2.jpg"
  }'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `imgUrls` 格式错误 | 该字段必须是字符串，多张图用英文逗号分隔，不是 JSON 数组 |
| 图片 URL 无法访问 | 传入的链接不是公网直链、已过期，或源站限制访问 |
| 抠图边缘效果不理想 | 原图主体与背景对比不足、边缘过于复杂，可换更清晰或背景更干净的源图 |
| 请求超时 | 批量图片较多或源图较大时，可适当增大超时时间 |

## 提示词处理
该接口不接收自然语言提示词，不需要构造额外文案。

执行时只需要：

1. 收集一张或多张图片 URL
2. 将多张 URL 用英文逗号拼接为 `imgUrls`
3. 在请求头中传入 `secretKey`
4. 调用接口并将返回的结果按逗号拆分后逐个展示

当用户明确要求“透明底”“抠出主体”“去掉背景”时，优先使用此技能；如果用户真正想要的是“换背景”而不是“去背景”，则更适合使用场景替换或局部重绘类技能。
