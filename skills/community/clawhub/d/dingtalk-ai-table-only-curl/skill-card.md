## Description:

Helps agents manage DingTalk AI Table (.able) sheets, fields, and records through curl-based Notable API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to prepare curl-based DingTalk Notable API calls for listing, creating, updating, and deleting AI Table sheets, fields, and records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide read, write, and delete operations against live DingTalk AI Table business data.

Mitigation: Use least-privilege DingTalk app permissions and require explicit user confirmation before update or delete operations.

Risk: The helper workflow stores DingTalk credentials and cached tokens on the local machine.

Mitigation: Use the skill only on trusted machines, avoid printing full secrets, and rotate credentials if exposure is suspected.

Risk: The security summary reports unsafe shell patterns.

Mitigation: Review generated shell commands before execution and keep sensitive values out of shared terminals, logs, and files.

## Reference(s):

- [dingtalk-ai-table API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/breath57/skills/dingtalk-ai-table-only-curl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, DingTalk configuration guidance, and confirmation prompts for write or delete operations.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
