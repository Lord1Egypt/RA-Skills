# parse_tasks — 批量任务解析

## 功能说明

把**主 Agent 已结构化**的批量任务解析为标准任务条目，写入台账
（`1688-item-batch-opt-apply/tasks.json`，目录名与技能名一致、与其他技能产物隔离），
并输出任务确认参数（当前主路径为 ask_user
表单勾选；升级路径为 `offer_select_card` route=`batch-task-confirm` 卡）。

**唯一入口**：主 Agent 从对话、上游交接或任意文件（Excel 指定 sheet/任意列语义/
多列素材融合、素材文件夹配对等）自行读取理解结构后，产出标准任务数组传入；
脚本只做校验与归一化，不解析任何文件、不做自然语言理解与列语义猜测。

两类任务：
- **商品任务**：`item_id`（纯数字）+ `op`，`input_images` 可选（作参考图）
- **素材任务**：无 `item_id`，必填 `input_images`（如「model 列模特图 × scene 列
  场景图融合，每行一个任务」；文件夹场景每图一个任务，可用 `source_file` 标注源文件）

## CLI 调用

```bash
# 商品任务
python3 "{baseDir}/cli.py" parse_tasks --tasks '[{"item_id":"1078187515442","op":"主图优化","requirements":"突出金属质感","item_title":"不锈钢保温杯"}]'
# 素材融合任务（主 Agent 读 Excel 后结构化，每行一个任务）
python3 "{baseDir}/cli.py" parse_tasks --tasks '[{"op":"多图合成","input_images":["https://.../model_01.jpg","https://.../scene_01.jpg"],"requirements":"把模特图与场景图融合生成新图","item_title":"红色连衣裙"}]'
# 素材文件夹（主 Agent 列目录后，每图一个任务并标注源文件）
python3 "{baseDir}/cli.py" parse_tasks --tasks '[{"op":"img_opt","input_images":["/abs/素材/a.jpg"],"source_file":"/abs/素材/a.jpg"}]'
```

## 参数表

| 参数 | 必填 | 说明 |
|---|---|---|
| `--tasks` | 是 | 主 Agent 已结构化的任务 JSON 数组；商品任务 `item_id` 纯数字 + `op`；素材任务必填 `input_images`（单值或数组），可选 `source_file` 标注源文件。`op` 支持中文标签或 op 键（见 SKILL.md 规则2 白名单，含「融合/合成/多图合成」→ multi_img_merge） |
| `--replace` | 否 | 清空台账重建；默认追加并对重复任务跳过。开新批次（replace 或旧台账不存在/损坏）时会先把现存台账归档为 `tasks_<店铺前缀>_<旧批次ID>.json`（无店铺名时 `tasks_<旧批次ID>.json`），旧批次记录不丢失 |
| `--store_name` | 否 | 当前操作店铺展示名（主 Agent 从宿主店铺上下文/选店结果取得，如 phoenix-pc 多店铺策略侧提供）。写入台账 `store_name` 字段，后续归档/导出产物文件名带店铺前缀，避免多店铺同会话运行时产物文件名重叠；不参与鉴权，未传时产物命名不带店铺前缀（与旧版兼容） |

## 返回数据

```json
{"success": true, "markdown": "...", "data": {
  "batch_id": "B...", "store_name": "<店铺展示名，未传时为空串>",
  "ledger_path": ".../1688-item-batch-opt-apply/tasks.json",
  "archived_ledger_path": "",
  "tasks": [...新任务条目...], "new_count": 2, "skip_duplicates": 0,
  "warnings": ["第3个任务缺少合法商品ID（纯数字）"],
  "confirm_card": {"route": "batch-task-confirm", "batchSize": 2, "tasks": [...]}
}}
```

## 异常处理

- 商品 ID 非纯数字且无输入图 / 优化项无法识别：该任务跳过并进 `warnings`，不阻断批次；
  `warnings` 必须向用户展示。全部任务非法时 `success:false` 整批拒绝并给出修正指引。
- `--source excel/folder` 已移除：任何文件/文件夹输入都由主 Agent 读取结构化后传
  `--tasks`；不要把文件路径直接传给脚本。

## 展示规范

- 成功时输出 `markdown`（含解析计数与 warnings），随后按 SKILL.md 规则3 进入任务
  确认：**当前主路径**是 `ask_user`（mode=form）多选题分页确认，`data.confirm_card`
  暂存备用、不弹卡；**升级路径**（batch-task-confirm 组件上线放量后）才把
  `data.confirm_card` 原样弹 `offer_select_card`（弹卡硬约束见
  [references/interaction-specs.md](../references/interaction-specs.md)）。
