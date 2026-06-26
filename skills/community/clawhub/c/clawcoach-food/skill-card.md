## Description: <br>
ClawCoach Food analyzes food photos or text meal descriptions, estimates calories and macros, and logs confirmed meals for ClawCoach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[authoredniko](https://clawhub.ai/user/authoredniko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External ClawCoach users use this skill to analyze meal photos or text descriptions, review estimated calories and macros, and save confirmed meal logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal logs and profile details are stored locally and may contain sensitive health or nutrition information. <br>
Mitigation: Treat ~/.clawcoach/ as sensitive local data and delete that directory when records should no longer be retained. <br>
Risk: Food photo analysis depends on Anthropic API access and estimated nutrition values may be inaccurate. <br>
Mitigation: Review estimates before confirming a meal and adjust unclear foods or portions before logging. <br>


## Reference(s): <br>
- [ClawCoach project homepage](https://github.com/clawcoach/clawcoach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown meal summaries and JSON meal-log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANTHROPIC_API_KEY and stores confirmed meal records locally under ~/.clawcoach/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
