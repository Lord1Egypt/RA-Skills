## Description: <br>
Api Test Reporter helps an agent turn API interface documentation into JSON-based HTTP test cases, execute them, and generate visual HTML reports with request, response, and validation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squidtestgary](https://clawhub.ai/user/squidtestgary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to derive API test plans from interface documentation, run POST or GET JSON API checks, and produce shareable HTML reports. It is useful when test coverage must include required fields, pagination, enums, date ranges, numeric ranges, status flags, combined scenarios, and boundary or exception cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated configurations can send live HTTP requests to configured API endpoints. <br>
Mitigation: Review every generated config before execution, replace all sample hosts and credentials, and run tests only against authorized staging or approved target APIs. <br>
Risk: Optional database fixtures can execute SQL queries and expose real records in tests. <br>
Mitigation: Use read-only test database accounts, inspect SQL queries before running them, and prefer sanitized or synthetic records where possible. <br>
Risk: HTML, JavaScript data, and JSON result files can preserve full request and response payloads. <br>
Mitigation: Treat generated reports as sensitive artifacts and redact them before placing them in shared folders or source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squidtestgary/api-test-reporter) <br>
- [API test workflow reference](references/workflow.md) <br>
- [Example test configuration](references/test_config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell commands; generated test outputs include HTML, JavaScript data, and JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include full request and response data, so generated files should be handled as potentially sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
