## Description:

输入ASIN，自动抓取数百条评论，AI逐条深度打标，生成痛点/卖点/Listing优化洞察报告。支持RapidAPI数据采集、OpenAI/DeepSeek兼容API、交互式HTML报告输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace operators, product managers, and ecommerce analysts use this skill to collect Amazon review data by ASIN, tag reviews with an OpenAI-compatible model, and produce product pain-point, selling-point, user-profile, and listing-optimization insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review data and LLM API keys can be sent to the configured model provider or to a custom OpenAI-compatible API base.

Mitigation: Use only trusted HTTPS API endpoints, avoid custom or misspelled API bases, and prefer provider-specific or throwaway keys with minimal permissions.

Risk: Generated HTML reports are built from review and model-derived content and are automatically opened by the scripts.

Mitigation: Treat generated reports as untrusted HTML until escaping and report-opening behavior are fixed; open them only in a controlled browser context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/amazon-review-analyzer)
- [RapidAPI Amazon APIs Hub](https://rapidapi.com/hub/amazon)
- [OpenAI-Compatible API Endpoint](https://api.openai.com/v1)
- [DeepSeek API Endpoint](https://api.deepseek.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use mock data for demos; production-style runs require an LLM API key and may use RapidAPI for review collection.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
