## Description:

Alibaba Cloud Elasticsearch instance diagnosis skill for cluster health checks, troubleshooting, and performance analysis on Elasticsearch instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to diagnose Alibaba Cloud Elasticsearch incidents by combining control-plane, CloudMonitor, Elasticsearch REST API, and SOP evidence into root-cause analysis and prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful Alibaba Cloud or Elasticsearch credentials may be exposed or overused during diagnosis.

Mitigation: Use configured local CLI profiles or local environment variables only, avoid plaintext secrets in chat or saved commands, and prefer least-privilege diagnostic users.

Risk: Authenticated Elasticsearch requests may run without strong transport protection.

Mitigation: Require HTTPS with certificate validation for authenticated requests, using an appropriate CA bundle or equivalent trust configuration.

Risk: Remediation examples that use PUT, POST, or DELETE can change cluster state or data.

Mitigation: Treat mutating API calls as proposed changes that require backups, explicit human authorization, and an approved change workflow before execution.

Risk: CLI or plugin installation drift can change diagnostic behavior.

Mitigation: Pin, update intentionally, and verify Aliyun CLI and plugin versions before relying on generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-elasticsearch-instance-diagnose)
- [Alibaba Cloud Elasticsearch CLI tools](https://api.aliyun.com/api-tools/cli/elasticsearch/2017-06-13)
- [Alibaba CloudMonitor CLI tools](https://api.aliyun.com/api-tools/cli/Cms/2019-01-01)
- [References index](references/README.md)
- [Related APIs](references/related-apis.md)
- [Elasticsearch API diagnosis strategy](references/es-api-diagnosis-strategy.md)
- [Elasticsearch REST API catalog](references/es-api-catalog.md)
- [Health events catalog](references/health-events-catalog.md)
- [Report template](references/report-template.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic report with inline shell commands, API calls, evidence keys, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include P0/P1/P2 findings, evidence chains, recency-ordered incident timelines, connectivity limits, and verification steps.]

## Skill Version(s):

0.0.1 (source: server release metadata, released 2026-04-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
