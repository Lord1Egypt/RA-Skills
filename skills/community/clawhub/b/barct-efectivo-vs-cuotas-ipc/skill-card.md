## Description:

Comparar efectivo, cuotas y tarjeta a fin de mes usando valor presente, con salida breve y clara.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barct](https://clawhub.ai/user/barct)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers and assistants in Argentina use this skill to compare cash discounts, installment plans, and deferred card payments by present value before making a purchase.

### Deployment Geography for Use:

Argentina

## Known Risks and Mitigations:

Risk: If no monthly opportunity rate is supplied, the skill may query a public government inflation-data API.

Mitigation: Provide the monthly opportunity rate directly or disable inflation projection to avoid that lookup.

Risk: The recommendation depends on accurate prices, discounts, installment counts, surcharges, days until payment, and rate assumptions.

Mitigation: Review the declared assumptions and verify inputs before relying on the present-value comparison.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barct/skills/barct-efectivo-vs-cuotas-ipc)
- [datos.gob.ar series API](https://apis.datos.gob.ar/series/api/series)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown-style text with a numeric present-value breakdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maximum 14 lines; includes Resumen, Desglose en valor presente, and Conclusion blocks.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
