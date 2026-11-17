## Description:

FreshBooks CLI for managing invoices, clients, and billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haseebuchiha](https://clawhub.ai/user/haseebuchiha)

### License/Terms of Use:


## Use Case:

External users, developers, and finance operators use this skill to authenticate a FreshBooks CLI and manage clients, invoices, invoice links, and billing lookup workflows from an agent-assisted command-line flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party CLI that handles FreshBooks credentials, access tokens, clients, invoices, and billing data.

Mitigation: Use only a trusted, reviewed, pinned version in an isolated environment before granting access to FreshBooks accounts.

Risk: The CLI can create, update, archive, or share invoice data.

Mitigation: Confirm every billing mutation or share-link action with the user before running the command.

Risk: OAuth client credentials and tokens are sensitive billing-system secrets.

Mitigation: Provide credentials through approved secret handling, restrict file permissions, and remove credentials with logout when access is no longer needed.

## Reference(s):

- [FreshBooks CLI ClawHub page](https://clawhub.ai/haseebuchiha/skills/freshbooks-cli)
- [haseebuchiha ClawHub publisher profile](https://clawhub.ai/user/haseebuchiha)
- [GitHub Package Registry](https://npm.pkg.github.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI outputs JSON to stdout and can create, update, archive, and retrieve FreshBooks billing records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
