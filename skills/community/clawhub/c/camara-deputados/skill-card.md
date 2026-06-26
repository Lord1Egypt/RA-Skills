## Description: <br>
Monitor and research Brazilian Chamber of Deputies legislative activity, including deputies, bills, votes, committees, agendas, expenses, and legislative statuses through the public Dados Abertos API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegantonov](https://clawhub.ai/user/olegantonov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, journalists, civic analysts, and developers use this skill to search and monitor public Câmara dos Deputados data for deputies, proposições, votes, events, committees, parties, expenses, and legislative reference data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, IDs, and date ranges used with the skill are sent to the public Câmara dos Deputados API. <br>
Mitigation: Use only public or approved research queries, and avoid sensitive internal terms when calling the API. <br>
Risk: Running the bundled Python client or CLI locally depends on Python package hygiene. <br>
Mitigation: Use a virtual environment and pin or update dependencies before using the tooling in local or CI workflows. <br>
Risk: Legislative agenda, vote, and status data can change as the public source updates. <br>
Mitigation: Verify time-sensitive conclusions against the live official API before publication or operational use. <br>


## Reference(s): <br>
- [Câmara dos Deputados Dados Abertos API](https://dadosabertos.camara.leg.br/api/v2) <br>
- [Câmara dos Deputados Swagger UI](https://dadosabertos.camara.leg.br/swagger/api.html) <br>
- [Portal de Dados Abertos da Câmara dos Deputados](https://www2.camara.leg.br/transparencia/dados-abertos) <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/olegantonov/camara-deputados) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with API URLs, curl examples, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public read-only Câmara dos Deputados API responses; no authentication is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
