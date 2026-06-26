## Description: <br>
Manages local clipboard history so users can save, search, pin, paste, and clear recent clipboard text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to manage frequently copied text through a local command-line clipboard history, including search, pinning, replaying entries to the clipboard, and clearing stored history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipboard contents may include sensitive text and can be saved in plaintext to local history. <br>
Mitigation: Avoid monitoring while copying secrets or private information, and clear ~/.clipboard_history.json on shared or sensitive machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/clipboard-manager) <br>
- [Publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores clipboard history in a local JSON file and uses CLIPBOARD_MAX to limit saved entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, _meta.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
