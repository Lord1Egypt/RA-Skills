## Description:

api-test-reporter helps agents turn API interface documentation for JSON POST/GET endpoints into grouped test cases, execute them, and generate structured HTML reports with request, response, and validation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squidtestgary](https://clawhub.ai/user/squidtestgary)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to derive API test cases from interface documentation, optionally populate positive cases from approved database fixtures, execute JSON HTTP requests, and inspect generated HTML and JSON reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports real-looking database credentials in examples.

Mitigation: Rotate any exposed credential that was ever valid and replace published examples with placeholders before use.

Risk: The skill can run database-backed API tests and execute configured fixture SQL.

Mitigation: Run only against approved staging systems, use least-privilege read-only database accounts, and restrict fixture SQL to reviewed SELECT queries.

Risk: Generated reports can contain sensitive request, response, personal, or business data.

Mitigation: Redact secrets and sensitive data from reports before sharing or storing them outside the approved test environment.

Risk: The security guidance calls for dependency and asset control.

Mitigation: Pin dependencies and bundle report assets locally where operational policy requires repeatable or offline execution.

## Reference(s):

- [API Test Workflow Reference](references/workflow.md)
- [Test Configuration Example](references/test_config.example.json)
- [ClawHub Skill Page](https://clawhub.ai/squidtestgary/skills/api-test-reporter)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, JSON, HTML]

**Output Format:** [Markdown guidance, JSON test configuration and results, shell commands, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces test_report_<method>_<timestamp>.html, __REPORT_DATA__.js, and test_results_<method>_<timestamp>.json when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
