## Description:

Automates user-directed API testing, response-time checks, status-code validation, performance tests, regression tests, and CI/CD-oriented test reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthasking123](https://clawhub.ai/user/arthasking123)

### License/Terms of Use:

MIT

## Use Case:

Developers and QA engineers use this skill to test API endpoints, validate basic response behavior, measure latency, and save local Markdown reports for review or automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing endpoints can write response previews to local Markdown reports, which may expose secrets, personal data, or confidential error details.

Mitigation: Use only approved test endpoints or sanitized environments, and avoid endpoints that return sensitive content unless saving the first 200 response characters is acceptable.

Risk: The skill sends HTTP requests to user-provided URLs, so misuse could target unintended or unauthorized services.

Mitigation: Run tests only against systems you are authorized to assess and review the target URL, method, and authentication option before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthasking123/skills/ai-api-test)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown API test reports with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves local Markdown reports under the artifact output directory and may include the first 200 response characters from tested endpoints.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
