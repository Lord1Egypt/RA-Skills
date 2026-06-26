# au-bas-gst-advisor

**BAS Prep & GST Triage Advisor for Australian businesses.**

An instruction-only AI agent skill covering every aspect of Australian Business Activity Statement preparation and GST classification. No APIs, no environment variables — all knowledge is embedded.

---

## What this skill does

Turns an AI agent into an expert BAS and GST advisor that can:

- Classify any supply as **taxable**, **GST-free**, or **input-taxed** under the GST Act 1999
- Explain every BAS field label: G1–G11, 1A, 1B, W1–W5, T1–T8, and specialty labels (LCT, WET, FTC)
- Determine **Simpler BAS** vs **full reporting** eligibility
- Confirm **GST registration** obligations including the ride-sourcing exception
- Calculate correct **lodgement due dates** for quarterly, monthly, and annual cycles
- Identify and explain **anomaly flags** that trigger ATO audits
- Walk users through **fixing BAS errors and adjustments**
- Explain **Failure to Lodge penalties** and **General Interest Charge** calculations
- Guide users on **tax invoice requirements** ($82.50 and $1,000 thresholds)
- Distinguish **cash vs accruals** accounting for GST purposes

---

## Who it's for

Australian businesses of all sizes — sole traders, partnerships, companies, and trusts — lodging BAS with the ATO. Designed for the Australian market only.

---

## How it works

The agent asks 1–3 targeted diagnostic questions to understand the user's situation (entity type, turnover, lodgement cycle, accounting method), then delivers tailored, step-by-step guidance.

All rules, formulas, thresholds, and examples are embedded directly in the SKILL.md. No external data sources or API calls are required.

---

## Requirements

- No environment variables
- No external APIs
- No binaries
- Compatible with: OpenClaw, Hermes Agent, Claude, and any instruction-following AI agent

---

## Limitations and disclaimer

This skill provides educational guidance based on ATO rules and public guidance current as of mid-2026. It is not a substitute for advice from a **registered BAS agent or tax agent**. For complex situations, audit responses, or material BAS amendments, users should engage a registered professional. Find a registered agent at [tpb.gov.au](https://www.tpb.gov.au).

---

## Sources

- ATO: _Business Activity Statements (BAS)_ — ato.gov.au
- ATO: _GST-free sales, Input-taxed sales_ — ato.gov.au
- ATO: _Choosing an accounting method for GST_ — ato.gov.au
- ATO: _PAYG withholding_ — ato.gov.au
- ATO: _Due dates for lodging and paying your BAS_ — ato.gov.au
- _A New Tax System (Goods and Services Tax) Act 1999_, Divisions 38 and 40
- Tax Practitioners Board: _tpb.gov.au_

---

## Version

1.0.0

---

## License

MIT
