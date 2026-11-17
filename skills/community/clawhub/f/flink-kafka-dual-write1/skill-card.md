## Description:

Generates Bethune Flink monitoring jobs that dual-write Kafka data to Hive and StarRocks, including Java job/model/PO files, synchronized config.properties updates, and compile validation when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[printsky](https://clawhub.ai/user/printsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers maintaining Bethune Flink monitoring pipelines use this skill to add Kafka-to-Hive-and-StarRocks dual-write jobs that follow established task 33/34/35/36 patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code can log raw Kafka message contents, which may expose sensitive data in production logs.

Mitigation: Remove or redact raw Kafka payload logging before production use and review generated jobs during normal change review.

Risk: The skill edits Java source and environment configuration files in the Bethune repository.

Mitigation: Review the generated file changes and all four config updates, then run the repository compile and test checks before deployment.

## Reference(s):

- [Bethune task pattern reference](references/bethune-patterns.md)

## Skill Output:

**Output Type(s):** [code, configuration, shell commands, guidance]

**Output Format:** [Markdown summary with Java file changes, config key updates, optional shell commands, and validation status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update Java source files and four environment config.properties files in the target Bethune repository.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
