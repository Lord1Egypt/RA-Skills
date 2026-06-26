# 周复盘流程

## 触发条件

- 用户说“复盘这周”
- 每周固定提醒触发

## 流程

### Step 1: 获取本周任务

按天收集本周任务，确保能按日期分组。

如果本地生产力系统已初始化，先准备并允许刷新这些文件：

- `dashboard.md`
- `commitments/promises.md`
- `commitments/delegated.md`
- `focus/sessions.md`
- `focus/distractions.md`
- `planning/weekly.md`
- `reviews/weekly.md`

推荐工具组合：

- 本周未完成：`list_undone_tasks_by_date`
- 本周已完成：`list_completed_tasks_by_date`

如果还要按优先级、标签、类型细分，可追加 `filter_tasks`。

### Step 2: 计算趋势

调用：

- `analyze_weekly_trends()`
- `identify_missed_patterns()`
- `suggest_automation()`

在分析前先确认完成状态来自当前任务实例，而不是历史完成记录。

### Step 3: 输出周报告

先给一段自然语言总结本周走势，再按需要补短结构。

建议结构：

```text
📈 本周统计
• 平均完成率：XX%
• 趋势：上升 / 下降 / 平稳

🏆 本周亮点
🔍 改进点
🤖 自动化机会
📋 下周建议
```

### Step 4: 引导下周策略

围绕这三个问题推进：

1. 哪些没完成的任务还值得继续？
2. 最高效时段下周要不要多放重要任务？
3. 哪些重复动作适合变成循环任务或提醒？

不要只做回顾；要把周复盘自然衔接到下周规划。
周复盘不是只看任务完成率，还要结合承诺、等待项和干扰模式。

如果状态字段与完成时间字段冲突，优先保守处理为“待人工确认”，不要直接算作已完成。

如果本周信息不多，不必硬套完整报告模板，优先输出最有价值的 2-3 个判断。
