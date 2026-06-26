# Prompt 2: Results & Metrics Section

## Purpose
B2B buyers make purchase decisions based on the results section more than any other part of a case study. This prompt produces a metrics-heavy, visually structured results section with an ROI calculation table and data visualization recommendations. This is the section sales reps screenshot and send to procurement.

---

## Prompt

```
You are a B2B content strategist. Using the case study narrative and metrics below, write the "Results" section of a professional case study.

This section must make a skeptical CFO or VP of Operations say: "Those numbers are real, and I want the same result."

STRUCTURE:

**1. Results Summary Box (top callout)**
Create a 3-stat callout box — the 3 most impressive, specific metrics from this case study. Format as:
| Metric | Before | After |
|--------|--------|-------|
| [Stat 1] | [Before] | [After] |
| [Stat 2] | [Before] | [After] |
| [Stat 3] | [Before] | [After] |

**2. Results Narrative (400–500 words)**
Expand each result into 1–2 paragraphs. For each metric:
- State the specific outcome
- Explain why it happened (the mechanism)
- Quote the customer contact reacting to it
- Connect it to a downstream business impact (what did the freed time/money/capacity enable?)

**3. ROI Calculation Table**
Build a simple ROI table:
| Cost item | Value |
|-----------|-------|
| Solution cost (annual) | $[PRICE] |
| Time saved/year | [HOURS] hrs × $[HOURLY RATE] = $[VALUE] |
| Revenue impact | $[AMOUNT] (if applicable) |
| **Total annual value** | **$[SUM]** |
| **ROI** | **[X]x in Year 1** |

Use conservative estimates. Show your math. If hourly rate isn't provided, use $35/hr as default for operations roles.

**4. Data Visualization Recommendations**
List 2–3 specific charts or visuals a designer should create:
- Chart type (bar, line, before/after comparison, funnel)
- What data it shows
- Why this visual helps a buyer understand the ROI quickly

**5. Timeline to Value**
Write a short paragraph (100 words) describing when results started appearing:
- Week 1: [early signal]
- Month 1: [first measurable result]
- Month 3: [full ROI realized]

INPUTS:
- Customer company: [COMPANY NAME]
- Your solution: [PRODUCT/SERVICE]
- Metrics (list all available): [PASTE METRICS FROM PROMPT 1 OR ADD NEW ONES]
- Solution annual cost: [PRICE — or write "not disclosed" to omit from table]
- Customer contact name/title: [NAME, TITLE]
- Hourly rate of affected roles (optional): [$/hr or leave blank for $35 default]

TONE:
- Specific and data-driven — no vague adjectives like "significant improvement"
- Every number should be defensible — cite timeframe (e.g., "in Q1 2025")
- Avoid percentages alone when absolute numbers are more compelling
- If you don't have a metric, write "[DATA NEEDED]" — do not fabricate
```

---

## Usage Notes

- Run after Prompt 1. The narrative gives context for why the numbers matter.
- If the customer won't share hard numbers, use ranges ("reduced by 6–8 hours per week") or proxies ("freed capacity equivalent to one full-time employee").
- The ROI table is the most forwarded element in B2B case studies — make it stand alone.
- "[DATA NEEDED]" placeholders are intentional — go back to the customer for those numbers rather than publishing without them.
