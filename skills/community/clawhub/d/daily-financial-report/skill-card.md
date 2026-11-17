## Description:

生成每日金融日报 orchestrates market and economic data collection, Word report generation, PPT briefing generation, and email delivery when the user asks for a daily financial report, today's report, or a morning brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szrw1825](https://clawhub.ai/user/szrw1825)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a daily financial-report workflow that collects market, economic, policy, and company news data, then produces Word and PowerPoint outputs and sends them by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on unaudited local configuration and sibling skills.

Mitigation: Install and run it only in a controlled OpenClaw workspace after reviewing the external config path and every referenced sibling skill.

Risk: The workflow automatically proceeds to an email-sending step.

Mitigation: Require manual confirmation of recipients, attachments, and output paths before email delivery.

Risk: Earlier report-generation stages may fail without stopping the email stage.

Mitigation: Check stage return codes and generated artifacts before allowing the email step to run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szrw1825/skills/daily-financial-report)
- [Publisher profile](https://clawhub.ai/user/szrw1825)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Word document, PowerPoint deck, JSON data file, log output, and email delivery status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow depends on local configuration, sibling skills, configured output paths, and email settings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
