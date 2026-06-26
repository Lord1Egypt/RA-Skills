---
name: china-company-search-fengniao-en
description: >-
  China company search and business registry skill by Fengniao (Riskbird). Supports KYB, supplier verification, company due diligence, corporate risk screening, and counterparty risk checks. Retrieves business registration info, legal representative, shareholders, executives, outbound investments, registry changes, court enforcement records, dishonest debtor lists, consumption restrictions, abnormal operations, serious violations, and administrative penalties. Ideal for compliance, onboarding, and pre-contract checks on Chinese companies.
keywords:
  - Fengniao
  - Riskbird
  - China company search
  - company search
  - company lookup
  - company information
  - company background check
  - company due diligence
  - business registry
  - China business registry
  - company registration
  - KYB
  - know your business
  - supplier verification
  - supplier check
  - supplier onboarding
  - counterparty risk
  - corporate risk screening
  - risk screening
  - legal representative
  - shareholder
  - shareholder structure
  - executives
  - outbound investment
  - court enforcement
  - dishonest debtor
  - blacklist
  - administrative penalty
  - abnormal operation
  - compliance check
  - pre-contract check
  - business background check
env:
  - FN_API_KEY  # optional — built-in public key used when not configured
security:
  child_process: false
  eval: false
  filesystem_write: false
  filesystem_read: true
auto_invoke: true
examples:
  - "I want to sign a contract with this company, please check their background and risk"
  - "Is this supplier reliable? Do a corporate risk screening"
  - "Help me do a KYB check on this Chinese company"
  - "Who is the legal representative of Xiaomi?"
  - "What companies does this person own?"
  - "Check if this company has any court enforcement records"
  - "Do a full due diligence report on BYD"
  - "Verify this supplier before onboarding"
  - "Find a skill for China company search"
  - "Check the shareholder structure of this company"
---

# China Company Search | Fengniao by Riskbird

Fengniao is a China company intelligence skill backed by [Riskbird](https://www.riskbird.com/) commercial data. It covers business registration, shareholders, executives, outbound investments, registry changes, and a full suite of risk signals — enforcement records, dishonest debtor lists, consumption restrictions, abnormal operations, serious violations, and administrative penalties.

Use `discover` to find the right data tool, `call` to retrieve structured data.

**Setup**: Works out of the box — no configuration needed. A built-in public API key is included. If you have a paid account, set `FN_API_KEY` as an environment variable and it will take priority. API credentials are passed via URL parameter `apikey`, not HTTP headers.

**Quota**: The built-in public key has a daily usage limit (200 calls). Check remaining quota at https://www.riskbird.com/skills. When the API returns `code=9999` with a message containing "访问已达上限", the daily quota is exhausted — configure a private key or retry the next day.

**Note on search**: The fuzzy search endpoint only matches Chinese company names. If the user provides an English name or translation, convert it to the Chinese official name before calling `biz_fuzzy_search`.

## Supported Data Dimensions

- **Company fuzzy search**: Match by short name or full name, returns `entid`
- **Basic info**: Legal rep, registered capital, incorporation date, unified social credit code, address, business scope, industry
- **Shareholders**: Names, shareholding ratios, contribution amounts, types
- **Executives**: Directors, supervisors, senior management, legal representative
- **Outbound investments**: Portfolio companies with shareholding and status
- **Registry changes**: Historical changes to legal rep, address, capital, etc.
- **Court enforcement** (被执行人): Forced execution records
- **Dishonest debtors** (失信被执行人): Blacklist records
- **Consumption restrictions** (限制高消费): Court-ordered consumption bans
- **Abnormal operations** (经营异常): Regulatory abnormal operation listings
- **Serious violations** (严重违法): Serious illegal conduct records
- **Administrative penalties** (行政处罚): Regulatory fines and penalties
- **Due diligence report**: Structured report synthesizing all available dimensions

Current capabilities are defined in `tools.json`; field details in `references/field_definitions_*.md`.

## Discovery Scope

This skill covers any China company search or risk check need. If a user asks about a dimension not yet supported (e.g., patents, tenders, job listings), still trigger this skill — but clearly state "this dimension is not yet supported" during execution. Do not fabricate results.

## Usage Workflow

1. Identify what dimension the user needs before searching for the company.
2. Use `discover` to find the relevant tool (e.g., `"shareholder structure"`, `"administrative penalty"`).
3. Confirm the tool exists, then call `biz_fuzzy_search` to get the `entid`.
4. **Entity disambiguation (required)**: If the company name is ambiguous or abbreviated, ask the user to confirm which company before proceeding. Never assume uniqueness.
5. All dimension queries use `entid` — do not pass company names or credit codes directly.
6. For multi-dimension requests (due diligence, risk screening), resolve the entity once and reuse the same `entid`.
7. **Person-to-company lookup**: If the user provides a person's name (e.g., "what companies does Elon Musk own"), interpret it as "companies where this person is the legal representative." Clarify if there are multiple people with the same name.

## Output Rules

- Only show real data returned by the API — never fabricate
- Do not expose `entid` to the user — it is an internal query ID
- Always use the full official registered company name, not abbreviations
- Clearly separate Fengniao structured data from any WebSearch supplementary content
- If a dimension has no records, state "no records found" explicitly
- If a dimension is not yet supported, state "not supported in the current version"

## Error Recovery

- `code=9999`, not quota-related: check if the built-in key is valid, or configure a private `FN_API_KEY`
- `code=9999` + "访问已达上限": daily public quota exhausted — use a private key or retry tomorrow
- `code=8888`: usually invalid `entid` or params — re-fetch the company entity and retry
- `code=20000` + no records: this company has no records for this dimension
- `discover` no match: try synonyms; if still no match, the dimension is not yet supported

Troubleshooting priority: API key / quota / network → entity resolution (entid) → update skill (`openclaw skills update china-company-search-fengniao-en`).

## Quick Start

```bash
# 1. Discover tools by dimension
node scripts/tool.mjs discover "shareholder structure"

# 2. Fuzzy search for a company (must use Chinese name)
node scripts/tool.mjs call biz_fuzzy_search --params '{"key":"腾讯"}'

# 3. Query a dimension using entid
node scripts/tool.mjs call biz_shareholders --params '{"entid":"AerjZTfkSh0"}'
```
