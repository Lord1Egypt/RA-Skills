## Description:

Coordinates scoped offline task handoffs, unfinished-work recovery, and evidence-based acceptance checks using available authorized tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to plan authorized cloud and local work, resume interrupted tasks without duplicating actions, and review deliverables against evidence. It can guide optional AI-HIVE use but does not provide the original product's capabilities or automatically execute external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive credentials or personal data may be exposed during login or uploads.

Mitigation: Use user-controlled login and OAuth; never paste passwords, tokens, codes, cookies, or full identity documents into the workflow, and confirm the permitted upload scope.

Risk: External actions or model calls may incur charges or modify accounts without intended consent.

Mitigation: Confirm current tools, price, currency, budget, and action-specific authorization before paid calls or external changes.

Risk: A structurally valid receipt or timed-out request may be mistaken for a completed task.

Mitigation: Check actual outputs and remote status before claiming completion or retrying writes and payments; treat the checker as structural validation only.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-dots-cloud-handoff)
- [AI-HIVE web access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [Task handoff workflow](references/workflow-18.md)
- [Task resumption workflow](references/workflow-19.md)
- [Completion review workflow](references/workflow-41.md)
- [Result and evidence contract](references/output-contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Configuration]

**Output Format:** [Markdown task plans and review tables, with optional JSON status and evidence records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results distinguish planned, submitted, completed, and accepted work; structural checks alone do not confirm remote success.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
