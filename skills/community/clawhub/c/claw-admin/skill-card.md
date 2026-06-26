## Description: <br>
Provision and manage @clawemail.com Google Workspace email accounts. Use when the user wants to create an email for their AI agent, check email availability, or manage existing ClawEmail accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cto1](https://clawhub.ai/user/cto1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create, check, list, suspend, unsuspend, and delete ClawEmail Google Workspace accounts for AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority over ClawEmail administration, including permanent deletion of email accounts and their data. <br>
Mitigation: Require manual confirmation before suspend or delete actions, especially permanent deletion. <br>
Risk: The skill handles API keys, returned passwords, and OAuth connection details. <br>
Mitigation: Use only an API key the user is comfortable giving to an agent and treat returned passwords and OAuth details as secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cto1/claw-admin) <br>
- [ClawEmail service](https://clawemail.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWEMAIL_API_KEY for administrative endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
