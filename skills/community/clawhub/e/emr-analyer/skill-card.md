## Description:

EMR Analyzer diagnoses open-source big-data services on Linux by checking service status, reading configuration parameters, analyzing task and log errors, and suggesting tuning or remediation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinyafei123](https://clawhub.ai/user/qinyafei123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect EMR-style big-data clusters, check service health, analyze logs, retrieve key configuration values, and draft tuning or repair guidance for services such as Hadoop, Spark, Hive, Kafka, and Flink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs host-level shell commands while reading service logs and configuration files that may contain sensitive operational data.

Mitigation: Run it only on trusted hosts with least-privilege read-only access, avoid sudo unless necessary, and redact sensitive logs or configs before analysis.

Risk: The security summary identifies command-injection risk when log filenames can be attacker-controlled.

Mitigation: Do not run it in log directories writable by untrusted users or services; remove shell=True and safely handle filenames before production use.

Risk: The security guidance notes a broken CONFIG_PATHS reference in the package.

Mitigation: Correct the CONFIG_PATHS reference before relying on all-service configuration checks in production.

## Reference(s):

- [Big Data Service Reference Manual](artifact/references/services.md)
- [Alibaba Cloud EMR documentation](https://help.aliyun.com/zh/emr/)
- [Alibaba Cloud EMR common file paths](https://help.aliyun.com/zh/emr/emr-on-ecs/user-guide/paths-of-frequently-used-files)
- [Apache Hadoop documentation](https://hadoop.apache.org/docs/)
- [Apache Spark documentation](https://spark.apache.org/docs/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON diagnostics with Markdown-facing explanations and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service status, log findings, configuration values, tuning suggestions, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
