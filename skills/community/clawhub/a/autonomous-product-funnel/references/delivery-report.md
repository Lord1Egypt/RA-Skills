# Final Delivery Report

Write this report in the user's active conversation language. Keep provider names, IDs, code identifiers, environment variables, event names, and URLs unchanged.

Use the following structure.

# Completion Summary

State the final status in one short paragraph:

- production live;
- staging ready;
- implementation complete but blocked by external action;
- partially complete because of an explicit technical/policy limitation.

Do not overstate completion.

## 1. Built

Summarize what was actually implemented:

- funnel pages;
- offer logic;
- checkout/payment;
- order state;
- transactional messaging;
- measurement;
- SEO;
- deployment;
- domain/SSL;
- QA.

## 2. Customer journey

Show the implemented path, for example:

`ad/organic traffic -> product landing -> quantity offer -> checkout -> payment -> verified paid order -> confirmation`

Mention recovery paths for failed/cancelled payment.

## 3. JEV decisions

Use a compact table:

| Decision | JEV choice | Evidence/constraint | Why | Effect |
| --- | --- | --- | --- | --- |

Include meaningful commercial and technical decisions only.

## 4. Offer

Report:

- target buyer;
- primary use case;
- positioning;
- price;
- quantity tiers/bundles;
- shipping threshold;
- upsell/order bump if any;
- urgency basis if any.

Distinguish verified business values from assumptions.

## 5. Payment and order integrity

Report:

- provider;
- checkout mode;
- server-side price validation;
- webhook/provider verification;
- idempotency approach;
- order state mapping;
- duplicate-payment/order protection;
- what was actually tested.

## 6. Tracking matrix

Include the completed matrix from `tracking-and-integrations.md`.

Clearly label each row as:

- verified;
- implemented but not externally verified;
- blocked;
- not applicable.

## 7. SEO and search

Report:

- title/meta/canonical;
- structured data;
- sitemap;
- robots;
- Search Console property/verification state;
- indexability checks;
- hreflang if relevant.

## 8. Deployment

Report:

- hosting provider;
- staging URL;
- production URL;
- domain state;
- SSL state;
- deployment status;
- environment configuration state.

Do not expose secrets.

## 9. QA completed

List the real tests run, including:

- mobile/desktop;
- offer/price;
- checkout;
- successful payment path;
- failed/cancelled path;
- webhook/order state;
- refresh/retry behavior;
- tracking;
- consent;
- email;
- SEO/indexability;
- console/runtime errors;
- accessibility/performance checks.

State any untestable path explicitly.

## 10. Assumptions

List only assumptions that could materially affect revenue, legal/compliance behavior, fulfillment, payment, tracking, or user experience.

## 11. Human intervention required

If none remain, write: `None.`

For each remaining item use this exact structure:

### [Human action name]

- **System/location:** exact dashboard, provider, settings area, DNS zone, or account.
- **Agent already completed:** surrounding work already done.
- **Manual action:** exact action the account owner must perform.
- **Field/secret/config:** exact field or environment variable name when applicable.
- **Value type:** describe the required type, never print or request the secret itself.
- **Why human action is required:** KYC, 2FA, ownership, missing permission, legal acceptance, unavailable credential, etc.
- **What it unlocks:** exact capability that becomes active afterward.
- **Verification after action:** exact test/check to confirm success.

Do not put ordinary unfinished coding tasks in this section.

## 12. Repository/deployment record

When available include:

- repository;
- branch;
- commit hash;
- changed documentation;
- migration status;
- deployment identifier.

## 13. Residual risks

Only list real unresolved risks. Avoid generic warnings.
