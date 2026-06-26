## Description: <br>
Provision and manage @clawemail.com Google Workspace email accounts for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cto1](https://clawhub.ai/user/cto1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create, check, list, suspend, unsuspend, or delete @clawemail.com Google Workspace accounts for AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer ClawEmail Google Workspace accounts, including suspension and permanent deletion, through a privileged API key. <br>
Mitigation: Install only if you trust ClawEmail, keep CLAWEMAIL_API_KEY secret, and require manual confirmation of the exact prefix or email before suspend or delete actions. <br>
Risk: Account creation returns sensitive credentials, including a one-time password and OAuth connection link. <br>
Mitigation: Store generated passwords and OAuth credentials securely, and avoid exposing them in logs, shared transcripts, or unsecured files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cto1/clawemail-admin) <br>
- [Publisher profile](https://clawhub.ai/user/cto1) <br>
- [ClawEmail service](https://clawemail.com) <br>
- [ClawEmail availability check](https://clawemail.com/check/DESIRED_PREFIX) <br>
- [ClawEmail self-service signup](https://clawemail.com/signup?prefix=DESIRED_PREFIX) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Admin actions require CLAWEMAIL_API_KEY; the availability check and self-service signup do not require an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
