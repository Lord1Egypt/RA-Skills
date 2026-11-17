## Description:

Enables OpenAI Codex CLI to use domestic Chinese AI models through protocol conversion and automated configuration across providers such as Qwen, Kimi, and GLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckkiven](https://clawhub.ai/user/luckkiven)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure Codex CLI to route requests through a local protocol bridge for supported Chinese model providers. It helps install, start, test, stop, and troubleshoot the bridge and related Codex configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation relies on mutable, unreviewed remote code that handles API keys, Codex configuration, and model traffic.

Mitigation: Review the upstream repository and installer before installing, and prefer a pinned commit or release with a verified digest.

Risk: Prompts and code may be sent to configured third-party model providers.

Mitigation: Use the bridge only with prompts and code that are appropriate to share with the selected providers.

Risk: Provider API keys are sensitive credentials used by the bridge.

Mitigation: Store keys in protected environment variables or local .env files, keep them out of version control, and rotate them if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luckkiven/skills/codex-cn-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include instructions that affect Codex CLI configuration, local service control, and provider API key handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
