> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.7 GET /openapi/drama/{play_id}/assets/{asset_type}/{asset_id}/general/candidates/final-candidates

获取该资产下已选为**终稿**的候选图列表，顺序由终稿选中时间等规则决定。

**路径参数（Path）：**

| 参数          | 必填 | 类型   | 说明                                                         |
|---------------|------|--------|--------------------------------------------------------------|
| `play_id`     | 是   | int    | 剧目 ID                                                      |
| `asset_type`  | 是   | int    | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他             |
| `asset_id`    | 是   | string | 资产 ID                                                      |

**请求体 / 查询参数：** 无

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "version": 2,
    "items": [
      {
        "candidate_id": "10",
        "image": "10_xxx.png",
        "path": "2/1_角色A/general/candidates/10_xxx.png",
        "has_unresolved_comments": false,
        "url": "/drama/1/assets/2/1/general/candidates/10/image/original?su_scene=drama_candidate_image&su_exp=1730000000&su_sig=<HMAC_SHA256_HEX>"
      }
    ]
  }
}
```

| 字段（`data`） | 类型          | 说明 |
|----------------|---------------|------|
| `version`      | int           | 终稿配置版本（当前常为 `2`） |
| `items`        | array\<object>| 终稿项列表，有序；无终稿时为 `[]` |

`items[]` 单项字段：

| 字段                        | 类型   | 说明 |
|-----------------------------|--------|------|
| `candidate_id`              | string | 候选图 ID |
| `image`                     | string | 候选图文件名 |
| `path`                      | string | 相对剧目根的资源路径 |
| `has_unresolved_comments`   | bool   | 该候选是否存在未解决评论 |
| `url`                       | string | 原图短时签名 URL（`/drama/.../image/original` + signed_url），可直接 GET |

**错误响应示例：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
