## Description:

Access 988+ datasets from the City of Calgary open data portal; search, fetch, and analyze city data on transit, environment, government, demographics, business, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to discover City of Calgary open datasets, inspect dataset metadata, and fetch public records through the Socrata API for analysis or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a bundled Python CLI that contacts data.calgary.ca.

Mitigation: Review planned commands before execution and allow network access only when the task requires live City of Calgary data.

Risk: The optional SOCRATA_APP_TOKEN is sent to the City of Calgary Socrata API when configured.

Mitigation: Use the token only when needed for rate-limit handling and avoid sharing sensitive or broad-scope credentials.

Risk: The CLI may create a local cache of the public dataset catalog.

Mitigation: Inspect or remove the script-local cache when cache retention is not desired.

## Reference(s):

- [City of Calgary Open Data Portal](https://data.calgary.ca)
- [Popular & Useful Calgary Open Data Datasets](references/datasets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON, CSV, or GeoJSON data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact data.calgary.ca and may create a small local cache; SOCRATA_APP_TOKEN is optional.]

## Skill Version(s):

1.0.2 (source: server release evidence, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
