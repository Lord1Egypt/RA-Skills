## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snilpmud](https://clawhub.ai/user/snilpmud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Google Workspace users use this skill to get setup guidance and `gog` CLI commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credentials and generated tokens can grant access to Google Workspace data. <br>
Mitigation: Use the minimum required OAuth services, protect `client_secret.json` and generated tokens, and avoid committing or sharing credentials. <br>
Risk: Commands can send email, create calendar entries, clear sheets, or modify production data. <br>
Mitigation: Explicitly confirm sensitive actions before execution and prefer `--json` plus `--no-input` for scripted workflows. <br>
Risk: The skill depends on the third-party `gog` CLI. <br>
Mitigation: Install only if you trust the `gog` CLI and need agent access to Google Workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snilpmud/cs-gog) <br>
- [Publisher profile](https://clawhub.ai/user/snilpmud) <br>
- [gog CLI homepage](https://gogcli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented CLI examples when the skill recommends `--json` output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
