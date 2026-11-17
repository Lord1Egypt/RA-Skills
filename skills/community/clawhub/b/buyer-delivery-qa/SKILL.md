---
name: buyer-delivery-qa
description: Verify that a digital-product listing's buyer files and access instructions match its customer-facing claims before promotion, renewal, or publication.
---

# Buyer Delivery QA

Use this skill for digital product listings when a seller needs to prevent a broken, missing, or misleading buyer delivery path. It is not a generic listing-copy or SEO workflow.

## Verification standard

For each requested listing:

1. Read the live listing state, title, description, delivery language, and stated deliverables.
2. Read back the platform's attached buyer files and record count, filenames, types, and sizes.
3. Compare the two. Mark a mismatch when the listing promises a file, template, access link, format, or instant delivery that the available evidence does not support.
4. If delivery depends on a third-party destination (for example, a Notion Duplicate link), verify the actual buyer-facing flow only with authenticated access. A public HTTP response or a file attachment alone does not prove that a buyer can duplicate the destination.
5. Report one verdict per listing:
   - **PASS** — files and delivery claims align; any external destination required by the claim is verified.
   - **FAIL** — a promised file, format, or delivery route is absent or inconsistent.
   - **BLOCKED** — necessary authenticated or buyer-side verification is unavailable. State the exact missing proof.

## Operating rules

- Treat buyer delivery as a revenue-path gate: do not recommend promotion, renewal, or stronger delivery claims for a FAIL or BLOCKED listing.
- Keep listing changes separate from the audit. Do not upload, replace, delete, renew, activate, deactivate, or alter a listing unless the user explicitly asks.
- Prefer the marketplace's own authenticated API or seller dashboard. If only partial evidence is available, say so rather than inferring a pass.
- Preserve buyer privacy. Do not inspect, copy, or expose purchaser data.

## Output

Give a compact audit table or bullets with: listing, customer promise, verified buyer file evidence, external-flow verification status, verdict, and the smallest corrective action. Include a single go/no-go recommendation for any requested promotion or renewal.
