## Description: <br>
Helps developers push backend API definitions to a frontend data-interface platform so frontend and backend API documentation stay synchronized. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowzhouj](https://clawhub.ai/user/snowzhouj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare JSON or OpenAPI-style endpoint definitions, push them to the configured frontend data-interface platform, validate results, and keep a local push history for coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API definitions may contain secrets, tokens, customer data, or sensitive internal details before upload. <br>
Mitigation: Review and sanitize API definitions before running the skill or asking an agent to push them. <br>
Risk: The script sends API specifications to a configured external endpoint. <br>
Mitigation: Use the skill only when the configured endpoint is an approved destination for the organization. <br>
Risk: Push results are retained in a local Markdown history file. <br>
Mitigation: Review local history entries and avoid storing sensitive response details in the artifact. <br>


## Reference(s): <br>
- [Frontend API platform documentation](references/frontend-api-docs.md) <br>
- [API definition standard](references/api-definition-standard.md) <br>
- [Push history record](references/push-history.md) <br>
- [ClawHub skill page](https://clawhub.ai/snowzhouj/api-push-frontend) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, Python script usage, and local Markdown history entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send API definitions to the configured endpoint and append push results to a local push-history Markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
