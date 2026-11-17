## Description:

Monitors OpenClaw cron job health, identifies failures, timeouts, and delivery issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw cron jobs, review recent run history, detect repeated failures or timeouts, and identify delivery or OpenRouter API-limit issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw cron job configuration and recent run logs from the user's OpenClaw home.

Mitigation: Install and run it only where local access to those cron files is appropriate.

Risk: Health output can include job errors, operational details, or account/API-limit information.

Mitigation: Review generated text or JSON reports before sharing them outside the intended operational context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/cron-health-check-zc)
- [ClawHub publisher profile](https://clawhub.ai/user/lean-zhouchao)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON health report with exit codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports healthy, warning, and critical status per cron job; exits 0 for healthy, 1 for warnings, and 2 for critical issues.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
