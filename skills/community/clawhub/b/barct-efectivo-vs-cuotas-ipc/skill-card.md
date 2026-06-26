## Description: <br>
Comparar efectivo, cuotas y tarjeta a fin de mes usando valor presente, con salida breve y clara. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barct](https://clawhub.ai/user/barct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can compare cash discounts, installment plans, and deferred card payment options in Argentina using present value. The skill produces a brief recommendation, present-value breakdown, estimated savings, and maximum supportable surcharge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inflation estimates may depend on public data availability or assumptions when tasa_oportunidad_mensual is not provided. <br>
Mitigation: Provide tasa_oportunidad_mensual explicitly, or ask the agent to show the source and assumptions when it estimates inflation. <br>
Risk: The recommendation can be misleading if price, discount, installment, surcharge, delay, or rate inputs are missing or incorrect. <br>
Mitigation: Review declared assumptions and provide missing inputs before relying on the comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barct/barct-efectivo-vs-cuotas-ipc) <br>
- [Argentina public series API](https://apis.datos.gob.ar/series/api/series) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise labeled sections and numeric currency values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maximum 14 lines; includes Resumen, Desglose en valor presente, and Conclusion.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
