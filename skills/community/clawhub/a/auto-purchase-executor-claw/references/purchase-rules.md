# 采购规则引擎配置指南

## 条件表达式语法

### 基础比较运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `<` | 小于 | `inventory < 100` |
| `<=` | 小于等于 | `inventory <= safety_stock` |
| `>` | 大于 | `price > 0` |
| `>=` | 大于等于 | `price >= min_price` |
| `==` | 等于 | `status == "active"` |
| `!=` | 不等于 | `supplier_status != "suspended"` |

### 逻辑组合

```
# AND：库存低于阈值 且 供应商可用
inventory < safety_stock AND supplier_status == "active"

# OR：库存极低 或 紧急标记
inventory < 50 OR emergency_flag == true

# NOT：非黑名单供应商
NOT supplier_id IN ["SUP-BLACKLIST-001", "SUP-BLACKLIST-002"]

# 复合条件
(inventory < safety_stock AND price <= target_price) OR emergency_flag == true
```

### 时间函数

```
# 每月1号触发
DAY_OF_MONTH() == 1

# 每周一触发
DAY_OF_WEEK() == "Monday"

# 距离到期日不足7天
DAYS_UNTIL(expiry_date) <= 7

# 工作时间内触发（9:00-18:00）
HOUR() >= 9 AND HOUR() <= 18
```

### 数学运算

```
# 库存覆盖天数低于阈值
inventory / daily_consumption < 7

# 价格低于历史均价的90%
current_price < avg_price_30d * 0.9
```

## 规则配置结构

```json
{
  "rule_id": "RULE-001",
  "name": "SKU-001 自动补货",
  "priority": 1,
  "enabled": true,
  "trigger_condition": "inventory < safety_stock AND supplier_status == 'active'",
  "items": [
    {
      "sku": "SKU-001",
      "quantity": 500,
      "supplier_id": "SUP-A",
      "fallback_supplier_id": "SUP-B"
    }
  ],
  "budget_limit": {
    "per_order": 50000,
    "monthly": 200000
  },
  "notification": {
    "channels": ["feishu", "email"],
    "recipients": ["purchase@company.com"]
  },
  "dedup_window_minutes": 60
}
```

## 优先级算法

优先级数值越小，优先级越高（1 = 最高）。

| 场景 | 建议优先级 |
|------|-----------|
| 生产线停工紧急采购 | 1 |
| 库存跌破最低安全线（<50%） | 2 |
| 常规安全库存补货 | 3 |
| 定期续订 | 4 |
| 促销窗口采购 | 5 |

多规则同时触发时：
1. 按 priority 升序排列
2. 相同优先级按 rule_id 字典序排列
3. 检查总预算余额，超限则跳过低优先级规则

## 风控规则

### 单笔限额
```json
{
  "per_order_limit": 100000,
  "action_on_exceed": "notify_and_pause"
}
```

### 日累计限额
```json
{
  "daily_limit": 500000,
  "action_on_exceed": "pause_until_next_day"
}
```

### 异常交易识别
- 同一 SKU 在 60 分钟内重复触发 → 去重拦截
- 单价偏离历史均价 ±30% → 人工复核
- 供应商账户变更后首笔订单 → 人工复核

## 异常处理规则

| 异常类型 | 处理策略 |
|---------|---------|
| 支付失败 | 间隔 5 分钟重试，最多 3 次 |
| 供应商 API 超时 | 切换备选供应商 |
| 库存数据延迟 | 使用上次有效数据，标记为"数据延迟" |
| 预算超限 | 暂停规则，通知财务审批 |
| 供应商缺货 | 自动切换 fallback_supplier_id |
