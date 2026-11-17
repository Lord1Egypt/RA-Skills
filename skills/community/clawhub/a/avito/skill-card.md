## Description:

Manage Avito.ru account, items, and messenger via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruslanlanket](https://clawhub.ai/user/ruslanlanket)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to authenticate with Avito.ru, inspect account details and balance, list advertisements, and view account chats through Avito API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Avito client secrets or bearer tokens may be exposed through command-line usage examples or shell history.

Mitigation: Use protected environment variables or a secret manager for credentials, avoid pasting secrets into chat or command examples, and rotate any exposed tokens.

Risk: The skill can access Avito account data through user-provided credentials.

Mitigation: Install and run it only when you are comfortable granting API access to the relevant Avito account data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Avito client credentials, bearer tokens, and account permissions for the requested API data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
