## Description:

Search Bing Maps for places or map results through the Dataify Bing Maps API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn natural-language Bing Maps place searches into Dataify API requests and return map search results, JSON, or HTML when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This is a read-only map search skill, but its token instructions are inconsistent and could lead users to expose a Dataify API token.

Mitigation: Review before installing. Use only if you are comfortable sending Bing Maps queries and any coordinates you provide to Dataify. Configure DATAIFY_API_TOKEN through a local environment variable or secure runtime secret, not by pasting it into chat and not with the --token command-line option; rotate the token if it was previously shared in chat or shell history.

## Reference(s):

- [Dataify Bing Maps API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-bing-maps)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance]

**Output Format:** [Markdown summaries by default, with raw JSON or HTML when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, result counts, truncation notes, or token setup guidance when authentication is missing.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
