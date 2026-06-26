## Description: <br>
Lead qualifier that scores inbound leads against custom criteria, prioritizes hot prospects, and drafts outreach for on-demand or scheduled pipeline review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and business operators use this skill to score inbound leads, rank prospects, identify disqualification reasons, and prepare follow-up drafts for qualified leads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose lead details through alerts or outreach actions. <br>
Mitigation: Use least-privilege CRM and email access, start in report-only mode, and require explicit approval before sending alerts or outreach. <br>
Risk: The artifact includes a hard-coded alert recipient named Stephen. <br>
Mitigation: Replace the hard-coded recipient with the configured business owner before installation or scheduled use. <br>
Risk: Automated CRM updates could misclassify or prematurely change lead status. <br>
Mitigation: Require review before updating CRM records, especially when running the skill on a cron schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/doctorclaw-lead-qualifier) <br>
- [DoctorClaw website](https://www.doctorclaw.ceo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown lead qualification report with scores, ranked categories, reasons, insights, and outreach drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed CRM status updates, alerts, or email outreach actions that should require user approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
