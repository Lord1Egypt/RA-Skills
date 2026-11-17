## Description:

防止AI幻觉的分级检查机制。高风险任务走完整流程，低风险走快速路径。无证据不输出，有疑问必标注。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyinli811-crypto](https://clawhub.ai/user/xiyinli811-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to apply a tiered anti-hallucination checklist before answering factual or source-dependent user requests. It guides high-risk tasks through evidence checks, uncertainty labels, and explicit handling of missing or incomplete data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to record mistake details into memory after an error.

Mitigation: Store only brief, non-sensitive corrections and avoid recording private task details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiyinli811-crypto/skills/anti-hallucination-1)
- [Publisher Profile](https://clawhub.ai/user/xiyinli811-crypto)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with checklists, decision rules, and confidence labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces process guidance for agent responses and does not require tools, API keys, or shell execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
