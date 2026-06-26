# 飞书群聊路由技能

## 群聊配置

| 部门 | Chat ID | Agent | 职责 |
|------|---------|-------|------|
| 太子 | oc_3fb10f3b8923fc61a821ef0a83c42874 | taizi | 消息分拣、皇上对接 |
| 中书省 | oc_269292a740047e2c10ac98b273798756 | zhongshu | 规划、方案制定 |
| 门下省 | oc_0f84567e21488624862ae097f101c435 | menxia | 审议、把关 |
| 尚书省 | oc_84c80796216bf463e002128afc63ff08 | shangshu | 执行、调度 |

## 路由规则

### 1. 检测群聊来源
每次收到消息时，检查 `chat_id`：
- 如果是 `oc_3fb10f3b8923fc61a821ef0a83c42874`（太子群）→ 自己处理
- 如果是 `oc_269292a740047e2c10ac98b273798756`（中书省群）→ 调用 zhongshu agent
- 如果是 `oc_0f84567e21488624862ae097f101c435`（门下省群）→ 调用 menxia agent
- 如果是 `oc_84c80796216bf463e002128afc63ff08`（尚书省群）→ 调用 shangshu agent

### 2. 调用子 Agent
使用 `sessions_spawn` 调用对应 agent：
```python
# 示例：调用中书省
result = sessions_spawn(
    agentId="zhongshu",
    task="中书省请注意：收到来自 [群名] 的消息：[消息内容]。请处理并回复。",
    mode="run",
    timeoutSeconds=60
)
```

### 3. 回复原群
将子 agent 的回复转发回原群聊。

## 注意事项

1. **不要直接调用 sessions_send** → 会被权限限制
2. **使用 sessions_spawn + mode="run"** → 等待子 agent 完成后获取结果
3. **子 agent 的回复需要太子转发** → 子 agent 不能直接发消息到飞书
4. **保持上下文** → 子 agent 需要知道原始消息和群聊信息
