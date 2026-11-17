# ICP worksheet - [product / service]

Fill this in before any account research. If a field is empty, it becomes an
assumption, and assumptions do not score.

## 1. What you sell

- **Product / service:** [one line]
- **Who pays for it:** [role that signs]
- **Price point:** [range]
- **Sales cycle:** [length]

## 2. Firmographics

| Criterion | Target | Weight | Notes |
| --- | --- | --- | --- |
| Industry | [e.g. commercial HVAC services] | 30 | [NAICS codes if relevant] |
| Employees | [20-200] | 25 | [why this band] |
| Revenue | [$5M-$50M] | 15 | |
| Geography | [US, except CA/NY] | 15 | |
| Tech stack | [only if you sell into it] | 10 | |
| Other | | | |

## 3. Triggers (what makes them contactable now)

- [ ] Recent funding or acquisition
- [ ] Hiring in the roles you sell into
- [ ] New service line or product launch
- [ ] Geographic expansion
- [ ] Leadership change in the buying role
- [ ] Compliance or renewal deadline
- [ ] Public review spike
- [ ] Website rebrand or repositioning

**Trigger freshness window:** [90] days

## 4. Disqualifiers (auto-exclude)

- [ ] Fewer than [10] employees
- [ ] No [field service] function
- [ ] Franchise-owned with no purchasing authority
- [ ] Outside the US
- [ ] Competitor or competitor's customer
- [ ] Already a customer
- [ ] Any competitor of a client

## 5. Tiering

| Tier | Score | Meaning | Action |
| --- | --- | --- | --- |
| A | >= [75] | Strong fit + live trigger | Personalize a 4-touch sequence |
| B | >= [50] | Good fit, no trigger yet | Nurture list, revisit monthly |
| C | >= [25] | Weak fit | Do not contact, keep for market research |
| X | any | Disqualified | Suppress |

## 6. The two questions a rep must be able to answer

1. **Why this account?** [one sentence, evidence-backed]
2. **Who do I talk to?** [role + why that role owns the budget]

## 7. Message hypothesis

- **Their words we can reuse:** [quote from their site or press release]
- **Our promise in one line:** [outcome, not feature]
- **The ask:** [one low-friction request - 15 minutes, a question, a benchmark]
- **What we do not say:** [claims we cannot substantiate]

## 8. Proof we can use

- [Customer story with permission to reference]
- [Benchmark or dataset with a date and a source]
- [Certification, compliance, or integration that applies]
- [Named customer, logo permission confirmed]

## 9. Inputs for `lead_sheet.py`

```json
{
  "weights": {
    "industry": {"include": ["hvac", "plumbing"], "weight": 30},
    "employees": {"min": 20, "max": 200, "ideal_min": 40, "ideal_max": 150, "weight": 25},
    "state": {"include": ["ID", "UT", "NV"], "weight": 15},
    "country": {"include": ["US"], "weight": 10}
  },
  "disqualifiers": [
    {"field": "employees", "op": "max", "value": 9},
    {"field": "country", "op": "not_equals", "value": "US"}
  ],
  "tiers": {"A": 75, "B": 50, "C": 25}
}
```
