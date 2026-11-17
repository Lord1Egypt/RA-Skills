## Description:

Configures AIsa as an OpenClaw model provider for access to Chinese AI models including Qwen, DeepSeek, Kimi K2.5, and Doubao.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure AIsa API credentials, provider settings, model selection, pricing checks, and troubleshooting for OpenClaw-compatible workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model prompts and outputs may be routed through the third-party AIsa provider.

Mitigation: Use the skill only for workloads approved for AIsa routing, and review provider defaults before sending sensitive requests.

Risk: API keys can be exposed through command-line arguments, shell history, or committed configuration.

Mitigation: Prefer interactive onboarding, environment variables, or a secure credential store, and avoid pasting real keys into CLI arguments or static config examples.

Risk: Pricing, model IDs, and provider availability can change after publication.

Mitigation: Check AIsa's live pricing and model list before relying on cost estimates or configuring production model IDs.

Risk: Kimi K2.5 requests fail when temperature is set to a value other than 1.0.

Mitigation: Use the model default or explicitly set temperature to 1.0 when routing requests to Kimi K2.5.

## Reference(s):

- [AIsa Provider Configuration Examples](references/config-examples.md)
- [AIsa Pricing Reference](references/pricing.md)
- [AIsa Chinese Usage Guide](references/guide-zh-CN.md)
- [AIsa homepage](https://aisa.one)
- [AIsa real-time pricing](https://marketplace.aisa.one/pricing)
- [AIsa marketplace](https://marketplace.aisa.one/)
- [AIsa models endpoint](https://api.aisa.one/v1/models)
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/aisa-provider)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY for provider setup; pricing and model availability should be checked against AIsa before use.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
