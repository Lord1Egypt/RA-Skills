## Description:

Research Brazil's Chamber of Deputies using its official open-data API. Use for federal deputies, Chamber bills, votes, events, committees, parliamentary fronts, and CEAP expenses; use senado-federal for Senate-only records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegantonov](https://clawhub.ai/user/olegantonov)

### License/Terms of Use:

MIT

## Use Case:

External users, researchers, journalists, and developers use this skill to query and interpret official Brazilian Chamber of Deputies open data for deputies, bills, votes, events, committees, parliamentary fronts, and CEAP expenses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP pagination or redirects could reach destinations outside the official Câmara API host.

Mitigation: Validate next-page and redirect destinations against the official API host before following them.

Risk: Use in environments with private internal networks or cloud metadata endpoints could amplify the impact of unintended outbound requests.

Mitigation: Review deployment context before installation and restrict outbound network access to the official Câmara API where practical.

Risk: Unreviewed dependency updates could change network or parsing behavior.

Mitigation: Use pinned, reviewed dependencies for managed deployments.

## Reference(s):

- [Câmara API endpoint reference](references/api-endpoints.md)
- [Chamber response, pagination, and time rules](references/response-shapes.md)
- [Tracking a proposition across both houses](references/cross-house.md)
- [Câmara dos Deputados Open Data API](https://dadosabertos.camara.leg.br/api/v2)
- [Câmara dos Deputados Swagger UI](https://dadosabertos.camara.leg.br/swagger/api.html)
- [Portal de Dados Abertos da Câmara dos Deputados](https://www2.camara.leg.br/transparencia/dados-abertos)
- [ClawHub skill page](https://clawhub.ai/olegantonov/skills/camara-deputados)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with API URLs, JSON field names, Python snippets, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite or return exact API URLs when auditability matters and separate official Chamber data from interpretation.]

## Skill Version(s):

1.1.1 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
