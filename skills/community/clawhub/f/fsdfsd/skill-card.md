## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hailinhmacduc](https://clawhub.ai/user/hailinhmacduc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up OAuth access and run gog commands for Gmail, Calendar, Drive, Contacts, Sheets, Docs, and related Google Workspace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access to real Google Workspace data across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>
Mitigation: Use the narrowest OAuth scopes and a low-privilege account where possible, and require explicit confirmation before sending email, changing calendar data, modifying Sheets, copying Docs, or exporting Workspace content. <br>
Risk: The skill points to mutable external instructions that may change after publication. <br>
Mitigation: Review external instructions manually before use instead of letting an agent treat them as trusted commands. <br>
Risk: OAuth client secret and token files can grant access to Workspace data if exposed. <br>
Mitigation: Protect client_secret.json and generated token files, keep them out of shared workspaces, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [External gog usage instructions](https://claude.ai/public/artifacts/59bf1058-3a4c-450b-af5b-c85c13cfa8ab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, OAuth, scripting, read, write, and export command examples for the gog CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
