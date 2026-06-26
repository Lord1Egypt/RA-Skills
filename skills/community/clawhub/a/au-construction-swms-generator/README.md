# au-construction-swms-generator

**Skill for:** OpenClaw · Hermes Agent · Claude  
**Region:** 🇦🇺 Australia only  
**Version:** 1.0.0

---

## What it does

Turns an AI agent into a site-specific SWMS generator for Australian construction businesses. The agent collects project and site details through targeted intake questions, then produces a fully structured, compliant Safe Work Method Statement covering the correct HRCW categories, hazards, hierarchy-of-controls measures, risk ratings, PPE requirements, emergency response, and worker sign-on register — all grounded in the model WHS Act 2011, WHS Regulations Part 6.2, and Safe Work Australia guidance.

---

## Coverage

| Capability                                                                                                                     | Included |
| ------------------------------------------------------------------------------------------------------------------------------ | -------- |
| All 19 HRCW categories mapped and explained                                                                                    | ✅       |
| Hierarchy of controls applied correctly (Elimination → PPE)                                                                    | ✅       |
| Hazard library for 7 major HRCW types (heights, excavation, electrical, asbestos, traffic, mobile plant, drowning, structural) | ✅       |
| General construction hazards (manual handling, silica dust, noise, UV/heat)                                                    | ✅       |
| 5×5 risk matrix with residual risk calculation                                                                                 | ✅       |
| SWMS mandatory content checklist (WHS Reg s.292–297)                                                                           | ✅       |
| High Risk Work Licence reference table (SB, SI, SA, RI, RA, DG, WP, LF, etc.)                                                  | ✅       |
| WHS penalty structure (2025–26 indexed amounts, Cat 1/2/3 + industrial manslaughter)                                           | ✅       |
| Principal contractor obligations ($250k+ projects)                                                                             | ✅       |
| All state/territory WHS regulator references                                                                                   | ✅       |
| SWMS review trigger conditions                                                                                                 | ✅       |
| Worker sign-on register template                                                                                               | ✅       |
| Structured SWMS output format (Sections 1–8)                                                                                   | ✅       |

---

## How to install

**OpenClaw / ClawHub:**

```
clawhub skill install au-construction-swms-generator
```

**Manual (Claude / Hermes):**  
Copy the contents of `SKILL.md` into your agent's system prompt or skill slot.

---

## Important limitations

- **Not professional WHS consulting advice.** Every SWMS output includes a mandatory disclaimer requiring review by a competent person before site use. Complex or high-consequence projects should involve a qualified WHS consultant.
- **Site-specific details required.** The agent will ask intake questions before generating — a SWMS without site-specific information is non-compliant under WHS Regulations.
- **Explosives, high-voltage live electrical, and radiological work are excluded** — these require specialist licensed input the agent cannot substitute.
- **No external API calls.** Pure reasoning + instructions only. No env vars, no bins, no network required.

---

## Key references

- Safe Work Australia (SWMS guidance): [safeworkaustralia.gov.au](https://www.safeworkaustralia.gov.au/duties-tool/construction/hazards-information/high-risk-construction-work-requiring-swms)
- Model WHS Regulations Part 6.2: [legislation.gov.au](https://www.legislation.gov.au/Series/F2011L01664)
- Model Code of Practice — Construction work: [safeworkaustralia.gov.au](https://www.safeworkaustralia.gov.au/doc/model-code-practice-construction-work)
- Dial Before You Dig: [1100.com.au](https://www.1100.com.au) | Call 1100

---

## License

MIT
