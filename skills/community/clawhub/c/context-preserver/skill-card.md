## Description: <br>
Context Preserver creates, restores, manages, imports, and exports local context snapshots for agent sessions, including automatic and on-demand snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve local session context, recover prior snapshots, and export or import snapshot metadata during long-running work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Snapshots and exports can include private local metadata such as working directory, username or home path, PATH, shell, platform, and process IDs. <br>
Mitigation: Treat exported snapshots as private, review or redact them before sharing, and disable automatic snapshots for sensitive work. <br>
Risk: Automatic snapshots persist session metadata without an explicit command each time when auto snapshotting is enabled. <br>
Mitigation: Use the provided configuration command to turn automatic snapshots off when working with sensitive projects or environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, JSON snapshot files, and Node.js API return values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snapshots are stored locally under the user's home directory and may be exported as JSON files or directories.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
