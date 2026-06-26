## Description: <br>
Use gog (Google CLI) without manual OAuth setup while Civic handles token management automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[civictechuser](https://clawhub.ai/user/civictechuser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let agents run Google Workspace commands through gog without manually creating OAuth credentials or managing refresh tokens. It is intended for workflows that need scoped access to Gmail, Calendar, Drive, Docs, Sheets, Slides, Tasks, Contacts, Chat, Forms, or Apps Script after user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable powerful Google Workspace actions after OAuth consent, including write, delete, share, send, transfer, and deploy operations. <br>
Mitigation: Authorize only the scopes needed for the task and review agent requests before commands that modify, share, send, transfer, or deploy account data. <br>
Risk: CIVIC_TOKEN grants access to the user's Civic account and the skill depends on trusting Civic and the external openclaw-google package to broker Google OAuth access. <br>
Mitigation: Install only when Civic and the package are trusted, protect CIVIC_TOKEN like an API key, avoid custom proxy URLs unless controlled by the user, and revoke Civic or Google access when the integration is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/civictechuser/civic-google) <br>
- [openclaw-google Source Code](https://github.com/civicteam/openclaw-google) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and CIVIC_TOKEN environment variable.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
