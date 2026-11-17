# 业务规则 - delivery-verifier

> 虚拟商品发货结果验证器，确认网盘链接可访问+闲鱼消息已发送+订单状态已变更。

## 规则列表

### 5个验证维度 (来源: 05文档§4.5 P0-6)

- existence(存在性): 网盘链接可访问，alist-mcp返回HTTP 200
- completeness(完整性): 闲鱼消息已发送，get_chat_history含链接消息
- correctness(正确性): 订单状态正确，get_order_status返回shipped/completed
- timeliness(时效性): 发货在SLA时限内完成，订单创建后30分钟内发货 (来源: 01手册§五5.1)
- safety(安全性): 分享链接安全合规，密码≥6位含字母+数字且有效期≤7天 (来源: 01手册§五5.1)

### SLA时限 (来源: 01手册§五5.1)

- 虚拟商品发货SLA: 订单创建后30分钟内完成发货
- 超SLA处理: status:warning + 记录超时时长 + 建议优化发货流程
- order_created_at缺失: 跳过timeliness验证，标注skipped:true

### 安全合规标准 (来源: 01手册§五5.1)

- 分享密码强度: ≥6位且含字母+数字
- 密码不达标: <6位或纯数字→status:warning + 建议重设
- 分享链接无密码: status:warning + 建议设置密码保护
- 有效期限制: ≤7天
- 有效期超限: >7天→status:warning + 建议缩短至7天内
- share_password/share_expiry缺失: 跳过safety验证，标注skipped:true

### 降级与熔断机制

- alist-mcp不可用: 降级为人工访问链接确认
- alist-mcp超时(>30秒): 重试1次，仍超时则降级为人工确认
- xianyu-agent-mcp不可用: 降级为人工检查闲鱼聊天记录
- xianyu-agent-mcp熔断(连续3次调用失败): 标记circuit_breaker=open，暂停自动验证，转人工处理

### 缓存机制

- 同一订单重复验证: 返回上次验证结果缓存，标注is_cached=true

### 验证结果状态

- pass: 全部5项验证通过
- warning: 存在warning项但无fail项(如超SLA、密码强度不足)
- fail: 存在fail项(如链接404、消息未找到、订单状态异常)

### 链接异常状态判定

- HTTP 404: 链接已失效，status:fail + 建议重新生成链接
- HTTP 403: 权限变更，status:fail + 建议检查分享权限设置
- 订单状态为退款中: status:fail + 标记退款风险，建议暂停后续发货
