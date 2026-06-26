## Description: <br>
Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and run a portable computer-use MCP runtime that selects the correct macOS, Windows, or Linux payload for the current host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose visible screen contents, clipboard text, application state, and GUI input through desktop-control behavior. <br>
Mitigation: Install and run it only in a trusted local desktop session, and avoid private documents, financial apps, credentials, or other sensitive workflows unless the permission flow has been reviewed. <br>
Risk: The security evidence says powerful screen, clipboard, app, and input permissions are granted silently where users may expect manual approval. <br>
Mitigation: Review or patch the permission flow before deployment, and require explicit operator approval for sensitive applications or actions. <br>


## Reference(s): <br>
- [Cross Platform Computer Use Skill on ClawHub](https://clawhub.ai/wimi321/cross-platform-computer-use-skill) <br>
- [macOS Computer-Use Skill on ClawHub](https://clawhub.ai/wimi321/computer-use-macos) <br>
- [Windows Computer-Use Skill on ClawHub](https://clawhub.ai/wimi321/computer-use-windows) <br>
- [Linux Computer-Use Skill on ClawHub](https://clawhub.ai/wimi321/computer-use-linux) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to build and run a host-specific MCP desktop-control runtime.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
