## Description:

AI 成本计算器 - 对比各大模型成本，优化 API 支出。适合：AI 应用开发者、成本敏感用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cost-sensitive AI users use this skill to estimate, compare, and report model API costs across common providers before choosing a model or usage strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model pricing changes frequently, so cost estimates may become outdated.

Mitigation: Verify provider prices against current official pricing pages before making spending or model-selection decisions.

Risk: Optional shell examples use curl to make outbound requests to public pricing pages.

Mitigation: Run those commands only in environments where outbound network access to the referenced providers is acceptable.

## Reference(s):

- [OpenAI API Pricing](https://openai.com/api/pricing)
- [DeepSeek API Pricing](https://api.deepseek.com/zh-CN/zh/cewin)
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-cost-calculator-cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with tables, cost calculations, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model cost comparisons, savings recommendations, and optional curl-based price checks.]

## Skill Version(s):

1.2.4 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
