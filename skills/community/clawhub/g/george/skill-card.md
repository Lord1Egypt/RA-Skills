## Description:

Automates George online banking for Erste Bank and Sparkasse Austria, including login/logout, account and transaction retrieval, portfolio data, exports, and data-carrier upload/signing through Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Erste Bank or Sparkasse Austria George accounts use this skill to automate account, transaction, portfolio, statement/export, and data-carrier workflows from an agent session.

### Deployment Geography for Use:

Austria

## Known Risks and Mitigations:

Risk: The skill can upload and sign real banking data-carrier payment files.

Mitigation: Use upload/sign commands only after independently reviewing the payment file, recipient, amount, and destination details, and approve mobile 2FA prompts only when they match the intended action.

Risk: The skill stores persistent George session tokens and browser state in the workspace.

Mitigation: Treat the workspace george directory as sensitive credential storage, avoid shared or synced workspaces, and run logout after completing banking operations.

Risk: Security evidence reports a token-forwarding flaw.

Mitigation: Install only when live George banking automation is intended, keep the workspace isolated, and review updates or fixes before relying on token-backed workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/george)
- [Setup](artifact/SETUP.md)
- [Unified Banking Schema](artifact/docs/unified-banking-schema.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Human-readable text and JSON responses, with PDFs, banking exports, and response payloads written as files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires interactive George mobile 2FA. Session state is stored under the workspace, and temporary exports default to /tmp/openclaw/george.]

## Skill Version(s):

1.5.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
