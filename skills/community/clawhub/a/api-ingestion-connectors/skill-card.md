## Description:

Connect to external APIs and ingest data into graph-ready structures for ETL pipelines and knowledge graph construction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design API ingestion connectors that collect REST, GraphQL, and authenticated API data and transform responses into graph-ready nodes, edges, triples, datasets, and ETL configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API requests can expose API keys, bearer tokens, Basic Auth credentials, or OAuth secrets if users place credentials in files, logs, shell history, screenshots, or support messages.

Mitigation: Use environment variables or a secrets manager, apply least-privilege tokens, and redact Authorization, API key, Basic Auth, and OAuth values from outputs and shared materials.

Risk: The helper prepares external API request configurations and does not enforce HTTPS for authenticated endpoints.

Mitigation: Use trusted HTTPS endpoints for authenticated requests and review downstream code that sends generated request configurations.

Risk: Large or rate-limited APIs can fail, throttle, or return incomplete data during ingestion.

Mitigation: Respect API terms and limits, configure retries with exponential backoff, handle pagination deliberately, and validate response schemas before transformation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fisa712/skills/api-ingestion-connectors)
- [ClawHub publisher profile](https://clawhub.ai/user/fisa712)
- [ClawHub homepage](https://clawhub.com)
- [API Connector Design Patterns](references/connector-patterns.md)
- [API Connector Examples](examples/example-connectors.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, shell, Python, GraphQL, Turtle, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces connector patterns, request configurations, transformation mappings, graph-ready node-edge structures, RDF triples, datasets, and ETL pipeline guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
