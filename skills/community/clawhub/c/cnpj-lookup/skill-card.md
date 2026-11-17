## Description:

Consulta CNPJ via APIs publicas brasileiras (BrasilAPI, CNPJ.ws, OpenCNPJ) com fallback automatico, cache e rate limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to look up Brazilian company registration details by CNPJ, including legal name, registration status, address, CNAE, QSA, contact data, and capital information. It supports quick summaries, detailed lookups, and normalized JSON export for downstream integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CNPJ lookup targets are sent to BrasilAPI, CNPJ.ws, and OpenCNPJ, which may reveal the queried company identity and timing to public API providers.

Mitigation: Use the skill only when those lookups are acceptable for the investigation context, and avoid it for confidential or sensitive lookup activity.

Risk: Lookup results are cached locally by default for up to 24 hours.

Mitigation: Use --no-cache for lookups that should not be retained in the skill cache, or set a shorter TTL when local retention should be reduced.

Risk: Public provider data can be incomplete or less authoritative than official records.

Mitigation: Treat results as enrichment data and verify important business, legal, or compliance decisions against official sources.

## Reference(s):

- [Provider endpoints and rate limits](references/providers.md)
- [Normalized CNPJ data schema](references/fields.md)
- [BrasilAPI CNPJ endpoint](https://brasilapi.com.br/api/cnpj/v1/{cnpj})
- [CNPJ.ws public endpoint](https://publica.cnpj.ws/cnpj/{cnpj_sem_pontuacao})
- [OpenCNPJ endpoint](https://api.opencnpj.org/{cnpj})

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands]

**Output Format:** [Markdown company summary or normalized JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source provider, cache status, fetch timestamp, and optional detailed company fields such as CNAE and QSA.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
