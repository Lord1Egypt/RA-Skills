## Description: <br>
Monitors OpenClaw cron job health, identifies failures, timeouts, and delivery issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check OpenClaw cron job run history, identify unhealthy jobs, and verify fixes after failures, timeouts, delivery problems, or API limit errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health reports may include job names or error log details that contain private operational information or secrets. <br>
Mitigation: Review output before sharing it and redact sensitive job names, error text, tokens, or private infrastructure details. <br>
Risk: The bundled cron example enables recurring agent-based monitoring. <br>
Mitigation: Enable the scheduled example only when recurring monitoring is intended and the selected agent, model, timeout, and delivery settings match operational requirements. <br>
Risk: The release is from a third-party publisher and evidence notes a naming mismatch to confirm before installation. <br>
Mitigation: Confirm the ClawHub publisher handle, release page, and package naming are acceptable before deploying the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lean-zhouchao/cron-health-check-zc) <br>
- [Publisher profile](https://clawhub.ai/user/lean-zhouchao) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON health report with status counts, per-job issues, recent errors, and exit codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 means all enabled jobs are healthy, 1 means warnings were found, and 2 means critical issues were found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
