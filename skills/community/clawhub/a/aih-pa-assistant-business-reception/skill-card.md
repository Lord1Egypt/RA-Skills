## Description:

把可公开的业务信息、答复范围与转人工条件整理成接待知识卡、问题台账和人工转接模板。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and their authorized assistants use this skill to draft responses to routine inquiries, track unanswered questions and prepare handoffs for decisions requiring the owner's approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private business information could be disclosed through optional uploads or connected tools.

Mitigation: Confirm the permitted upload scope, minimize or redact sensitive data, and use the official OAuth flow without sharing credentials in chat.

Risk: Unapproved replies, contracts, payments or business-system changes could bind or misrepresent the owner.

Mitigation: Keep deliverables as reviewable drafts; require separate explicit approval for external actions and refer commitments to the owner.

Risk: Optional paid model calls could incur unanticipated charges.

Mitigation: Review current pricing, currency, upload scope and spending limit before paid calls; start with a small sample.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-assistant-business-reception)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP connection](https://ai-hive.iclip.cn/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, JSON, CSV]

**Output Format:** [Reviewable reception knowledge card, question log and human-handoff template; optional JSON or CSV records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; unknown answers remain marked for review and external actions require explicit authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
