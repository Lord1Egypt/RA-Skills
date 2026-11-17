## Description:

This skill allows the assistant to launch files and open them with their default applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[badwolf-63](https://clawhub.ai/user/badwolf-63)

### License/Terms of Use:

MIT-0

## Use Case:

People using Windows can ask an assistant to open documents, media files, images, playlists, or programs with the default application registered for that file type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an assistant to open local files or launch programs without confirmation or safety limits.

Mitigation: Require explicit user confirmation, show the resolved path before opening it, and block executables, scripts, shortcuts, installers, and untrusted locations by default.

## Reference(s):

- [File Launcher on ClawHub](https://clawhub.ai/badwolf-63/skills/file-launcher)
- [badwolf-63 publisher profile](https://clawhub.ai/user/badwolf-63)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Text with Windows PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Windows file associations through Invoke-Item; behavior depends on the local default application for the target path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
