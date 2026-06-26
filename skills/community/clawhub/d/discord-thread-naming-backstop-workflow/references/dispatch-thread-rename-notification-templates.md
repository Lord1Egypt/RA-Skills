# dispatch 线程命名兜底：通知模板与输出约束

适用于 Discord `dispatch-thread-rename-backstop` 任务在**最终失败**或**先失败后成功**时的标准通知输出。

## 发送目标

- 通知频道 ID：`1478996389727043584`
- 仅在以下场景发送：
  - `P2`：最终失败
  - `RESOLVED`：同一 `opId` 内先失败，后经重试或一致性检查判定成功

## P2 模板

仅当以下任一情况发生时发送：
- `thread-list` 连续两次失败，此时必须使用 `threadId=list`
- 单个线程经历 `channel-edit` 重试与 `channel-info` 一致性检查后，仍未满足命名规范

```text
━━━━━━━━━━━━━━
🚨 任务告警 · dispatch-thread-rename-backstop
等级：P2
状态：🔴 失败
日期：YYYY-MM-DD (Asia/Shanghai)

对象：threadId=<id> opId=<opId>
原因：<最终失败摘要，不超过60字>
影响：线程命名规范可能未及时生效
动作：请人工介入排查并重试

追踪：#cron #dispatch #naming #incident
━━━━━━━━━━━━━━
```

## RESOLVED 模板

仅当**同一 `opId` 中曾出现失败记录**，但最终又成功时发送。若全程无失败，则即使成功也不发送任何消息。

```text
━━━━━━━━━━━━━━
✅ 任务回补 · dispatch-thread-rename-backstop
状态：🟢 RESOLVED
日期：YYYY-MM-DD (Asia/Shanghai)

对象：threadId=<id> opId=<opId>
说明：重命名过程中出现瞬时失败，已自动恢复并满足命名规范
结果：<最终名称>

追踪：#cron #dispatch #naming #resolved
━━━━━━━━━━━━━━
```

## 输出约束

### 1. 单线程单次运行最多 1 条通知
同一线程在一次运行内，最终只允许输出：
- `0` 条消息；或
- `1` 条消息

禁止重复刷屏，尤其不能同时发多条 P2 或重复发 RESOLVED。

### 2. threadId 占位规则
- 禁止使用：`0`、`n/a` 等伪占位值
- 仅在**线程列表读取失败**且无法获得真实线程 ID 时，允许使用：`threadId=list`

### 3. 日期与时区
- 模板中的日期必须使用 `Asia/Shanghai`
- 推荐格式：`YYYY-MM-DD`

### 4. 文本风格
- 纯文本
- 保留分隔线与 emoji 头部，便于人工检索与频道内快速识别
- `原因` 字段应控制在 60 字以内，强调“最终失败摘要”而不是过程流水账

## 判定建议

### 发送 P2
- 两次 `thread-list` 都失败
- 单线程两次 `channel-edit` 失败，且 `channel-info` 显示当前名称既不等于 `newName`，也不符合规范正则

### 发送 RESOLVED
- 第一次或第二次 `channel-edit` 报错
- 但之后通过再次重试，或 `channel-info` 发现实际上已成功改名/已符合规范

### 保持静默
- 没有候选线程
- 候选线程已符合命名规范
- 改名过程全程成功且没有中间失败

## 实施意义

该模板集的核心目标是：
- 让高频 backstop 任务在成功时保持低噪音
- 让真正需要人工介入的失败具备统一格式
- 让“先失败后恢复”的情况有明确回补闭环，避免误以为问题仍未解决
