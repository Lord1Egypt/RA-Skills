## Description:

FreeRide Gateway helps an agent detect and use a local OpenAI-compatible FreeRide gateway to route chat-completion workloads across configured free-tier providers with failover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaivpidadi](https://clawhub.ai/user/shaivpidadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure OpenAI-compatible clients against a local FreeRide gateway, discover models, diagnose provider and key failures, and understand failover and telemetry behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing via a remote shell script, which can execute unverified code.

Mitigation: Inspect the installer or use a verifiable package before running installation commands.

Risk: Troubleshooting commands can expose provider API keys if environment variables are printed directly.

Mitigation: Redact secrets before sharing command output or logs.

Risk: Telemetry is enabled by default and sends installation and usage metadata hourly.

Mitigation: Turn telemetry off when installation or usage metadata should not be sent.

Risk: AI prompts routed through FreeRide may be sent to configured external providers.

Mitigation: Confirm the configured providers are acceptable for the data being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaivpidadi/skills/freeride-gateway)
- [Publisher profile](https://clawhub.ai/user/shaivpidadi)
- [FreeRide Gateway on PyPI](https://pypi.org/project/freeride-gateway/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, configuration examples, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may involve routing prompts through external configured providers and handling provider failover.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
