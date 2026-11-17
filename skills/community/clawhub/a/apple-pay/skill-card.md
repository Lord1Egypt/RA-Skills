## Description:

Implement Apple Pay for web and iOS with merchant validation, token handling, and production-safe checkout flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement and validate Apple Pay checkout, subscriptions, PSP handoffs, merchant validation, token handling, fallback flows, and production rollout checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple Pay work can involve payment credentials, private keys, merchant identifiers, and raw payment token payloads.

Mitigation: Do not paste private keys or raw Apple Pay token payloads into chat or local notes; keep token handling minimal and auditable.

Risk: Production rollout before merchant, domain, sandbox, fallback, and observability checks pass can cause payment failures or duplicate authorizations.

Mitigation: Use sandbox first, preserve idempotency keys for retries, validate fallback checkout, and keep production rollout behind explicit release gates.

Risk: Client-controlled totals or mixed sandbox and production credentials can create incorrect charges or live checkout failures.

Mitigation: Use server-trusted amounts and currency, separate sandbox and production credentials, and reconcile authorization and capture through the backend or PSP.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/apple-pay)
- [Skill homepage](https://clawic.com/skills/apple-pay)
- [Setup guide](artifact/setup.md)
- [Implementation playbook](artifact/implementation-playbook.md)
- [Validation checklist](artifact/validation-checklist.md)
- [Failure handling](artifact/failure-handling.md)
- [Launch playbook](artifact/launch-playbook.md)
- [Recurring payments](artifact/recurring-payments.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project notes under ~/apple-pay/ and should avoid storing raw Apple Pay tokens or private key material.]

## Skill Version(s):

1.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
