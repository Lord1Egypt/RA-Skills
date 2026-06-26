## Description: <br>
Generates Bethune Flink monitoring tasks that read Kafka logs, write to Hive and StarRocks, update the required configuration files, and run compile validation when feasible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[printsky](https://clawhub.ai/user/printsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill in Bethune-style repositories to add Kafka-to-Hive-and-StarRocks Flink monitoring jobs from an existing task pattern, including Java model/job classes and synchronized environment configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Java and configuration changes can target incorrect Bethune product, stage, topic, table, or task values. <br>
Mitigation: Use the skill in a version-controlled Bethune-style repository and review the generated Java files plus all four config.properties updates before deployment. <br>
Risk: Generated error logging can expose Kafka message payloads when topics contain sensitive data. <br>
Mitigation: Redact or truncate Kafka message payloads in generated error logs before using the task with sensitive topics. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/printsky/flink-kafka-dual-write1) <br>
- [Bethune Patterns Reference](references/bethune-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown summary with Java and configuration file edits, compile-validation results, and optional Hive or StarRocks DDL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository files and should report changed files, new configuration keys, generation mode, and compile status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
