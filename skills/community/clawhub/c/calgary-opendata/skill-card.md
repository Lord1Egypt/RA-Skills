## Description: <br>
Access 988+ datasets from the City of Calgary open data portal, with commands to search, fetch, export, and analyze municipal datasets through the Socrata SODA API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, civic technologists, and agents use this skill to discover Calgary open datasets, inspect dataset metadata, and retrieve records for analysis or export. It supports JSON, CSV, and GeoJSON workflows for transit, environment, government, demographics, health, business, and related municipal data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to data.calgary.ca and may be affected by service availability, rate limits, or upstream data changes. <br>
Mitigation: Use the optional Socrata app token for higher limits, keep query limits scoped, and verify important results against the City of Calgary Open Data Portal. <br>
Risk: User-supplied SODA query filters, selections, and ordering can produce incorrect, overly broad, or misleading extracts. <br>
Mitigation: Review dataset metadata and column names before running filtered fetches, start with small limits, and validate exported CSV or GeoJSON before using it in downstream analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raychanpmp/calgary-opendata) <br>
- [City of Calgary Open Data Portal](https://data.calgary.ca) <br>
- [Popular & Useful Calgary Open Data Datasets](references/datasets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command results may be JSON, CSV, GeoJSON, or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses optional SOCRATA_APP_TOKEN for Socrata API rate-limit handling and caches the dataset catalogue locally for one hour.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
