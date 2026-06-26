# 快手磁力引擎 API 参考

## 认证方式

### Bearer Token

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API 端点

### 获取广告计划数据

```
POST https://api.kuaishou.com/openapi/ad/report/campaign
```

**请求体:**
```json
{
  "start_date": "2026-03-20",
  "end_date": "2026-03-20",
  "metrics": ["impression", "click", "cost", "conversion"],
  "dimensions": ["campaign_id", "campaign_name"]
}
```

**响应:**
```json
{
  "result": 1,
  "data": {
    "list": [
      {
        "campaign_id": 789012,
        "campaign_name": "计划名称",
        "impression": 10000,
        "click": 500,
        "cost": 1000.00,
        "conversion": 50,
        "ctr": 0.05,
        "cvr": 0.10
      }
    ]
  }
}
```

### 转化回传

```
POST https://api.kuaishou.com/openapi/ad/convert
```

**请求体:**
```json
{
  "cid": "CID123456",
  "event_type": "purchase",
  "convert_time": 1679414400000,
  "value": 299.00,
  "order_id": "ORDER_001"
}
```

## 事件类型

| 事件 | 说明 |
|------|------|
| `purchase` | 购买 |
| `form_submit` | 表单提交 |
| `phone_call` | 电话拨打 |
| `add_to_cart` | 加入购物车 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| 1 | 成功 |
| 401 | 认证失败 |
| 429 | 请求过于频繁 |

## 限流说明

- 报表接口：50 次/分钟
- 转化回传：200 次/分钟
