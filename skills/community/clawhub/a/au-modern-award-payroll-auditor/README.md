# au-modern-award-payroll-auditor

**Skill for:** OpenClaw · Hermes Agent · Claude  
**Region:** 🇦🇺 Australia only  
**Version:** 1.0.0

---

## What it does

Turns an AI agent into a Modern Award payroll compliance auditor for Australian businesses. The agent asks targeted intake questions, identifies the correct award and classification level, then verifies base rates, penalty rates, overtime, allowances, casual loading, annualised salary BOOT compliance, and superannuation — all against current Fair Work Commission standards.

---

## Coverage

- All 121 modern awards under the **Fair Work Act 2009 (Cth)**
- 2025–26 Annual Wage Review rates (3.5% increase, effective 1 July 2025)
- National Minimum Wage: **$24.95/hr** | **$948.00/week**
- Superannuation Guarantee: **12%** of OTE (from 1 July 2025)
- Criminal wage theft provisions (**Closing Loopholes Act**, from 1 January 2025)
- Payday Super change (from 1 July 2026) — awareness included

---

## What the agent can audit

| Element                                              | Covered |
| ---------------------------------------------------- | ------- |
| Award identification (121 awards)                    | ✅      |
| Classification level decision tree                   | ✅      |
| Base rate verification (junior, adult, casual)       | ✅      |
| Penalty rates (Sat / Sun / PH / evening / overnight) | ✅      |
| Overtime rate logic (150% / 200%)                    | ✅      |
| Shift loading (afternoon / night)                    | ✅      |
| Casual loading (25%) and interaction with penalties  | ✅      |
| Annualised salary BOOT test                          | ✅      |
| Allowances (tool, meal, laundry, first aid, travel)  | ✅      |
| Superannuation on OTE                                | ✅      |
| Record-keeping obligations (7-year rule, payslips)   | ✅      |
| Casual conversion assessment                         | ✅      |
| Back-pay calculation and limitation periods          | ✅      |
| Civil and criminal penalty awareness                 | ✅      |

---

## How to install

**OpenClaw / ClawHub:**

```
clawhub skill install au-modern-award-payroll-auditor
```

**Manual (Claude / Hermes):**  
Copy the contents of `SKILL.md` into your agent's system prompt or skill slot.

---

## Important limitations

- **General guidance only — not legal advice.** Every response includes a disclaimer directing users to the Fair Work Ombudsman (1300 724 854) or an employment lawyer for complex matters.
- **Rates must be verified.** Dollar amounts change every 1 July. The skill instructs the agent to direct users to the FWO's PACT tool for current dollar figures: [calculate.fairwork.gov.au](https://calculate.fairwork.gov.au)
- **WA state public sector** is outside the national Fair Work system — the skill flags this and redirects.
- **No external API calls.** Pure reasoning + instructions only. No env vars, no bins, no network calls required.

---

## Key references

- Fair Work Commission (awards): [fwc.gov.au](https://www.fwc.gov.au)
- Fair Work Ombudsman (compliance): [fairwork.gov.au](https://www.fairwork.gov.au)
- Pay and Conditions Tool (PACT): [calculate.fairwork.gov.au](https://calculate.fairwork.gov.au)
- Enterprise Agreement search: [agreements.fwc.gov.au](https://agreements.fwc.gov.au)

---

## License

MIT
