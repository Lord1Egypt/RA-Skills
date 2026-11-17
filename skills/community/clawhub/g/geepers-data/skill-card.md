## Description:

Fetch structured data from 17 authoritative APIs, including arXiv, Census Bureau, GitHub, NASA, Wikipedia, PubMed, news, weather, finance, and FEC, through a single endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeslp](https://clawhub.ai/user/lukeslp)

### License/Terms of Use:


## Use Case:

Developers, researchers, and analysts use this skill to discover available data sources and request structured external data for research, visualizations, pipelines, and dataset enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and selected data-source requests are sent to the third-party api.dr.eamer.dev service.

Mitigation: Avoid sending secrets, private data, or sensitive business context unless the provider and its data handling terms have been separately vetted.

Risk: The skill requires a DREAMER_API_KEY for API access.

Mitigation: Store the API key as a secret environment variable and avoid committing or sharing it in prompts, logs, examples, or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukeslp/skills/geepers-data)
- [Dreamer Data API](https://api.dr.eamer.dev)
- [List available data sources](https://api.dr.eamer.dev/v1/data)
- [Search data sources endpoint](https://api.dr.eamer.dev/v1/data/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline HTTP examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DREAMER_API_KEY and sends data-source queries to api.dr.eamer.dev.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
