## Description: <br>
api-toolkit helps development teams test and debug APIs through regression suites, local mock servers, load testing, OpenAPI contract checks, error-code lookup, and collaboration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, SREs, and API platform teams use this skill to create and run API tests, mock services, validate OpenAPI contracts, diagnose errors, and produce API testing or performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Load testing can send heavy traffic to API targets. <br>
Mitigation: Run tests only against APIs the user owns or is explicitly authorized to test, use conservative concurrency and rate limits, and avoid production or third-party targets unless approved. <br>
Risk: Record and replay workflows can persist real API traffic, including credentials or sensitive data. <br>
Mitigation: Configure redaction for credentials and sensitive fields, store recordings securely, and keep recordings out of source control. <br>
Risk: API workflows may require credentials for collaboration spaces or target services. <br>
Mitigation: Use environment-based credential handling, avoid hardcoded keys, and limit credentials to the minimum permissions needed for the test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/api-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples, YAML and JSON snippets, and report file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference HTML, JSON, or JUnit XML reports when used for regression or load testing workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
