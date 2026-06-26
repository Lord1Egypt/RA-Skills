# Pattern 3.3: 三门控记忆合并（3-Gate Consolidation）

## 问题

跨多个 session 积累了大量碎片化的 handoff 文档和记忆文件，重复信息多、互相矛盾。

## 原理

定期合并记忆，但用三个门控避免不必要的合并操作。来自 Claude Code 内部的 AutoDream——一个 "sleep consolidation" 机制，在 session 之间自动整理积累的知识。

## 三个门控

1. **Time Gate**：距上次合并 >= 24 小时。避免频繁合并。
2. **Session Gate**：有 >= 5 个新 session 积累。确保有足够的新内容值得合并。
3. **Lock Gate**：获取文件锁确认无其他进程正在合并。10 次重试，5-100ms 指数退避。

三个门控按计算成本从低到高排列。时间检查最便宜（读一个时间戳），session 计数次之（数文件数），加锁最贵（文件系统操作）。任一门控失败，跳过本次合并。

## 合并操作

通过门控后，遍历所有 `sessions/*/handoffs/` 目录：
1. 按时间排序所有 handoff 文档
2. 提取 Decided/Rejected 段落
3. 合并去重，解决冲突（后来的决策覆盖早期的）
4. 写入精简的经验总结文件

## Claude Code 的 AutoDream 机制

AutoDream 在 session 之间运行，通过 `runForkedAgent` 生成一个独立 agent：
- 读取积累的 transcripts
- 编辑 memdir 中的 Markdown 文件来 consolidate learnings
- 通过 `TaskListV2` 提供实时状态更新

Memory taxonomy：
- `user`：个人偏好和习惯
- `feedback`：纠正和表扬
- `project`：架构、非显而易见的目标
- `reference`：外部文档和流程

安全措施包括 `sanitizePathKey`（拒绝 null bytes、URL 编码遍历、Unicode 规范化攻击）和 `realpathDeepestExisting`（解析 symlinks 防止逃逸）。
