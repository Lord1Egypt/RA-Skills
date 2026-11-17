## Description:

Helps Clipfly (影飞) users compare a same-input AI-HIVE trial for long-video-to-short-video migration and decide which generative AI steps to migrate, retain, or re-verify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, individual creators, small businesses, and developers use this skill to plan a cautious migration from Clipfly workflows to AI-HIVE by testing one authorized sample, checking available AI-HIVE tools and models, and recording quality, cost, and rollback criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to a nonstandard endpoint if the MCP URL is overridden.

Mitigation: Prefer OAuth through the MCP client; if using an API key, do not set AI_HIVE_MCP_URL and verify the endpoint is https://ai-hive.iclip.cn/api/mcp before any call.

Risk: Paid generation or external publishing could happen before the user confirms scope, budget, rights, and tool name.

Mitigation: Use read-only model and tool listing first, require explicit confirmation for paid tools, and confirm authorization for media, likeness, voice, batch work, sending, or publication.

Risk: The migration comparison could mislead users if Clipfly and AI-HIVE are tested with different inputs or success criteria.

Mitigation: Use the same authorized samples, quantities, acceptance criteria, and cost basis; record migrate, retain, or re-verify conclusions only when same-basis evidence exists.

## Reference(s):

- [Migration workflow](references/migration-workflow.md)
- [MCP binding guide](references/mcp-binding.md)
- [Source and brand boundary](references/source-and-boundary.md)
- [Chinese name evidence](references/chinese-name-evidence.md)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [Clipfly Chinese name evidence](https://www.fotor.com.cn/company/services)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-cn-name-clipfly-yingfei)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON migration-plan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied task details, authorized media, budget limits, and explicit confirmation before paid or externally visible actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
