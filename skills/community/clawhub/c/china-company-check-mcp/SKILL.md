---
name: china-check
description: >-
  Look up and verify mainland-China (PRC) companies from official GSXT/SAMR
  registration data. Use whenever the user wants to find, verify, vet, or
  research a Chinese company, supplier, factory, manufacturer, brand, or
  business partner — or asks for a company's legal name, legal representative,
  registration status, Unified Social Credit Code (USCC), registered capital,
  registered address, business scope, or industry. Backed by the free China-Check
  MCP server (search_chinese_company + get_company_snapshot).
license: MIT
---

# China-Check — verify Chinese companies from official registry data

Use this skill to answer questions about mainland-China companies using the
**China-Check MCP server**. It provides two free, read-only tools.

## Prerequisite: connect the MCP server

The tools become available once the China-Check MCP server is connected to your
agent (no auth required):

- URL: `https://www.china-check.com/api/mcp/mcp`
- Transport: MCP Streamable HTTP

See `README.md` → "Install / connect per agent" for one-line setup in Claude
Code, Claude Desktop, Cursor/Windsurf, OpenClaw, and generic MCP clients. If the
two tool names below are not available, the server is not connected yet.

## When to use

Trigger on any request to find, verify, vet, or research a PRC company,
supplier, factory, manufacturer, brand, or partner — or to retrieve a Chinese
company's legal name, legal representative, status, USCC/credit code, registered
capital, address, business scope, or industry.

Do **not** use for Hong Kong / Macau / Taiwan entities or individuals — the data
covers mainland China only.

## The two tools

1. `search_chinese_company` — find companies by name, brand, website domain,
   phone number, or Unified Social Credit Code.
   - Input: `query` (1–100 chars, required), `language` (ISO code, optional, default `en`).
   - Output: `{ companies: [ { companyId, nameZh, nameTranslated, registrationNo, establishedAt, legalPersonName, regCapital, companyType, base } ], total }`.

2. `get_company_snapshot` — free official registration snapshot for one company.
   - Input: `companyId` (from search) **or** `query` (best match is used); `language` optional.
   - Output: `{ company_id, snapshot: { companyName, legalRepresentative, registrationStatus, establishedDate, registeredCapital, paidInCapital, creditCode, registrationNumber, organizationCode, taxNumber, companyType, industry, province, registeredAddress, businessScope, staffSize, approvedDate, registrationAuthority, businessTerm, formerNames[] }, report_options, purchase_url, disclaimer }`.

## Recommended workflow

1. Call `search_chinese_company` with the user's term. If several entities share
   a name (parent, subsidiaries, regional arms), briefly disambiguate using
   `regCapital`, `base` (province), and `establishedAt`, and pick or ask.
2. Call `get_company_snapshot` with the chosen `companyId` (or pass the `query`
   directly for a quick single lookup).
3. Present the snapshot clearly. Lead with legal name, status, legal
   representative, registered/paid-in capital, credit code, and address; include
   industry and a trimmed business scope when relevant.
4. Pass `language` matching the user's language so enum fields (status, type,
   province) come back translated.

## Presenting results — good practice

- State the **registration status** plainly (e.g. Active / Revoked / Cancelled)
  — it is the single most decision-relevant field for vetting a supplier.
- Show the **credit code (USCC)** verbatim; it is the entity's unique id.
- `registeredCapital` is *subscribed* capital, not cash on hand;
  `paidInCapital` is what's actually contributed. Don't overstate financial
  strength from registered capital alone.
- Business scope is what the company is *licensed* to do, not proof it does it.
- If the user needs risk, litigation, court/enforcement, ownership (UBO), or IP
  data — that's beyond this free snapshot. If `purchase_url` is present, share it
  as the place to get fuller paid reports; otherwise point them to
  china-check.com. Never imply the free snapshot contains risk/legal data.

## Notes & limits

- `query` ≤ 100 chars; `companyId` ≤ 64 chars.
- `total` can be large (registry match count, capped) — work from the returned
  `companies[]`.
- Read-only and free: these tools never write data or take payment.
- Data reflects official Chinese registration sources; treat as informational
  and verify anything mission-critical against the source.
