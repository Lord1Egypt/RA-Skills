## Description:

A Python technical analysis skill based on 100 popular TradingView Pine Script indicators, providing indicator calculation, analysis, and visualization support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-analysis users use this skill to request technical indicator calculations, analysis, and visualization based on converted TradingView Pine Script indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can send task text, trading context, conversation identifiers, and Prana API credentials to a configurable Prana endpoint.

Mitigation: Install only when Prana and the configured HTTPS endpoint are trusted, and avoid sending sensitive trading or account data.

Risk: The wrapper can auto-fetch and save Prana credentials in local plaintext configuration files.

Mitigation: Prefer environment variables or a secret manager, and disable automatic key fetching or disk writes in sensitive environments.

Risk: Generic account, email, or phone environment variables may be used while fetching Prana API keys.

Mitigation: Avoid exposing unrelated identity environment variables to the skill runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luokeer52/skills/100-indicators-analysis)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown or plain text returned through the Prana wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote execution may require Prana API credentials and a reachable HTTPS Prana endpoint.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
