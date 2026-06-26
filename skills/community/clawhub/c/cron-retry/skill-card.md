## Description: <br>
Auto-retries failed cron jobs after connection recovery by using heartbeat checks to identify network-related failures and rerun eligible enabled jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrbobbyhansen-pixel](https://clawhub.ai/user/jrbobbyhansen-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to recover cron jobs that failed because of transient network or connection errors. It guides an agent to inspect cron job status, identify retryable network failures, rerun eligible enabled jobs, and report recovery attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic retries can rerun broad background jobs without clear retry limits or per-job safeguards. <br>
Mitigation: Enable the skill only for explicitly allowlisted cron jobs that are safe to repeat, and configure a retry cap and cooldown before heartbeat-based retries run. <br>
Risk: Retried jobs may post publicly, send duplicate messages, spend money, or modify important data. <br>
Mitigation: Exclude jobs with public posting, payment, duplicate-message, or important data-modification side effects unless they have idempotency controls and human approval. <br>


## Reference(s): <br>
- [Cron Retry on ClawHub](https://clawhub.ai/jrbobbyhansen-pixel/cron-retry) <br>
- [Publisher profile](https://clawhub.ai/user/jrbobbyhansen-pixel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and heartbeat configuration text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces retry criteria, cron command examples, and recovery reporting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
