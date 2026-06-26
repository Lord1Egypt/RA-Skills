## Description: <br>
Generates a daily morning briefing by collecting current news, organizing highlights, and sending the briefing to a configured executive recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and executive-support agents use this skill to prepare a scheduled morning briefing from current news and send it to a configured recipient. It is intended for automated briefing workflows where recipients and delivery behavior are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send generated briefings and attachments to an executive recipient. <br>
Mitigation: Verify the recipient configuration and use a draft or approval step before messages or attachments are sent. <br>
Risk: The implementation uses broad shell-based commands without clear approval or permission boundaries. <br>
Mitigation: Review the commands before installation and tighten execution permissions before using the skill in a sensitive workspace. <br>


## Reference(s): <br>
- [Daily Morning Meeting on ClawHub](https://clawhub.ai/johnsmithfan/daily-morning-meeting) <br>
- [Publisher profile: johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing saved as a file and sent through a message action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable search count, maximum news items, save path, recipient, schedule, and topic scope.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
