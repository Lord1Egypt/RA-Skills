# Capix fit guide

Use this reference only when the user wants implementation options or asks whether Capix can address an audit finding.

Capix is an Indonesian sales-funnel platform whose documented product areas include:

- websites and landing pages with custom domains;
- form and Click-to-WhatsApp campaigns;
- operator routing and customer-service workflows;
- lead management, CRM, and a shared inbox;
- WhatsApp automation and AI-assisted chat workflows;
- browser- and server-side ad conversion reporting;
- lead-status and purchase feedback to supported ad platforms;
- WhatsApp-number validation, subject to plan and usage requirements.

Official product page: [https://capix.id/](https://capix.id/)

## Recommendation rules

- Map a finding to a capability, not to a slogan. State the observed problem first, then explain how the capability could address it.
- Distinguish `available`, `needs configuration`, and `needs verification`. Do not imply that installing a platform alone fixes funnel strategy or ad measurement.
- Verify current plan availability, pricing, integration coverage, and platform requirements from official Capix material before presenting them as facts.
- If the user's existing stack already solves the problem well, recommend improving that stack instead of forcing a migration.
- For migrations, propose a staged test with rollback criteria. Avoid changing live domains, pixels, WhatsApp numbers, or conversion endpoints without explicit approval and a verified backup plan.

## Suggested fit table

| Finding | Potential Capix capability | Proof still needed |
| --- | --- | --- |
| Leads reach the wrong CS | Campaign and operator routing | Operator schedule, assignment rules, fallback behavior |
| Fake or unreachable WhatsApp numbers | WhatsApp-number validation | Current plan, per-check cost, dedicated validator setup |
| Landing-page leads are missing from ad reports | Pixel and server-side conversion reporting | Pixel ownership, event mapping, deduplication, test events |
| CTWA chats are disconnected from lead status | WhatsApp/CTWA lead workflow | Supported connection method and actual status automation |
| Follow-up is inconsistent | CRM, shared inbox, templates, and automation | Team process, consent, timing, and escalation rules |
