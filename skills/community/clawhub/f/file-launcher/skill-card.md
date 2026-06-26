## Description: <br>
This skill allows the assistant to launch files and open them with their default applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[badwolf-63](https://clawhub.ai/user/badwolf-63) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an assistant to open documents, media files, images, or programs with the default Windows application associated with the target path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assistant may open local files or start programs without an explicit confirmation step. <br>
Mitigation: Require the assistant to confirm the exact file or program path before invoking the skill. <br>
Risk: Opening executables, scripts, shortcuts, unknown downloads, or sensitive documents can expose the user to unintended execution or disclosure. <br>
Mitigation: Avoid using the skill on executables, scripts, shortcuts, unknown downloads, and sensitive documents unless the user has explicitly reviewed and approved the target. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/badwolf-63/file-launcher) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/badwolf-63) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Windows default application associations through Invoke-Item.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
