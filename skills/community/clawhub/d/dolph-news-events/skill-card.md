## Description:

Monitors premium RSS feeds for breaking news, matches stories to Polymarket markets via keyword analysis, and can generate or execute trade signals when estimated price impact exceeds 12%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this automaton to monitor breaking news feeds and produce Polymarket trade signals, with live trading available when explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real financial trades from RSS-driven heuristics without per-trade approval.

Mitigation: Run in dry-run first, use a dedicated low-privilege API key in an isolated environment, keep trade sizes small, and require review or exposure limits before enabling live trading.

Risk: Feed validation, dependency pinning, and state-file handling need review before unattended operation.

Mitigation: Validate RSS sources, pin dependencies, review the state-file behavior, and use strict venue settings before scheduled or live deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-news-events)
- [ClawHub publisher profile](https://clawhub.ai/user/richducat)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration]

**Output Format:** [Console text and API trade requests from a Python automaton]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live mode can place trades when --live is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
