## Description: <br>
Casdoor API Assistant helps agents identify Casdoor API endpoints, generate curl, JavaScript, and Python examples, and debug Casdoor authentication, OIDC, and API issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y-victor](https://clawhub.ai/user/y-victor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to select Casdoor REST API endpoints, create request examples, and troubleshoot authentication or OIDC failures without manually scanning the full endpoint index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated API examples may include credentials or target data-changing Casdoor endpoints. <br>
Mitigation: Verify the Casdoor host, tenant, authentication mode, and endpoint side effects before running generated requests. <br>
Risk: Prompts may contain sensitive credentials or production user data while debugging authentication failures. <br>
Mitigation: Use placeholders for access tokens, client secrets, passwords, payment data, and production user data unless working in an intentionally secure environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/y-victor/casdoor) <br>
- [API Groups](references/api-groups.md) <br>
- [Endpoint Index](references/endpoint-index.md) <br>
- [Example Patterns](references/example-patterns.md) <br>
- [Auth And Debugging](references/auth-and-debugging.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with inline curl, JavaScript, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for hosts, tenants, tokens, and other sensitive values unless the user provides them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
