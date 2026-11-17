# build_apply_card — 批量应用到商品卡

## 功能说明

把主 Agent 逐任务从执行技能拿到的**单条目应用参数**（如 1688-item-image-agent 的
`prepare_image_apply` 返回 `data.card_params`）按 item_id 粒度合并成批量应用卡
（升级路径，`offer_select_card` route=`batch-apply`）。每项默认不应用
（`defaultApplied:false`），用户在卡片中全选/反选/逐项调整后一次确认；**写入商品由
组件完成，本 CLI 只组装参数并置 requested 状态**（一卡多应用确认卡由端侧组件实现，
宿主只做管道）。

**调用时机**：batch-apply 组件上线放量前本命令仅暂存备用——**当前主路径**是
逐任务执行执行技能自己的单条目应用卡（见 SKILL.md 规则6）。

## CLI 调用

```bash
python3 "{baseDir}/cli.py" build_apply_card --items '[
  {"task_id": "T001", "card_params": {"offerId": "1078187515442", "imageType": "main",
   "updatedImages": ["https://cbu01.alicdn.com/img/ibank/a.jpg"],
   "currentImages": ["..."], "originalCount": 5, "isWhiteList": false,
   "productInfo": {...}, "loginId": "...", "store_ref": "..."}},
  {"task_id": "T003", "card_params": {"...": "标题优化执行技能返回的应用参数"}}
]'
```

## 参数表

| 参数 | 必填 | 说明 |
|---|---|---|
| `--items` | 是 | JSON 数组；每元素含 `task_id`（或 `item_id`+`op` 联合定位）与 `card_params`（执行技能返回的单条目应用参数**原样 JSON**，字段契约归执行技能所有） |
| `--base_dir` | 否 | 台账根目录（默认当前工作目录） |

## 返回数据

```json
{"success": true, "markdown": "...", "data": {
  "card": {
    "route": "batch-apply", "batchId": "B...",
    "items": [{"taskId": "T001", "itemId": "...", "itemTitle": "...",
                "op": "main_img_opt", "opLabel": "主图优化", "applyParams": {...}}],
    "defaultApplied": false
  },
  "updated_count": 2, "task_ids": ["T001", "T003"], "stats": {...}}}
```

## 状态与回执

- 任务须有商品 ID、执行成功、apply_status 为 pending/failed/unknown；重复任务拒绝。
- CPV 查询、校验与必要确认由主 Agent 在当前上下文完成；本命令不读取或保存 CPV 记录。
- 本命令在查询与必要澄清完成后调用，不是第一次「应用」按钮的入口，也不直接写入。

- 命中的任务会被置 `apply_status=requested`（表示已提交应用、回执未到）。
- 卡片回执（应用成功/失败明细，含用户逐项取消的）到达后，主 Agent 必须逐任务
  调 `save_result --task_id ... --apply_status applied/failed/cancelled/unknown
  --apply_detail ...` 落账。

## 异常处理

- `items` 非法 / 元素缺 `card_params`：`success:false`，按提示修正 JSON。
- 任务定位失败（task_id 不存在、`item_id+op` 多命中）：`success:false`，改用
  `task_id` 定位。
- 任务 `status != success`（如 parsed/failed）：**拒绝进卡**，防呆——先完成执行
  并 `save_result --status success` 落账。
- 卡片组件未上线（当前状态）：不调用本命令，逐任务执行执行技能自己的单条目
  应用卡，见 [references/interaction-specs.md](../references/interaction-specs.md)。

## 展示规范

- **当前主路径（组件未上线）**：不调用本命令；逐任务执行执行技能自己的单条目
  应用卡（如 image-agent 的 `image-apply` 单卡），回执逐任务落账 apply_status。
- **升级路径（组件上线放量后）**：成功时输出 `markdown`，把 `data.card` 原样作为
  `offer_select_card --json` 弹出应用确认卡；**弹卡是本轮最后一个工具调用**，
  弹卡后停轮等回执。
- 不要向用户复述 `applyParams` 内部字段；应用结果以卡片回执与落账后的
  `build_result_card` 进度为准。
