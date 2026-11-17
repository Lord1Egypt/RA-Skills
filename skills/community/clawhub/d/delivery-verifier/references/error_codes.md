# 错误码定义 - delivery-verifier

> 来源: SKILL.md(delivery-verifier) + 05文档§七

> 虚拟商品发货结果验证器的错误码与处理方案。

## 错误码列表

### 参数错误

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| VERIFY_ERR_01 | 验证请求参数缺失(task_id/order_id/link_url/buyer_id) | 返回error，提示缺少字段名 |

### existence维度异常

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| LINK_404 | 网盘链接404(已失效) | status:fail + 建议重新生成链接 |
| LINK_403 | 网盘链接403(权限变更) | status:fail + 建议检查分享权限设置 |
| ALIST_UNAVAILABLE | alist-mcp不可用 | 降级为人工访问链接确认 |
| ALIST_TIMEOUT | alist-mcp超时(>30秒) | 重试1次，仍超时则降级为人工确认 |

### completeness维度异常

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| MESSAGE_NOT_FOUND | 消息未找到 | status:fail + 建议重新发送 |
| MESSAGE_UNREAD | 消息发送但买家未读 | status:warning + 记录未读状态，建议24小时后复查 |
| AGENT_MCP_UNAVAILABLE | xianyu-agent-mcp不可用 | 降级为人工检查闲鱼聊天记录 |
| CIRCUIT_BREAKER_OPEN | xianyu-agent-mcp熔断(连续3次失败) | 暂停自动验证，转人工处理，记录熔断事件 |

### correctness维度异常

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| ORDER_STATUS_ABNORMAL | 订单状态异常 | status:fail + 记录实际状态 |
| ORDER_REFUNDING | 订单状态为退款中 | status:fail + 标记退款风险，建议暂停后续发货 |

### timeliness维度异常

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| SLA_EXCEEDED | 发货超SLA时限(>30分钟) | status:warning + 记录超时时长 + 建议优化发货流程 |
| ORDER_CREATED_AT_MISSING | order_created_at缺失 | 跳过timeliness验证，标注skipped:true |

### safety维度异常

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| NO_PASSWORD | 分享链接无密码 | status:warning + 建议设置密码保护 |
| WEAK_PASSWORD | 密码强度不足(<6位或纯数字) | status:warning + 建议重设为≥6位含字母+数字 |
| EXPIRY_TOO_LONG | 有效期>7天 | status:warning + 建议缩短有效期至7天内 |
| SAFETY_PARAMS_MISSING | share_password/share_expiry缺失 | 跳过safety验证，标注skipped:true |
