## Description: <br>
Daily Calorie Balance combines Calorie Visualizer food intake with clawhealth-garmin calorie expenditure data to calculate a daily net calorie balance summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvzaiyi-afk](https://clawhub.ai/user/lvzaiyi-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who track diet and Garmin activity use this skill to combine food intake and calorie expenditure into a daily net calorie balance summary, either on demand or through a scheduled run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes private food intake and Garmin activity data and can automatically send daily summaries to a fixed QQ recipient. <br>
Mitigation: Install only if you recognize and control the recipient, change the recipient before enabling scheduled auto mode, or avoid auto mode. <br>
Risk: Summaries and health-oriented advice can be misleading when food records are missing or Garmin data has not been synced. <br>
Mitigation: Confirm calorie records and Garmin data are current before relying on the generated balance or advice. <br>
Risk: Garmin data access depends on the configured account region. <br>
Mitigation: Confirm the Garmin region setting matches the user's account before using the skill. <br>


## Reference(s): <br>
- [Daily Calorie Balance on ClawHub](https://clawhub.ai/lvzaiyi-afk/daily-calorie-balance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style daily summary with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print a manual summary or send an automatic summary to a configured messaging recipient.] <br>

## Skill Version(s): <br>
1.2.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
