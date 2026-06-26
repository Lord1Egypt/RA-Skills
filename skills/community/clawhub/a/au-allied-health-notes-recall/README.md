# au-allied-health-notes-recall

**Skill for:** OpenClaw · Hermes Agent · Claude  
**Region:** 🇦🇺 Australia only  
**Version:** 1.0.0

---

## What it does

Turns an AI agent into an allied health documentation and recall engine for Australian practices. The agent collects context, then drafts audit-safe SOAP clinical notes, identifies correct Medicare MBS item numbers, generates patient recall and reminder messages (SMS, email, phone script), and produces GP report letters — all grounded in current MBS rules (2025–26) and Australian Privacy Act requirements.

---

## Coverage

| Capability                                                                              | Included |
| --------------------------------------------------------------------------------------- | -------- |
| SOAP note templates (initial, follow-up, discharge, telehealth)                         | ✅       |
| Profession-specific note guidance (physio, OT, psychology, SP, EP, podiatry, dietitian) | ✅       |
| Medicare audit compliance requirements (PSR/contemporaneous documentation rules)        | ✅       |
| CDM / GPCCMP allied health item numbers (10950–10980 series)                            | ✅       |
| Better Access psychology items (80000–80175 series)                                     | ✅       |
| Eating disorder treatment items (82000–82035 series)                                    | ✅       |
| Disability/developmental disorder items (paediatrician pathway)                         | ✅       |
| Telehealth item number guidance                                                         | ✅       |
| Session limit tracking logic (CDM 5/yr, Better Access 10/yr, ED 20 lifetime)            | ✅       |
| GPMP → GPCCMP transition rules (1 July 2025 changes)                                    | ✅       |
| Better Access referral changes (1 November 2025 changes)                                | ✅       |
| Patient recall SMS, email, and phone script templates                                   | ✅       |
| GP report / treating practitioner letter template                                       | ✅       |
| Record retention requirements (Privacy Act, 7yr adult / age-25 minor rule)              | ✅       |

---

## How to install

**OpenClaw / ClawHub:**

```
clawhub skill install au-allied-health-notes-recall
```

**Manual (Claude / Hermes):**  
Copy the contents of `SKILL.md` into your agent's system prompt or skill slot.

---

## Important limitations

- **Not clinical or legal advice.** Every response includes a disclaimer directing users to verify item numbers at mbsonline.gov.au and contact Services Australia (132 150) for billing queries.
- **Item numbers and rebates change.** The agent presents item codes as reference only — current fees must be verified on MBS Online before billing.
- **No HPOS access.** The agent cannot check a patient's real-time session count — users must verify this in HPOS or their practice management system.
- **No external API calls.** Pure reasoning + instructions only. No env vars, no bins, no network required.

---

## Key references

- MBS Online (item numbers, descriptors, fees): [mbsonline.gov.au](https://www.mbsonline.gov.au)
- Services Australia — Allied Health billing: [servicesaustralia.gov.au/mbs](https://www.servicesaustralia.gov.au/medicare-benefits-schedule-mbs)
- AHPRA (record keeping): [ahpra.gov.au](https://www.ahpra.gov.au/Resources/Managing-health-records.aspx)
- GPCCMP changes (from 1 July 2025): [servicesaustralia.gov.au](https://www.servicesaustralia.gov.au/allied-health-and-other-primary-health-care-referrals-for-gp-chronic-condition-management-plans)
- Better Access changes (from 1 November 2025): [health.gov.au](https://www.health.gov.au/topics/mental-health-and-suicide-prevention/what-were-doing/better-access-initiative)

---

## License

MIT
