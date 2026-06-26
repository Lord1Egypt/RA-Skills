---
name: product-color-change
description: >-
  通过 Flyelep AI 工具接口智能识别图片中的商品并进行换色处理。
  当用户要求修改商品颜色、保持商品不变只换配色、生成同款不同颜色展示图时使用此技能。
---
# Flyelep 商品换色
通过 Flyelep AI Tool API 对图片中的商品进行换色处理，并返回换色后的新图片 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange`
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
  "sourceUrl": "https://example.com/product_red.jpg",
  "textPrompt": "将商品颜色改为深蓝色",
  "modelType": 0
}
```

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": "https://example.com/product_blue.jpg"
}
```

- `code=200` 表示调用成功
- `msg` 为接口返回说明
- `data` 为换色后的图片 URL

返回结果应直接展示给用户，不要回读图片内容。

## 参数说明
### 必传参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| sourceUrl | - | 原图链接 |
| modelType | - | 模型类型：`0=gemini-2.5`，`1=gemini-3-pro` |

### 推荐传入参数
| 字段 | 默认值 | 说明 |
|------|--------|------|
| textPrompt | - | 换色提示词，如“将商品颜色改为深蓝色” |

## 参数映射规则
### sourceUrl
- 传入待换色商品的原图公网 URL
- 必须是图片直链，不要传网页地址
- 原图应尽量清晰展示商品主体和原始颜色

### modelType
- `0`：`gemini-2.5`
- `1`：`gemini-3-pro`

推荐默认规则：

- 用户未指定模型时，默认传 `0`

### textPrompt
- 文档将其标为必需
- 直接描述目标颜色及必要约束
- 应尽量明确“将什么改成什么颜色”

推荐写法示例：

- `将商品颜色改为深蓝色`
- `把包包主体颜色改为奶油白，保留金属扣件颜色不变`
- `将耳机外壳换成哑光黑色，保持材质质感与光影不变`
- `把杯身改为浅绿色，保留品牌标识和背景不变`

### 提示词边界
- 优先描述颜色，不要把换色需求扩写成换材质或换商品
- 如果用户只是想“更换商品”，应改用商品替换 skill
- 如果用户想“换背景”，应改用场景替换 skill

> **说明**：场景替换、商品替换、商品换色三个接口共用同一 DTO，由接口内部自动设置 `type` 字段，调用方无需传入 `type`。

## 调用示例
**基础商品换色：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "sourceUrl": "https://example.com/product_red.jpg",
    "textPrompt": "将商品颜色改为深蓝色",
    "modelType": 1
  }'
```

**强调保留材质与光影的换色：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "sourceUrl": "https://example.com/product_watch.jpg",
    "textPrompt": "将表带改为深棕色皮革观感，保留金属表盘和整体光影不变",
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
| 换色结果偏差较大 | `textPrompt` 过于模糊，可补充目标颜色、材质观感和保留项 |
| 局部也被错误换色 | 原图主体边界不清晰，可换更干净的源图或在提示词里强调保留范围 |
| 请求超时 | 图片较大或处理复杂时，可适当增大超时时间 |

## 提示词处理
该接口支持 `textPrompt`，商品换色的结果高度依赖提示词描述质量。

执行时应遵循：

1. 明确目标颜色
2. 明确保留项：材质、品牌标识、背景、光影、构图
3. 避免把“换色”写成“换商品”或“换背景”
4. 对多部件商品可明确指定仅修改哪个部位

当用户要求“同款不同色”“把红色改成蓝色”时，优先使用此技能；如果用户想替换为完全不同的商品，应改用商品替换 skill。
