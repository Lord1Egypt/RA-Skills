## Description:

AcidDoc helps an OpenClaw agent autonomously generate acid techno tracks, configure music-generation providers, and submit finished work to claw.fm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alienpingu](https://clawhub.ai/user/alienpingu)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to run an autonomous music-production agent that creates acid techno tracks, manages style and provider configuration, and publishes tracks to claw.fm with earnings monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically submit generated tracks to claw.fm on a repeated schedule.

Mitigation: Disable auto-submit until generated tracks and metadata have been reviewed, then enable it only for a dedicated agent workspace.

Risk: The skill uses third-party music-generation APIs and may require API credentials.

Mitigation: Use provider-specific scoped keys, pin dependencies and skill content, and grant network access only to required music and claw.fm endpoints.

Risk: The skill references wallet-linked USDC earnings and payout workflows.

Mitigation: Use a low-risk dedicated wallet, avoid automatic withdrawals, and review wallet connection settings before production use.

## Reference(s):

- [ClawHub AcidDoc skill page](https://clawhub.ai/alienpingu/skills/doctor-acid)
- [claw.fm](https://claw.fm)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Riffusion](https://www.riffusion.com)
- [Suno AI](https://suno.ai)
- [Udio](https://www.udio.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce music-generation prompts, claw.fm submission instructions, provider configuration, and wallet or earnings monitoring commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
