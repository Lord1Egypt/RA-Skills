## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aceundefeated](https://clawhub.ai/user/aceundefeated) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run the `gog` CLI for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. It supports OAuth setup, read operations, exports, and state-changing commands such as sending mail or updating spreadsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external `gog` CLI with broad Google Workspace account access. <br>
Mitigation: Install only if the `gog` CLI and Homebrew source are trusted, use the least-privileged Google account practical, and review OAuth scopes during consent. <br>
Risk: Commands can send email, create calendar items, modify Sheets, copy or export Docs, and touch shared Drive content. <br>
Mitigation: Require explicit approval before running state-changing or shared-content commands, and prefer `--json` plus `--no-input` for scripted read workflows. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [Aj Gog ClawHub page](https://clawhub.ai/aceundefeated/aj-gog) <br>
- [Publisher profile](https://clawhub.ai/user/aceundefeated) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external `gog` binary, Google OAuth credentials, and user confirmation for sensitive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
