## Description: <br>
Generates one OpenTelemetry Collector or Filebeat YAML configuration for collecting file, OTLP or webhook, or Kafka log input and sending it to Alibaba Cloud Elasticsearch or self-managed Elasticsearch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to build a single Elasticsearch log-ingestion configuration after confirming the collector stack, input source, destination, authentication, TLS, and optional reliability features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Templates can expose ingestion endpoints without authentication or on public interfaces. <br>
Mitigation: Bind listeners to localhost or private interfaces unless public exposure is required, and enable TLS plus authentication or HMAC before production use. <br>
Risk: High-privilege or destructive options may increase operational impact if enabled without review. <br>
Mitigation: Avoid Docker socket or root access where possible, and do not enable source log deletion without backups and verified delivery. <br>
Risk: Kafka headers, request metadata, or log fields may carry sensitive values into Elasticsearch. <br>
Mitigation: Redact, mask, or allowlist metadata and sensitive fields before shipping logs to Elasticsearch. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/sdk-team/skills/alibabacloud-elasticsearch-log-config-generator) <br>
- [RAM Permission Policy](references/ram-policies.md) <br>
- [OpenTelemetry elasticsearchexporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/elasticsearchexporter/README.md) <br>
- [OpenTelemetry filelogreceiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/filelogreceiver/README.md) <br>
- [OpenTelemetry kafkareceiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/kafkareceiver/README.md) <br>
- [OpenTelemetry otlpreceiver](https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver/README.md) <br>
- [Filebeat configuration overview](https://www.elastic.co/docs/reference/beats/filebeat/configuring-howto-filebeat) <br>
- [Filebeat Elasticsearch output](https://www.elastic.co/docs/reference/beats/filebeat/elasticsearch-output) <br>
- [Filebeat filestream input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-filestream) <br>
- [Filebeat kafka input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-kafka) <br>
- [Filebeat http_endpoint input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-http_endpoint) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, code, shell commands, guidance] <br>
**Output Format:** [YAML configuration with concise Markdown guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates exactly one configuration file and references credentials through environment variables.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
