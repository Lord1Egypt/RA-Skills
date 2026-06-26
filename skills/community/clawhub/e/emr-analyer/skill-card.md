## Description: <br>
Analyzes open-source big data services on Linux by checking service status, reading configuration, analyzing logs, and suggesting fixes or tuning guidance for common EMR components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinyafei123](https://clawhub.ai/user/qinyafei123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to diagnose EMR and big data clusters, including YARN, Hive, HDFS, Spark, Kafka, ZooKeeper, HBase, Flink, and related services. It helps produce health reports, configuration observations, log analysis, repair suggestions, and performance tuning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads server logs and configuration that may contain credentials, internal hostnames, usernames, IP addresses, or customer data. <br>
Mitigation: Run it only on trusted Linux cluster hosts and redact sensitive logs or configuration values before sharing outputs. <br>
Risk: Server security evidence flags unsafe shell command handling patterns. <br>
Mitigation: Review or patch command handling before use on shared systems, and run with the least privilege needed. <br>


## Reference(s): <br>
- [Service reference](references/services.md) <br>
- [Aliyun EMR documentation](https://help.aliyun.com/zh/emr/) <br>
- [Aliyun EMR common file paths](https://help.aliyun.com/zh/emr/emr-on-ecs/user-guide/paths-of-frequently-used-files) <br>
- [Apache Hadoop documentation](https://hadoop.apache.org/docs/) <br>
- [Apache Spark documentation](https://spark.apache.org/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize service health, log findings, configuration values, tuning suggestions, and remediation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
