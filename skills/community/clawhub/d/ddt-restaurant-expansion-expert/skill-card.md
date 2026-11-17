## Description:

Helps restaurant brand expansion and site-selection teams analyze published store snapshots for regional growth, competitor density near candidate sites, and practical location risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant expansion managers, site-selection teams, and brand leaders use this skill to identify opportunity cities, compare candidate addresses, assess nearby competitors, and decide what to validate next in the field.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brand or location queries are sent to the gotoshop-ai.com API.

Mitigation: Use the skill only when users are comfortable sharing those business queries with that service.

Risk: The API key could be exposed if pasted into chat or output.

Mitigation: Keep DDT_API_KEY in a local environment variable and never include the key in model-visible messages.

Risk: Users may try to extract bulk store lists or treat limited previews as complete directories.

Mitigation: Follow the skill's aggregate-first workflow and built-in preview limits; ask users to narrow the requested brand, area, date, or store when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-restaurant-expansion-expert)
- [DDT restaurant expansion homepage](https://gotoshop-ai.com/ddtclaw/)
- [DDT API key setup](https://gotoshop-ai.com/ddtclaw/open)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, limited detail checks, and follow-up validation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DDT_API_KEY environment variable and uses aggregate-first API results before any limited store-level lookups.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
