## Description:

Research observed Steam price history and compare current game editions or PlayStation offers using Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Players and game-price researchers use this skill to compare dated Steam price observations with current Steam or PlayStation offers, keeping editions, regions, currencies, and subscription conditions distinct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora queries can expose search terms and consume API credits.

Mitigation: Keep the API key private and limit request counts and page sizes to the research scope.

Risk: Incomplete price history or unmatched editions can yield misleading comparisons.

Mitigation: Identify the exact offer and currency, report observed dates and gaps, and separate current offers from stored history.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/game-price-history-research)
- [Crawlora endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown price research brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dated observations, currencies, edition and region distinctions, coverage gaps, and source links when available.]

## Skill Version(s):

1.0.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
