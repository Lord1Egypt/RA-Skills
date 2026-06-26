# 巨量引擎 API 参考

## 认证方式

### Access Token

```http
Access-Token: YOUR_ACCESS_TOKEN
```

## API 端点

### 获取广告计划数据

```
GET https://ad.oceanengine.com/open_api/v1.3/report/campaign/
```

**参数:**
- `app_id`: 应用 ID
- `start_date`: 开始日期 (YYYYMMDD)
- `end_date`: 结束日期 (YYYYMMDD)
- `dimensions`: ['campaign_id', 'campaign_name']
- `metrics`: ['impression', 'click', 'cost', 'convert']

**响应:**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "list": [
      {
        "campaign_id": 123456,
        "campaign_name": "计划名称",
        "statistics": {
          "impression": 10000,
          "click": 500,
          "cost": 1000.00,
          "convert": 50,
          "ctr": 0.05,
          "convert_rate": 0.10
        }
      }
    ]
  }
}
```

### 转化回传

```
POST https://ad.oceanengine.com/open_api/v2.0/promotion/conversion
```

**请求体:**
```json
{
  "app_id": "YOUR_APP_ID",
  "event_type": "purchase",
  "context": {
    "cid": "CID123456",
    "convert_time": 1679414400
  },
  "properties": {
    "value": 299.00,
    "order_id": "ORDER_001"
  }
}
```

## 事件类型

| 事件 | 说明 |
|------|------|
| `purchase` | 购买 |
| `form_submit` | 表单提交 |
| `phone_call` | 电话拨打 |
| `add_to_cart` | 加入购物车 |
| `follow` | 关注 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 401 | 认证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器错误 |

## 限流说明

- 普通接口：100 次/分钟
- 报表接口：20 次/分钟
- 转化回传：500 次/分钟

## 文档链接

https://oceanengine.github.io/open-platform/
