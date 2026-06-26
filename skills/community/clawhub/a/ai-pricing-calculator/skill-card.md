## Description: <br>
AI 模型成本优化器 - 自动计算 API 费用，推荐最优模型，对比 DeepSeek/智谱/通义/GPT 成本。省钱必备工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to compare AI model API pricing, estimate token usage costs, and choose lower-cost model options for common OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pricing and savings recommendations may become stale because the artifact uses static provider prices. <br>
Mitigation: Check the linked provider pricing pages before making purchasing or model-switching decisions. <br>
Risk: The skill provides model-switching guidance that can change future OpenClaw provider behavior when followed. <br>
Mitigation: Review the target provider, pricing, and data-handling terms before editing configuration or running a separate installer skill. <br>
Risk: The documented report command references report.js, but no report.js artifact is present. <br>
Mitigation: Use the included compare.js, calculate.js, and recommend.js commands unless a report script is supplied in a later release. <br>


## Reference(s): <br>
- [AI 价格计算器 on ClawHub](https://clawhub.ai/yang1002378395-cmyk/ai-pricing-calculator) <br>
- [DeepSeek Platform](https://platform.deepseek.com) <br>
- [智谱 AI Open Platform](https://open.bigmodel.cn) <br>
- [DashScope](https://dashscope.aliyun.com) <br>
- [OpenAI Pricing](https://openai.com/pricing) <br>
- [Anthropic Pricing](https://www.anthropic.com/pricing) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses static pricing data from the artifact; users should confirm current provider pricing before acting on recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
