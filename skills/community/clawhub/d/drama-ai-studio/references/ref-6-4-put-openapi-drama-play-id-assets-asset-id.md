> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.4 PUT /openapi/drama/{play_id}/assets/{asset_id}

更新已有资产的名称、类型、描述、来源集数、**提示词**等。请求体 **至少提供一个**可更新字段；仅允许修改**未软删除**的资产。

**路径参数（Path）：**

| 参数       | 必填 | 类型   | 说明     |
|------------|------|--------|----------|
| `play_id`  | 是   | int    | 剧目 ID  |
| `asset_id` | 是   | string | 资产 ID  |

**请求体（JSON）：** 以下字段均为可选，但 **不能全部省略**（至少传一项）。

```json
{
  "name": "角色A（改名）",
  "type": 2,
  "description": "新的描述；传空字符串可清空",
  "source_episode_nos": [1, 3],
  "prompt": "更新后的资产主提示词；传空字符串可清空",
  "prompt_by_mode": {
    "face_closeup": "特写提示词",
    "full_body": "全身提示词"
  }
}
```

**字段说明**：

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `name` | 否 | string | 资产名称 |
| `type` | 否 | int | 资产类型（1场景,2角色,3道具,4平面,5其他） |
| `description` | 否 | string | 资产描述，传空字符串可清空 |
| `source_episode_nos` | 否 | array\<int> | 来源集数数组 |
| `prompt` | 否 | string | 资产主提示词，传空字符串可清空 |
| `prompt_by_mode` | 否 | object | 按 `prompt_mode_key` 保存的提示词映射；可传空对象清空 |

> 说明：以上字段均为可选，但不能全部省略（至少传一项）。

**`prompt` 与 `prompt_by_mode` 的关系：**

- `prompt` 是资产级单值提示词，不区分模式。
- `prompt_by_mode` 是按模式保存的提示词映射（key 为模式，value 为该模式提示词文本）。
- 两者在后端并列、独立存储：更新其中一个不会自动同步改写另一个。
- 建议多模式场景优先维护 `prompt_by_mode`；`prompt` 可作为统一展示或兜底文案使用。

**`prompt_by_mode` 在不同资产类型下的推荐取值（mode_key）：**

- `type=1`（场景）：`panorama`、`top_view`、`specific_angle`、`nine_grid`、`sphere_360`
- `type=2`（角色）：`face_closeup`、`full_body`、`three_view`、`tone`
- `type=3`（道具）：`front_view`、`three_view`、`prop_character_ref`
- `type=4`（平面）：`default`
- `type=5`（其他）：`default`

> 兼容性说明：服务端会接受并保存任意非空字符串 key；以上为当前内置模板与模式配置中的推荐值。

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "id": "1",
    "type": 2,
    "name": "角色A（改名）",
    "description": "新的描述",
    "prompt": "…",
    "deleted": false,
    "operation_time": "2025-01-01T12:00:00"
  }
}
```

**错误响应示例：** 参数缺失（未提供任何可更新字段）、资产不存在或已删除、类型非法等，返回 `code=-1` 及 `msg` / `data.error` 说明（HTTP 状态码以网关为准，常见为 400/500）。
