## Description:

Interact with DataWorks Data Agent for conversational data analysis, session lifecycle management, and artifact download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to create or resume Alibaba Cloud DataWorks Data Agent sessions, send data-analysis prompts, manage session history, retrieve artifacts, check token usage, and cancel active sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional file attachments are sent to Alibaba Cloud DataWorks for processing.

Mitigation: Use only authorized data and avoid attaching secrets, credential files, personal data, or regulated business data unless approved for Alibaba Cloud processing.

Risk: File attachment prompts can reference local file paths.

Mitigation: Review file:// paths before use and exclude sensitive system, credential, SSH, Kubernetes, and Alibaba Cloud configuration directories.

Risk: The skill depends on an aliyun CLI profile and scoped DataWorks RAM permissions.

Mitigation: Grant only the documented Data Agent session permissions and verify CLI profile configuration without reading or exposing credential files.

## Reference(s):

- [DataWorks Data Agent API Reference](references/api-reference.md)
- [DataWorks Data Agent Examples](references/examples.md)
- [RAM Policies](references/ram-policies.md)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataworks-data-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and JSON parameter snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DataWorks session IDs, artifact metadata, token usage summaries, and retrieved artifact content when requested.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
