## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erdmannsilva](https://clawhub.ai/user/erdmannsilva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run the gog CLI for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Google Workspace OAuth access and can access or change account data. <br>
Mitigation: Authorize only the needed Google services and account, review requested OAuth scopes, and revoke the grant when the skill is no longer needed. <br>
Risk: Commands may send email, create calendar events, or modify Sheets and Drive data. <br>
Mitigation: Review commands before execution, especially write operations, and prefer JSON or no-input modes for scripted workflows. <br>
Risk: The workflow depends on the external gog CLI distributed through a Homebrew tap. <br>
Mitigation: Install only if the gog CLI and tap are trusted in the target environment. <br>


## Reference(s): <br>
- [gog homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/erdmannsilva/erdmannsilva-gog) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/erdmannsilva) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read or modify Google Workspace data through the gog CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
