## Description:

Researches global news and US television coverage through Crawlora's GDELT search, context, timeline, and sentiment endpoints, returning structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, journalists, and media-monitoring teams use this skill to compare global news and US television coverage, track volume and tone over time, and examine sentence-level context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and filters are sent to Crawlora with API-key-authenticated requests.

Mitigation: Use only queries suitable for disclosure to Crawlora; omit secrets, credentials, private identifiers, and highly sensitive investigative content.

Risk: Exposing the Crawlora API key could allow unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY in the environment and do not commit it or place it in query parameters.

## Reference(s):

- [GDELT endpoint reference](reference/endpoints.md)
- [Crawlora API and access](https://crawlora.net)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/gdelt-research)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON data]

**Output Format:** [Markdown guidance and shell commands; JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected GDELT endpoint and query filters.]

## Skill Version(s):

1.0.15 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
