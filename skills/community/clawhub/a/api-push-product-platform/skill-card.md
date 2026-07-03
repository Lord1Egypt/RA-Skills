## Description: <br>
Pushes backend API interface definitions to a product data platform for centralized documentation management and synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowzhouj](https://clawhub.ai/user/snowzhouj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare, validate, and push backend API definitions associated with PRD IDs into a product data platform. It supports guided natural-language use, direct API calls, and script-based or CI/CD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends local API-definition data to a configured plain-HTTP product-platform endpoint. <br>
Mitigation: Install only for an approved product-platform destination, review and sanitize API definition JSON before pushing, and use an HTTPS/authenticated endpoint if available. <br>
Risk: Automation examples can push API documentation through CI/CD or Git hooks with limited manual review. <br>
Mitigation: Use automation only after team approval and keep a human review gate for generated or changed API definitions. <br>


## Reference(s): <br>
- [Product Platform API Docs](references/product-platform-api-docs.md) <br>
- [API Definition Standard](references/api-definition-standard.md) <br>
- [Push History Log](references/push-history.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare or submit API definition JSON for a provided PRD ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
