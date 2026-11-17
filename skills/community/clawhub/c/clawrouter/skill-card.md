## Description:

Clawrouter is a hosted-gateway LLM router and local proxy that forwards requests to the blockrun.ai gateway for model routing, paid inference, market data, image/video generation, and prediction-market tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1bcmax](https://clawhub.ai/user/1bcmax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to install and configure Clawrouter as an OpenClaw model provider that routes LLM calls through blockrun.ai and exposes paid data and media-generation tools. It is for hosted inference workflows, not local-only inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and request parameters are sent to the blockrun.ai hosted gateway for inference.

Mitigation: Do not use the skill for workloads that require local-only inference, and avoid sending data you would not share with a hosted LLM provider.

Risk: The skill installs an external npm package whose published contents may differ by version.

Mitigation: Verify the exact npm package version and compare it with the declared release before installation.

Risk: The OpenClaw configuration stores generated wallet signing keys in plaintext.

Mitigation: Protect the OpenClaw config file as sensitive key material, use disk encryption where appropriate, and rotate keys if the host is compromised.

Risk: Automatic per-request payments can spend funds from the configured wallet.

Mitigation: Use a dedicated low-balance wallet funded only with the amount intended for LLM and tool calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1bcmax/skills/clawrouter)
- [Clawrouter Homepage](https://blockrun.ai/clawrouter.md)
- [Declared Source Repository](https://github.com/BlockRunAI/ClawRouter)
- [npm Package](https://www.npmjs.com/package/@blockrun/clawrouter)
- [BlockRun Privacy](https://blockrun.ai/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw model-provider setup, package-install commands, and agent tool usage guidance.]

## Skill Version(s):

0.12.171 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
