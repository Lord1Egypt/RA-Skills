# API Reference - 301重定向检查

## Base URL

```
https://xiaomeng-api.qisir.com
```

## Endpoints

### 1. Create Order

Create a new order for the service.

**Request**

```http
POST /api/createOrder
Content-Type: application/json

{
  "reqData": {
    "question": "your analysis request",
    "serviceId": "301重定向检查"
  }
}
```

**Response**

```json
{
  "resultCode": "0000",
  "resultData": {
    "orderNo": "ORD123456789",
    "amount": 8.0,
    "currency": "CNY"
  }
}
```

### 2. Get Result

Get the result after payment is completed.

**Request**

```http
POST /api/getResult
Content-Type: application/json

{
  "reqData": {
    "orderNo": "ORD123456789",
    "credential": "your_credential",
    "question": "your analysis request",
    "serviceId": "301重定向检查"
  }
}
```

**Response**

```json
{
  "resultCode": "0000",
  "resultData": {
    "result": "analysis result content",
    "metadata": {
      "service_id": "301重定向检查",
      "price": 8.0,
      "currency": "CNY"
    }
  }
}
```

## Payment Flow

1. Call `createOrder` to get `orderNo`
2. User completes payment via ClawTip
3. Call `getResult` with `orderNo` and `credential`
4. Receive analysis result

## Pricing

- **Price**: ¥8 CNY per request
- **Currency**: CNY (Chinese Yuan)
- **Payment Method**: ClawTip (JD Wallet)

## Error Codes

| Code | Description |
|------|-------------|
| 0000 | Success |
| 1001 | Invalid request |
| 1002 | Payment required |
| 1003 | Service unavailable |
| 2001 | Order not found |
| 2002 | Payment not completed |

## SDK

### Python

```python
import requests

api_base = "https://xiaomeng-api.qisir.com"

# Create order
resp = requests.post(f"{api_base}/api/createOrder", json={
    "reqData": {
        "question": "your analysis request",
        "serviceId": "301重定向检查"
    }
})
order = resp.json()["resultData"]

# After payment, get result
resp = requests.post(f"{api_base}/api/getResult", json={
    "reqData": {
        "orderNo": order["orderNo"],
        "credential": "your_credential",
        "question": "your analysis request",
        "serviceId": "301重定向检查"
    }
})
result = resp.json()["resultData"]
```

## Support

- **Provider**: XiaoMeng AGI
- **Version**: 1.0.0
- **Last Updated**: 2026-07-08
