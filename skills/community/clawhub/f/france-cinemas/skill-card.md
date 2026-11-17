## Description:

Search French cinema establishments using the open data.culture.gouv.fr API by city, region, proximity, screen count, Art et Essai label, and multiplex status with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deiu](https://clawhub.ai/user/deiu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to construct queries against the French Ministry of Culture cinema establishments dataset and interpret returned cinema records, including locations, screen counts, attendance, Art et Essai status, and multiplex status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location-based searches can send coordinates or other location hints to data.culture.gouv.fr.

Mitigation: Avoid using sensitive personal locations unless the user is comfortable sharing them with the public data API.

## Reference(s):

- [French Ministry of Culture cinema establishments API](https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records)
- [ClawHub skill page](https://clawhub.ai/deiu/skills/france-cinemas)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API query examples]

**Output Format:** [Markdown with URL query examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; generated queries may include city names, cinema names, filters, or geographic coordinates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
