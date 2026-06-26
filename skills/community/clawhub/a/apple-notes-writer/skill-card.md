## Description: <br>
Writes formatted HTML or Markdown content to Apple Notes on macOS, with support for folders, updates, and simple note lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnmuin](https://clawhub.ai/user/johnmuin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to create, update, read, list, and organize Apple Notes from formatted content. It is useful when an agent needs to save meeting notes, imported Markdown, or structured text into Apple Notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify persistent Apple Notes data through AppleScript. <br>
Mitigation: Confirm each create, read, list, folder-create, and update request before execution, and avoid granting access to sensitive Notes folders unless the task requires it. <br>
Risk: Dynamic AppleScript construction with weak scoping can target unintended notes or folders if supplied with untrusted titles, folder names, note IDs, or content. <br>
Mitigation: Use trusted inputs, specify the intended account and folder, review the target note before updates, and avoid passing untrusted note metadata or content until argument handling is improved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnmuin/apple-notes-writer) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [Apple Notes automation reference](artifact/REFERENCE.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown or HTML note content with Python API calls and CLI commands; command results are plain text status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Python 3.7+, Apple Notes.app, and user-granted automation access to Notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
