## Description: <br>
Give OpenClaw a body: a tiny fluid glass ball desktop pet with voice cloning, 15+ eye expressions, desktop lyrics overlay, and 7 mood colors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk43994](https://clawhub.ai/user/kk43994) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and run a desktop companion that gives an OpenClaw agent a visual presence, speech output, desktop lyrics, mood colors, and optional Feishu/Lark synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an external Electron project and install npm dependencies. <br>
Mitigation: Install only from the referenced repository, review dependencies before use, and run without administrator privileges where possible. <br>
Risk: Optional voice cloning can create consent and privacy concerns. <br>
Mitigation: Use MiniMax voice cloning only with consent from the voice owner and review voice settings before enabling the feature. <br>
Risk: Optional Feishu/Lark synchronization can expose sensitive workplace messages. <br>
Mitigation: Enable chat synchronization only for approved workspaces and avoid syncing sensitive messages unless the organization permits it. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kk43994/desktop-pet) <br>
- [GitHub repository](https://github.com/kk43994/claw-desktop-pet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes npm-based setup steps, optional MiniMax voice configuration, and OpenClaw gateway startup guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
