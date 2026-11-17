## Description:

Sends urgent Feishu reminders through in-app urgent push notifications or phone urgency calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace operators use this skill to ask an agent to send urgent Feishu reminders to themselves or resolved Feishu users, including optional phone urgency for time-critical issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secret exposure through command-line arguments, logs, transcripts, or local configuration files.

Mitigation: Avoid passing secrets in logged or shared environments, store .feishu.env outside shared repositories with restrictive permissions, and rotate any App Secret that has already appeared in logs or transcripts.

Risk: Overbroad Feishu permissions can allow urgent messages, phone urgency, and user lookup beyond the user's actual need.

Mitigation: Grant only the Feishu permissions needed for the intended workflow, and avoid enabling phone urgency or contact lookup when those features are not required.

Risk: Phone urgency can interrupt recipients and consume enterprise quota.

Mitigation: Reserve phone urgency for genuinely time-critical notifications and use in-app urgent or ordinary messages for lower-priority reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/skills/feishu-meeting-call)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu Open APIs](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu notification side effects through a local Python helper when credentials and permissions are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog list 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
