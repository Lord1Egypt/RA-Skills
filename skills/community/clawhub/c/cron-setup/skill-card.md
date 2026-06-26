## Description: <br>
Create and manage OpenClaw cron jobs following our conventions. Use when setting up periodic tasks, reminders, automated checks, or any scheduled work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to define scheduled OpenClaw agent work, including recurring checks, reminders, digests, and notification jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs can grant recurring command-execution authority and route results to external message destinations. <br>
Mitigation: Review each scheduled payload before enabling it, avoid secrets or private workspace data in messages, and require user-controlled destinations plus explicit approval for recurring jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/cron-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron schedule patterns, job templates, model guidance, delivery mode guidance, and notification conventions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
