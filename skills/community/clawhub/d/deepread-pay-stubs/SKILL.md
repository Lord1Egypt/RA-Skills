---
name: deepread-pay-stubs
title: DeepRead Pay Stubs
description: Extract structured data from pay stubs and earnings statements — employer, employee, pay period, gross/net pay, taxes, deductions, and YTD totals — as typed JSON. Ideal for income verification and lending. Per-field confidence flags. PII redaction built in. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Pay Stubs

Turn pay stubs and earnings statements into clean, typed JSON — employer, employee, pay period, gross and net pay, tax withholdings, deductions, and year-to-date totals — with a `needs_review` flag on every field. Built for income verification, where a misread number has real consequences.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "employer_name", "value": "Acme Corp", "needs_review": false, "location": {"page": 1}},
      {"key": "employee_name", "value": "Jordan Rivera", "needs_review": false, "location": {"page": 1}},
      {"key": "pay_period_start", "value": "2026-03-16", "needs_review": false, "location": {"page": 1}},
      {"key": "pay_period_end", "value": "2026-03-31", "needs_review": false, "location": {"page": 1}},
      {"key": "pay_date", "value": "2026-04-04", "needs_review": false, "location": {"page": 1}},
      {"key": "gross_pay", "value": 3520.00, "needs_review": false, "location": {"page": 1}},
      {"key": "net_pay", "value": 2614.18, "needs_review": false, "location": {"page": 1}},
      {"key": "ytd_gross", "value": 21120.00, "needs_review": false, "location": {"page": 1}},
      {"key": "deductions", "value": [
        {"type": "Federal Tax", "amount": 528.00},
        {"type": "Social Security", "amount": 218.24},
        {"type": "Health Insurance", "amount": 159.58}
      ], "needs_review": false, "location": {"page": 1}}
    ]
  }
}
```

## Setup

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## Schema

```json
{
  "type": "object",
  "properties": {
    "employer_name":   {"type": "string", "description": "Employer name"},
    "employee_name":   {"type": "string", "description": "Employee name"},
    "pay_period_start":{"type": "string", "description": "Pay period start (YYYY-MM-DD)"},
    "pay_period_end":  {"type": "string", "description": "Pay period end (YYYY-MM-DD)"},
    "pay_date":        {"type": ["string","null"], "description": "Pay/check date (YYYY-MM-DD)"},
    "pay_frequency":   {"type": ["string","null"], "description": "Weekly, biweekly, semimonthly, monthly"},
    "gross_pay":       {"type": "number", "description": "Gross pay this period"},
    "net_pay":         {"type": "number", "description": "Net (take-home) pay this period"},
    "ytd_gross":       {"type": ["number","null"], "description": "Year-to-date gross pay"},
    "ytd_net":         {"type": ["number","null"], "description": "Year-to-date net pay"},
    "deductions": {
      "type": "array",
      "description": "Itemized deductions and taxes",
      "items": {"type": "object", "properties": {
        "type":   {"type": "string", "description": "Deduction name (Federal Tax, 401k, Health, ...)"},
        "amount": {"type": "number", "description": "Amount this period"}
      }, "required": ["type", "amount"]}
    }
  }
}
```

## Verify Income (Python)

```python
fields = {f["key"]: f["value"] for f in result["extraction"]["fields"]}
gross = fields["gross_pay"]
freq = (fields.get("pay_frequency") or "").lower()
periods = {"weekly":52,"biweekly":26,"semimonthly":24,"monthly":12}.get(freq)
if periods:
    print(f"Estimated annual gross: ${gross * periods:,.0f}")
# Sanity-check: net + sum(deductions) should ≈ gross
ded = sum(d["amount"] for d in fields.get("deductions", []))
if abs((fields["net_pay"] + ded) - gross) > 1.0:
    print("⚠ net + deductions != gross — review extraction")
```

## Use Cases

- **Lending / mortgage** — verify applicant income from recent pay stubs
- **Rental / tenant screening** — confirm income-to-rent ratios
- **HR / payroll audits** — reconcile stubs against payroll runs
- **Gig / benefits eligibility** — compute annualized income

## Redact Before Sharing

Pay stubs carry names, partial SSNs, and bank details. Redact with `deepread-pii` before sending externally: `clawhub install uday390/deepread-pii`

## Tips

- **Compute the annualization in code** (shown above) — don't ask the model to guess pay frequency math.
- **Recurring employer format?** Build a blueprint at `https://www.deepread.tech/dashboard/optimizer`.
- **Check `needs_review`** — flagged amounts are the only ones to eyeball.

## Related DeepRead Skills

- **deepread-tax-forms** — W-2/1099 income verification — `clawhub install uday390/deepread-tax-forms`
- **deepread-bank-statements** — income deposits from statements — `clawhub install uday390/deepread-bank-statements`
- **deepread-pii** — redact sensitive data — `clawhub install uday390/deepread-pii`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
