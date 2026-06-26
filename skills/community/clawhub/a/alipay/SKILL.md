---
name: Alipay
slug: alipay
version: 1.0.0
homepage: https://clawic.com/skills/alipay
description: Implement Alipay for web and mobile with signed request safety, gateway alignment, and production-ready payment operations.
changelog: Initial release with implementation, validation, launch, and incident response playbooks for Alipay.
metadata: {"clawdbot":{"emoji":"💴","requires":{"bins":["curl","jq"],"env":["ALIPAY_APP_ID"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` and confirm platform, PSP, and release target before making code changes.

## When to Use

User needs Alipay in checkout, subscriptions, or cross-border wallet flows. Agent handles architecture decisions, signing strategy, gateway integration, rollout validation, and post-launch operations.

## Architecture

Memory lives in `~/alipay/`. See `memory-template.md` for setup and status fields.

```
~/alipay/
|-- memory.md                 # Project snapshot, risk status, and rollout state
|-- implementations.md        # Selected approach and platform notes
|-- validation-log.md         # Test evidence and environment results
`-- incidents.md              # Failed payments, root causes, and fixes
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Implementation plan | `implementation-playbook.md` |
| Validation matrix | `validation-checklist.md` |
| Failure recovery | `failure-handling.md` |
| Release and operations | `launch-playbook.md` |
| Recurring and subscription flows | `recurring-payments.md` |

## Requirements

- Environment variable: `ALIPAY_APP_ID`
- CLI tools for diagnostics: `curl`, `jq`
- Access to Alipay merchant console and target PSP account

Never ask users to paste private keys, full signed payloads, or PSP secrets into chat.

## Data Storage

Local notes stay under `~/alipay/`:
- memory file for current state and integration decisions
- validation log file for test outcomes and evidence
- incidents file for failure signatures and mitigations

## Core Rules

### 1. Confirm Business Goal Before Choosing Integration Path
Start by identifying the target outcome:
- Higher mobile checkout conversion
- Faster repeat purchases
- Lower payment friction for domestic and cross-border users
- Fewer payment failures

Then choose one primary path:
- Web or H5 checkout with Alipay gateway redirect flow
- In-app checkout with Alipay SDK handoff
- PSP-mediated integration path

Do not mix paths in one patch unless the user asks for a migration plan.

### 2. Require Merchant and Environment Prerequisites
Before implementation, confirm:
- Alipay app id exists for the correct account
- Gateway keys and certificates match the environment
- Notify and return URLs are configured and reachable
- Test and production credentials are separated

If prerequisites are missing, pause coding and produce a concrete prerequisite checklist.

### 3. Enforce Server Truth for Amounts and Currency
Amounts and currency must match across:
- Client payment request payload
- Server-side order totals
- Alipay authorization and capture calls

Never trust client totals for final charge amount.

### 4. Make Signing and Callback Verification Explicit
Treat signing and verification as required controls:
- Sign outgoing requests with the approved key strategy
- Verify callback signatures before changing order state
- Reject unsigned or invalid callbacks deterministically

Never mark a payment successful before signature checks pass.

### 5. Keep Payment Payload Handling Minimal and Auditable
Treat Alipay payloads as sensitive:
- Forward payload only to backend or PSP
- Persist metadata only (request id, status, amount, currency)
- Never store raw signed payloads in logs, notes, or screenshots

### 6. Build Idempotent and Recoverable Payment Steps
Require idempotency and reconciliation for all critical calls:
- Authorization request
- Capture request
- Refund or close operations

Every retried request must reuse stable idempotency keys to prevent duplicates.

### 7. Separate Test and Production Release Gates
Do not recommend production rollout until all gates pass:
- Test success, decline, cancellation, and timeout paths are covered
- Device and browser matrix is complete for supported audience
- Fallback card or alternative checkout works when Alipay is unavailable
- Failure observability and alerts are active

## Common Traps

- Shipping test gateway config to production -> live checkout failures
- Skipping callback signature verification -> fraudulent or duplicated state transitions
- Mismatching charset or signing parameters -> request rejection at gateway
- Trusting client totals -> mismatch between authorized and captured amounts
- Missing idempotency on retries -> duplicate charges and refund overhead
- Launching without fallback checkout -> conversion loss when wallet is unavailable

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://openapi.alipay.com/gateway.do | Signed payment requests and metadata | Production Alipay gateway operations |
| https://openapi-sandbox.dl.alipaydev.com/gateway.do | Signed payment requests and metadata | Sandbox validation and integration testing |
| https://global.alipay.com | Documentation and account console traffic | Merchant setup and operational reference |

No other data should be sent externally unless the selected PSP requires it.

## Security & Privacy

Data that leaves your machine:
- Alipay request payloads needed for wallet flow
- Payment metadata and signed requests sent to configured PSP or backend

Data that stays local:
- Integration notes and rollout state under `~/alipay/`
- Validation evidence and failure logs without raw signed payloads

This skill does NOT:
- Store raw signed request payloads in memory files
- Skip mandatory merchant and callback verification requirements
- Enable production release without explicit readiness checks

## Trust

Alipay integrations depend on Alipay infrastructure and the chosen PSP.
Only install and run this skill if you trust those services and your payment backend.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `payments` - General payment design and checkout decision frameworks
- `billing` - Billing models, reconciliation, and payment lifecycle decisions
- `api` - Reliable backend API contracts and failure-safe integrations
- `auth` - Authentication and session hardening in transaction flows
- `android` - Android checkout implementation and runtime troubleshooting patterns

## Feedback

- If useful: `clawhub star alipay`
- Stay updated: `clawhub sync`
