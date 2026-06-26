# GitHub Copilot Billing API Reference

Source: https://docs.github.com/en/rest/billing/usage
Last verified: 2026-04

## ⚠️ Critical Limitation: No Quota Endpoint

**The GitHub Billing API does not expose the plan quota (monthly premium request allowance).**
There is no field, endpoint, or header that returns values like 50, 300, or 1500.
The only solution is to have the user configure their plan manually. See SKILL.md for config file details.

## Auth Requirements

- **Token type**: Personal Access Token (classic) — fine-grained tokens NOT supported
- **Required scopes**: `manage_billing:copilot` + `user`
- Usage: `gh api ...` (inherits `gh auth` automatically)

## User-Level Endpoint: Premium Request Usage

```
GET /users/{login}/settings/billing/premium_request/usage
```

> Note: Use `/users/{login}/` (not `/user/`). Resolve `{login}` via `gh api /user --jq '.login'`

Only applicable when Copilot is billed directly to the personal account.
If billed through org/enterprise, use the org-level endpoint instead.

### Query Parameters (all optional)

| Parameter | Type    | Description                        |
|-----------|---------|------------------------------------|
| year      | integer | e.g. 2026 (defaults to current)    |
| month     | integer | 1–12 (defaults to current)         |
| day       | integer | 1–31                               |
| model     | string  | filter by model name (case-insensitive) |
| product   | string  | filter by product name             |

### Response Schema

```json
{
  "timePeriod": { "year": 2026, "month": 4 },
  "user": "username",
  "usageItems": [
    {
      "product": "Copilot",
      "sku": "Copilot Premium Request",
      "model": "Claude Sonnet 4.6",
      "unitType": "requests",
      "pricePerUnit": 0.04,
      "grossQuantity": 300.0,
      "grossAmount": 12.0,
      "discountQuantity": 300.0,
      "discountAmount": 12.0,
      "netQuantity": 0.0,
      "netAmount": 0.0
    }
  ]
}
```

### Field Definitions

| Field             | Meaning                                                        |
|-------------------|----------------------------------------------------------------|
| `grossQuantity`   | Total premium requests consumed (already includes multiplier)  |
| `discountQuantity`| Requests covered by monthly plan allowance (not billed)        |
| `netQuantity`     | Overage requests billed at $0.04 each                         |
| `netAmount`       | Cost of overage in USD                                         |
| `pricePerUnit`    | Always $0.04 — the overage rate, NOT the multiplier            |

## Plan Quotas (not from API — hardcoded reference)

| Plan               | Premium Requests/month |
|--------------------|------------------------|
| Free               | 50                     |
| Student            | 300                    |
| Pro                | 300                    |
| Pro+               | 1,500                  |
| Business           | 300 per user           |
| Enterprise         | 1,000 per user         |

## Org-Level Endpoint (for Business/Enterprise)

```
GET /organizations/{org}/settings/billing/premium_request/usage
```

Same query parameters and response schema as user-level endpoint.
Requires org admin or billing manager role.

## Rate Limits

Standard GitHub REST API rate limits apply: 5,000 requests/hour for authenticated users.
No special limit on billing endpoints.

## Notes

- Data resets on the 1st of each month at 00:00 UTC
- Only last 24 months of data accessible
- Counters only started from June 18, 2025 (paid plans on GitHub.com)
