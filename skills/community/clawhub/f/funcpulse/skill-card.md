## Description:

FuncPulse maps financial AI requirements, PRDs, test cases, and multi-repository code changes into traceability matrices to identify coverage gaps, missing compliance evidence, defect priorities, and acceptance risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[start-fish](https://clawhub.ai/user/start-fish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use FuncPulse to validate whether PRD requirements and test cases are covered by implementation changes across one or more repositories. It helps produce acceptance evidence, coverage analysis, defect prioritization, and standardized business test validation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation reports, defect details, traceability data, tester identity, and repository metadata may be uploaded to a fixed plaintext HTTP endpoint.

Mitigation: Use a local-only workflow or require HTTPS, redaction, and explicit approval before any report upload, especially for private, regulated, or proprietary projects.

Risk: Generated QA analysis can be incomplete or incorrect if PRDs, test cases, repository paths, or diffs are missing or stale.

Mitigation: Provide current requirements, test cases, repository context, and code changes, then have QA or engineering reviewers confirm coverage findings before acceptance decisions.

## Reference(s):

- [FuncPulse ClawHub skill page](https://clawhub.ai/start-fish/skills/funcpulse)
- [Publisher profile](https://clawhub.ai/user/start-fish)
- [Financial AI Validation Playbook](references/financial-ai-validation-playbook.md)
- [Test Validation Report Template](references/test-validation-report.md)
- [QA Analysis Methods](references/qa-analysis-methods.md)
- [Multi-Repo Analysis Guide](references/multi-repo-analysis.md)
- [Test Case Traceability Guide](references/test-case-traceability.md)
- [Code Change Test Coverage Guide](references/code-change-test-coverage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown validation reports with traceability matrices, coverage summaries, defect lists, remediation guidance, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include repository metadata, tester identity, test counts, coverage metrics, issues, recommendations, and remote report links when upload is enabled.]

## Skill Version(s):

1.0.4 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
