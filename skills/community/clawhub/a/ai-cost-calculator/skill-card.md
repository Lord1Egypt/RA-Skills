## Description:

AI cost calculator that compares model pricing and helps AI application developers and cost-sensitive users optimize API spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI application teams use this skill to estimate API usage costs, compare model pricing, and choose lower-cost models for routine workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static model prices can become outdated and lead to incorrect cost estimates.

Mitigation: Verify current provider pricing before relying on calculated savings or budget recommendations.

Risk: Optional curl commands contact external AI provider pricing pages.

Mitigation: Run network commands only in environments where contacting those provider URLs is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-cost-calculator)
- [OpenAI API Pricing](https://openai.com/api/pricing)
- [DeepSeek Pricing](https://api.deepseek.com/zh-CN/zh/cewin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with cost tables, recommendations, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static pricing examples should be checked against provider pricing pages before business decisions.]

## Skill Version(s):

1.2.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
