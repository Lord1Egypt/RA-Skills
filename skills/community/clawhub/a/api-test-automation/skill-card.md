## Description: <br>
API Test Automation helps agents create and run REST and GraphQL API tests, including functional, performance, contract, mock-service, and reporting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to generate and run API test automation for REST and GraphQL services, including contract checks, load testing, mock services, and test reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API, load, or contract tests can affect live services if run against systems the user does not own or is not authorized to test. <br>
Mitigation: Run generated tests only against owned or explicitly authorized development, staging, or test systems. <br>
Risk: The mock server captures requests in an in-memory log, which can retain credentials or sensitive payloads sent during testing. <br>
Mitigation: Use test credentials and sanitized payloads, and avoid sending real secrets through mock-server scenarios. <br>
Risk: The skill depends on multiple Python packages that may change behavior or expose vulnerabilities over time. <br>
Mitigation: Pin and audit dependencies before using the skill in CI or shared development environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/api-test-automation) <br>
- [Project homepage](https://github.com/kaiyuelv/api-test-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated API test code, mock-service setup, performance test guidance, and report-generation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
