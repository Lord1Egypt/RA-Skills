## Description:

Use local All Routes APIs, repo-backed handlers, and optional local MCP for airport, airline, route-map, timetable-context, and dataset-health lookups without hosted credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for local, credential-free airport, airline, route-map, timetable-context, and dataset-health lookups. It is best suited to route discovery that must stay grounded in local All Routes surfaces or offline repository inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may try to use hosted services, hosted credentials, or arbitrary web scraping when local surfaces are the intended path.

Mitigation: Use local All Routes web APIs, optional localhost MCP, or offline code inspection; do not require hosted tokens or scrape third-party route sites.

Risk: Offline or code-backed route answers may be mistaken for live endpoint results.

Mitigation: Label each answer as coming from local API output, local MCP, or offline code inspection, and preserve unsupported filters as visible limitations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skylinehk/skills/all-routes-offline)
- [Local Surfaces](artifact/references/local-surfaces.md)
- [Query Normalization](artifact/references/query-normalization.md)
- [Filter Intelligence](artifact/references/filter-intelligence.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with local API paths, local MCP surface names, shell commands, applied-filter notes, and source-labeling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label whether answers come from local API responses, local MCP, or offline code inspection.]

## Skill Version(s):

1.3.24 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
