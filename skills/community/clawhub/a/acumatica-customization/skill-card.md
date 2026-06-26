## Description: <br>
Manage Acumatica ERP customization projects via the CustomizationApi web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allanwei](https://clawhub.ai/user/allanwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Acumatica administrators use this skill to list, export, import, validate, publish, unpublish, delete, and check customization projects, and to toggle maintenance mode during customization lifecycle work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help run ERP-changing operations such as import, publish, unpublish, delete, and maintenance-mode commands. <br>
Mitigation: Require explicit human approval before those commands, especially for production systems or all-tenant scope. <br>
Risk: The helper uses local Acumatica credentials and session-based authentication. <br>
Mitigation: Use HTTPS, least-privileged Acumatica accounts, keep acumatica.conf out of source control, and restrict it with chmod 600. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allanwei/acumatica-customization) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that call Acumatica REST endpoints and require local acumatica.conf credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
