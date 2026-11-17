## Description:

Find markets where Simmer's AI consensus diverges from the real market price, then trade on the mispriced side using Kelly sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to scan prediction markets for divergence between Simmer AI consensus and external market prices, report candidate opportunities, and optionally execute bounded trades when live mode is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute live trades using a Simmer trading API key.

Mitigation: Keep the skill in dry-run until the API key scope, venue, per-trade limit, daily budget, and live-mode settings have been reviewed.

Risk: Financial losses may occur if divergence signals, market prices, fees, or safeguards are inaccurate or stale.

Mitigation: Use conservative trade limits, review candidate trades before enabling live mode, and monitor fee filtering, position checks, and daily spend controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-ai-divergence)
- [Simmer API](https://api.simmer.markets)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, API calls]

**Output Format:** [Console text or JSON reports with optional trade execution through the Simmer SDK]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run unless live mode or a simulated venue is selected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
