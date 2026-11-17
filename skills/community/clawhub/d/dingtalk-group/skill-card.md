## Description:

Provides DingTalk Open Platform guidance and a TypeScript script for creating internal DingTalk group chats, with additional group management operations documented as planned workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n-wen](https://clawhub.ai/user/n-wen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DingTalk workspace administrators use this skill to create internal project or operations group chats through DingTalk app credentials and command-line parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses privileged DingTalk app credentials to mutate collaboration resources.

Mitigation: Install it only in an environment scoped to the intended DingTalk organization, use a least-privilege DingTalk application, and keep DINGTALK_APP_KEY and DINGTALK_APP_SECRET out of shared shells and CI logs.

Risk: Debug output can expose request parameters or full API responses in shared logs.

Mitigation: Avoid --debug in shared logging contexts and review logs before sharing troubleshooting output.

Risk: Documented future workflows include destructive or sensitive operations such as group disbanding and member removal.

Mitigation: Require explicit human confirmation before any disband or member-removal workflow is added or run.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON success or error output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DingTalk app credentials from environment variables and writes operational logs to stderr while returning result JSON on stdout.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
