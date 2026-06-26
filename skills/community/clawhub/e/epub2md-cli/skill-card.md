## Description: <br>
Use the local `epub2md` CLI to inspect EPUB files and convert them into Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujuntao123](https://clawhub.ai/user/liujuntao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local EPUB metadata and convert EPUB books into split or merged Markdown outputs, with optional image localization when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EPUB conversion runs a local CLI and writes files into a workspace. <br>
Mitigation: Confirm the source path and requested output mode before conversion, and keep generated files in the documented workspace unless the user requests another location. <br>
Risk: Remote images may be fetched when image localization is enabled. <br>
Mitigation: Use localization only when the user intentionally wants remote assets downloaded from URLs contained in the EPUB. <br>
Risk: The converter may require a global npm install if `epub2md` is missing. <br>
Mitigation: Ask the user to approve any global install and verify the Node.js requirement before using image localization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujuntao123/epub2md-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file paths; converted EPUB content is written as Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce split chapter files, a merged Markdown file, inspection text, and optional localized image assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
