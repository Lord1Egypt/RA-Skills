---
name: b2b-lead-generation
description: "Aggregate B2B lead-gen skill: customs trade intelligence + global company due-diligence + LinkedIn data. Analyze HS code market distribution/trends/shares, profile a company's trade scale/partners/products/ports, get macro trade overviews and top buyers/suppliers, run company background checks (employees, shareholders/UBO, decision-makers), map LinkedIn networks (colleagues, alumni, career & education).

Trigger: B2B lead generation, customs trade analysis, HS code search, trade area distribution, import export trends, trade percentage by company, company trade statistics, trade partner analysis, macro trade overview, top buyers suppliers, US import data, global company search, company employee list, shareholder UBO, person search, colleague alumni, work experience education history, school detail, due diligence background check, LinkedIn company search, LinkedIn people search, professional network mapping, executive headhunting, overseas lead generation, cross-border supplier sourcing"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🎯","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# B2B Lead Generation

Aggregate skill for B2B lead generation: **customs trade intelligence** + **global-company deep due-diligence** + **LinkedIn professional data**. 38 scripts across 3 data sources, routed by domain index.

## Overview

Three data sources, each behind a domain index (intent → script decision table):

| Data source | What it answers | Index |
|-------------|-----------------|-------|
| Customs - HS code analysis | Market distribution / trends / share for a product (HS code) | [indexes/customs-analysis.md](indexes/customs-analysis.md) |
| Customs - company trade | One company's trade scale, partners, products, ports, trends | [indexes/customs-company.md](indexes/customs-company.md) |
| Customs - macro overview | Country-level trade totals, top buyers/suppliers, US imports | [indexes/customs-overview.md](indexes/customs-overview.md) |
| Global company - deep | Firmographics, shareholders/UBO, employees, decision-makers (全球企业库) | [indexes/global-depth.md](indexes/global-depth.md) |
| LinkedIn | Professional network: companies, people, colleagues, alumni, career | [indexes/linkedin.md](indexes/linkedin.md) |

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_analysis_area.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_analysis_area.py`.

### How to pick a script

1. Match the user's intent to a **data source** in the table above.
2. Open the corresponding `indexes/<domain>.md` - it is an intent→script decision table that pins each intent to exactly one script.
3. Open that script's `references/<xxx>-api.md` for exact parameter names/formats - **never guess parameters**.

## Routing Decision Tree

| User Intent | Route to |
|-------------|----------|
| Analyze an HS code's market distribution / trends / share / overview | [indexes/customs-analysis.md](indexes/customs-analysis.md) |
| Profile one company's trade scale / partners / products / ports / trends | [indexes/customs-company.md](indexes/customs-company.md) |
| Macro country trade overview / Top buyers & suppliers / US imports | [indexes/customs-overview.md](indexes/customs-overview.md) |
| Company firmographics / shareholders-UBO / employees / decision-makers (background check) | [indexes/global-depth.md](indexes/global-depth.md) |
| LinkedIn companies / people / professional network / career & education | [indexes/linkedin.md](indexes/linkedin.md) |

### Cross-skill handoff (capabilities NOT in this skill)

These belong to standalone companion skills - hand off when the user needs them:

| User wants | Hand off to |
|------------|-------------|
| Buyers/suppliers with **real trade records** (trade record search) | `upkuajing-customs-trade-company-search` (= `upkuajing-trade-company-search`) |
| **Quick** company/person lookup + contact info (shallow search) | `upkuajing-company-people-search` (= `upkuajing-global-company-people-search`) |
| Validate / clean contact info before outreach | `b2b-outreach` (phone/email/domain validity) or `upkuajing-contact-info-validity-check` |
| Send email / SMS / map merchant harvesting after leads found | `b2b-outreach` |

## Combined Workflows (cross-source, only possible in this aggregate)

1. **Full overseas-buyer pipeline** (cross-skill): `upkuajing-customs-trade-company-search` (find buyers with trade records) → this skill `global-depth`/`linkedin` (find decision-makers) → `b2b-outreach` validity (clean contacts) → `b2b-outreach` (reach out).
2. **Supplier due-diligence**: `global-depth` (`global_company_search` → `company_shareholder_list` / `company_employee_list`) → `customs-company` (`customs_company_stats` to gauge real trade scale).
3. **Talent mapping**: `linkedin` (`linkedin_company_employee_list`) → `linkedin_person_experience_list` / `linkedin_person_education_list` (background).
4. **Market sizing then targeting**: `customs-overview` (`summary` / `top_n` to size a market) → `customs-analysis` (`trade_percent` to find dominant players) → `global-depth` (background the top players).

## API Key and Top-up

This skill requires an API key, stored in `~/.upkuajing/.env`:
```bash
cat ~/.upkuajing/.env
```
```
UPKUAJING_API_KEY=your_api_key_here
```

### API Key Not Set
First check if `~/.upkuajing/.env` has `UPKUAJING_API_KEY`. If not, prompt the user to choose:
1. User has one: user provides it (manually add to `~/.upkuajing/.env`)
2. User doesn't have one: apply via `auth.py --new_key` (auto-saved to `~/.upkuajing/.env`)

Wait for user selection.

### Account Top-up
When API response indicates insufficient balance:
1. Create top-up order (`auth.py --new_rec_order`)
2. Send the payment page URL to the user, guide them to open & pay; proceed after they confirm success.

### Get Account Information
`python scripts/auth.py --account_info`

Newly applied keys must be registered/bound at [UpKuaJing Open Platform](https://developer.upkuajing.com/).

### **Report Skill Call Errors**
When an API call fails or returns abnormal data (server error, timeout, malformed response, etc.), explain the anomaly to the user in natural language and ask whether to report it to the platform for troubleshooting. Only run the report after user confirmation:
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/area","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Customs area distribution query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**; billing methods differ per interface.

**Latest pricing**: visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html), or run:
```bash
python scripts/auth.py --price_info
```
(returns complete pricing for all interfaces - the aggregate auth.py queries the full price list and falls back to per-original-skill lookup if needed.)

### Billing rules (summary)
- **query_count search** (4 scripts: `global_company_search`, `global_company_person_search`, `linkedin_company_search`, `linkedin_person_search`): billed by calls = `ceil(query_count / 20)`; each call returns up to 20 records (`query_count` range 20–1000). When `query_count > 20`, inform the user of the expected call count first.
- **All other scripts** (customs analysis/company/overview; global/linkedin list & detail endpoints): billed **per call**. Cursor-paginated scripts return one page per call - pass `cursor` from the previous response to fetch the next page; single-record scripts (stats, summary, date, school detail) return one result per call.
- **All calls incur fees** - there are no free queries in this skill.
- Per-interface billing detail lives in the corresponding `references/<xxx>-api.md`.

### Fee Confirmation Principle

**Any operation that incurs fees must first inform the user and wait for explicit confirmation in a separate message. Do not execute in the same message as the notification.** When `query_count` exceeds one page, inform the user of the expected number of calls first.

## Error Handling

- **API key invalid/non-existent**: check `UPKUAJING_API_KEY` in `~/.upkuajing/.env`
- **Insufficient balance**: guide user to top up
- **Invalid parameters**: **must first check the corresponding API doc in `references/`** - get correct parameter names/formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

**customs-analysis** (route: [indexes/customs-analysis.md](indexes/customs-analysis.md))
- [area](references/customs-analysis-area-api.md) | [hscode-detail](references/customs-analysis-hscode-detail-api.md) | [hscode-search](references/customs-analysis-hscode-search-api.md) | [overview](references/customs-analysis-overview-api.md) | [trade-percent](references/customs-analysis-trade-percent-api.md) | [trends](references/customs-analysis-trends-api.md)

**customs-company** (route: [indexes/customs-company.md](indexes/customs-company.md))
- [area-list](references/customs-company-area-list-api.md) | [area-stats](references/customs-company-area-stats-api.md) | [hscode-list](references/customs-company-hscode-list-api.md) | [hscode-stats](references/customs-company-hscode-stats-api.md) | [partner-stats](references/customs-company-partner-stats-api.md) | [port-list](references/customs-company-port-list-api.md) | [product-list](references/customs-company-product-list-api.md) | [stats](references/customs-company-stats-api.md) | [trends](references/customs-company-trends-api.md)

**customs-overview** (route: [indexes/customs-overview.md](indexes/customs-overview.md))
- [date](references/customs-overview-date-api.md) | [summary](references/customs-overview-summary-api.md) | [top-n](references/customs-overview-top-n-api.md) | [trade-list](references/customs-overview-trade-list-api.md) | [trend](references/customs-overview-trend-api.md) | [us-import](references/customs-overview-us-import-api.md)

**global-depth** (route: [indexes/global-depth.md](indexes/global-depth.md))
- [global-company-list](references/global-company-list-api.md) | [company-employee-list](references/company-employee-list-api.md) | [company-shareholder-list](references/company-shareholder-list-api.md) | [global-company-person-list](references/global-company-person-list-api.md) | [person-colleague-list](references/person-colleague-list-api.md) | [person-alumni-list](references/person-alumni-list-api.md) | [person-experience-list](references/person-experience-list-api.md) | [person-education-list](references/person-education-list-api.md) | [school-detail](references/school-detail-api.md)

**linkedin** (route: [indexes/linkedin.md](indexes/linkedin.md))
- [linkedin-company-list](references/linkedin-company-list-api.md) | [linkedin-company-employee-list](references/linkedin-company-employee-list-api.md) | [linkedin-person-list](references/linkedin-person-list-api.md) | [linkedin-person-colleague-list](references/linkedin-person-colleague-list-api.md) | [linkedin-person-alumni-list](references/linkedin-person-alumni-list-api.md) | [linkedin-person-experience-list](references/linkedin-person-experience-list-api.md) | [linkedin-person-education-list](references/linkedin-person-education-list-api.md) | [linkedin-school-detail](references/linkedin-school-detail-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Notes

- `countryType`: `1` = exporting countries (suppliers), `2` = importing countries (buyers).
- IDs are source-specific: a global-depth `pid`/`hid` is not the same as a LinkedIn `pid`/`hid` - stay within one source per investigation.
- Large **search** queries (global/linkedin `*_search`) return a `task_id` + `file_url`; resume with `--task_id` to append. Customs & list scripts use **cursor** pagination - pass the `cursor` from the previous response (inside `--params`) to fetch the next page.
- `task_data/` stores results under UUID subdirectories.
- File paths use forward slashes on all platforms.
- **Prohibit outputting technical parameter format**: convert code-style params to natural language in responses.
- **Do not** estimate per-call fees - use `auth.py --price_info` for accurate pricing.
- **Do not** guess parameter names - read the `references/<xxx>-api.md` first.

## Related Skills

Other UpKuaJing skills you might find useful:

- b2b-outreach - Send email/SMS, harvest map merchants, validate contact info (phone/email/domain)
- upkuajing-customs-trade-company-search (= upkuajing-trade-company-search) - Search companies with real customs trade records
- upkuajing-company-people-search (= upkuajing-global-company-people-search) - Quick shallow company/person lookup + contact info
- upkuajing-contact-info-validity-check - Validate contact info (phone/email/domain) standalone
- upkuajing-email-tool - Standalone email send & task tracking
- upkuajing-sms-tool - Standalone SMS send & task tracking
- upkuajing-map-merchants-search - Standalone Google Maps merchant harvesting
