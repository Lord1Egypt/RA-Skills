## Description:

Guides OpenClaw users in syncing bank transactions, fetching Gmail bills, and exporting financial records to Beancount or Ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbinkai](https://clawhub.ai/user/xbinkai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can connect financial and email accounts to collect transactions and bills, then export records for personal accounting. Bank and email integrations require separate packages and user-provided credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local-only privacy claims may obscure provider processing of bank transactions and email-derived data.

Mitigation: Review Plaid, GoCardless, and Gmail permissions and data practices before connecting accounts.

Risk: Installing third-party packages and configuring credentials can expose sensitive financial or email data.

Mitigation: Review the npm packages before installation, enable only needed integrations, and safeguard credentials.

## Reference(s):

- [BillClaw on ClawHub](https://clawhub.ai/xbinkai/skills/billclaw)
- [OpenClaw plugin package](https://www.npmjs.com/package/@firela/billclaw-openclaw)
- [Optional CLI package](https://www.npmjs.com/package/@firela/billclaw-cli)
- [Optional OAuth server package](https://www.npmjs.com/package/@firela/billclaw-connect)
- [Project documentation linked in the skill](https://github.com/fire-la/firela-bot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown text with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accounting exports and local records are created by separately installed BillClaw packages.]

## Skill Version(s):

0.8.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
