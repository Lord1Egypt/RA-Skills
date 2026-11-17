## Description:

根据已授权客户记录、沟通历史和触达规则，整理客户跟进台账、个性化话术草稿和待批准动作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

销售人员使用已获授权的客户资料梳理承诺和下一步，按客户阶段拟定跟进台账与个性化消息草稿，供人工审阅和批准。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer data could be shared beyond its authorized scope when using external services.

Mitigation: Confirm permitted uploads, minimize and redact customer information, and keep credentials out of chat.

Risk: Incorrect or unwanted outreach could misrepresent customer intent or contact an opted-out customer.

Mitigation: Prioritize do-not-contact requests, review drafts against source records, and require explicit approval before sending.

Risk: Paid or business-system actions could occur without clear authorization.

Mitigation: Confirm costs and permissions before use; require separate approval for payment or system changes and verify uncertain results before retrying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-customer-followup)
- [客户跟进流程与验收](artifact/references/workflow-29.md)
- [结果与证据要求](artifact/references/output-contract.md)
- [AI-HIVE 连接说明](artifact/references/ai-hive-connection.md)
- [AI-HIVE 网页入口](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [CSV files, Text drafts, Guidance]

**Output Format:** [CSV follow-up ledger, message drafts and proposed actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; outbound messages and business-system changes require separate explicit approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
