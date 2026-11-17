# 示例 - customer-crm

> 示例来源：`skills/customer-crm/SKILL.md` 示例与输入/输出格式。
> 支持的 action：record_source(记录来源) / get_customer_profile(获取客户档案) / recommend_repurchase(复购推荐) / attribute_stats(归因统计)。

## 示例1: 记录闲鱼来源（record_source）

### 输入
```json
{
  "action": "record_source",
  "customer_id": "xianyu_user_12345",
  "source": "xianyu",
  "platform": "xianyu",
  "tenant_id": "default"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "customer_id": "xianyu_user_12345",
    "source": "xianyu",
    "recorded": true
  },
  "error": null,
  "code": "CRM-SUCCESS-01"
}
```

## 示例2: 归因统计（attribute_stats）

### 输入
```json
{
  "action": "attribute_stats",
  "tenant_id": "default"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "by_source": {
      "wechat_official": 45,
      "xianyu": 120,
      "douyin": 30,
      "direct": 15
    },
    "total_customers": 210
  },
  "error": null,
  "code": "CRM-SUCCESS-01"
}
```

## 示例3: 异常 - 客户ID为空

### 输入
```json
{
  "action": "record_source",
  "customer_id": "",
  "source": "xianyu"
}
```

### 输出
```json
{
  "success": false,
  "data": {},
  "error": "customer_id 不能为空",
  "code": "CRM-ERR-01"
}
```
