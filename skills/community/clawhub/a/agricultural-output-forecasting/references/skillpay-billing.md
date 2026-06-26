# SkillPay Billing API Reference

## Overview

This skill integrates with SkillPay for pay-per-use monetization.

## Pricing Model

| Item | Value |
|------|-------|
| 1 USDT | 1000 tokens |
| Per call | 1 token (~0.001 USDT) |
| Minimum deposit | 8 USDT |

## Configuration

Set via environment variables:
- `SKILL_BILLING_API_KEY` - Your SkillPay API key
- `SKILL_ID` - Your Skill ID from SkillPay Dashboard

## API Endpoints

### 1. Charge / 扣费

```python
POST https://skillpay.me/api/v1/billing/charge

Headers:
  X-API-Key: <your-api-key>
  Content-Type: application/json

Body:
{
  "user_id": "user_123",
  "skill_id": "your-skill-id",
  "amount": 0  // 0 means use default (1 token)
}
```

**Response:**
```json
{
  "success": true,
  "balance": 995,
  "payment_url": null
}
```

### 2. Check Balance / 查余额

```python
GET https://skillpay.me/api/v1/billing/balance?user_id=user_123

Headers:
  X-API-Key: <your-api-key>
```

**Response:**
```json
{
  "balance": 995
}
```

### 3. Payment Link / 充值链接

```python
POST https://skillpay.me/api/v1/billing/payment-link

Headers:
  X-API-Key: <your-api-key>
  Content-Type: application/json

Body:
{
  "user_id": "user_123",
  "amount": 8  // USDT amount
}
```

**Response:**
```json
{
  "payment_url": "https://skillpay.me/pay/..."
}
```

## Usage Example

```python
import os
from scripts.forecast import forecast_output

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Make forecast (automatically deducts 1 token)
result = forecast_output(
    crop_type="wheat",
    area_hectares=100,
    region="North China",
    season="spring",
    user_id="user_123"
)

if result["success"]:
    print("Forecast:", result["forecast"])
    print("Remaining balance:", result["balance"])
else:
    print("Error:", result["error"])
    if "paymentUrl" in result:
        print("Please recharge:", result["paymentUrl"])
```

## Multi-language Support

- **EN**: 1 USDT = 1000 tokens | 1 call = 1 token | Min deposit 8 USDT
- **中文**: 1 USDT = 1000 tokens | 每次 1 token | 最低充值 8 USDT
- **日本語**: 1 USDT = 1000トークン | 1回1トークン | 最低8 USDT
- **한국어**: 1 USDT = 1000토큰 | 1회 1토큰 | 최소 8 USDT
- **Русский**: 1 USDT = 1000 токенов | 1 вызов = 1 токен | Мин. 8 USDT
