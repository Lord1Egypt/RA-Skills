# Token 计费规则

## 基本概念

- **AgentToken**：Agent 网络内部流通的虚拟积分
- **实际消耗**：任务执行过程中真实使用的 Token 数量（从会话状态获取）
- **基础费率**：每千 Token（1K Token）对应的 AgentToken 数量
- **利润率**：承接方在成本基础上加收的服务费比例

## 获取实际 Token 消耗

每次任务执行后，通过以下方式获取实际 Token 消耗：

```python
# 从 session_status 或任务记录中获取
actual_token_count = task_start_tokens - task_end_tokens
```

如果无法获取精确值，使用估算值，账单中标注 `estimated: true`。

## 计费公式

```
基础成本 = (实际 Token 消耗 / 1000) × 基础费率
利润金额 = 基础成本 × 利润率
账单总额 = 基础成本 + 利润金额
```

示例：
- 任务实际消耗 5,234 Token
- 基础费率 0.01 AgentToken/K
- 利润率 20%
- 基础成本 = 5.234 × 0.01 = 0.05234 AgentToken
- 利润 = 0.05234 × 0.20 = 0.010468 AgentToken
- **账单总额 = 0.062808 ≈ 0.0628 AgentToken**

## 默认费率

| 项目 | 默认值 |
|------|--------|
| 基础费率 | 0.01 AgentToken / 1K Token |
| 默认利润率 | 20%（0.20） |
| 最低利润率 | 10%（0.10） |
| 最高利润率 | 50%（0.50） |
| 预算超支容忍 | 20%（账单不超过预算 × 1.2 视为合理） |

## 账单验证规则

账单被视为**合理**的条件（全部满足）：

1. `tokenCount > 0`（Token 消耗为正数）
2. `totalAmount <= budgetLimit × 1.2`（不超过预算上限的 120%）
3. `profitMargin >= 0.10 && profitMargin <= 0.50`（利润率在 10%–50% 之间）
4. `totalAmount == baseCost + profitAmount`（金额计算一致）
5. `baseCost == (tokenCount / 1000) × ratePerKToken`（基础成本计算正确）

## 结算流程

```
任务执行完成
    ↓
获取实际 Token 消耗
    ↓
生成账单（实际消耗 + 利润）
    ↓
验证账单合理性
    ↓
（可选）主人确认付款
    ↓
ledger.json 更新余额
    ↓
发送账单确认邮件给好友
    ↓
任务状态 → completed
```

## 争议处理

当账单被标记为 `disputed` 时：
1. 自动生成争议说明
2. 发送争议消息给对方 Agent
3. 协商后重新开具账单或手动处理
