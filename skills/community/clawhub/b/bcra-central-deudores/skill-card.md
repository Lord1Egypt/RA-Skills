## Description: <br>
Query the BCRA Central de Deudores API to check current debts, historical debt status, and rejected checks for individuals or companies in Argentina by CUIT, CUIL, or CDI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferminrp](https://clawhub.ai/user/ferminrp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and business or legal workflow agents use this skill to retrieve and interpret Argentine credit/debt registry information by authorized CUIT, CUIL, or CDI lookup. <br>

### Deployment Geography for Use: <br>
Argentina <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive credit and debt information by tax identifier. <br>
Mitigation: Use it only for your own records or clearly authorized business or legal workflows, and avoid sharing retrieved results unnecessarily. <br>
Risk: A mistyped CUIT, CUIL, or CDI could return information for the wrong person or company. <br>
Mitigation: Verify the 11-digit identifier before querying and treat no-record responses as inconclusive rather than proof of no debts. <br>
Risk: The optional third-party visual interface may expose lookup data outside the official API path. <br>
Mitigation: Prefer the official BCRA API unless the user intentionally asks to use the third-party UI. <br>


## Reference(s): <br>
- [Central de Deudores OpenAPI specification](references/openapi-spec.json) <br>
- [BCRA API base URL](https://api.bcra.gob.ar) <br>
- [ClawHub release page](https://clawhub.ai/ferminrp/bcra-central-deudores) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON response summaries and optional inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interpreted credit situation codes, debt amounts in thousands of ARS, historical trend notes, and rejected check status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
