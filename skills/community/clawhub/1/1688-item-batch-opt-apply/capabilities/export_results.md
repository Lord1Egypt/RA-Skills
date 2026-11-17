# export_results — Excel 产物导出

## 功能说明

把任务台账导出为 Excel 产物文件（openpyxl 可用时 .xlsx，缺失时自动 pip 安装
openpyxl 兜底，仍失败降级 .csv），并把成功任务的本地产物图（按
`task_id_商品标题` 重命名归入 images/）与表格一起压成 zip 包，落盘到
`1688-item-batch-opt-apply/批量任务结果_<批次ID>.xlsx` 与 `...zip`；台账带
`store_name`（parse_tasks `--store_name` 传入）时为
`批量任务结果_<店铺>_<批次ID>.xlsx`（目录名与技能名
一致，与其他技能产物隔离）。**非交互式**：导出后由
主 Agent 用宿主 `present_files` 把文件作为产物展示/下载（钉钉文档「Excel（Skill）、
文件下载支持，非交互式，在产物中展示」口径）。

## CLI 调用

```bash
python3 "{baseDir}/cli.py" export_results
python3 "{baseDir}/cli.py" export_results --only_done
```

## 参数表

| 参数 | 必填 | 说明 |
|---|---|---|
| `--only_done` | 否 | 只导出已完成的任务（成功/失败/跳过/取消） |
| `--base_dir` | 否 | 台账根目录（默认当前工作目录） |

## 返回数据

```json
{"success": true, "markdown": "...", "data": {
  "file_path": "/abs/批量任务结果_B....xlsx", "file_format": "xlsx",
  "row_count": 3, "batch_id": "B...", "stats": {...},
  "package_path": "/abs/批量任务结果_B....zip", "package_file_count": 4}}
```

导出列：任务ID / 商品ID / 商品标题 / 优化项 / 要求 / 执行状态 / 执行结果 /
应用状态 / 应用回执 / 失败原因（状态值为中文）。`package_path` 仅在存在可入包的
本地产物图时返回（zip 内：表格在根、图片在 images/ 下）。

**防覆盖**：目标表格/zip 同名已存在（重复导出、历史批次撞名、多店铺多批次同会话
运行）时文件名自动加序号（`批量任务结果_<批次ID>_2.xlsx`、`_3`…），表格与 zip
共用同一变体名，不静默覆盖既有产物；多店铺同会话运行时优先靠
`--store_name` 店铺前缀从源头隔离文件名。

## 异常处理

- 台账为空 / 没有可导出任务：`success:false`，先 `parse_tasks` 并落账结果。
- 写文件失败：如实报错，检查磁盘/目录权限后重试。

## 展示规范

- 成功后按 `data.file_path`（表格）与 `data.package_path`（zip 包，存在时）调用宿主
  `present_files` 展示产物；`markdown` 已含引导语，不要把文件路径再贴一遍长链接给用户。
