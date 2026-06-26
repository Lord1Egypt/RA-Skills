## Description: <br>
Generate comprehensive OpenAPI 3.0 specs, markdown reference docs, and SDK quickstarts from API endpoint descriptions with examples and error codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn API endpoint descriptions, route files, schemas, or controller code into consistent API documentation and onboarding material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Endpoint examples, route files, or controller code may contain real API keys, production secrets, customer data, or sensitive internal implementation details. <br>
Mitigation: Use sanitized examples and remove secrets or sensitive data before providing API material to the agent runtime. <br>
Risk: Generated API documentation can become inaccurate if endpoint behavior, authentication, pagination, or error handling is underspecified. <br>
Mitigation: Review the generated OpenAPI YAML, reference docs, and quickstart snippets against the implemented API before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-api-docs) <br>
- [Publisher profile](https://clawhub.ai/user/1kalin) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration] <br>
**Output Format:** [OpenAPI 3.0 YAML, markdown API reference, and markdown quickstart guide with code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint descriptions, parameter tables, request and response examples, error code references, authentication notes, rate limiting notes, and SDK quickstart snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
