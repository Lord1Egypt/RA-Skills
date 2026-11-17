## Description:

Configures OpenClaw to use SiliconFlow as an OpenAI-compatible model provider, including provider registration, model definitions, aliases, fallback setup, and verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunerw-dev](https://clawhub.ai/user/sunerw-dev)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw administrators use this skill to add SiliconFlow as a third-party model provider, configure recommended model aliases, and optionally add SiliconFlow models to the OpenClaw fallback chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback-chain changes could route future OpenClaw prompts to a third-party provider unexpectedly.

Mitigation: Review and explicitly approve the fallback-chain configuration before applying it, and keep the documented backup so the provider can be removed.

Risk: SiliconFlow API keys could be exposed if stored directly in shared configuration.

Mitigation: Use a protected environment variable or secret store for the API key where possible.

Risk: Sensitive prompts could be sent to a third-party model provider during testing or fallback use.

Mitigation: Avoid testing with sensitive prompts and install the skill only when SiliconFlow routing is intended.

## Reference(s):

- [SiliconFlow documentation](https://docs.siliconflow.cn)
- [SiliconFlow pricing](https://siliconflow.cn/pricing)
- [SiliconFlow website](https://siliconflow.cn)
- [OpenClaw repository](https://github.com/openclaw/openclaw)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/sunerw-dev/skills/add-siliconflow-provider-1)
- [Publisher profile](https://clawhub.ai/user/sunerw-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw provider, alias, fallback, and verification guidance for SiliconFlow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
