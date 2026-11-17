## Description:

Automates payments, invoices, expenses, and financial reports with Stripe webhooks and real-time Telegram notifications for streamlined finance management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers and finance operators use this skill to run a Node.js service that records Stripe and Lemon Squeezy payments, manages invoices and expenses, generates finance reports, and sends real-time notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial read/write APIs may be exposed without implemented authentication or role-based authorization.

Mitigation: Add authentication and role-based authorization before deployment, keep the service on a trusted network until then, and use only test data during review.

Risk: Webhook tunnels or public endpoints may expose more of the server than intended during setup.

Mitigation: Expose only the webhook path, verify provider webhook signatures, and avoid sharing temporary tunnel URLs beyond the payment provider configuration.

Risk: Secrets for Stripe, Lemon Squeezy, Telegram, OpenClaw, SMTP, and the database can grant access to financial data or notifications.

Mitigation: Store secrets in protected environment configuration, rotate them after testing, and avoid committing .env files or credentials.

Risk: Invoices, receipts, logs, notifications, and financial records may contain sensitive business or customer data.

Mitigation: Verify retention, encryption, and notification content policies before storing records or sending Telegram/OpenClaw alerts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/finance-automation)
- [README.md](artifact/README.md)
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md)
- [QUICKSTART.md](artifact/QUICKSTART.md)
- [Stripe API Docs](https://stripe.com/docs/api)
- [Lemon Squeezy Docs](https://docs.lemonsqueezy.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Notifications]

**Output Format:** [Markdown guidance with inline shell and JavaScript examples, JSON API responses, generated invoice files, and notification messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured payment, database, email, Telegram, and OpenClaw services; webhook behavior depends on external provider credentials.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
