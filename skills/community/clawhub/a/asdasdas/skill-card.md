## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hailinhmacduc](https://clawhub.ai/user/hailinhmacduc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Google Workspace users use this skill to set up and run gog commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external gog CLI and Google Workspace OAuth access. <br>
Mitigation: Install gog only from a trusted source, grant only the Google services needed, and revoke OAuth access when it is no longer required. <br>
Risk: Commands can send mail, create events, or update and clear spreadsheet data. <br>
Mitigation: Review send, create, update, and clear commands before running them, especially in scripted or no-input workflows. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/hailinhmacduc/asdasdas) <br>
- [gog homepage](https://gogcli.sh) <br>
- [Installation and use instructions](https://claude.ai/public/artifacts/59bf1058-3a4c-450b-af5b-c85c13cfa8ab) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may use JSON output for scripting with gog flags such as --json and --no-input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
