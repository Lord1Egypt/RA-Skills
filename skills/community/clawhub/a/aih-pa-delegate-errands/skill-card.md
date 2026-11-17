## Description:

将用户的交办事项拆分为可审阅的委托单、任务队列和待确认清单，并在需要外部工具时核对权限与费用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和助理可将交办原文、截止时间及不可代办事项整理成可核对的任务草稿，标明缺失信息、所需授权与完成证据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External sending, payment, deletion, publication, or business-system changes could occur without informed consent.

Mitigation: Keep the default draft-first mode and obtain separate explicit authorization for each external action.

Risk: Optional AI-HIVE/MCP use could expose sensitive materials or incur unexpected charges.

Mitigation: Review discovered tools, upload scope, pricing, currency, and spending cap before connecting, uploading, or paying; use a minimal sample first.

Risk: Incomplete details or missing receipts could be mistaken for completed tasks.

Mitigation: Keep missing fields pending and verify actual outputs and receipts before reporting completion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-delegate-errands)
- [AI-HIVE connection and authorization guidance](artifact/references/ai-hive-connection.md)
- [Result and evidence contract](artifact/references/output-contract.md)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [JSON delegation brief, CSV task queue, and review checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; unknown details and unverified external actions remain explicitly pending.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
