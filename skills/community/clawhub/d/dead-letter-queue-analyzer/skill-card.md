## Description:

Analyze dead letter queue (DLQ) messages to identify failure patterns, root causes, and remediation strategies. Supports AWS SQS, RabbitMQ, Kafka, Azure Service Bus, and generic message queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect dead letter queue messages, categorize failure causes, decide which messages are replayable, and plan remediation for AWS SQS, RabbitMQ, Kafka, Azure Service Bus, or generic message queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DLQ message inspection can expose sensitive message payloads or attributes.

Mitigation: Use least-privileged queue access, inspect only necessary samples, and redact sensitive values before sharing reports.

Risk: Replay guidance can change production queues if used before the failure cause is fixed.

Mitigation: Confirm the root cause is fixed, consumers are idempotent, the destination queue is correct, and replay rate limits are appropriate before moving messages.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes DLQ analysis reports, replay command guidance, monitoring alert recommendations, and message-handling prevention guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
