## Description: <br>
Let agents control software, including Adobe Photoshop, Illustrator, After Effects, Premiere, Autodesk 3DS Max, Blender, Unity, Houdini, and Microsoft Office. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkislev](https://clawhub.ai/user/sfkislev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Flue when a user asks for bounded inspection or edits inside supported desktop applications, including creative, 3D, game-development, and Office workflows. The skill is intended for user-directed automation in a specific requested application, not unattended background changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control live creative, 3D, and Office desktop applications when the user allows it. <br>
Mitigation: Confirm the target application, file or project, and whether the requested action is read-only or allowed to edit before using Flue. <br>
Risk: Automation can modify important local files or active projects. <br>
Mitigation: Work on copies for important files, prefer small inspectable steps, and avoid destructive actions unless the user explicitly requested them. <br>
Risk: Installation or setup changes the local environment. <br>
Mitigation: Install or run setup only after explicit approval in the current session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sfkislev/flue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, app-specific code snippets, and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to send small app-specific scripts through Flue bridge commands and interpret structured JSON returned by desktop application runtimes.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
