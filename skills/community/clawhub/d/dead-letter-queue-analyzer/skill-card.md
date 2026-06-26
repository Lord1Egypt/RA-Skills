## Description: <br>
Analyze dead letter queue (DLQ) messages to identify failure patterns, root causes, and remediation strategies. Supports AWS SQS, RabbitMQ, Kafka, Azure Service Bus, and generic message queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect DLQ backlogs, categorize message failures, identify likely root causes, and plan safe remediation or replay steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DLQ message bodies and attributes may contain sensitive operational or customer data. <br>
Mitigation: Use least-privilege queue credentials, limit reads to the minimum needed for analysis, and treat message payloads as sensitive data. <br>
Risk: Replaying DLQ messages before the underlying cause is fixed can repeat failures or trigger duplicate and unsafe side effects. <br>
Mitigation: Confirm the target environment and queues, fix the root cause first, review replay scope, throttle replay, and account for idempotency and duplicate handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/dead-letter-queue-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, tables, reports, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include queue inspection commands, DLQ analysis summaries, replay guidance, monitoring recommendations, and prevention recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
