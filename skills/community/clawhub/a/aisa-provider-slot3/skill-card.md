## Description:

Configure AIsa as an OpenAI-compatible provider endpoint for OpenClaw and related runtimes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an AIsa OpenAI-compatible provider endpoint, set AISA_API_KEY, select model IDs, and troubleshoot routing for OpenClaw-compatible runtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes model requests and potentially sensitive data to the external AIsa gateway.

Mitigation: Confirm trust in AIsa and verify current retention, routing, privacy, and provider terms before sending sensitive or regulated data.

Risk: AISA_API_KEY is a sensitive credential that could be exposed through shell history, logs, or shared configuration.

Mitigation: Use a dedicated revocable API key, prefer environment variables or interactive onboarding, and avoid printing or pasting the real secret in shared output.

Risk: Model availability, pricing, account limits, and model-specific constraints can change over time.

Mitigation: Check the current AIsa model catalog, pricing page, and API documentation before production use or purchasing decisions.

## Reference(s):

- [AIsa Provider on ClawHub](https://clawhub.ai/aisadocs/skills/aisa-provider-slot3)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://aisa.one/docs/api-reference)
- [AIsa Pricing](https://marketplace.aisa.one/pricing)
- [AIsa Provider Configuration Examples](references/config-examples.md)
- [AIsa Provider Chinese Guide](references/guide-zh-CN.md)
- [AIsa Pricing Notes](references/pricing.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and routes configured model requests to the external AIsa OpenAI-compatible endpoint.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
