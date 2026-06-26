## Description: <br>
Generates mock API servers and static fixtures from OpenAPI 3.x and Swagger 2.0 specs with schema-aware fake data, response delays, error simulation, and CORS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create live mock APIs, static JSON fixtures, route listings, and sample responses for frontend development, testing, demos, and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API specifications may contain real secrets or personal data that could be copied into generated fixtures or served mock responses. <br>
Mitigation: Review API specifications for secrets and personal data before generating fixtures or serving responses. <br>
Risk: A live mock server can expose generated endpoints if bound to a network interface beyond localhost. <br>
Mitigation: Keep the default localhost binding unless network exposure is intentional and reviewed. <br>
Risk: YAML support requires installing PyYAML, which adds dependency supply-chain exposure. <br>
Mitigation: Install PyYAML only from a trusted package source when YAML input support is needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON or Python artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local server commands, static mock files, route manifests, and sample JSON responses from an API specification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
