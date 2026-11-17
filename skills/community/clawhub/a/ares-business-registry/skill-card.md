## Description:

Query Czech ARES business registry by ICO or name with human/JSON/raw outputs, retries, and legal-form decoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pghostek](https://clawhub.ai/user/pghostek)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to look up Czech ARES business registry entities by ICO, name, city, or CZ-NACE code and return either concise summaries, normalized JSON, or raw ARES payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill can send requests to arbitrary URLs through the --base option instead of only the official ARES service.

Mitigation: Use the skill only where outbound network access is acceptable and do not allow prompts or untrusted inputs to set --base; prefer restricting requests to the official ARES host.

## Reference(s):

- [ARES Links](references/ares-links.md)
- [ClawHub skill page](https://clawhub.ai/pghostek/skills/ares-business-registry)
- [ARES Swagger UI](https://ares.gov.cz/swagger-ui/#/)
- [ARES ICO endpoint](https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico})
- [ARES technical documentation catalog, 2023](https://mf.gov.cz/assets/attachments/2023-08-01_ARES-Technicka-dokumentace-Katalog-verejnych-sluzeb_v07.pdf)
- [ARES technical documentation catalog, 2024](https://mf.gov.cz/assets/attachments/2024-02-16_ARES-Technical-documentation-Catalog-of-public-services_v02.pdf)
- [CZ-NACE classification](https://www.czso.cz/csu/czso/klasifikace_ekonomickych_cinnosti_cz_nace)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text, normalized JSON, or raw JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports validation-error, ARES-error, and network-error JSON contracts when --json is used.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
