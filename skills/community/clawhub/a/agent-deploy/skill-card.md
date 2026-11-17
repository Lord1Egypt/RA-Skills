## Description:

Deploy a new isolated OpenClaw agent with its own Telegram bot, workspace, and session storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe7921](https://clawhub.ai/user/joe7921)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy, list, and remove isolated OpenClaw agents backed by separate Telegram bot accounts, workspaces, and session storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies existing API credentials into newly deployed agents.

Mitigation: Review credential scope before use and prefer explicit allowlists for credentials copied into new agents.

Risk: The skill modifies OpenClaw agent, binding, Telegram, workspace, and auth profile configuration.

Mitigation: Review planned changes before execution, validate with OpenClaw doctor, and keep backups available for rollback.

Risk: Bot tokens are accepted as command arguments and may appear in local process or shell history.

Mitigation: Use short-lived or rotated Telegram bot tokens where possible and avoid exposing token values in shared terminals or logs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing deployment guidance and command outcomes; the underlying scripts update OpenClaw agent, binding, Telegram, workspace, and auth profile configuration.]

## Skill Version(s):

2.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
