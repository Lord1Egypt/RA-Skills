## Description: <br>
Control your Fellow Aiden smart coffee brewer via AI assistant to view brewer status, manage brew profiles, import and share brew links, and manage brewing schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mogglemoss](https://clawhub.ai/user/mogglemoss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users with a Fellow Aiden brewer use this skill to let an AI assistant inspect brewer information, list and retrieve profiles, and list schedules through their Fellow account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Fellow account email and password to access brewer data. <br>
Mitigation: Store credentials with a secure secret mechanism when possible and avoid putting passwords in shared shell profiles or logs. <br>
Risk: Some advertised profile and schedule management commands are not implemented in the reviewed script. <br>
Mitigation: Confirm command support before relying on create, delete, import, share, or schedule-management workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mogglemoss/fellow-aiden) <br>
- [Skill homepage](https://github.com/9b/fellow-aiden) <br>
- [Fellow Aiden product page](https://fellowproducts.com/products/aiden) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and Fellow account credentials supplied through FELLOW_EMAIL and FELLOW_PASSWORD.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
