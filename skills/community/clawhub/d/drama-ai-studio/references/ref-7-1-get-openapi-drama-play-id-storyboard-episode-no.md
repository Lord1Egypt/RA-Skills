> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 7.1 GET /openapi/drama/{play_id}/storyboard/{episode_no}

获取某集分镜；尚未分析时 `shots` 为空。

**路径参数（Path）：**

| 参数         | 必填 | 类型 | 说明    |
|--------------|------|------|---------|
| `play_id`    | 是   | int  | 剧目 ID |
| `episode_no` | 是   | int  | 集号    |

**请求体：** 无

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "play_id": "1",
    "episode_no": 1,
    "analyzed_at": null,
    "shots": []
  }
}
```

当该集已分析时，`data.shots` 为镜头数组；单个镜头对象字段（来自后端写入/编辑）：

| 字段            | 类型                | 说明 |
|-----------------|---------------------|------|
| `id`            | string              | 镜头 ID（形如 `s1`、`s2`） |
| `order`         | int                 | 镜头序号 |
| `description`   | string              | 镜头描述 |
| `original_script` | string\|null      | 对应剧本原文片段（可为空） |
| `scene_ids`     | array\<string>      | 场景资产 ID 列表（可为空） |
| `character_ids` | array\<string>      | 角色资产 ID 列表 |
| `prop_ids`      | array\<string>      | 道具资产 ID 列表 |
| `surface_ids`   | array\<string>      | 平面资产 ID 列表 |
| `other_ids`     | array\<string>      | 其他资产 ID 列表 |
| `dialogues`     | array\<object>      | 台词列表（见下） |
| `prompt`        | string\|null        | 提示词（可为空） |
| `duration_sec`  | number\|null        | 时长（可为空） |
| `shot_type`     | string\|null        | 镜头类型/景别（可为空） |

`dialogues[]` 每项字段：

| 字段            | 类型         | 说明 |
|-----------------|--------------|------|
| `speaker_id`    | string\|null | 说话人角色资产 ID（可能为空） |
| `speaker_name`  | string       | 说话人名称 |
| `content`       | string       | 台词内容 |
| `delivery`      | string       | 语气/方式 |
| `is_inner_voice`| bool         | 是否内心独白 |

**错误响应结构：**

```json
{
  "code": -1,
  "msg": "错误描述"
}
```
