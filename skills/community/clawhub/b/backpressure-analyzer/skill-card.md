## Description: <br>
Detect and resolve backpressure issues in data pipelines, message queues, and streaming systems. Identify bottleneck stages, measure queue depths and processing rates, and recommend flow control strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to diagnose backpressure in data pipelines, message queues, and streaming systems, then plan flow-control responses such as rate limiting, autoscaling, bounded buffers, circuit breakers, or load shedding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic commands may query production brokers, queues, cloud accounts, namespaces, or clusters and expose operational metadata. <br>
Mitigation: Review commands before running them, use least-privilege read-only credentials where possible, and confirm the target environment. <br>
Risk: Recommendations such as autoscaling, circuit breakers, or load shedding can change production behavior if applied directly. <br>
Mitigation: Treat recommendations as operational proposals that require normal human approval, testing, and rollback planning. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic reports, command suggestions, flow-control recommendations, and alerting rule examples for human review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
