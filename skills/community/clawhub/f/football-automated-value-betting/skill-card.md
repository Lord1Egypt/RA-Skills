## Description:

Automates real-time football value-betting analysis for Singbet Asian Handicap markets using live odds and in-play match data.

This skill is for research and development only.

## Publisher:

[hga030888-blip](https://clawhub.ai/user/hga030888-blip)

### License/Terms of Use:


## Use Case:

External users can use this skill to monitor live football odds, assess Asian Handicap or totals value, and produce betting rationale, execution requests, and activity summaries with stated daily stake limits.

### Deployment Geography for Use:

Global, subject to local sports-betting laws and platform availability.

## Known Risks and Mitigations:

Risk: The skill is framed around automated real-money-style sports betting and does not provide clear user confirmation before execution.

Mitigation: Require explicit user approval before any wager-related action and confirm that use complies with local law and platform terms.

Risk: The artifact can report a successful bet even though the security evidence says transaction verification is not reliable.

Mitigation: Treat placement messages as unverified and confirm wager status directly in the betting account or official platform record.

Risk: The artifact includes an exposed API key in configuration.

Mitigation: Replace exposed credentials before use and manage secrets outside the skill artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hga030888-blip/skills/football-automated-value-betting)
- [The Odds API](https://the-odds-api.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or plain text with JSON-like live-odds data, betting rationale, status messages, and activity summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include betting execution status messages that should be independently verified against the user's betting account.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact configuration)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
