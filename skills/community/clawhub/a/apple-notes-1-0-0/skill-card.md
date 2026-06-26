## Description: <br>
Manage Apple Notes via the `memo` CLI on macOS, including creating, viewing, editing, deleting, searching, moving, and exporting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[readbyte-ai](https://clawhub.ai/user/readbyte-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Mac users and agents use this skill to manage Apple Notes from a terminal workflow through the third-party `memo` CLI. It is useful for creating, finding, organizing, exporting, and deleting notes when Apple Notes.app and macOS Automation access are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party macOS CLI that can access Apple Notes. <br>
Mitigation: Install only from a trusted `memo` source and grant Notes Automation access only when needed. <br>
Risk: Editing, moving, exporting, or deleting the wrong selected note can expose or alter personal note content. <br>
Mitigation: Review note titles and selected folders before confirming interactive `memo notes` actions. <br>
Risk: Deleted notes may be difficult or impossible to recover. <br>
Mitigation: Treat deletion as irreversible and prefer export or backup before destructive actions. <br>
Risk: The `memo` CLI cannot edit notes that contain images or attachments. <br>
Mitigation: Use Apple Notes.app directly for notes with images or attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/readbyte-ai/apple-notes-1-0-0) <br>
- [readbyte-ai publisher profile](https://clawhub.ai/user/readbyte-ai) <br>
- [memo project](https://github.com/antoniorodr/memo) <br>
- [Homebrew formula: antoniorodr/memo/memo](https://github.com/antoniorodr/memo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target macOS and require the `memo` CLI plus Apple Notes Automation access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
