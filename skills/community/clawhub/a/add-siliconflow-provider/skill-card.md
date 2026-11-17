## Description:

Configures SiliconFlow as an OpenClaw model provider with OpenAI-compatible API settings, model definitions, aliases, fallback routing, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jooey](https://clawhub.ai/user/jooey)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw administrators use this skill to add SiliconFlow as a model source, configure selected free, budget, and flagship models, and validate provider connectivity before routing agent traffic through it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw traffic and prompts may be routed through SiliconFlow after the provider and fallback settings are applied.

Mitigation: Install only when SiliconFlow routing is intended, review the provider and fallback configuration before applying it, and confirm organizational approval for the external model provider.

Risk: The SiliconFlow API key is placed into local OpenClaw configuration and could be exposed if the config is shared or committed.

Mitigation: Treat the API key as a secret, keep the OpenClaw configuration out of source control, and rotate the key if exposure is suspected.

Risk: The artifact includes an invitation signup link that may not be the desired enrollment path for all users.

Mitigation: Use a neutral official SiliconFlow signup path instead when referral links are not appropriate.

## Reference(s):

- [SiliconFlow](https://siliconflow.cn)
- [SiliconFlow Documentation](https://docs.siliconflow.cn)
- [SiliconFlow Pricing](https://siliconflow.cn/pricing)
- [SiliconFlow API Key Console](https://cloud.siliconflow.cn/account/ak)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands, code]

**Output Format:** [Markdown with JSON configuration snippets and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for modifying local OpenClaw provider, alias, fallback, and validation configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
