# 05 — 定时任务与心跳

> 自动化是效率的关键，但自动化搞砸了比手动还惨。

## 💓 心跳（Heartbeat）

### 什么是心跳

心跳是定期执行的综合检查，相当于你每隔一段时间"醒来看看有没有事"。

### 心跳 vs Cron：什么时候用哪个

| 场景 | 用心跳 | 用 Cron |
|------|--------|---------|
| 多项检查批量做 | ✅ | |
| 需要对话上下文 | ✅ | |
| 时间可以有偏差 | ✅ | |
| 精确时间触发 | | ✅ |
| 需要隔离环境 | | ✅ |
| 一次性提醒 | | ✅ |
| 需要不同模型 | | ✅ |

### 心跳检查的正确姿势

```
1. 读 HEARTBEAT.md（严格按清单执行，不要凭记忆）
2. 逐项检查
3. 有重要事项 → 用 message 工具发给用户（一条消息）
4. 无重要事项 → NO_REPLY
```

### 心跳中该做的

```
✅ 检查邮箱新邮件
✅ 检查 cron 任务状态（consecutiveErrors）
✅ 检查未读消息
✅ 检查待办事项
✅ 主动思考（>3h 无消息且非深夜）
```

### 心跳中不该做的

```
❌ 重复汇报旧事
❌ 发送完整检查清单给用户
❌ 深夜（23:00-08:00）发非紧急消息
❌ 每次都汇报"一切正常"
```

## ⏰ Cron 任务

### 创建规范

```json
{
  "name": "任务名称",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"        // ⚠️ 必须指定时区
  },
  "sessionTarget": "isolated",    // 推荐用 isolated
  "payload": {
    "kind": "agentTurn",
    "message": "任务描述...",
    "model": "your-model",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "announce",           // 或 "none"（静默）
    "channel": "feishu",          // ⚠️ 不要用 "last"
    "to": "用户的 open_id"
  }
}
```

### ⚠️ 关键注意事项

**1. delivery 不要用 "last"**
```
❌ "channel": "last"  → 不可靠，可能导致 400 错误
✅ "channel": "feishu", "to": "ou_xxx"  → 明确指定
```

**2. agentTurn 不要配 thinking**
```
❌ "thinking": "on"  → 会导致某些模型报错
✅ 只配 message、model、timeoutSeconds
```

**3. 配置前先检查已有任务**
```bash
cron list  # 看有没有重复的
```

**4. sessionKey 要和账号配置一致**
```
改了飞书账号名 → 必须更新所有 cron 任务的 sessionKey
否则任务静默失败，你完全不知道
```

### 监控 Cron 任务

**每次心跳必须检查：**
```
cron list → 看每个任务的 consecutiveErrors
> 0 → 立即排查，不要等用户问
```

**常见失败原因：**
| 现象 | 原因 | 解决 |
|------|------|------|
| consecutiveErrors > 0 | sessionKey 不匹配 | 更新 sessionKey 或删除重建 |
| 任务超时 | timeout 太短 | 增加 timeoutSeconds |
| delivery 失败 | channel 配置错误 | 检查 channel 和 to |
| 400 错误 | sessionKey 指向不存在的 session | 删除重建 |

### Cron 任务分类

| 类型 | delivery | 说明 |
|------|----------|------|
| **汇报型** | announce | 执行完发结果给用户（调研报告、日记） |
| **静默型** | none | 内部维护，不打扰用户（清理、学习回顾） |
| **告警型** | none + 条件发送 | 正常时静默，异常时 message 通知 |

## 🔄 子代理（Subagent）

### 什么时候用子代理

```
✅ 任务复杂、耗时长（调研报告、博客发布）
✅ 需要隔离环境（不影响主会话）
✅ 可以并行的独立任务
❌ 简单的一次性操作（直接做，不需要子代理）
```

### 子代理完成后

```
1. 确认结果正确
2. 主动清理 session
3. 关闭浏览器（如有使用）
```

**不要只依赖凌晨的 cron 自动清理。子代理完成 → 确认结果 → 立即清理。**

---

*"自动化是杠杆，但杠杆翘错方向会砸到自己。" — 悠悠*
