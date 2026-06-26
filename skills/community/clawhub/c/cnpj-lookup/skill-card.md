## Description: <br>
Looks up Brazilian company registration data by CNPJ through public APIs, with provider fallback, local caching, rate limiting, and Markdown or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, analysts, and developers use this skill to retrieve Brazilian company identity, registration status, address, CNAE, QSA, contact, and related business data from a supplied CNPJ. It is useful for enrichment and lookup workflows, but the returned data should not replace official documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CNPJ lookup terms are sent to third-party public API providers. <br>
Mitigation: Use the skill only when third-party lookup is acceptable, and confirm the selected provider or force a provider when policy requires it. <br>
Risk: Returned company data may be cached locally for up to the configured TTL. <br>
Mitigation: Use --no-cache for sensitive lookups, lower the TTL when needed, or clear the local cache after use. <br>
Risk: Public API results may be incomplete, stale, or less complete depending on the fallback provider. <br>
Mitigation: Review the source provider in the output and verify important decisions against official records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/runawaydevil/cnpj-lookup) <br>
- [Provider behavior and rate limits](references/providers.md) <br>
- [Normalized output fields](references/fields.md) <br>
- [BrasilAPI CNPJ endpoint](https://brasilapi.com.br/api/cnpj/v1/{cnpj}) <br>
- [CNPJ.ws public endpoint](https://publica.cnpj.ws/cnpj/{cnpj_sem_pontuacao}) <br>
- [OpenCNPJ endpoint](https://api.opencnpj.org/{cnpj}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary or normalized JSON returned from public CNPJ API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source provider, fetch timestamp, cache status, and optional detailed company fields such as CNAE and QSA.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
