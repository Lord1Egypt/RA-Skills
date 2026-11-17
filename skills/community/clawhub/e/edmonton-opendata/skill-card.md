## Description:

Access City of Edmonton open data through a Bash-invoked CLI that searches, lists, fetches, and exports Socrata datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and civic-data users use this skill to discover City of Edmonton datasets, inspect dataset metadata, and retrieve public data for analysis or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports contain remote public data and can be unsafe when opened directly in spreadsheet applications.

Mitigation: Prefer JSON output for analysis, or sanitize exported CSV files before opening them in spreadsheet tools.

Risk: The helper contacts data.edmonton.ca and caches the public dataset catalog locally.

Mitigation: Use the skill only in environments where outbound access to data.edmonton.ca and local catalog caching are acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/raychanpmp/skills/edmonton-opendata)
- [City of Edmonton Open Data Portal](https://data.edmonton.ca)
- [Curated Edmonton dataset examples](references/datasets.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI output in JSON, CSV, or GeoJSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact data.edmonton.ca and may cache the public dataset catalog locally.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
