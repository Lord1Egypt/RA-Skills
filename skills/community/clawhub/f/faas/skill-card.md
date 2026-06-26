## Description: <br>
Deep workflow for serverless workloads: event sources, IAM, cold start/latency, limits, observability, security, cost, and deployment patterns for functions, containers, and step functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to design or debug serverless workloads across AWS Lambda, Google Cloud Functions, Azure Functions, and edge workers, with attention to triggers, IAM, networking, performance, observability, and cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cloud commands, IAM policy edits, or deployment changes could affect live infrastructure if applied without review. <br>
Mitigation: Review proposed infrastructure changes, especially IAM and deployment updates, before running them in production environments. <br>
Risk: Incorrect retry, idempotency, or dead-letter handling guidance could cause duplicate side effects or missed failure recovery in serverless workflows. <br>
Mitigation: Confirm event contracts, idempotency keys, retry policies, and DLQ replay procedures against the target cloud platform and workload. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists and optional inline commands or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory workflow; review generated cloud commands, IAM policy edits, and deployment changes before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
