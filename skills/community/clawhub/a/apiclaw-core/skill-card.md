## Description:

ZooData is an API endpoint reference and bundled client for agent access to ZooData commerce and keyword-intelligence data, including endpoint inputs, response fields, authentication, credit tracking, and local review-toolkit behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to understand and call ZooData endpoints for Amazon product, market, competitor, review, price-band, brand, history, and keyword-intelligence lookups. It is suited for data-backed commerce analysis workflows that require endpoint selection, parameter guidance, API-key authentication, and credit-aware execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live API calls use a user-provided ZooData API key and may spend account credits.

Mitigation: Configure credentials intentionally, prefer ZOODATA_API_KEY for short sessions, and ask the agent to estimate and confirm cost before broad or ambiguous multi-call scans.

Risk: Persisted credentials in ~/.zoodata/config.json could be exposed if local file permissions are too broad.

Mitigation: Keep the local credential file private and use restrictive directory and file permissions when persistent storage is needed.

Risk: Endpoint parameters and live API field names may change, causing failed calls or misleading analysis if stale schemas are used.

Mitigation: Use the bundled references and current ZooData OpenAPI specification for endpoint selection, supported parameters, and response-field interpretation.

## Reference(s):

- [ZooData skill page](https://clawhub.ai/apiclaw/skills/zoodata)
- [ZooData API keys](https://zoodata.ai/en/api-keys)
- [ZooData OpenAPI specification](https://zoodata.ai/api/v1/openapi-spec)
- [ZooData Skills homepage](https://github.com/SerendipityOneInc/ZooData-Skills)
- [CLI contract](references/cli-contract.md)
- [OpenAPI reference](references/openapi-reference.md)
- [ZooData API field reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY for live API calls; each API call may consume ZooData account credits.]

## Skill Version(s):

1.1.9 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
