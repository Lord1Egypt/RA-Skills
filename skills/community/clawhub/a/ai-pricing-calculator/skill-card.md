## Description:

Calculates and compares AI model API costs, estimates token usage expenses, and recommends lower-cost model options for common usage scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to compare AI provider pricing, estimate API spend from token volume, and choose cost-conscious model configurations for OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running a separate OpenClaw installer skill that was not included in the reviewed artifact.

Mitigation: Prefer manual configuration, or use only a pinned and independently reviewed installer version.

Risk: Cost estimates and recommendations rely on hardcoded provider prices that may become outdated.

Mitigation: Check current provider pricing before making purchasing, routing, or budget decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-pricing-calculator)
- [DeepSeek platform pricing](https://platform.deepseek.com)
- [Zhipu AI platform](https://open.bigmodel.cn)
- [Alibaba Cloud DashScope](https://dashscope.aliyun.com)
- [OpenAI pricing](https://openai.com/pricing)
- [Anthropic pricing](https://www.anthropic.com/pricing)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses hardcoded pricing tables; users should confirm current provider pricing before acting on cost estimates.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
