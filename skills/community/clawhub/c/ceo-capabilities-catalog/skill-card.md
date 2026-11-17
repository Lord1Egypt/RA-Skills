## Description:

Catalogs the current OpenClaw instance's installed skills, custom skills, and coordination-oriented capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingfan0828](https://clawhub.ai/user/xingfan0828)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inventory an OpenClaw instance's installed skills and summarize coordination capabilities. It helps answer what the agent can do while avoiding claims about unverified channels, API keys, or integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to read local workspace memory, which may include private project, customer, workflow, or personal context.

Mitigation: Review before installing in sensitive workspaces, and narrow use to explicit allowed files and fields when private context may be present.

Risk: Capability summaries could disclose secrets or imply that unavailable channels or API keys are working.

Mitigation: Follow the artifact guidance to avoid exposing secrets and to verify channels or credentials before claiming they are available.

## Reference(s):

- [CEO Capabilities Catalog on ClawHub](https://clawhub.ai/xingfan0828/skills/ceo-capabilities-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text capability summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should omit secrets and avoid unsupported claims about unavailable channels or credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
