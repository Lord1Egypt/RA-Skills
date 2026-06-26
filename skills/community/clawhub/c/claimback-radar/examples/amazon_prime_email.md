# Example: Amazon Prime Renewal Notice

## Input

```json
{
  "source": "email_text",
  "content": "Your Amazon Prime membership will renew on May 1, 2026.\n\nAnnual fee: $139.00\n\nBenefits include free shipping, Prime Video, and more.\n\nTo cancel or manage your membership, go to amazon.com/prime.\n\nNeed help? Call 1-888-280-4331.\n\nNote: If you cancel within 3 business days of renewal, you may receive a full refund.",
  "user_timezone": "America/Los_Angeles",
  "current_date": "2026-04-22",
  "user_context": {
    "last_used_date": "2026-04-20",
    "monthly_budget": 100
  }
}
```

## Expected Output

```json
{
  "confirmation_card": {
    "service_name": "Amazon Prime",
    "provider": "Amazon",
    "amount": "139.00",
    "currency": "USD",
    "billing_cycle": "yearly",
    "effective_date": null,
    "next_charge_date": "2026-05-01",
    "refund_deadline": "2026-05-06",
    "refund_policy": "Full refund if cancelled within 3 business days of renewal",
    "warranty_expiry": null,
    "warranty_scope": null,
    "cancellation_method": "URL",
    "cancellation_link": "https://amazon.com/prime"
  },
  "action_receipts": [
    {
      "action_id": "act-003",
      "action_type": "review_usage",
      "title": "Review Prime usage before $139 renewal",
      "deadline": "2026-04-30",
      "priority": "medium",
      "reason": "Annual renewal ($139) hits in 9 days. You used it recently, but confirm value before auto-charge.",
      "estimated_savings": "$139.00",
      "cta_link": "https://amazon.com/prime",
      "steps": ["Review last 30 days of Prime usage", "Check if free shipping alone justifies $139", "If not, cancel before May 1"]
    }
  ],
  "risk_flags": ["upcoming_charge", "auto_renew_on"],
  "summary": "Amazon Prime $139/year renews May 1. Review value before auto-charge. Refund possible until May 6."
}
```