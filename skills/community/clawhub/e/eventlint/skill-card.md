## Description: <br>
Event & message queue anti-pattern analyzer -- detects producer/consumer issues, schema problems, dead letter queue gaps, ordering failures, and observability gaps in event-driven architectures (Kafka, RabbitMQ, SQS, NATS, Redis Pub/Sub). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use EventLint to scan codebases for event-driven architecture anti-patterns across Kafka, RabbitMQ, SQS, NATS, and Redis Pub/Sub. It supports local quality checks, CI/CD gating, report generation, and optional git hook integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is classified as suspicious because local execution, optional git-hook installation, and license handling create review-worthy risks. <br>
Mitigation: Review the skill before installing it, enable hooks only in repositories where automatic EventLint checks and possible commit or push blocking are intended, and keep hook configuration under source review. <br>
Risk: Paid-tier, status, report, and hook commands depend on license-key handling that the security guidance says should be avoided until the parser is fixed. <br>
Mitigation: Use free local scans for initial evaluation, avoid untrusted license keys, and avoid paid-tier, status, report, and hook commands until the license parser has been reviewed and fixed. <br>


## Reference(s): <br>
- [EventLint homepage](https://eventlint.pages.dev) <br>
- [EventLint hook documentation](https://eventlint.pages.dev/docs/hooks) <br>
- [ClawHub EventLint listing](https://clawhub.ai/suhteevah/eventlint) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, JSON, HTML, Shell commands, Configuration] <br>
**Output Format:** [Text, JSON, HTML, and Markdown reports with shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scan results include findings, severity, recommendations, scores, grades, and exit codes; optional git hooks can block commits or pushes when checks fail.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
