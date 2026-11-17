## Description:

将获准使用的会议纪要、邮件或聊天片段整理为可追溯的承诺台账、逾期清单和跟进草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other authorized users can turn meeting notes, emails, or chat excerpts into a source-linked commitment ledger, overdue items, and reviewable follow-up drafts. Sending messages or using external services requires separate authorization and available tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private messages or documents could be shared outside the user's approved scope.

Mitigation: Use only authorized excerpts; confirm upload scope and minimize sensitive data before any external service call.

Risk: An inferred intention could be mistaken for a firm commitment or an overdue obligation.

Mitigation: Require a source quote for each commitment, keep intentions separate, and leave uncertain dates or owners unresolved.

Risk: Follow-up messages or paid actions could occur without informed approval.

Mitigation: Deliver drafts by default; separately confirm message authorization and the exact price, budget, and scope before external actions. Never request credentials in chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-commitment-ledger)
- [Commitment-tracking workflow](artifact/references/workflow-11.md)
- [Result and evidence contract](artifact/references/output-contract.md)
- [AI-HIVE connection guidance](artifact/references/ai-hive-connection.md)
- [AI-HIVE service](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [CSV commitment ledger, overdue list, and reviewable text or Markdown follow-up drafts; optional JSON result record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each confirmed commitment cites its source; unknown details remain marked as unknown. External actions are not automatic.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
