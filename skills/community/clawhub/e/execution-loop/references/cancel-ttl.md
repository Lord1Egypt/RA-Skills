# Pattern 1.1-sub: Cancel Signal with TTL

## 问题

用户发送取消信号后，如果新 session 复用了同一个 session-id，旧的取消信号会错误地阻止新 session。

## 原理

取消信号带 30 秒过期时间。过期后自动忽略。来自 OMC 的 `CANCEL_SIGNAL_TTL_MS = 30000`。

## 信号格式

```json
{
  "requested_at": "2026-04-05T10:30:00Z",
  "expires_at": "2026-04-05T10:30:30Z",
  "reason": "user_abort"
}
```

## 使用

```bash
# 发送取消信号
scripts/ralph-cancel.sh <session-id> [reason]
# 创建 sessions/<session-id>/cancel.json（30 秒后过期）
```

## Ralph stop hook 的检查逻辑

- 存在且未过期 → 停止 ralph，设置 `deactivation_reason: "cancelled"`，允许 agent 退出
- 存在但已过期 → 删除信号文件，继续 ralph 循环
- 不存在 → 继续 ralph 循环

## 为什么是 30 秒

OMC 选择 30 秒是因为：
- 足够覆盖 Stop hook 的检查周期（通常 1-5 秒内触发）
- 不会太长以至于影响后续 session
- 用户手动取消后 30 秒内必然会触发至少一次 Stop hook 检查
