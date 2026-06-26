## Description: <br>
Query and interact with ClassCharts, a UK education classroom management platform, through the classcharts-api JavaScript library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m0nkmaster](https://clawhub.ai/user/m0nkmaster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, students, and authorized developers use this skill to work with ClassCharts data such as homework, behavior points, timetables, detentions, attendance, announcements, and rewards. It supports parent and student login flows for scripting or integrating with ClassCharts accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access children's school records and ClassCharts account data. <br>
Mitigation: Use only accounts and pupil records the user is authorized to access, keep credentials in environment variables or a secure secret store, and request only the minimum necessary data. <br>
Risk: The skill documents account-modifying actions such as changing a parent password and purchasing rewards. <br>
Mitigation: Require explicit user confirmation before any password change, reward purchase, or other account-modifying action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/m0nkmaster/classcharts) <br>
- [Library docs](https://classchartsapi.github.io/classcharts-api-js) <br>
- [Unofficial API docs](https://classchartsapi.github.io/api-docs/) <br>
- [classcharts-api-js GitHub repository](https://github.com/classchartsapi/classcharts-api-js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment variable guidance for ClassCharts credentials and date-format requirements.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
