# Browser Ops High Autonomy

High-autonomy browser workflow skill for approved domains.

## What it does
- Completes routine browser tasks end-to-end with minimal interruption.
- Restricts operations to explicitly approved domains.
- Escalates only when legal/payment/login/security challenge events occur.

## Escalation statuses
- `LOGIN_REQUIRED`
- `SECURITY_CHALLENGE`
- `LEGAL_REVIEW_REQUIRED`
- `PAYMENT_REVIEW_REQUIRED`
- `DOMAIN_NOT_ALLOWED`
- `BLOCKED`
- `DONE`

## Security policy
- Never bypasses security controls.
- Never bypasses access restrictions.
- Returns explicit status and next action metadata.

## Typical use cases
- Customer support workflows
- Email operations
- CRM updates
- Administrative forms and platform operations
- Structured data extraction and research
