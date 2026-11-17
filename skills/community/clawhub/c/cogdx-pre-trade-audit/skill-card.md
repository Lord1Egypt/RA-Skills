## Description:

Verify trading reasoning with cognitive diagnostics before executing trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to check prediction-market trade reasoning for logical fallacies, calibration issues, and reasoning gaps before deciding whether to proceed. It can return an audit verdict and, when explicitly run live, submit a Polymarket trade through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real prediction-market trades when live execution is enabled.

Mitigation: Keep dry-run mode enabled unless intentional, use a least-privilege Simmer API key with strict account limits, and review audit results before enabling live trades.

Risk: Trade reasoning may contain confidential strategy or personal data that is sent to the CogDx API for processing.

Mitigation: Avoid submitting confidential or personal information in the reasoning field unless the operator accepts external CogDx processing.

Risk: The artifact declares a managed cron schedule that is not explained in the user-facing instructions.

Mitigation: Review scheduled execution behavior before deployment and disable or constrain automation where unattended trade checks are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drkavner/skills/cogdx-pre-trade-audit)
- [Cerebratech CogDx API](https://api.cerebratech.ai)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Python dictionary or JSON-formatted CLI output with audit status, issues, recommendation, and optional trade details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live trading requires the live flag and a Simmer API key.]

## Skill Version(s):

1.0.0 (source: server evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
