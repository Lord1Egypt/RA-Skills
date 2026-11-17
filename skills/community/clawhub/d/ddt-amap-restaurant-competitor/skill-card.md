## Description:

Analyzes restaurant competitor network changes, priority regions, and market action recommendations from DDT published store snapshots using copied Amap place and address text as location input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External business, market, and sales users use this skill to compare published restaurant brand store-network snapshots, identify expansion or contraction patterns, inspect priority regions, and produce actionable competitor-intelligence summaries. The skill also supports limited address-based checks when the user provides specific Amap place or address text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brand, place, or address queries are sent to the external GotoShop/DDT service.

Mitigation: Confirm the service is acceptable for the intended workflow and avoid submitting sensitive private locations unless they are necessary for the analysis.

Risk: Exposing DDT_API_KEY could allow unauthorized use of the external API.

Mitigation: Store the API key only in a local environment variable and do not paste, print, or include it in generated responses.

Risk: Incomplete coverage, truncated previews, or unavailable capabilities can make competitor conclusions misleading.

Mitigation: Use the published coverage period, capability flags, response status, and preview truncation markers; narrow the query or stop the conclusion when the required data is unavailable.

## Reference(s):

- [GotoShop/DDT ClawHub integration homepage](https://gotoshop-ai.com/ddtclaw/)
- [GotoShop/DDT API key setup](https://gotoshop-ai.com/ddtclaw/open)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-amap-restaurant-competitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise findings, key metrics, coverage notes, caveats, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY and the GotoShop/DDT service; store-level previews are intentionally limited and should be narrowed with specific brand, address, date, or geography inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
