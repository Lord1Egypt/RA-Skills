## Description:

Ball Ranks AI fantasy football (NFL) and fantasy basketball (NBA) rankings and projections for agents. Use for weekly NFL start/sit by position (QB, RB, WR, TE, K, DST) in PPR, half-PPR, or standard scoring; season draft boards for both sports; and player rank and projection lookups, via the read-only Ball Ranks MCP server or REST API. Model Zero works without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ollynov](https://clawhub.ai/user/ollynov)

### License/Terms of Use:

MIT-0

## Use Case:

External fantasy sports players use this skill to look up and compare published NFL and NBA season rankings, player projections, and weekly NFL start/sit rankings by position and scoring format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional API key is a secret credential.

Mitigation: Only send it to Ball Ranks as an Authorization Bearer token; keep it out of URLs, logs, answers, and committed files.

## Reference(s):

- [Ball Ranks Developer Documentation](https://ballranks.com/developers)
- [Ball Ranks OpenAPI Schema](https://ballranks.com/openapi.json)
- [Ball Ranks MCP Server](https://ballranks.com/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Rankings and projections]

**Output Format:** [Natural-language answers with Ball Ranks source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses published rankings and projections; football scoring format and basketball scoring mode are identified when relevant.]

## Skill Version(s):

1.0.2 (source: frontmatter; server-resolved release 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
