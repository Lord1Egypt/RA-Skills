## Description: <br>
Access 2,179+ datasets from the City of Edmonton open data portal to search, fetch, and analyze city data on transit, traffic, environment, census, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and civic-data users use this skill to discover City of Edmonton datasets, inspect dataset metadata, fetch filtered rows, and export results for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper runs Python commands that contact data.edmonton.ca and write a local dataset catalog cache. <br>
Mitigation: Review commands before execution, allow network access only to the City of Edmonton open-data portal, and remove the local cache if a fresh catalog is required. <br>
Risk: The optional SOCRATA_APP_TOKEN may be exposed if an unrelated credential is provided. <br>
Mitigation: Set only a Socrata app token when higher rate limits are needed, and do not provide unrelated secrets. <br>
Risk: Fetched public datasets may be incomplete, stale, or unavailable depending on the upstream portal. <br>
Mitigation: Check dataset metadata, update timestamps, and portal availability before relying on generated analysis. <br>


## Reference(s): <br>
- [City of Edmonton Open Data Portal](https://data.edmonton.ca) <br>
- [Popular & Useful Edmonton Open Data Datasets](references/datasets.md) <br>
- [ClawHub release page](https://clawhub.ai/raychanpmp/edmonton-opendata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper script output may be JSON, CSV, GeoJSON, or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an optional SOCRATA_APP_TOKEN for Socrata rate limits and may write a small dataset catalog cache under the skill scripts directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
