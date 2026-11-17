## Description:

Connects a user to a Feishu bot by creating a registration session, returning the required Feishu setup link, and polling once after the user confirms setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easelearnai](https://clawhub.ai/user/easelearnai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to help connect, bind, or create a Feishu bot for OpenClaw pairing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials may be exposed in command output.

Mitigation: Redact client_secret from user-visible output and logs, and store credentials only in an approved secret manager.

Risk: Cookie handling uses a predictable temporary cookie jar path.

Mitigation: Use a unique protected temporary cookie jar for each session and clean it up after use.

Risk: The workflow restricts relevant permission and approval guidance after setup confirmation.

Mitigation: Allow the agent to provide necessary Feishu permission, approval, and setup guidance when it is relevant to successful connection.

Risk: The Feishu setup link requires from=maxclaw attribution without explaining it to the user.

Mitigation: Disclose the attribution parameter and its purpose before asking the user to open the link.

## Reference(s):

- [Feishu app registration endpoint](https://accounts.feishu.cn/oauth/v1/app/registration)
- [Feishu OpenClaw registration page](https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=maxclaw)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline shell commands and plain setup links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Feishu setup URL, user code handling guidance, and one follow-up poll instruction.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
