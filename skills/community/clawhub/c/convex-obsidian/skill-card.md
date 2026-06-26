## Description: <br>
Adds persistent OpenClaw memory by saving conversation turns to Convex and searching Convex plus local Obsidian Markdown notes for relevant context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreytsushima](https://clawhub.ai/user/andreytsushima) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent memory that can save conversation turns, search recent cloud memory and local Obsidian notes, and inject retrieved context when prior discussion is relevant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically store conversation content in a Convex cloud deployment. <br>
Mitigation: Use a Convex deployment you control, rotate exposed deployment keys, and enable automatic save only after confirming retention, deletion, and access controls. <br>
Risk: Automatic context injection may reuse previous conversations when trigger phrases are detected. <br>
Mitigation: Disable automatic context injection unless explicitly wanted and review injected context before relying on it. <br>
Risk: Local Obsidian searches can expose note previews in agent context. <br>
Mitigation: Set a narrow vault path and avoid storing secrets, client data, or regulated personal information in searchable notes. <br>
Risk: Artifact setup text includes hardcoded Convex deployment details. <br>
Mitigation: Remove hardcoded endpoints or keys before installation and rotate any exposed deployment keys. <br>


## Reference(s): <br>
- [ClawHub skill page: Convex Obsidian](https://clawhub.ai/andreytsushima/convex-obsidian) <br>
- [ClawHub publisher profile: andreytsushima](https://clawhub.ai/user/andreytsushima) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write conversation memories to Convex and Markdown notes to an Obsidian vault when configured or invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
