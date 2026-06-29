## Description: <br>
Enable real-time collaboration by exposing a local collaborative editing tool via aitun tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI agents, and users use this skill to set up real-time co-editing sessions for code, documents, configuration files, or whiteboards through a temporary aitun tunnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose an unauthenticated browser editor or other local collaboration service to the public internet. <br>
Mitigation: Enable authentication on the editor or whiteboard, use it only for deliberate collaboration sessions, avoid sensitive repositories or credentials, and stop the tunnel and collaboration server when finished. <br>
Risk: The tunnel can expose local services beyond the intended collaboration surface if broad or sensitive ports are selected. <br>
Mitigation: Limit tunneling to the intended HTTP collaboration port and do not expose SSH, databases, or credential-bearing services through this workflow. <br>
Risk: Installer commands that pipe remote scripts to a shell increase setup-time trust requirements. <br>
Mitigation: Prefer pip or uv installation for aitun, and review any remote installer before executing it. <br>


## Reference(s): <br>
- [Aitun](https://aitun.cc) <br>
- [ClawHub listing](https://clawhub.ai/ctz168/collab-edit) <br>
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/collab-edit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public collaboration URLs and local process identifiers for cleanup.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
