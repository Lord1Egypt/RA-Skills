## Description: <br>
Chat Bus provides a shared-directory message bus that lets users or agents exchange direct, room, broadcast, and history messages through JSON files on a filesystem-backed shared folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate conversations between users or agents through a shared directory when a lightweight filesystem-backed chat channel is sufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages are stored as plaintext files in the shared directory and rely on that directory's access controls. <br>
Mitigation: Use a dedicated shared folder with trusted participants, restrict filesystem permissions, and avoid sending secrets. <br>
Risk: Server security evidence reports that unchecked room and user path inputs can affect files outside the intended chat directory. <br>
Mitigation: Avoid room or user names from untrusted input and deploy only with trusted participants until path validation, containment checks, and registration checks are added. <br>
Risk: Usernames and room membership are not described as authenticated identities. <br>
Mitigation: Do not treat displayed usernames or room membership as proof of identity; verify sensitive actions through a separate trusted channel. <br>


## Reference(s): <br>
- [chat-bus protocol](references/protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell examples and JSON command/response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses timestamped JSON files in a user-provided shared chat directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
