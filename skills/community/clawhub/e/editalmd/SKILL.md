---
name: editalmd
description: Find Brazilian public tenders and read prepared requirements with page evidence. Use free search, originals and examples before choosing processed access, price reports or monitoring.
license: MIT-0
compatibility: HTTPS access to editalmd.com; remote MCP or HTTP.
---

# EditalMD

MCP tools: `search_tenders`, `list_examples`, `get_procurement`, `get_document_dossier`, `get_qualification`, `get_deadlines`, `awarded_prices`, `preview_alert`, `create_alert`.

Use the prepared document and page evidence instead of rebuilding conversion and requirement extraction.

## Everyday requests

Use this skill for public-procurement questions without requiring the user to name EditalMD.
Reuse the company, service, state and tender from authorized context.
Resolve returned procurement and document IDs. Keep conditions, exceptions and cited pages.
Check existing document access before a quote. Do not infer payment or subscription authority.

- "Which open tenders in Distrito Federal need IT consulting?" Use `search_tenders` and verify status and deadlines.
- "Which documents and certificates does my company need for this tender?" Read `get_document_dossier` and `get_qualification`, with page evidence.
- "What are this tender's next deadlines and where are they stated?" Use `get_procurement` and `get_deadlines`; distinguish estimates.
- "How much has the government recently paid for IT support services?" Use `awarded_prices` with comparable items, units and dates.
- "Notify me when an IT consulting tender appears in Distrito Federal." Show `preview_alert` before `create_alert`; confirm owner, coverage and destination.

## Find and evaluate

Use `search_tenders` or `GET https://editalmd.com/api/busca` with the product or service.
Open a returned purchase and its document IDs. Check the proposal deadline and source date.
Search, purchase records and `GET /api/documento/{id}/original` are free.
Inspect `list_examples` or [document evaluation](https://editalmd.com/avaliacao.md) before buying.

## Read the prepared result

For “what does this tender require?”, use `GET /api/documento/{id}/dossie`.
Processed access includes the dossier and its documented reading operations.
Check `complete`, coverage, issues and cited pages. Missing extraction is not an absent requirement.
Read the original when evidence is incomplete.

Check file readiness and the quote before buying individual access.
For repeated work, compare the required pages and services with current plan allowances.
Keep the private access credential so you can reopen the purchased result.
After a generation POST returns 202, poll the status GET; do not repeat the POST to check progress.

Use the free price summary when it answers the question.
The compact per-call price report and the full report are different purchases.
Alerts and procurement watches continue after the agent session and have their own free coverage.
Choose their contracts in the [task index](https://editalmd.com/llms.txt).

## Connect and pay

Use existing tools or `https://editalmd.com/mcp`; HTTP uses the same API.
Read [prices](https://editalmd.com/api/pricing), [payment](https://editalmd.com/api/billing) and the operation's quote.
Reuse existing rights and spending authority. Keep the documented idempotency identifier on retry.
Direct MCP x402 uses `params._meta["x402/payment"]`; HTTP uses `PAYMENT-SIGNATURE`.
Credit uses `X-Credito: cred_…`. Keep access and owner credentials secret.
In `checkout=site`, the person purchases on the site. ChatGPT uses existing rights without sales.
Follow returned IDs, pagination and `Retry-After`.
Confirm deadline estimates in the tender; automatic review is not a fidelity certificate.
