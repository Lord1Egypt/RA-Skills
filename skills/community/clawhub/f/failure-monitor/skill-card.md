## Description: <br>
Automated failure detection, diagnosis, and auto-repair system for cron jobs. Monitors task health, fixes common issues automatically, and requests human confirmation when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw cron jobs, diagnose failed scheduled tasks, apply simple automated repairs, and escalate failures that need human action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically edit cron jobs and change file permissions with weak safeguards. <br>
Mitigation: Use only in a controlled OpenClaw environment, add dry-run or explicit approval for cron and permission changes, and constrain edits to trusted targets. <br>
Risk: Hardcoded local paths and a Discord target may send reports or apply changes in the wrong environment. <br>
Mitigation: Make paths and notification targets configurable before deployment and review them during installation. <br>
Risk: Shell commands are built from job-derived values. <br>
Mitigation: Replace shell interpolation with argument-based execution and validate cron IDs, channels, and script paths before running commands. <br>


## Reference(s): <br>
- [Failure Monitor on ClawHub](https://clawhub.ai/sunnyhot/failure-monitor) <br>
- [Publisher profile: sunnyhot](https://clawhub.ai/user/sunnyhot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON configuration, and notification-style status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron health summaries, repair recommendations, and records of automated or manual follow-up actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
