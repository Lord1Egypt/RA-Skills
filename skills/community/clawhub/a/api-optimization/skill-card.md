## Description:

Finds free and low-cost AI models and helps configure OpenClaw routing and fallback behavior across SiliconFlow, NVIDIA NIM, OpenRouter, DeepSeek, and Zhipu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenni666](https://clawhub.ai/user/chenni666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to identify free or low-cost model providers and generate cost-aware routing and fallback configuration. It supports normal agent setup workflows where provider choices, fallback order, and budget posture need to be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated OpenClaw configuration can change routing priorities or switch the primary model in savings mode.

Mitigation: Review the generated configuration before applying it, replace any primary-model placeholder with the intended model, and keep a backup of the existing OpenClaw configuration.

Risk: Provider API keys are required for some discovery and health-check flows.

Mitigation: Store provider keys in environment variables, avoid committing them to repositories, and rotate keys if they are exposed.

Risk: The SiliconFlow invitation URL is a referral-style registration link.

Mitigation: Treat the link as a referral and use a direct provider registration path when referral attribution is not desired.

Risk: Free model availability, pricing, and rate limits can change over time.

Mitigation: Run discovery again and review provider pricing or quota information before relying on a generated low-cost routing plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenni666/skills/api-optimization)
- [SiliconFlow documentation](https://docs.siliconflow.cn)
- [SiliconFlow pricing](https://siliconflow.cn/pricing)
- [NVIDIA NIM](https://build.nvidia.com)
- [OpenRouter](https://openrouter.ai)
- [DeepSeek platform](https://platform.deepseek.com/)
- [Zhipu BigModel platform](https://open.bigmodel.cn/)
- [OpenClaw provider documentation](https://docs.openclaw.ai/providers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY for OpenRouter discovery; optional provider keys enable additional model checks.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
