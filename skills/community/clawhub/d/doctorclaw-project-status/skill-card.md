## Description: <br>
Project status board - compile daily status from tasks, calendar, and team updates into one dashboard. Daily cron or on-demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers, operators, and team leads use this skill to compile a daily project status board from task systems, calendar-derived milestones, blockers, and team workload inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may collect or summarize sensitive project tasks, calendar-derived milestones, and team workload details. <br>
Mitigation: Limit configured sources to approved projects and people, and redact sensitive client, personnel, or confidential delivery details before sharing reports. <br>
Risk: Scheduled delivery could send status reports to an inappropriate or overly broad channel. <br>
Mitigation: Use only approved private delivery channels and confirm recipients before enabling daily cron delivery. <br>
Risk: Archived reports may retain sensitive project history longer than intended. <br>
Mitigation: Set a retention or cleanup policy for saved reports under memory/project-status. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ceobotson-bot/doctorclaw-project-status) <br>
- [DoctorClaw website](https://www.doctorclaw.ceo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown status board with project health, progress, blockers, team workload, and priority actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be delivered on demand or scheduled for daily reporting, and may be archived as dated Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
