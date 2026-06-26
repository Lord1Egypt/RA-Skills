## Description: <br>
Search French cinema establishments using the open data.culture.gouv.fr API by city, region, proximity, screen count, Art et Essai label, and multiplex status without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deiu](https://clawhub.ai/user/deiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to construct searches against the French Ministry of Culture cinema establishments dataset. It helps find cinemas by place, name, proximity, venue type, capacity, attendance, and regional aggregates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exact coordinates used in nearby-cinema examples are sent to the public data API. <br>
Mitigation: Use city names or approximate coordinates when location privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deiu/france-cinemas) <br>
- [French Ministry of Culture cinema establishments API](https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API query URLs, JSON] <br>
**Output Format:** [Markdown guidance with API query examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required; public API responses are paginated with a maximum limit of 100 records per request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
