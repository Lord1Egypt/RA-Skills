## Description:

Amazon 产品全链路深度研究助手，可从一句产品名、ASIN或描述自动完成产品搜索、评论采集、AI情感打标、关键词扩展、VOC痛点聚类、竞品分析、新品机会分析，并生成交互式HTML可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, product researchers, and ecommerce operators use this skill to investigate Amazon product categories, compare competitors, identify review-derived pain points, expand keywords, and evaluate new product opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send product ideas, review text, and LLM API credentials to a configured OpenAI-compatible provider endpoint.

Mitigation: Use only trusted HTTPS provider endpoints, avoid unknown api_base values, and provide credentials with the minimum scope needed for the run.

Risk: Generated reports may include content derived from live marketplace data and are automatically opened as local HTML.

Mitigation: Prefer mock mode for demonstrations and review generated HTML from live data carefully until the escaping issue identified by the security scan is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/amazon-product-research)
- [Amazon APIs on RapidAPI](https://rapidapi.com/hub/amazon)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, HTML files]

**Output Format:** [Markdown guidance with shell commands, Python-driven analysis output, and generated interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use mock data without API keys; live analysis can call RapidAPI and an OpenAI-compatible LLM endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
