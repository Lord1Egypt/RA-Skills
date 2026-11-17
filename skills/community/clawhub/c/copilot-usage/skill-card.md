## Description:

Display GitHub Copilot premium request usage, quota, billing stats, and per-model multipliers for the authenticated user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitman86r](https://clawhub.ai/user/hitman86r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GitHub Copilot users use this skill to review premium request usage, remaining configured quota, overage costs, and per-model usage for personal, Business, or Enterprise plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The alert command has a command-execution vulnerability according to the authoritative security evidence.

Mitigation: Review or patch scripts/copilot-alert.sh before installing or using the alert command, especially in automation.

Risk: The skill requires GitHub CLI authentication with billing-related scopes and uses a classic token path.

Mitigation: Use the skill only where that account access is acceptable, and verify gh authentication scopes before execution.

Risk: The skill writes and reads a local plan and quota configuration file because the GitHub API does not expose plan quota.

Mitigation: Confirm the configured plan and quota before relying on remaining-quota or alert results.

## Reference(s):

- [GitHub REST Billing Usage API](https://docs.github.com/en/rest/billing/usage)
- [GitHub Copilot Model Multipliers](https://docs.github.com/en/copilot/concepts/billing/copilot-requests#model-multipliers)
- [API Reference](references/api.md)
- [Model Multipliers](references/multipliers.md)
- [Copilot Usage on ClawHub](https://clawhub.ai/hitman86r/skills/copilot-usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal text and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local plan and quota configuration file under ~/.config/copilot-usage/config.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
