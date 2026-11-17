# save_result — 执行/应用结果落账

## 功能说明

把单条任务的执行或应用结果合并进台账。**主 Agent 每处理一个任务都必须调用一次**
（执行开始、执行成功/失败、应用回执到达、用户跳过/取消）。未落账的结果不会出现在
结果展示卡与 Excel 导出中。

批量场景多条落账可**合并进单条 bash 串联执行**（`;` 分隔，每任务仍是独立一次 CLI
调用），以减少交互轮次；**禁止**并行发起多条写台账的命令（台账是读改写文件，
并行写会互相覆盖）——主循环的分批调度见 SKILL.md 规则4 与 task-contract §4。

## CLI 调用

```bash
# 任务开始执行
python3 "{baseDir}/cli.py" save_result --task_id T001 --status confirmed
python3 "{baseDir}/cli.py" save_result --task_id T001 --status running
# 执行成功（result_images 为完整覆盖式列表）
python3 "{baseDir}/cli.py" save_result --task_id T001 --status success --result_summary "主图已优化完成" --result_images "https://cbu01.alicdn.com/img/ibank/a.jpg"
# 执行失败
python3 "{baseDir}/cli.py" save_result --task_id T002 --status failed --error "生图服务超时"
# 应用回执（卡片回传后）
python3 "{baseDir}/cli.py" save_result --task_id T001 --apply_status applied --apply_detail "已应用为主图"
python3 "{baseDir}/cli.py" save_result --task_id T002 --apply_status unknown --apply_detail "已提交，稍后请到商家后台核对"
```

## 参数表

| 参数 | 必填 | 说明 |
|---|---|---|
| `--task_id` | 二选一 | 任务 ID（T001…，优先）；或 `--item_id` + `--op` 联合唯一定位 |
| `--status` | 否 | `confirmed/skipped/running/success/failed/cancelled` |
| `--result_summary` | 否 | 执行结果一句话摘要 |
| `--result_images` | 否 | 产物图列表（https:// 或 media-output 路径）；传入即整表替换 |
| `--apply_status` | 否 | `requested/applied/failed/unknown/cancelled` |
| `--apply_detail` | 否 | 应用回执自然语言摘要 |
| `--error` | 否 | 失败原因（自然语言） |

至少传一个更新字段；未传字段保持台账原值。

## 返回数据

`data` 含 `task_id/item_id/op/status/apply_status/batch_stats`（批次进度统计）。

## 异常处理

- 无台账 / task_id 不存在 / (item_id, op) 多命中：`success:false`，按提示改用
  `--task_id` 或先运行 `parse_tasks`。
- 非法状态值：参数错误，修正后重试。

## 展示规范

- 输出 `markdown`（落账确认 + 批次进度）；不需要向用户展开内部字段。
