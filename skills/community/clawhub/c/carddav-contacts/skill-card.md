## Description: <br>
Sync and manage CardDAV contacts (Google, iCloud, Nextcloud, etc.) using vdirsyncer + khard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcromero](https://clawhub.ai/user/jcromero) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to configure, sync, search, inspect, and manage CardDAV address books through vdirsyncer and khard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose contact data and account access through vdirsyncer, khard, local contact files, and an app-password file. <br>
Mitigation: Use an app-specific password where possible and restrict permissions on the password file and local contact storage. <br>
Risk: Contact edit, move, remove, sync, or conflict-resolution operations can change or delete address book data. <br>
Mitigation: Review conflict-resolution settings and ask the agent to confirm the exact contact before edit, move, or delete operations. <br>


## Reference(s): <br>
- [CardDAV Contacts on ClawHub](https://clawhub.ai/jcromero/carddav-contacts) <br>
- [Publisher profile](https://clawhub.ai/user/jcromero) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command and configuration guidance for vdirsyncer and khard; does not directly sync contacts without user execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
