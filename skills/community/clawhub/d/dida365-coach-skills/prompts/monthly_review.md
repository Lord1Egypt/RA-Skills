# 月复盘流程

## 触发条件

- 用户说“复盘这个月”“做月复盘”
- 月末或月初的管理回顾

## 流程

### Step 1: 先刷新本地生产力摘要

如果本地生产力系统已初始化，先准备：

- `dashboard.md`
- `commitments/promises.md`
- `commitments/delegated.md`
- `focus/sessions.md`
- `focus/distractions.md`
- `reviews/weekly.md`

再结合滴答近期任务情况，避免只凭感觉做复盘。

### Step 2: 拉取本月执行层信号

优先获取：

- 本月未完成任务：`list_undone_tasks_by_date`
- 本月已完成任务：`list_completed_tasks_by_date`

必要时追加：

- `filter_tasks`

如果完成状态和历史完成记录冲突，优先保守处理，不要把历史完成误当本月已完成。

### Step 3: 识别月度瓶颈

重点看这几类问题：

- 承诺是否持续堆积
- 高优先级事项是否总在等待或延后
- 专注被什么反复打断
- 例行流程是否失效
- 目标、项目、任务是否脱节

先给一段自然语言总结本月走势，再补短结构。

### Step 4: 输出月复盘

建议结构：

```text
📈 本月走势
🏆 有效动作
⚠️ 主要阻塞
🧭 下月重点
```

如果信息不完整，不必硬凑完整报告；优先输出最有判断力的 2-4 条结论。

### Step 5: 更新本地文件

如果用户允许写入本地系统：

- 更新 `reviews/monthly.md`
- 必要时同步更新 `dashboard.md`
- 如果承诺和等待项有明显变化，再刷新 `commitments/`

写入前先说明将更新哪些模块。
