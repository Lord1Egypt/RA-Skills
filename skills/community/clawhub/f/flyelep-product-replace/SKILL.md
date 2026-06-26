---
name: product-replace
description: >-
  通过 Flyelep AI 工具接口将图片中的商品替换为指定商品图，同时保留原图背景及光影效果。
  当用户要求替换商品主体、保留原场景换产品、保持背景不变更换展示商品时使用此技能。
---
# Flyelep 商品替换
通过 Flyelep AI Tool API 将图片中的商品替换为目标商品，并返回替换后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productReplace`
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
  "sourceUrl": "https://example.com/scene_with_old_product.jpg",
  "replaceImageUrl": "https://example.com/new_product.jpg",
  "modelType": 0,
  "textPrompt": "保留背景和光影，将主体商品替换为新的白色保温杯"
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/product_replaced.jpg"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为商品替换后的图片 URL

返回结果应直接展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| sourceUrl | - | 原图链接，包含原始商品的图片 |
| modelType | - | 模型类型：`0=gemini-2.5`，`1=gemini-3-pro` |

### 可选参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| replaceImageUrl | - | 目标商品图链接，多张时用英文逗号分隔 |
| textPrompt | - | 用户提示词 |

## 参数映射规则
### sourceUrl
- 传入待替换商品的原图公网 URL
- 必须是图片直链，不要传网页地址
- 原图中应清楚包含待替换商品和原背景环境

### modelType
- `0`：`gemini-2.5`
- `1`：`gemini-3-pro`

推荐默认规则：

- 用户未指定模型时，默认传 `0`
- 若用户追求更好的效果，可先传 `1`

### replaceImageUrl
- 用于提供目标商品图
- 暂时只支持单图
- 当用户明确说“把原商品换成另一件商品”时，优先传入该字段

### textPrompt
- 用于补充替换要求，例如材质、颜色、角度、尺寸观感、保留方式
- 可用于强调“保留原场景、保留光影、保留构图”
- 当用户有明确风格要求时建议一并传入

推荐写法示例：

- `保留背景和桌面反光，将商品替换为黑色蓝牙耳机`
- `保持原场景与阴影效果，将主体换成白色保温杯`
- `保留背景展台不变，将中间产品替换为新的香水瓶，风格保持高级简洁`

> **说明**：场景替换、商品替换、商品换色三个接口共用同一 DTO，由接口内部自动设置 `type` 字段，调用方无需传入 `type`。

## 调用示例
**结合目标商品图与文本约束替换商品：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productReplace" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "sourceUrl": "https://example.com/scene_with_old_product.jpg",
    "replaceImageUrl": "https://example.com/new_product_front.jpg,https://example.com/new_product_side.jpg",
    "modelType": 1,
    "textPrompt": "将商品替换为我上传的图片，颜色为红色"
  }'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `sourceUrl` 无法访问 | 原图 URL 不是公网直链、已过期，或源站限制访问 |
| `replaceImageUrl` 无法访问 | 目标商品图 URL 无效、不可公开访问，或链接格式不正确 |
| `modelType` 非 0/1 | 模型类型只支持 `0` 或 `1` |
| 替换结果不像目标商品 | 目标商品图不够清晰或角度不足，可增加更多参考图并补充 `textPrompt` |
| 商品替换后背景不协调 | 提示词未强调保留原背景和光影，可在 `textPrompt` 中补充说明 |
| 请求超时 | 原图较大、参考商品图较多或生成复杂时，可适当增大超时时间 |

## 提示词处理
该接口支持 `textPrompt`，但在商品替换场景下，目标商品图通常比纯文字更关键。

执行时应遵循：

1. 优先保证 `sourceUrl` 清晰展示原场景和原商品
2. 优先提供 `replaceImageUrl`，帮助模型准确识别目标商品
3. 通过 `textPrompt` 强调保留项：背景、光影、角度、构图、摆放位置
4. 通过 `textPrompt` 补充目标商品要求：颜色、材质、风格、展示方式

当用户真正想改的是“背景场景”而不是“商品主体”时，应改用场景替换 skill；当用户只是想换颜色而不是换商品，应改用商品换色类 skill。
