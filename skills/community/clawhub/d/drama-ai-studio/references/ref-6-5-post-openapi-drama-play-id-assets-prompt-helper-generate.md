> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 6.5 POST /openapi/drama/{play_id}/assets/prompt-helper/generate

调用大模型 **辅助生成资产图像提示词**：根据资产类型、模式与描述等，经模板渲染后请求文本模型，返回一段可直接用于图像生成的中文提示词。

**说明：** 响应中的 `generated_prompt` **不会**自动写入资产；若需保存，请调用 **§6.4** `PUT /openapi/drama/{play_id}/assets/{asset_id}`，将内容写入资产的 `prompt` 字段并保存。

**路径参数（Path）：**

| 参数       | 必填 | 类型 | 说明    |
|------------|------|------|---------|
| `play_id`  | 是   | int  | 剧目 ID |

**请求体（JSON）：**

```json
{
  "asset_type": 2,
  "mode_key": "face_closeup",
  "template": "可选：自定义模板文本（可含占位符，由服务端渲染）",
  "initial_description": "资产名称、设定或剧本相关描述，供模板填充",
  "personalized_requirements": "可选：额外画面/风格/构图等约束"
}
```

| 字段                         | 必填 | 类型   | 说明                                                                 |
|------------------------------|------|--------|----------------------------------------------------------------------|
| `asset_type`                 | 是   | int    | 资产类型：1 场景、2 角色、3 道具、4 平面、5 其他                     |
| `mode_key`                   | 是   | string | 提示词模式键（须非空），与剧目侧提示词模板配置一致（如某类资产的视角/模式） |
| `template`                   | 否   | string | 模板全文；若省略或仅为空白，则由服务端根据 `play_id`、`asset_type`、`mode_key` 解析默认模板 |
| `initial_description`        | 是   | string | 资产初始描述（须非空），参与模板占位符替换并作为生成依据                 |
| `personalized_requirements`  | 否   | string | 个性化补充要求，默认空字符串                                         |

`mode_key` 可选值（按 `asset_type`）：

| `asset_type` | 类型 | `mode_key` 可选值 |
|--------------|------|-------------------|
| `1` | 场景 | `panorama`、`top_view`、`specific_angle`、`nine_grid`、`sphere_360` |
| `2` | 角色 | `face_closeup`、`full_body`、`three_view`、`tone` |
| `3` | 道具 | `front_view`、`three_view`、`prop_character_ref` |
| `4` | 平面 | `default` |
| `5` | 其他 | `default` |

**成功响应结构：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "generated_prompt": "由模型输出的、可直接用于图像生成的中文提示词全文…"
  }
}
```

| 字段                | 类型   | 说明                           |
|---------------------|--------|--------------------------------|
| `generated_prompt`  | string | 模型生成的一条完整图像提示词   |

**错误响应示例：**

- 参数不合法（如缺少 `asset_type`、`initial_description` 为空、`mode_key` 为空等）：HTTP **400**。
- 大模型调用失败或计费相关异常：HTTP **500**。

```json
{
  "code": -1,
  "msg": "错误描述",
  "data": {
    "error": "具体错误信息"
  }
}
```
