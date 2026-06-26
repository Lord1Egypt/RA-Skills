---
name: scene-replace
description: >-
  通过 Flyelep AI 工具接口将图片中的背景场景替换为指定场景，可结合参考图和文本提示词精准控制效果。
  当用户要求更换背景场景、替换商品展示环境、保留主体改场景时使用此技能。
---
# Flyelep 场景替换
通过 Flyelep AI Tool API 将图片中的背景场景替换为目标场景，并返回替换后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/sceneReplace`
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
  "sourceUrl": "https://example.com/product.jpg",
  "replaceImageUrl": "https://example.com/scene.jpg",
  "textPrompt": "室内现代风格展厅",
  "modelType": 0
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/scene_replaced.jpg"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为场景替换后的图片 URL

返回结果应直接展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| sourceUrl | - | 原图链接 |
| modelType | - | 模型类型：`0=gemini-2.5`，`1=gemini-3-pro` |

### 条件必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| replaceImageUrl | - | 场景参考图链接，多张时用英文逗号分隔|
| textPrompt | - | 用户提示词，描述目标场景|

## 参数映射规则
### sourceUrl
- 传入待替换场景的原图公网 URL
- 必须是图片直链，不要传网页地址

### modelType
- `0`：`gemini-2.5`
- `1`：`gemini-3-pro`

推荐默认规则：

- 用户未指定模型时，默认传 `0`

### replaceImageUrl
- 用于提供目标场景参考图
- 暂时只支持单图

### textPrompt
- 用自然语言描述目标场景，如风格、环境、光线、氛围、陈列方式
- 参考图负责场景基准，文字负责补充约束

> **说明**：场景替换、商品替换、商品换色三个接口共用同一 DTO，由接口内部自动设置 `type` 字段，调用方无需传入 `type`。

## 调用示例
**结合参考图与文本描述替换场景：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/sceneReplace" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "sourceUrl": "https://example.com/product.jpg",
    "replaceImageUrl": "https://example.com/scene1.jpg,https://example.com/scene2.jpg",
    "textPrompt": "室内现代风格展厅，暖色灯光，突出高级陈列感",
    "modelType": 1
  }'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `sourceUrl` 无法访问 | 原图 URL 不是公网直链、已过期，或源站限制访问 |
| `modelType` 非 0/1 | 模型类型只支持 `0` 或 `1` |
| `replaceImageUrl` 与 `textPrompt` 都没传或少传 | 两者都需要提供 |
| 场景效果不理想 | 文字描述过于模糊，可补充风格、光线、空间类型、氛围等信息 |
| 请求超时 | 原图较大、参考图较多或生成复杂时，可适当增大超时时间 |

## 提示词处理
该接口支持通过 `textPrompt` 控制目标场景，因此提示词质量很重要。

执行时应遵循：

1. 明确保留项：主体商品、角度、构图、光影关系
2. 明确替换项：背景环境、风格、空间、色温、陈列方式
3. `replaceImageUrl`和`textPrompt`皆为必需，两者共同控制生成效果

当用户要求“换背景场景但保留产品不变”时，提示词应明确写出“保留主体不变”；如果用户真正想改的是商品本身而不是背景，应改用商品替换类 skill。
