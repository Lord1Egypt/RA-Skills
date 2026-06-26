## Description: <br>
Configure AIsa as a first-class model provider for OpenClaw, enabling production access to major Chinese AI models including Qwen, DeepSeek, Kimi K2.5, and Doubao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure AIsa API access in OpenClaw, select Chinese model providers, compare pricing, switch between Qwen, DeepSeek, Kimi, and Doubao models, and troubleshoot provider setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive AIsa API credentials and includes setup paths that can expose API keys if copied into command history. <br>
Mitigation: Provide AISA_API_KEY through a protected environment variable or secret manager, avoid command-line API-key arguments, and keep the skill enabled only for explicit AIsa setup or troubleshooting. <br>
Risk: Pricing and model availability guidance can become stale because the artifact states that real-time AIsa rates may change. <br>
Mitigation: Confirm current pricing and available model IDs against the AIsa pricing page and model list before using the guidance for cost decisions. <br>
Risk: Kimi K2.5 calls fail when temperature is set to values other than 1.0. <br>
Mitigation: Use the model default or set temperature to 1.0 when configuring Kimi K2.5. <br>


## Reference(s): <br>
- [AIsa Provider on ClawHub](https://clawhub.ai/baofeng-tech/aisa-provider) <br>
- [AIsa Homepage](https://aisa.one) <br>
- [AIsa Pricing](https://marketplace.aisa.one/pricing) <br>
- [Configuration Examples](references/config-examples.md) <br>
- [Pricing Reference](references/pricing.md) <br>
- [Chinese Guide](references/guide-zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY for provider setup and model API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
