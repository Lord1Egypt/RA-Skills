## Description:

Generates standardized Chinese similar-case retrieval reports by guiding an agent through case fact collection, Deli Legal CLI search, case screening, comparison, and rule analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

External legal practitioners, court staff, and in-house legal teams use this skill to collect case facts, retrieve similar Chinese judgments, compare outcomes, and draft a standardized similar-case report for court submission or internal strategy.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party CLI.

Mitigation: Pin and review the Deli Legal CLI version before use, and execute it only in trusted environments.

Risk: Case facts, API keys, and legal materials may be confidential or sensitive.

Mitigation: Avoid passing API keys directly on the command line, and redact privileged, sealed, personal, or commercially sensitive facts unless disclosure is authorized.

Risk: The generated report can contain incomplete or stale case information if CLI results are missing, unavailable, or not independently checked.

Mitigation: Do not fabricate missing case fields; verify important cases, citations, court names, dates, and conclusions through official sources before legal reliance.

## Reference(s):

- [deli-cli 通用前置](references/cli-common.md)
- [类案检索 CLI 策略指南](references/api-guide.md)
- [类案检索报告标准模板](references/report-template.md)
- [类案检索制度法律依据](references/legal-basis.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown case-retrieval report with structured tables and CLI command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one final report; case facts, retrieved case details, legal citations, and conclusions require review before legal reliance.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
