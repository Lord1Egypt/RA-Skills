## Description:

Full Didit identity verification platform management for account creation, API keys, sessions, workflows, questionnaires, users, billing, blocklists, webhooks, and other platform administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to administer Didit identity-verification workflows, create and retrieve verification sessions, manage user and billing operations, configure blocklists and webhooks, and work with the bundled helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with a Didit administrative API key and access identity-verification records.

Mitigation: Use scoped keys where available, store DIDIT_API_KEY outside shared terminals and logs, and redact API responses before sharing them.

Risk: The skill covers destructive and high-impact account actions such as deleting sessions or users, changing verification status, blocklisting identities, and modifying webhooks.

Mitigation: Confirm delete, status, billing, blocklist, and webhook actions manually before execution.

Risk: The helper scripts may print full API responses that include credentials, verification data, or session details.

Mitigation: Avoid running scripts in CI or shared terminals and review output before pasting it into chats or tickets.

Risk: Billing and top-up operations can create payment flows or consume account credits.

Mitigation: Check balances and intended amounts before billing operations, and require an operator confirmation for top-ups.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Didit API Overview](https://docs.didit.me/sessions-api/management-api)
- [Didit Programmatic Registration Guide](https://docs.didit.me/integration/programmatic-registration)
- [Didit Webhooks Guide](https://docs.didit.me/integration/webhooks)
- [Didit AI Agent Integration Guide](https://docs.didit.me/integration/ai-agent-integration)
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/skills/didit-verification-management)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, environment variable setup, helper-script commands, and administrative workflow guidance.]

## Skill Version(s):

4.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
