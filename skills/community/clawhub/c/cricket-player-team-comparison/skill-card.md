## Description:

Compare cricket player and team records using Crawlora Cricinfo data while preserving match format, filters, and source context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Cricket analysts and developers use this skill to compare player or team batting, bowling, and fielding statistics across defined match formats and date ranges, with source context and denominators preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cricket query values and source identifiers are sent to Crawlora.

Mitigation: Use only relevant public cricket data in query values and avoid private or unrelated information.

Risk: Access requires a Crawlora API key.

Mitigation: Provide a scoped key and keep it out of shared outputs.

Risk: Incomplete tables or incompatible match formats can produce misleading comparisons.

Mitigation: Limit requests to the needed scope, preserve filters and table definitions, and disclose missing or truncated results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/cricket-player-team-comparison)
- [Cricinfo endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown comparison tables and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes match-class filters, units, denominators, source references, and coverage limitations.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
