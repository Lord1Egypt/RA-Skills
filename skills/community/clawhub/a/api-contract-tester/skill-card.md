## Description: <br>
Validate API contracts between services by generating and verifying consumer-driven Pact contracts, OpenAPI compliance tests, and schema compatibility checks for microservices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate contract tests, verify APIs against Pact or OpenAPI contracts, detect breaking API changes, and map consumer dependencies before API releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest local tooling commands or package installation while inspecting API contracts. <br>
Mitigation: Review generated commands before execution and run them only in the intended repository and environment. <br>
Risk: Contract verification may send requests to provider APIs or validation endpoints. <br>
Mitigation: Use non-production endpoints or scoped test credentials when verifying contracts, and avoid sending sensitive data in generated tests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python test examples, shell commands, compatibility tables, and breaking-change reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for local repository analysis and API contract validation; it does not declare a fixed machine-readable output schema.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
