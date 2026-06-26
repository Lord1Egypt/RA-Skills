# Example: Netflix Subscription Email

## Input

```json
{
  "source": "email_text",
  "content": "Hi User,\n\nThank you for staying with Netflix!\n\nYour plan: Standard - $15.49/month\nNext billing date: May 15, 2026\n\nYou can cancel anytime at netflix.com/cancel\n\nIf you cancel within 7 days of being charged, you may be eligible for a refund.\n\nQuestions? Visit help.netflix.com\n",
  "user_timezone": "America/New_York",
  "current_date": "2026-04-22",
  "user_context": {
    "last_used_date": "2026-03-15",
    "monthly_budget": 50
  }
}
```

## Expected Output

```json
{
  "confirmation_card": {
    "service_name": "Netflix",
    "provider": "Netflix",
    "amount": "15.49",
    "currency": "USD",
    "billing_cycle": "monthly",
    "effective_date": null,
    "next_charge_date": "2026-05-15",
    "refund_deadline": "2026-04-29",
    "refund_policy": "Eligible for refund if cancelled within 7 days of being charged",
    "warranty_expiry": null,
    "warranty_scope": null,
    "cancellation_method": "URL",
    "cancellation_link": "https://netflix.com/cancel"
  },
  "action_receipts": [
    {
      "action_id": "act-001",
      "action_type": "claim_refund",
      "title": "Claim refund before window closes",
      "deadline": "2026-04-29",
      "priority": "critical",
      "reason": "Refund window closes in 7 days. If you cancel now, you can get your last payment back.",
      "estimated_savings": "$15.49",
      "cta_link": "https://netflix.com/cancel",
      "steps": ["Go to netflix.com/cancel", "Confirm cancellation", "Contact support if refund not auto-processed"]
    },
    {
      "action_id": "act-002",
      "action_type": "cancel_subscription",
      "title": "Cancel unused Netflix subscription",
      "deadline": "2026-05-10",
      "priority": "high",
      "reason": "You have not used Netflix for 38 days but are paying $15.49/month.",
      "estimated_savings": "$15.49/month",
      "cta_link": "https://netflix.com/cancel",
      "steps": ["Login to Netflix", "Go to Account > Cancel Membership", "Confirm cancellation"]
    }
  ],
  "risk_flags": ["refund_window_closing", "unused_service"],
  "summary": "Netflix $15.49/month — refund window closes Apr 29, unused for 38 days. Potential savings: $15.49/month."
}
```