---
name: commsharbor
description: Use domain mail without operating a mail server, or inspect public email-security records. Evaluate free DNS checks and mailbox activation before buying service.
license: MIT-0
---

# CommsHarbor

MCP tools: `commsharbor_email_security_check`, `commsharbor_email_workspace`, `commsharbor_billing_catalog`, `commsharbor_email_domain_get`, `commsharbor_email_domain_setup`, `commsharbor_email_mailbox_create`, `commsharbor_email_job_get`, `commsharbor_email_google_catalog`, `commsharbor_email_google_connect`.

Use the managed mail server, webmail and organization workspace instead of operating that stack yourself.

## Everyday requests

Use this skill for domain-mail setup, mailbox management and public email-protection questions.
Reuse the authorized domain and organization. Ask for missing identity or scope.
Start by reading current state. A diagnostic request does not authorize DNS changes or mail delivery.
Follow accepted jobs to completion. Preserve organization isolation and keep passwords secret.

- "Is my company domain protected against email spoofing?" Use `commsharbor_email_security_check`.
- "What is missing before I can use email on my company domain?" Read the domain and its setup requirements.
- "Show my company's mailboxes and the state of each one." Read `commsharbor_email_workspace`.
- "Create a contact mailbox on my company domain." Confirm verified domain, capacity and authority; create the mailbox and follow `commsharbor_email_job_get`.
- "How can I bring my Google email into my company's domain mail?" Read the Google catalog, then start a connection only with organization authority.

## Choose the task

For a DNS check, use `GET https://commsharbor.com/api/email-check`.
The free and paid checks return the same analysis. Use the free allowance when it covers the task.
Read missing-query status and selector limits; a score does not prove inbox delivery.

For domain mailboxes, read `GET /api/email/plans`.
Check `trial.activation_ready` before starting a receive-only trial.
Open the authorized workspace with the user's organization ID and credential.
Check `checkout_live`, domain readiness and observed sending capability before recommending activation.
An accepted job or payment does not prove that a mailbox works.

Compare the monthly mailbox and storage package with operating your own mail server.
The human account accepts renewal and cancellation. An organization key manages service but cannot buy it.
Contracts: [task index](https://commsharbor.com/llms.txt).

## Connect and pay

Use existing tools or `https://commsharbor.com/mcp`; HTTP uses the same API.
Read [prices](https://commsharbor.com/api/pricing) and [payment](https://commsharbor.com/api/billing).
Reuse existing access and spending authority. Keep credentials and mailbox passwords secret.
Direct MCP x402 uses `params._meta["x402/payment"]`; HTTP uses `PAYMENT-SIGNATURE`.
Credit uses `Authorization: Bearer cred_…` or `X-Credito`.
In `checkout=site`, the person purchases on the site. ChatGPT uses existing rights without sales.
Do not offer campaign or transactional sending tools.
