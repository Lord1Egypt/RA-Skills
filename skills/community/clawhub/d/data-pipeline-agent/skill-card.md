## Description:

ETL pipeline builder for business data covering API extraction, data cleaning, transformation, warehouse loading, recurring data syncs, and data quality audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and operations teams use this skill to design ETL workflows that extract business data from APIs or CSV files, clean and normalize records, merge sources, load warehouses or databases, and schedule recurring syncs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample API extractor can forward authorization headers to pagination URLs that are not validated against the original trusted HTTPS host.

Mitigation: Restrict pagination to the original trusted HTTPS host before sending credentials or other headers.

Risk: Pipelines may process financial or business data and real credentials.

Mitigation: Review before installation or real use, load secrets from environment variables or 1Password CLI, and avoid hardcoding credentials.

Risk: Long-running API extraction can run without explicit timeout or page limits.

Mitigation: Add request timeouts, retry bounds, and maximum page limits before production use.

Risk: Dependency installation examples are not pinned to exact versions.

Mitigation: Install dependencies in an isolated environment and pin package versions for repeatable execution.

Risk: Status alerts could expose sensitive operational details if notifications include raw pipeline output.

Mitigation: Send only sanitized status text in Telegram or other notification channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/data-pipeline-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks plus configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ETL patterns, dependency commands, scheduling examples, data quality checks, and file organization guidance.]

## Skill Version(s):

98.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
