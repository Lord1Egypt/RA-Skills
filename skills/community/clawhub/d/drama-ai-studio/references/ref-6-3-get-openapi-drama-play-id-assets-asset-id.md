> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.3 GET /openapi/drama/{play_id}/assets/{asset_id}

获取单个资产详情。

**路径参数（Path）：**

| 参数       | 必填 | 类型   | 说明     |
|------------|------|--------|----------|
| `play_id`  | 是   | int    | 剧目 ID  |
| `asset_id` | 是   | string | 资产 ID  |

**请求体 / 查询参数：** 无

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "1",
    "type": 2,
    "name": "角色A",
    "description": "可选描述",
    "source_episode_nos": [1, 2],
    "deleted": false,
    "prompt": "<该字段可能不存在>资产级主提示词，用于图像生成等综合场景",
    "candidate_image_urls": [
      "https://示例域/openapi/drama/1/assets/2/1/general/candidates/10/image/original?su_scene=drama_candidate_image&su_exp=1730000000&su_sig=<HMAC_SHA256_HEX>"
    ],
    "operation_time": "2025-01-01T12:00:00"
  }
}
```

**字段说明（`data`，除与 §6.1 相同的 `id` / `type` / `name` / `description` / `source_episode_nos` / `deleted` / `operation_time` 外）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `prompt` | string | **可选。** 资产维度的**主提示词**，供生图等流程使用；未保存过则无此键 |
| `candidate_image_urls` | array\<string> | 该资产下各候选**原图**的可 GET 相对 URL 列表（`/drama/.../image/original` + signed_url）；无候选图为 `[]` |

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
