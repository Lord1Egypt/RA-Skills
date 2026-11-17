## Description:

Diagnose and manage Alibaba Cloud databases through natural language for database performance, status, SQL, health, and security baseline workflows across supported Alibaba Cloud database products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, database administrators, and cloud operations engineers use this skill to send natural-language questions to Alibaba Cloud DAS Agent for database diagnostics, health inspection, SQL optimization, and instance troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require broad Alibaba Cloud database authority and may access sensitive database diagnostics.

Mitigation: Run it with a dedicated Alibaba Cloud RAM user or role limited to the minimum needed permission, preferably das:Chat rather than FullAccess.

Risk: DAS output, tool previews, stdout logs, and session IDs may contain sensitive operational or database information.

Mitigation: Treat outputs and session identifiers as sensitive, limit log exposure, and share results only with authorized users.

Risk: Natural-language database management requests may lead to state-changing database actions.

Mitigation: Confirm any state-changing database action with the user before sending it through the skill.

## Reference(s):

- [DAS Agent API Reference](references/api-reference.md)
- [RAM Policies](references/ram-policies.md)
- [Alibaba Cloud credential configuration](https://www.alibabacloud.com/help/en/sdk/developer-reference/v2-manage-python-access-credentials)
- [Alibaba Cloud API signature documentation](https://help.aliyun.com/document_detail/185337.htm)
- [Alibaba Cloud RAM permission guidance](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-a-ram-user)
- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-das-agent)

## Skill Output:

**Output Type(s):** [text, markdown, JSONL, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSONL from a command-line DAS Agent client, with diagnostic answers and optional session and tool progress events.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session IDs, tool progress, and truncated tool output previews; diagnostic stdout is intended to be relayed to the user.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
