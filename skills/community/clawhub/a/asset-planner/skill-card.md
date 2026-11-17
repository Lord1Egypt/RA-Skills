## Description:

Asset Planner (规划虾) is an AI financial advisor that analyzes asset allocation screenshots and generates rebalancing strategies based on the All-Weather Portfolio and S&P Asset Quadrant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wltongxue](https://clawhub.ai/user/wltongxue)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to consolidate personal portfolio screenshots, classify holdings, assess allocation health, and generate rebalancing guidance. The workflow is tailored to China-market personal investing and uses a four-layer allocation model informed by S&P-style asset quadrants and All-Weather portfolio concepts.

### Deployment Geography for Use:

Global, with content tailored to China-market personal investing

## Known Risks and Mitigations:

Risk: Users may share sensitive financial screenshots, account details, portfolio amounts, or historical allocation data.

Mitigation: Remove account identifiers before upload and avoid retaining financial history unless the user explicitly requests it.

Risk: The skill can produce specific trading steps, product names, fund codes, and allocation amounts that may be unsuitable or incorrect for the user.

Mitigation: Treat outputs as allocation calculations and information organization only; independently verify products, fees, tax effects, suitability, and amounts before trading.

Risk: Screenshot recognition or asset classification errors could distort health scores and rebalancing guidance.

Mitigation: Ask the user to confirm extracted assets and missing holdings before generating the final analysis.

## Reference(s):

- [AI 资产配置助手 底层知识库 & SOP](references/knowledge-base.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown conversation with tables, ranked findings, and action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include asset classifications, health scores, rebalancing amounts, product names, fund codes, platform-specific steps, and investment disclaimers.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
