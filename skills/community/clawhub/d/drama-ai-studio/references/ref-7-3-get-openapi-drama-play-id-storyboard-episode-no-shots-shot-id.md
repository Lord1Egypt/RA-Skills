> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 7.3 GET /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}

获取单个镜头详情，包含 `prompt`、`description`、`original_script` / `original_content`。

**路径参数（Path）：**

| 参数         | 必填 | 类型   | 说明    |
|--------------|------|--------|---------|
| `play_id`    | 是   | int    | 剧目 ID |
| `episode_no` | 是   | int    | 集号    |
| `shot_id`    | 是   | string | 镜头 ID |

**请求体：** 无

**成功响应结构：**

在基础镜头字段（见 7.1 的 `shots[]`）之上，额外返回：

| 字段                    | 类型            | 说明 |
|-------------------------|-----------------|------|
| `original_content`      | string          | 由镜头描述 + 剧本原文 + 关联资产名称拼接的展示文本 |
| `reference_image_paths` | array\<string>  | 参考图相对路径列表（最多 4 张，用于初始化参考图模式） |
| `reference_image_names` | array\<string>  | 与 `reference_image_paths` 对应的资产名称列表 |

响应示例（省略部分字段）：

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "s1",
    "order": 1,
    "description": "镜头描述",
    "original_script": "剧本原文片段",
    "scene_ids": ["1"],
    "character_ids": ["2"],
    "prop_ids": [],
    "surface_ids": [],
    "other_ids": [],
    "dialogues": [],
    "prompt": null,
    "duration_sec": null,
    "shot_type": null,
    "original_content": "用于展示的拼接文本",
    "reference_image_paths": ["characters/2_角色A/general/candidates/10/图.png"],
    "reference_image_names": ["角色A"]
  }
}
```

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
