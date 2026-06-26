## Description: <br>
Apple Notes.app integration for macOS. List folders, read, create, search, edit, and delete notes via AppleScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shad0wca7](https://clawhub.ai/user/shad0wca7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to automate Apple Notes workflows, including folder navigation, note search, note reading, note creation, note editing, note deletion, and attachment export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad Apple Notes contents, attachments, and OCR search results. <br>
Mitigation: Grant access only when that scope is acceptable, prefer narrow folder arguments, and avoid broad searches unless necessary. <br>
Risk: The skill can edit or delete notes and partial title matching may target the first matching note. <br>
Mitigation: Review edit and delete requests before execution, use exact note IDs where possible, and provide narrow folder scopes for name-based operations. <br>
Risk: Read and export operations can copy note attachments to /tmp/notes-export. <br>
Mitigation: Clean /tmp/notes-export after workflows that read or export attachments. <br>
Risk: Untrusted search text may produce unexpected Spotlight or AppleScript search behavior. <br>
Mitigation: Avoid untrusted query strings and prefer simple, specific search terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shad0wca7/apple-notes-applescript) <br>
- [Publisher profile](https://clawhub.ai/user/shad0wca7) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text command output, shell command examples, note metadata, note body text, and filesystem paths for exported attachments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary files for note bodies and exported attachments under /tmp, including /tmp/notes-export.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
