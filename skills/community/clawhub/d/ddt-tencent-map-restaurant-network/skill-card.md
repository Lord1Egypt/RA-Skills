## Description:

Analyzes restaurant brand openings, closures, regional expansion, competitor density, and candidate site opportunities from Tencent Map address text using published Diandiantong store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, restaurant expansion teams, and sales teams use this skill to turn pasted Tencent Map place or address text and Diandiantong snapshots into restaurant network, competitor, and site-screening analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may send pasted restaurant or address text to the Diandiantong/gotoshop-ai API.

Mitigation: Confirm users are comfortable using that external API and avoid sending sensitive or confidential locations.

Risk: DDT_API_KEY can grant API access if exposed.

Mitigation: Keep the key in local environment variables and never paste or display it in chat or generated output.

Risk: Business conclusions rely on published snapshot analysis, not official Tencent Map data or verified financial performance.

Mitigation: Report the coverage period and data basis, and avoid claims about official opening dates, closures, revenue, profit, AUV, or closure reasons.

## Reference(s):

- [Diandiantong homepage](https://gotoshop-ai.com/ddtclaw/)
- [Diandiantong API key setup](https://gotoshop-ai.com/ddtclaw/open)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-restaurant-network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise findings, key metrics, coverage notes, and optional bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY; uses published snapshot data and restricted preview endpoints when appropriate.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
