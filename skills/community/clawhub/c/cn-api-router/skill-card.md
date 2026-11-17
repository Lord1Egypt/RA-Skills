## Description:

国内 AI 模型 API 配置向导，帮助 OpenClaw 用户配置 DeepSeek、通义千问、智谱GLM、Moonshot、百川、零一万物等国内大模型 API，并生成可合并的 OpenClaw provider 配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironmanc2014](https://clawhub.ai/user/ironmanc2014)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate and apply provider configuration for Chinese AI model APIs, add backup models, switch defaults, and compare provider cost options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose real provider API keys through command arguments, visible input, printed JSON, or agent transcripts.

Mitigation: Review the skill before installation, avoid passing keys through --api-key where possible, treat generated output as sensitive, and rotate any key pasted into or captured by the workflow.

## Reference(s):

- [Provider configuration details](references/providers.md)
- [ClawHub skill page](https://clawhub.ai/ironmanc2014/skills/cn-api-router)
- [DeepSeek platform](https://platform.deepseek.com)
- [Alibaba Cloud DashScope](https://dashscope.aliyun.com)
- [Zhipu GLM platform](https://open.bigmodel.cn)
- [Moonshot platform](https://platform.moonshot.cn)
- [Baichuan platform](https://platform.baichuan-ai.com)
- [01.AI platform](https://platform.lingyiwanwu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated provider configuration can contain real API keys and should be handled as sensitive output.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
