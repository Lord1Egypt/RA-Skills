## Description: <br>
Provides a local command-line entry database for storing, listing, searching, removing, exporting, and summarizing user-provided text entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to run shell commands that manage simple local text entries, including adding, listing, searching, deleting, exporting, viewing status and statistics, and configuring the data directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release description presents the skill as a dialog UI/design generator, while the artifact behaves as a local entry-management CLI. <br>
Mitigation: Review and deploy it only when a local JSONL entry-management tool is intended. <br>
Risk: User-entered text is persisted locally and can be exported to JSON or CSV. <br>
Mitigation: Avoid entering secrets or sensitive project data, set DIALOG_DIR deliberately, and review exported files before sharing. <br>


## Reference(s): <br>
- [Dialog on ClawHub](https://clawhub.ai/ckchzh/dialog) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text stdout with JSONL local storage and optional JSON or CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ~/.dialog by default, or under DIALOG_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
