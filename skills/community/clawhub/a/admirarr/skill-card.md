## Description: <br>
Manage a Jellyfin/Plex + *Arr media server stack: check status, add content, monitor downloads, diagnose issues, and restart services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxtechera](https://clawhub.ai/user/maxtechera) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and advanced home-lab users use this skill to ask an agent for Admirarr CLI commands and workflows for managing self-hosted Jellyfin, Plex, and *Arr media server stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Admirarr CLI installer. <br>
Mitigation: Install only when the user trusts the Admirarr project and the get.admirarr.dev installer. <br>
Risk: Admirarr commands can change media-server services, downloads, and configuration. <br>
Mitigation: Require explicit user approval before restart, remove, sync, setup, migrate, or fix actions. <br>
Risk: Download removal can delete files when a delete-files option is used. <br>
Mitigation: Avoid delete-files behavior unless the user explicitly confirms they intend to remove files. <br>


## Reference(s): <br>
- [ClawHub Admirarr skill page](https://clawhub.ai/maxtechera/admirarr) <br>
- [Admirarr installer](https://get.admirarr.dev) <br>
- [Publisher profile](https://clawhub.ai/user/maxtechera) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to prefer JSON CLI output for parsing and clean tables for user-facing summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
