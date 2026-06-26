## Description: <br>
Audits and hardens API credential handling across environment variables, separation, rotation planning, least privilege, and auditability for integrations and deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when integrating services or preparing deployments to map API credentials, move secrets to environment variables or secret manager references, plan rotation, reduce permissions, and document audit trails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste real API keys, tokens, private keys, or unredacted environment files into the agent while requesting an audit. <br>
Mitigation: Use redacted snippets and placeholders only, and keep real secrets in approved secret stores or deployment-time injection. <br>
Risk: Example dotenv settings may be copied into production without review, including n8n authentication-related values. <br>
Mitigation: Review every setting against production requirements, enable appropriate authentication, and treat the dotenv file as a placeholder template. <br>
Risk: Credential plans can suggest permissions, owners, or rotation procedures that do not match an API's actual requirements. <br>
Mitigation: Validate scopes, ownership, cadences, and rollback steps with service documentation and responsible system owners before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KOwl64/api-credentials-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with credential maps, checklists, runbooks, and placeholder environment-template content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces technical documentation and placeholder templates only; it should not output real secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
