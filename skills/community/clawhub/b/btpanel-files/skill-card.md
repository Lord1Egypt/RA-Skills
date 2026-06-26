## Description: <br>
Provides BT Panel file-management actions for browsing directories, reading and editing files, creating and deleting paths, changing permissions, downloading files, and extracting archives on configured servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aapanel](https://clawhub.ai/user/aapanel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operations teams use this skill to let an agent inspect and manage files on configured BT Panel servers. It supports routine remote file workflows such as listing directories, reading logs, editing configuration files, changing permissions, downloading assets, and extracting archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires BT Panel API tokens and stores server configuration for agent-driven operations. <br>
Mitigation: Use the least-privileged token available, protect the configuration file, and avoid exposing full configuration output in shared logs. <br>
Risk: The skill can modify remote server state by editing, deleting, downloading, unzipping, or recursively changing permissions on files. <br>
Mitigation: Manually confirm the target server, path, and expected effect before any destructive or broad operation, and keep backups for important files. <br>
Risk: The skill can inspect remote file contents that may include sensitive data. <br>
Mitigation: Limit use to trusted servers and avoid reading credential files, environment files, private keys, or other sensitive paths unless explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aapanel/btpanel-files) <br>
- [aapanel publisher profile](https://clawhub.ai/user/aapanel) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Usage README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-like command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include remote file contents, directory listings, permission details, progress messages, and configuration steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
