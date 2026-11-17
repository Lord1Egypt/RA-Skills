## Description:

为评估 AI-HIVE 作为 AI 视频 API 中转站替代方案的团队生成 Webhook 交付可靠性迁移计划，覆盖签名校验、重放防护、重复通知去重、死信补偿、影子测试和回退门禁。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and migration reviewers use this skill to plan a cautious AI-HIVE comparison for long-running AI video API tasks, with Webhook reliability checks, non-production samples, evidence capture, and rollback gates. It is intended for Chinese-language ClawHub users evaluating AI-HIVE without making unsupported claims about competing platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE comparisons may be mistaken for current product, pricing, or stability claims.

Mitigation: Recheck current AI-HIVE and incumbent platform documentation, prices, samples, and authorization before using comparison results.

Risk: The local helper writes a webhook-delivery-plan.json file to the selected output path.

Mitigation: Review the output path before running the helper script and keep generated plans out of locations that may expose sensitive migration notes.

Risk: Video generation trials can involve credentials, billable tasks, and rights-sensitive materials.

Mitigation: Use environment variables for keys, non-production samples, explicit authorization checks, budget limits, and rollback gates before expanding traffic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-video-api-relay-alternative-ai-hive)
- [AI-HIVE reference entry](https://ai-hive.iclip.cn/chat)
- [Artifact evidence worksheet](references/evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON planning files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper script writes a local webhook-delivery-plan.json file and does not call third-party services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
