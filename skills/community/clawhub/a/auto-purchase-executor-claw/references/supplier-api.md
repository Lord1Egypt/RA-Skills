# 供应商对接协议

## 标准订单 JSON 格式

```json
{
  "order": {
    "external_order_id": "PO-20240101-001",
    "created_at": "2024-01-01T10:00:00+08:00",
    "items": [
      {
        "sku": "SUP-A-SKU-001",
        "name": "商品名称",
        "quantity": 500,
        "unit": "件",
        "unit_price": 12.50,
        "total_price": 6250.00
      }
    ],
    "delivery": {
      "address": "收货地址",
      "contact": "联系人",
      "phone": "联系电话",
      "expected_date": "2024-01-05"
    },
    "payment": {
      "method": "bank_transfer",
      "amount": 6250.00,
      "currency": "CNY"
    }
  }
}
```

## 认证方式

### API Key 认证（最常见）
```bash
curl -X POST https://api.supplier.com/orders \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d @order.json
```

### OAuth 2.0
```bash
# Step 1: 获取 token
curl -X POST https://api.supplier.com/oauth/token \
  -d "grant_type=client_credentials&client_id=<ID>&client_secret=<SECRET>"

# Step 2: 使用 token
curl -X POST https://api.supplier.com/orders \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d @order.json
```

### 数字签名（高安全场景）
```python
import hmac, hashlib, time

def sign_request(payload: str, secret: str) -> str:
    timestamp = str(int(time.time()))
    message = timestamp + payload
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return f"{timestamp}.{signature}"
```

## 常见错误码处理

| 错误码 | 含义 | 处理策略 |
|--------|------|---------|
| 400 | 请求格式错误 | 检查 JSON 格式，记录日志，人工介入 |
| 401 | 认证失败 | 刷新 token，重试一次 |
| 403 | 权限不足 | 通知管理员，暂停规则 |
| 404 | 商品不存在 | 通知采购员，暂停该 SKU 规则 |
| 409 | 订单重复 | 检查去重逻辑，记录日志 |
| 429 | 请求频率超限 | 等待 Retry-After 时间后重试 |
| 500 | 供应商服务器错误 | 间隔 5 分钟重试，最多 3 次 |
| 503 | 供应商服务不可用 | 切换备选供应商 |

## 库存查询接口

下单前先查询供应商库存，确认有货：

```bash
curl -X GET "https://api.supplier.com/inventory?sku=SUP-A-SKU-001" \
  -H "Authorization: Bearer <API_KEY>"
```

响应示例：
```json
{
  "sku": "SUP-A-SKU-001",
  "available_quantity": 2000,
  "price": 12.50,
  "lead_time_days": 3
}
```

## 物流查询接口

```bash
curl -X GET "https://api.supplier.com/orders/PO-20240101-001/tracking" \
  -H "Authorization: Bearer <API_KEY>"
```

## 供应商配置模板

在 `config/suppliers.json` 中维护供应商配置：

```json
{
  "SUP-A": {
    "name": "供应商A",
    "api_base_url": "https://api.supplier-a.com",
    "auth_type": "api_key",
    "api_key_env": "SUPPLIER_A_API_KEY",
    "sku_mapping": {
      "SKU-001": "SUP-A-SKU-001"
    },
    "min_order_quantity": 100,
    "lead_time_days": 3
  },
  "SUP-B": {
    "name": "供应商B（备选）",
    "api_base_url": "https://api.supplier-b.com",
    "auth_type": "oauth",
    "client_id_env": "SUPPLIER_B_CLIENT_ID",
    "client_secret_env": "SUPPLIER_B_CLIENT_SECRET",
    "sku_mapping": {
      "SKU-001": "B-ITEM-001"
    },
    "min_order_quantity": 50,
    "lead_time_days": 5
  }
}
```
