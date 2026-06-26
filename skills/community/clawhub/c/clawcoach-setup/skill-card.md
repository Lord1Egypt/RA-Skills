## Description: <br>
One-time setup for ClawCoach AI health coaching. Configures your profile, goals, macro targets, dietary preferences, and coach personality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[authoredniko](https://clawhub.ai/user/authoredniko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to complete first-run setup for ClawCoach by recording profile details, goals, macro targets, dietary preferences, and coach persona. It guides the conversation, explains why personal details are requested, and stores the resulting local configuration for later ClawCoach interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup process collects and stores sensitive personal, health, diet, and preference details on the user's machine. <br>
Mitigation: Provide only fields the user wants stored locally, and review or delete ~/.clawcoach/ when the profile or logs should no longer be retained. <br>
Risk: Nutrition targets are calculated from self-reported profile details and may be inappropriate if the inputs are omitted or inaccurate. <br>
Mitigation: Treat generated targets as configurable setup values, allow user adjustment, and use qualified health guidance for medical or high-stakes dietary decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/authoredniko/clawcoach-setup) <br>
- [Publisher profile](https://clawhub.ai/user/authoredniko) <br>
- [Project homepage](https://github.com/clawcoach/clawcoach) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational Markdown guidance with local JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The setup flow may create or update profile, food-log, and daily-total JSON files under ~/.clawcoach/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
