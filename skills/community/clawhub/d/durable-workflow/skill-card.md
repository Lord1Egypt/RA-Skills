## Description: <br>
Patterns and procedures for building AI agent workflows that survive real-world failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[old-greggyboy](https://clawhub.ai/user/old-greggyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design multi-step automations, pipelines, and agent workflows with checkpoints, retries, locks, dead letter handling, and failure alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persisted workflow state, dead letter files, outputs, or lock files can expose secrets or collide with other runs if copied without path planning. <br>
Mitigation: Choose dedicated state, DLQ, output, and lock paths before running or adapting the scripts, and avoid storing secrets in persisted files. <br>
Risk: Failure alerts can send sensitive error text to Telegram or another external service. <br>
Mitigation: Redact error messages and review alert destinations before enabling external alerting. <br>


## Reference(s): <br>
- [Agent Workflow Failure Taxonomy](references/failure-taxonomy.md) <br>
- [Durable Workflow on ClawHub](https://clawhub.ai/old-greggyboy/durable-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow design patterns and reusable Node.js helper code for checkpointing, retries, locking, dead letter queues, and alerting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
