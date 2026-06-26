# Task: <任务名称>
## Status: <start / working / end>
## TaskID: <task-id>

[start done]
[working done] <步骤1>
[working] <步骤2>        ← 崩溃恢复从此行开始
[end]

---
规则：
1. 每次状态切换时全量覆盖 task.md
2. [working] 行描述 = 对应步骤文件名（去掉非法字符）
3. 恢复时：扫到第一个 [working] 且无对应 [working done]，从那里继续
