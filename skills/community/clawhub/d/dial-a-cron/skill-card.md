## Description: <br>
Stateful cron system for OpenClaw with persistent memory, change detection, smart routing, token budget tracking, and self-healing; requires openclaw and gog CLIs and has broad I/O capabilities that require careful review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenthyjack](https://clawhub.ai/user/agenthyjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Dial A Cron to add persistent state, change detection, routing, token-budget tracking, and self-healing behavior to scheduled OpenClaw jobs for monitoring, reporting, data pipeline, and maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job configs can run shell commands and include unsanitized values in shell-based delivery paths. <br>
Mitigation: Audit all job configs before use, restrict who can edit them, and run the skill with least privilege in an isolated account or container. <br>
Risk: Diffs and routes can read local files, fetch arbitrary HTTP URLs, and send outputs to external endpoints. <br>
Mitigation: Allowlist HTTP targets, restrict diff file paths to safe directories, disable or tightly control webhooks and external routes, and avoid jobs that collect secrets. <br>
Risk: Persisted state and logs may contain sensitive job output. <br>
Mitigation: Set DAC_JOBS_DIR, DAC_STATE_DIR, and DAC_LOG_DIR to controlled locations with restrictive permissions and review retained outputs regularly. <br>
Risk: The skill depends on openclaw and gog CLIs for expected operation. <br>
Mitigation: Confirm those CLIs are installed, patched, and configured with minimal credentials before enabling scheduled jobs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agenthyjack/dial-a-cron) <br>
- [Job Config Schema Reference](references/job-config-schema.md) <br>
- [Security Review](references/security-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON job configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent state, logs, routed notifications, and DAC_CONTEXT text during job execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
