## Description:

Multi-cloud management and smart-advisor support for architecture visualization, risk assessment, and AI-powered operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1ncludesteven](https://clawhub.ai/user/1ncludesteven)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud and platform engineering teams use CloudQ to ask questions about Tencent Cloud and other cloud resources, review architecture diagrams and assessments, and handle supported AIOps and CloudOps tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment checks or setup can change cloud authorization and permissions.

Mitigation: Start with read-only checks; require explicit approval before enabling Advisor authorization or creating roles.

Risk: Cleanup can delete a role the tool did not create.

Mitigation: Check that deletion targets the exact role created by this tool, and avoid --all --cloud on shared accounts.

Risk: Credential or passwordless-link exposure could expose cloud access.

Mitigation: Keep secrets out of forwarded questions and protect passwordless login links.

## Reference(s):

- [CloudQChatCompletions API reference](references/api/CloudQChatCompletions.md)
- [CloudQ on ClawHub](https://clawhub.ai/1ncludesteven/skills/cloudq)
- [Tencent Cloud Smart Advisor overview](https://cloud.tencent.com/developer/article/2645159)
- [Tencent Cloud API documentation](https://cloud.tencent.com/document/product/213/30654)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Cloud operations guidance]

**Output Format:** [Markdown responses with shell-command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the remote CloudQ service and the user's cloud account permissions.]

## Skill Version(s):

1.10.0 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
