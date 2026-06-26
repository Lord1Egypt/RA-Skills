> **说明**：本文为《drama-ai-studio》技能中单个 HTTP 接口的完整说明。

### 7.5 POST /openapi/drama/{play_id}/storyboard/{episode_no}/shots/{shot_id}/optimize-prompt

生成或优化分镜视频合成的提示词（专门针对SD2.0智能参考视频生成模式）。

**路径参数（Path）：**

| 参数         | 必填 | 类型   | 说明    |
|--------------|------|--------|---------|
| `play_id`    | 是   | int    | 剧目 ID |
| `episode_no` | 是   | int    | 集号    |
| `shot_id`    | 是   | string | 镜头 ID |

**请求体（JSON）：** 体本身可为空对象 `{}`；下列字段均为可选，但需满足文末**上下文约束**（否则返回 400）。

| 字段                       | 必填 | 类型                  | 说明 |
|----------------------------|------|-----------------------|------|
| `user_requirement`         | 否   | string                | 用户对优化结果的要求；不传则仅按其余上下文与当前提示词优化 |
| `original_script`          | 否   | string                | 原始剧本文本片段；不传则使用镜头自身 `original_script` |
| `description`              | 否   | string                | 镜头描述；不传则使用镜头自身 `description` |
| `dialogues`                | 否   | array\<object>        | 台词列表；不传则使用镜头自身 `dialogues` |
| `duration_sec`             | 否   | number\|string\|null  | 时长；不传则使用镜头自身 `duration_sec`（字符串会尝试解析为数字，失败则视为无时长） |
| `reference_explanations`   | 否   | array\<object>        | 参考图解释列表；用于在无 `reference_explanations_text` 时拼接参考说明文本 |
| `reference_explanations_text` | 否 | string             | 参考图解释汇总文本；**优先于**由 `reference_explanations` 拼接的结果；二者均为空时，后端按镜头已绑定资产生成与前端一致的默认「【@图N】…」多行说明（仍无资产则为空） |
| `current_prompt`           | 否   | string                | 当前提示词；不传则按 `prompt_mode` 从镜头读取对应字段（见下） |
| `prompt_fixed_prefix`      | 否   | string                | 固定前缀；非空时拼在模型生成结果之前（中间空一行）再返回/回写 |
| `prompt_mode`              | 是   | string                | 要求必填，且设置为`reference` |
| `save`                     | 否   | bool\|int\|string     | 是否回写到镜头；**默认 true**（接口层对多种形态做布尔解析） |
| `async_task`               | 否   | bool\|int\|string     | 为真时走 AI 任务队列，HTTP 立即返回 `taskId` 等；**默认 false**（同步返回 `prompt`）。解析规则：`true` / 非 0 数字 / 字符串 `1`、`true`、`yes`、`on`（大小写不敏感）为真；`false`、`null`、缺省、空串、`0` 为假（与 `save` 的字符串宽松解析不同） |

`reference_explanations[]` 每项常见字段（按后端拼接逻辑读取；**整项对象及下属字段均非必填**）：

| 字段             | 必填 | 类型 | 说明 |
|------------------|------|------|------|
| `image_index`     | 否   | int  | 图片序号（用于生成“图N”描述） |
| `asset_type_label`| 否   | string | 资产类型中文标签（如“角色/场景/道具”） |
| `asset_name`      | 否   | string | 资产名称 |
| `explain_text`    | 否   | string | 已写好的解释文本（若存在则优先使用） |

**请求体示例（`prompt_mode` 为 `reference`）：** 以下表示「参考图视频」模式：未传 `current_prompt` 时用镜头上的 `prompt` 作为优化起点；其余上下文字段不传则仍从镜头自带数据补齐。

```json
{
  "prompt_mode": "reference",
  "user_requirement": "加强镜头运动感，保留与参考图的角色对应关系",
  "save": true,
  "async_task": false
}
```

**上下文约束：** 若 `current_prompt` 为空，且按 `prompt_mode` 从镜头解析出的当前提示词（`reference` 用 `prompt`，否则用 `prompt_head_tail`）也为空，且以下也全部为空——`original_script`、`description`、台词上下文、`reference_explanations_text`（及由 `reference_explanations` 或镜头资产默认生成的参考说明）——则接口返回错误，提示缺少可用于生成的上下文。

**成功响应结构（同步，`async_task` 未开启）：**

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "prompt": "优化后的提示词文本",
    "saved": true
  }
}
```

**成功响应结构（异步，`async_task` 为真）：** `data` 含任务信息，生成和优化结果在任务完成后通过任务详情/前端轮询获取。

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "taskId": "任务 ID",
    "queuePosition": 0,
    "message": "任务已提交，后台运行中，可到 AI 任务列表查看"
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
