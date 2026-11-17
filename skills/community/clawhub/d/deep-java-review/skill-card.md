## Description:

Reviews Java repository changes by analyzing Git diffs and call-chain context, inferring business requirements, scoring code quality, and generating PRD and review reports with checks for Java, Spring, MyBatis, transactions, SQL/DDL, concurrency, performance, exception handling, null safety, and resource management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qfann](https://clawhub.ai/user/qfann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Java code changes, understand their business impact, identify implementation risks, and produce structured PRD and review reports before merging or releasing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repository changes and write review or PRD reports to the workspace.

Mitigation: Specify the branch or files to review and confirm report-writing behavior before running it.

Risk: Generated review findings or inferred business requirements may be incomplete or incorrect.

Mitigation: Have a developer review the generated reports before relying on them for merge, release, or product decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qfann/skills/deep-java-review)
- [Publisher profile](https://clawhub.ai/user/qfann)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports, PRD files, and console text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write code-review-report.md and prd-{version}.md in the workspace after reviewing Git diffs and project context.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
