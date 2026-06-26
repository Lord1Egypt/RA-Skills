# Invoice Analyzer — Code Examples

## Example 1

```json
{
  "invoice": {
    "number": "INV-2024-001234",
    "date": "2024-01-15",
    "due_date": "2024-02-15",
    "vendor": {
      "name": "Acme Corp",
      "id": "VEN-001234"
    },
    "amounts": {
      "subtotal": 1500.00,
      "tax": 150.00,
      "discount": -50.00,
      "total": 1600.00,
      "currency": "USD"
    }
  },
  "extraction": {
    "confidence": 0.965,
    "flags": []
  },
  "validation": {
    "amount_valid": true,
    "tax_valid": true,
    "three_way_match": true
  },
  "fraud_detection": {
    "risk_score": 15,
    "risk_level": "low",
    "anomalies": []
  },
  "categorization": {
    "gl_code": "1400-100",
    "cost_center": "Engineering",
    "project": "Project-Alpha"
  },
  "workflow": {
    "approval_required": false,
    "auto_approved": true,
    "ready_for_payment": true
  }
}
```
