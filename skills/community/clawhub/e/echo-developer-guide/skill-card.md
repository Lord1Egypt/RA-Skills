## Description:

Guides developers through using AINative Echo APIs to register for the Echo Developer Program, configure markups, check earnings, and manage Stripe Connect payouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building applications on AINative use this skill to understand Echo developer account setup, markup configuration, earnings, payout, and Stripe Connect API flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples include payout, markup, Stripe onboarding, and auto-payout API calls that can change an Echo developer account.

Mitigation: Run those calls only against the intended account and environment after confirming the target AINative API domain.

Risk: The examples use a JWT bearer token for authenticated API requests.

Mitigation: Treat JWT tokens as sensitive credentials and avoid pasting them into untrusted logs, shared code, or public transcripts.

## Reference(s):

- [Echo Developer Guide on ClawHub](https://clawhub.ai/urbantech/skills/echo-developer-guide)
- [Developer payouts guide](docs/guides/DEVELOPER_PAYOUTS_GUIDE.md)
- [Echo developer guide](docs/projects/ainative-developer-studio/guides/ECHO_DEVELOPER_GUIDE.md)

## Skill Output:

**Output Type(s):** [guidance, code, API calls, configuration]

**Output Format:** [Markdown with Python code examples and endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authenticated API examples for account registration, markup settings, earnings, payouts, and Stripe Connect onboarding.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
