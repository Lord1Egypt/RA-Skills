## Description: <br>
Generates API test analysis documents from OpenAPI or Swagger specs, simplified interface definitions, or natural language descriptions, covering parameter validation, business logic, response verification, security, performance, compatibility, and common API testing pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackbat1988](https://clawhub.ai/user/blackbat1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and API reviewers use this skill to turn API specifications into structured Markdown test analysis reports for planning, review, and coverage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL injection, XSS, and other security test payloads could be harmful if run against systems without authorization. <br>
Mitigation: Review generated payloads before execution and only test APIs that the user owns or is authorized to assess. <br>
Risk: Generated test analysis may be incomplete or may not match an API's real business rules. <br>
Mitigation: Have API owners or QA reviewers validate the generated report before relying on it for release decisions. <br>


## Reference(s): <br>
- [API Test Create Skill Page](https://clawhub.ai/blackbat1988/apitestcreate) <br>
- [Test Case Design Guide](references/test-case-design.md) <br>
- [Common API Testing Pitfalls](references/common-pitfalls.md) <br>
- [OpenAPI Example](examples/openapi-example.yaml) <br>
- [Simple Definition Example](examples/simple-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands] <br>
**Output Format:** [Markdown test analysis reports with optional command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include prioritized test points, risk notes, test data suggestions, execution guidance, and coverage statistics.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
