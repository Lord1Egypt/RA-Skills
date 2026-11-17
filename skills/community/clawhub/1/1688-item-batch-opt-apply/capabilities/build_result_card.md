# build_result_card — 执行结果展示卡

## 功能说明

汇总台账生成结果展示参数（升级路径为 `offer_select_card` route=`batch-result-view`
卡片；**当前主路径**用其 `progress/tasks` 数据渲染正文 Markdown 表格）：
批次进度、逐任务执行结果、可应用任务清单（钉钉文档「执行结果展示」章节：
进度展示 + 结果明细 + 应用到商品入口）。卡片参数只引用台账字段，**不内嵌图片
URL**——组件按 item_id 自行取图渲染，避免参数膨胀。

## CLI 调用

```bash
python3 "{baseDir}/cli.py" build_result_card
python3 "{baseDir}/cli.py" build_result_card --item_ids '["1078187515442"]'
```

## 参数表

| 参数 | 必填 | 说明 |
|---|---|---|
| `--item_ids` | 否 | JSON 数组；只展示指定商品的任务（用于用户只关心部分商品时） |
| `--base_dir` | 否 | 台账根目录（默认当前工作目录） |

## 返回数据

```json
{"success": true, "markdown": "...", "data": {
  "card": {
    "route": "batch-result-view", "batchId": "B...",
    "progress": {"total": 5, "done": 3, "success": 2, "failed": 1, "skipped": 0},
    "tasks": [{"taskId": "T001", "itemId": "...", "itemTitle": "...", "op": "main_img_opt",
                "opLabel": "主图优化", "status": "success", "resultSummary": "...",
                "applyStatus": "pending", "applyDetail": "", "error": ""}],
    "appliableTaskIds": ["T001"]
  },
  "batch_id": "B...", "appliable_count": 1, "stats": {...}}}
```

`appliableTaskIds` 的口径：`status=success` 且有商品 ID 且 `apply_status` 为
`pending/failed/unknown`（failed/unknown 允许重试应用）。

## 异常处理

- 台账为空 / `--item_ids` 无命中：`success:false`，先 `parse_tasks` 或修正商品 ID。
- 组件未上线（当前状态）：走主路径 Markdown 表格 + `export_results` Excel 产物，
  见 [references/interaction-specs.md](../references/interaction-specs.md)。

## 展示规范

- **当前主路径（组件未上线）**：成功时输出 `markdown`（进度摘要），并在助手正文用
  Markdown 表格展示进度与逐任务结果；`data.card` 落账备用，**不弹卡**。
- **升级路径（组件上线放量后）**：把 `data.card` 原样作为 `offer_select_card --json`
  弹出结果展示卡；**弹卡是本轮最后一个工具调用**，弹卡后停轮等回执。执行过程中
  可多次弹出（每若干任务或阶段结束时刷新进度），不要求等全部完成。
