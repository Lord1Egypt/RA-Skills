---
name: echo-developer-guide
description: Build apps on AINative and earn revenue through the Echo Developer Program. Use when (1) Registering as a developer, (2) Setting markup rates (0-40%), (3) Checking earnings and payouts, (4) Integrating Stripe Connect for payouts, (5) Building apps that bill customers for API usage. Revenue = your markup on customers' API usage, platform fee 5%. Closes #1520.
---

# Echo Developer Program Guide

## How It Works

1. You build an app using AINative APIs
2. Your customers use your app → they consume API credits
3. You set a markup (0–40%) on top of AINative's cost
4. AINative takes 5% platform fee
5. You receive the rest via weekly Stripe Connect payouts

**Example:** Customer uses 1,000 credits at base cost $0.10. You set 30% markup → you earn $0.03, AINative takes $0.0015.

## Register as a Developer

```python
import requests

requests.post(
    "https://api.ainative.studio/api/v1/echo/register",
    headers={"Authorization": f"Bearer {jwt_token}"},
    json={"developer_name": "My App", "website": "https://myapp.com"}
)
```

## Set Your Markup Rate

```python
# Set 25% markup (range: 0.0 to 0.40)
requests.put(
    "https://api.ainative.studio/api/v1/echo/markup",
    headers={"Authorization": f"Bearer {jwt_token}"},
    json={"markup_rate": 0.25}
)
```

## Check Earnings

```python
earnings = requests.get(
    "https://api.ainative.studio/api/v1/echo/earnings",
    headers={"Authorization": f"Bearer {jwt_token}"}
).json()

print(f"Total earned: ${earnings['total_earnings']}")
print(f"This month: ${earnings['current_period_earnings']}")
print(f"Pending payout: ${earnings['pending_amount']}")
```

## Connect Stripe for Payouts

```python
# Start Stripe Connect onboarding
onboard = requests.post(
    "https://api.ainative.studio/api/v1/echo/connect/onboard",
    headers={"Authorization": f"Bearer {jwt_token}"}
).json()

# Redirect your user to:
print(onboard["onboarding_url"])  # Stripe Connect Express page

# Check status
status = requests.get(
    "https://api.ainative.studio/api/v1/echo/connect/status",
    headers={"Authorization": f"Bearer {jwt_token}"}
).json()
print(f"Payouts enabled: {status['payouts_enabled']}")
```

## Request Manual Payout

```python
# Minimum payout: $10
payout = requests.post(
    "https://api.ainative.studio/api/v1/echo/payout",
    headers={"Authorization": f"Bearer {jwt_token}"},
    json={"amount": 50.00}
).json()
print(f"Payout requested: ${payout['amount']}, ETA: {payout['estimated_arrival']}")
```

## Auto-Payout Settings

```python
# Enable weekly automatic payouts
requests.post(
    "https://api.ainative.studio/api/v1/echo/settings/auto",
    headers={"Authorization": f"Bearer {jwt_token}"},
    json={"enabled": True, "minimum_amount": 10.00, "schedule": "weekly"}
)
```

## Earnings History

```python
history = requests.get(
    "https://api.ainative.studio/api/v1/echo/earnings/history",
    headers={"Authorization": f"Bearer {jwt_token}"},
    params={"days": 30}
).json()
```

## Echo API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/echo/register` | POST | Register as developer |
| `/api/v1/echo/markup` | PUT | Set markup rate (0-40%) |
| `/api/v1/echo/earnings` | GET | Current earnings summary |
| `/api/v1/echo/earnings/history` | GET | Earnings over time |
| `/api/v1/echo/earnings/breakdown` | GET | Breakdown by app/customer |
| `/api/v1/echo/payouts` | GET | List past payouts |
| `/api/v1/echo/payout` | POST | Request manual payout |
| `/api/v1/echo/balance` | GET | Available payout balance |
| `/api/v1/echo/connect/onboard` | POST | Start Stripe Connect |
| `/api/v1/echo/connect/status` | GET | Check Stripe Connect status |
| `/api/v1/echo/settings/auto` | GET/POST | Auto-payout settings |

## Key Concepts

- **Developers build their OWN apps** — not upload models to AINative
- **Customers pay developers** — developers bill customers using AINative pricing + markup
- **Weekly payouts** via Stripe Connect Express, minimum $10
- **Platform fee** 5% of developer earnings (deducted automatically)
- **Markup range** 0% to 40% — set per developer account

## References

- `src/backend/app/api/v1/endpoints/developer_earnings.py` — 21 route handlers
- `src/backend/app/services/stripe_service.py` — Stripe Connect integration
- `src/backend/app/tasks/developer_payouts.py` — Weekly Celery payout tasks
- `docs/guides/DEVELOPER_PAYOUTS_GUIDE.md` — Full payouts guide
- `docs/projects/ainative-developer-studio/guides/ECHO_DEVELOPER_GUIDE.md` — External dev guide (1,283 lines)
