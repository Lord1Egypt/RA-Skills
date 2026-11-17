## Description:

根据用户的任务、预算、隐私和设备限制，制定私人 AI 助理试用题集、评分表及选择建议，并在获得授权和可用工具时核对实际结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和顾问可用同一组实际任务、质量要求和总成本比较私人 AI 助理，获取可审阅的试用题集、评分表及选择建议；外部试用须由用户授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account credentials or private materials may be exposed when connecting to AI-HIVE or uploading files.

Mitigation: Keep credentials out of chat; confirm the upload scope and redact sensitive materials before sharing.

Risk: Paid calls or external actions may incur costs or change data without clear approval.

Mitigation: Confirm the specific action, current price, currency, and budget before proceeding; start with a small sample and check the original task status before retrying.

Risk: Scores or completion claims may be misleading when tools, prices, or external receipts are unverified.

Mitigation: Check actual tool access, current pricing, scorecards, and external receipts; mark unknown or unexecuted work for review.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-assistant-trial-benchmark)
- [Trial workflow and acceptance criteria](artifact/references/workflow-56.md)
- [Output and evidence contract](artifact/references/output-contract.md)
- [AI-HIVE connection and authorization](artifact/references/ai-hive-connection.md)
- [Product scope and sources](artifact/references/scope-and-sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Trial cases and selection guidance in text or Markdown, a CSV scorecard, and optional JSON result records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes proposals from observed results; records sources and unknowns, with external actions subject to user authorization.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
