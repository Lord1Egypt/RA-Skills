# AI 能力 API

## POST /skill/ai/outfit-recommend

AI 智能搭配推荐。根据用户性别、风格偏好、场景和天气情况，生成个性化搭配建议。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| gender | string | 是 | 性别：`男` 或 `女` |
| style | string | 否 | 风格偏好 |
| occasion | string | 否 | 场景（如：上班、约会、运动） |
| temperature | string | 否 | 温度，如 `10℃～20℃` |
| weather | string | 否 | 天气 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/ai/outfit-recommend \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "gender=女&occasion=约会&temperature=15℃～25℃&weather=晴"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "推荐搭配内容..."
  }
}
```

---

## POST /skill/ai/kb-search

知识库搜索。在服饰知识库中搜索匹配的单品，支持按品类和风格过滤。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索内容 |
| gender | string | 是 | 性别：`男` 或 `女` |
| scope | string | 否 | 搜索范围：`user`（默认，用户私有+公共）或 `public`（仅公共库） |
| class_name | string | 否 | 品类过滤（如：上衣、裤子、裙子） |
| style_name | string | 否 | 风格过滤（如：休闲、正式、运动） |
| top_k | int32 | 否 | 返回数量，默认 10 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/ai/kb-search \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "query=白色连衣裙&gender=女&top_k=5"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "list": [
      {
        "id": "1",
        "title": "白色连衣裙",
        "image": "https://...",
        "score": 0.95
      }
    ],
    "message": "搜索结果"
  }
}
```

---

## POST /skill/ai/virtual-tryon

虚拟试衣。将服饰图片合成到模特身上，预览穿着效果。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| garment_image | string | 是 | 服饰图片 URL |
| model_image | string | 否 | 模特图片 URL（不传则使用默认模特） |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/ai/virtual-tryon \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "garment_image=https://example.com/dress.jpg"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result_image": "https://...",
    "message": "试衣成功"
  }
}
```
