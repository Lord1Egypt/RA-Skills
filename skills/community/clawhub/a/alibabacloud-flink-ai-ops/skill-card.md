## Description:

Supports Alibaba Cloud Flink AI assistant conversations and intelligent patrol configuration, triggering, and report review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud Realtime Compute for Apache Flink operators and developers use this skill to ask the AI assistant questions, continue approval workflows, manage scheduled patrols, trigger checks, and interpret patrol reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign, medium-confidence security verdict conflicts with a critical do-not-install scanner recommendation.

Mitigation: Review the discrepancy before installation, especially when consistent scanner results are required.

Risk: Assistant approval continuations and patrol configuration can lead to cloud-side write operations.

Mitigation: Confirm the authorized scope and parameters, review each approval item, and verify write outcomes with the documented read-only checks.

Risk: Cloud credentials are needed for authenticated operations.

Mitigation: Use the SDK default credential chain; never request, print, or store secret values, and rely on the skill’s redacted output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-ai-ops)
- [Alibaba Cloud Flink development console API overview](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/api-ververica-2022-07-18-overview)
- [Alibaba Cloud Flink AI assistant](https://help.aliyun.com/zh/flink/realtime-flink/flink-ai-assistant-beta)
- [Alibaba Cloud intelligent patrol](https://help.aliyun.com/zh/flink/realtime-flink/intelligent-inspection)
- [Command and authentication guidance](artifact/references/command-and-auth.md)
- [Assistant and human approval workflows](artifact/references/assistant-and-hitl.md)
- [Patrol workflows](artifact/references/patrol-workflows.md)
- [RAM permissions](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON, Markdown, Shell commands, Configuration instructions]

**Output Format:** [JSON operation results with concise Markdown explanations and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations require user-confirmed scope and parameters; credentials are not included in output.]

## Skill Version(s):

0.0.1 (source: server-resolved release, references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
