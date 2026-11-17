## Description:

Provision and manage @clawemail.com Google Workspace email accounts. Use when the user wants to create an email for their AI agent, check email availability, or manage existing ClawEmail accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cto1](https://clawhub.ai/user/cto1)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create, inspect, suspend, unsuspend, or delete ClawEmail Google Workspace accounts for AI agents. It also guides users through checking address availability and handling OAuth setup after account creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose temporary passwords, OAuth links, and credentials JSON during account setup.

Mitigation: Treat returned passwords, OAuth links, and credentials JSON as secrets; avoid exposing them in chat or logs and store them securely.

Risk: Account suspension, unsuspension, and deletion can affect real Google Workspace accounts, and deletion is permanent.

Mitigation: Require explicit user confirmation before suspend, unsuspend, or delete actions, with extra confirmation for deletion.

Risk: Using a real CLAWEMAIL_API_KEY grants access to administrative ClawEmail endpoints.

Mitigation: Review the skill before installation in environments with a real CLAWEMAIL_API_KEY and restrict the key to trusted agents and workflows.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/cto1/skills/clawemail-admin)
- [ClawEmail Service](https://clawemail.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive temporary passwords, OAuth links, and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
