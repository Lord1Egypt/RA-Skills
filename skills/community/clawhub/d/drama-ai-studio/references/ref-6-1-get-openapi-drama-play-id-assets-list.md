> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.1 GET /openapi/drama/{play_id}/assets/list

按类型、集数、名称过滤资产列表，并附带封面与是否有终稿图标记。

**路径参数（Path）：**

| 参数      | 必填 | 类型 | 说明    |
|-----------|------|------|---------|
| `play_id` | 是   | int  | 剧目 ID |

**查询参数（Query）：**

| 参数              | 必填 | 类型   | 说明                                                                 |
|-------------------|------|--------|----------------------------------------------------------------------|
| `type`            | 否   | int    | 资产类型：1=场景, 2=角色, 3=道具, 4=平面, 5=其他；不传返回所有类型   |
| `include_deleted` | 否   | string | 是否包含已软删除资产，默认 `'false'`；传 `'true'` 时包含             |
| `episode_no`      | 否   | int    | 仅返回在该集分镜中出现过的资产                                       |
| `name`            | 否   | string | 名称关键词（不区分大小写），匹配 `name` 包含该子串的资产            |

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": [
    {
      "id": "1",
      "type": 2,
      "name": "角色A",
      "description": "可选描述",
      "source_episode_nos": [1, 2],
      "deleted": false,
      "operation_time": "2025-01-01T12:00:00",
      "cover_url": "https://示例域/openapi/drama/1/assets/2/1/general/candidates/10/image/original?su_scene=drama_candidate_image&su_exp=1730000000&su_sig=<HMAC_SHA256_HEX>",
      "has_final_image": true
    }
  ]
}
```

字段说明（单个资产）：

| 字段                | 类型         | 说明                                                         |
|---------------------|--------------|--------------------------------------------------------------|
| `id`                | string       | 资产 ID（剧目内唯一）                                       |
| `type`              | int          | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他             |
| `name`              | string       | 资产名称                                                     |
| `description`       | string\|null | 资产描述，可为空                                             |
| `source_episode_nos`| array\<int>  | 可选，资产首次出现的集号列表                                 |
| `deleted`           | bool         | 是否已软删除                                                 |
| `operation_time`    | string       | 最后操作时间（字符串时间戳）                                 |
| `cover_url`         | string\|null | 封面图可 GET 的相对 URL：`/drama/{play_id}/assets/{type}/{id}/general/candidates/{cand_id}/image/original` + 短时 signed_url；无终稿封面时为 `null` |
| `has_final_image`   | bool         | 是否已有终稿图                                               |

**错误响应示例（HTTP 500）：**

```json
{
  "code": -1,
  "msg": "error",
  "data": {
    "error": "具体错误信息"
  }
}
```
