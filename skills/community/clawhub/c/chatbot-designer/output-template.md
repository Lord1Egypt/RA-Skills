# Chatbot Flow Design Document

## Project Overview
- **Brand:** 
- **Platform:** Shopify / WooCommerce / Custom
- **Chatbot tool:** Gorgias / Tidio / Intercom / Zendesk / Custom
- **OMS integration:** Yes / No / Planned
- **Launch date target:** 

## Intent Priority Matrix
| Rank | Intent | % of ticket volume | Automation potential | Build priority |
|---|---|---|---|---|
| 1 | | % | High/Medium/Low | Launch / Phase 2 |
| 2 | | % | | |
| 3 | | % | | |
| 4 | | % | | |
| 5 | | % | | |

## Main Menu Design
```
Welcome message: 

Menu options:
1. 
2. 
3. 
4. 
5. Talk to a person
```

## Flow Designs

### Flow 1: [Intent Name]
**Trigger:** (menu selection / keywords / both)  
**Data required:** 

```
Step 1 — Acknowledge:

Step 2 — Data collect:

Step 3 — Lookup/check:

Step 4A — Resolve (success):

Step 4B — Cannot resolve:

Step 5 — Escalation:

Step 6 — Confirmation:
```

### Flow 2: [Intent Name]
**Trigger:**  
**Data required:** 

```
[Repeat structure]
```

## Escalation Rules
| Trigger | Rule | Action |
|---|---|---|
| Frustration keywords | "ridiculous", "furious", "unacceptable", "worst" | Immediate human handoff |
| 2 failed resolution attempts | Any intent | Escalate with transcript |
| Explicit request | "human", "agent", "real person" | Immediate handoff |
| High-value customer | LTV > $[threshold] | Priority queue |

## Response Time Commitments (communicated to customer)
- Business hours escalation: respond within ___ hours
- After-hours escalation: respond by ___ next business day
- Acknowledgement message: sent immediately upon escalation

## Measurement Plan
| KPI | Baseline | 30-day target | 90-day target |
|---|---|---|---|
| Containment rate | | >50% | >65% |
| Escalation rate | | <40% | <30% |
| CSAT (bot) | | >3.5/5 | >3.8/5 |
| Drop-off rate | | <20% | <15% |

## Unhandled Intent Review Schedule
- Weekly review: Mondays, 30 minutes
- New flow threshold: intent appears 10+ times in a week → add to build queue
