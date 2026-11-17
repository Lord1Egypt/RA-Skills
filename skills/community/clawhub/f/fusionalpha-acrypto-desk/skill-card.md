## Description:

A dual-market A-share and crypto analysis skill that produces data-anchored Markdown reports, trading-plan style summaries, and morning briefings from user-provided or script-fetched JSON evidence.

This skill is for research and development only.

## Publisher:

[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate structured A-share, crypto, and morning-market analysis from explicit market data. The README states the outputs are for research and learning only and are not investment, legal, or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate trading-plan style market reports that may be mistaken for financial advice.

Mitigation: Use outputs for research and learning only, require explicit evidence lists, and independently review decisions before acting.

Risk: Helper scripts fetch network data and may return partial or unavailable fields when upstream sources fail.

Mitigation: Review `meta.errors`, treat missing data as a limitation, and avoid conclusions not supported by at least two concrete input fields.

Risk: CryptoPanic credentials may be supplied through environment or command-line workflows.

Mitigation: Prefer `CRYPTOPANIC_TOKEN` only for explicit news fetches, avoid command-line token arguments, and do not echo or store credentials.

Risk: Bootstrap installs Python dependencies before helper scripts can run.

Mitigation: Review `scripts/requirements.txt` and the bootstrap behavior before installing dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinyuqinfeng/skills/fusionalpha-acrypto-desk)
- [Data Sources & How to Fetch](references/data_sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with evidence lists and optional JSON-producing shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit input data for market conclusions; helper scripts can fetch public market data and optional CryptoPanic news.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
