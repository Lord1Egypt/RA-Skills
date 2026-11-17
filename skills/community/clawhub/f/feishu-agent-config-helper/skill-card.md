## Description:

Helps OpenClaw users generate Feishu bot configuration snippets and manual binding guidance for connecting a Feishu bot to an Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe12801](https://clawhub.ai/user/joe12801)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill when configuring a Feishu bot account, binding it to an Agent at account or group-chat scope, and applying the required session scope and gateway restart steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated configuration workflows can expose Feishu App Secrets through shell history, CI logs, or pasted output.

Mitigation: Avoid passing real App Secrets through shell history or CI logs, review generated snippets before use, and rotate any secret that has already been exposed.

Risk: The generated defaults can allow overly broad bot access, including allowFrom: ["*"] and an open DM policy.

Mitigation: Replace allowFrom: ["*"] with a narrow allowlist where possible and prefer restrictive DM policies for agents with tools, private context, or paid resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joe12801/skills/feishu-agent-config-helper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style CLI output with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Feishu App ID and App Secret; provides snippets and instructions but does not modify openclaw.json directly.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
