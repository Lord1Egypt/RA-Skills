## Description: <br>
Manage CalDAV calendars from the command line, including iCloud, Google, Yandex, and custom CalDAV servers with OAuth2 or Basic authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberash-dev](https://clawhub.ai/user/cyberash-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and calendar power users use this skill to install and operate caldav-cli for managing CalDAV accounts, listing calendar events, and creating events from Linux or macOS terminals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI connects to calendar accounts and can read calendar data or create events in connected calendars. <br>
Mitigation: Only connect calendar accounts intended for this workflow, review event creation commands before execution, and confirm target account and calendar flags. <br>
Risk: The workflow requires calendar credentials, OAuth2 tokens, OAuth client credentials, and OS keychain access. <br>
Mitigation: Use the documented OS keychain storage path, verify the local config file is limited to account metadata, and install caldav-cli only from a trusted npm package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberash-dev/caldav-cli) <br>
- [caldav-cli source link from metadata](https://github.com/cyberash-dev/caldav-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; caldav-cli can return table or JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the caldav-cli binary, local config at ~/.config/caldav-cli/config.json, and OS keychain access.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
