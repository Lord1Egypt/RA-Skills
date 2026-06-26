## Description: <br>
AI model cost optimizer that calculates API fees, recommends lower-cost models, and compares DeepSeek, Zhipu, Tongyi, GPT, Claude, and related model pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and teams use this skill to estimate AI API token costs, compare model pricing, and choose cost-effective models for common workloads. It also provides guidance for reviewing model provider choices and OpenClaw configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model prices can change after release, making embedded cost comparisons inaccurate. <br>
Mitigation: Treat recommendations as advisory and verify pricing against the linked provider pricing pages before making purchasing or routing decisions. <br>
Risk: Suggested OpenClaw configuration changes could route usage to a different model provider than intended. <br>
Mitigation: Review configuration edits before applying them and confirm provider, model ID, billing, and data-handling expectations. <br>
Risk: The documentation mentions a report command, but the artifact evidence does not include a matching report.js file. <br>
Mitigation: Use the included compare, calculate, and recommend scripts unless the missing report command is supplied in a later release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/ai-cost-optimizer-cn) <br>
- [DeepSeek platform pricing](https://platform.deepseek.com) <br>
- [Zhipu AI platform](https://open.bigmodel.cn) <br>
- [Alibaba Cloud DashScope](https://dashscope.aliyun.com) <br>
- [OpenAI pricing](https://openai.com/pricing) <br>
- [Anthropic pricing](https://www.anthropic.com/pricing) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory pricing estimates based on embedded model price tables; does not call provider APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
