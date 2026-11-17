## Description:

Query the BCRA Central de Deudores API to check the credit status, current and historical debts, and rejected checks of individuals or companies in Argentina using a CUIT, CUIL, or CDI number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferminrp](https://clawhub.ai/user/ferminrp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to query Argentina Central Bank debtor registry data for authorized credit-status checks, debt history review, and rejected-check reporting by CUIT, CUIL, or CDI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive credit-status information tied to CUIT, CUIL, or CDI identifiers.

Mitigation: Use it only for authorized debtor-registry lookups and avoid checking unrelated people or companies without consent or a valid legal basis.

Risk: The optional compara.ar web interface can disclose the queried identifier to a third-party site.

Mitigation: Prefer the public BCRA API when possible, and use the compara.ar link only after accepting that disclosure.

Risk: A 404 response may be misread as proof that no debt exists.

Mitigation: Present missing records carefully as no records found for that identifier and note that the identifier may be incorrect.

## Reference(s):

- [OpenAPI specification](references/openapi-spec.json)
- [BCRA API base URL](https://api.bcra.gob.ar)
- [ClawHub skill page](https://clawhub.ai/ferminrp/skills/bcra-central-deudores)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces interpreted debtor-registry results and cautions for missing records, reported amounts, risk codes, and unpaid rejected checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
