## Description: <br>
Helps agents discover and configure free or very low-cost AI models with task-aware routing and fallback chains across SiliconFlow, NVIDIA NIM, OpenRouter, DeepSeek, and Zhipu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenni666](https://clawhub.ai/user/chenni666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find lower-cost model options, generate routing and fallback configuration, and decide when to use free models versus a primary paid model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated routing or fallback configuration can change which providers handle future AI requests. <br>
Mitigation: Review the generated provider list and selected mode before applying configuration. <br>
Risk: Generated configuration may contain placeholders or provider choices that do not match the user's account setup. <br>
Mitigation: Replace placeholders, confirm API keys and provider access, and keep the backup before patching OpenClaw configuration. <br>
Risk: Health checks and future prompts may reach SiliconFlow, OpenRouter, NVIDIA, DeepSeek, or Zhipu depending on mode and configuration. <br>
Mitigation: Confirm the chosen providers are acceptable for the data being routed before enabling monitoring or fallback behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenni666/api-optimization) <br>
- [NVIDIA NIM model catalog](https://build.nvidia.com) <br>
- [OpenRouter API keys](https://openrouter.ai/settings/keys) <br>
- [SiliconFlow documentation](https://docs.siliconflow.cn) <br>
- [SiliconFlow pricing](https://siliconflow.cn/pricing) <br>
- [DeepSeek platform](https://platform.deepseek.com/) <br>
- [Zhipu BigModel platform](https://open.bigmodel.cn/) <br>
- [OpenClaw provider documentation](https://docs.openclaw.ai/providers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate OpenClaw routing and fallback JSON for royal, balanced, or savings mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
