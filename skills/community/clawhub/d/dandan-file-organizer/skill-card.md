## Description: <br>
Dandan File Organizer helps agents safely scan and organize a user's desktop or folder by proposing and, after confirmation, moving files into type- or pattern-based folders without deleting or overwriting files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realorange1994](https://clawhub.ai/user/realorange1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and general agent users can use this skill to organize cluttered desktops or folders into safe, reviewable categories. It is intended to scan a selected directory, present a proposed organization plan, and move files only after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose file names, folder paths, and proposed moves in chat or local rollback logs. <br>
Mitigation: Review the target folder, proposed moves, and generated log path before confirming organization, and avoid highly sensitive directories unless those details are acceptable to disclose locally. <br>
Risk: Incorrect categorization could move files into unexpected folders. <br>
Mitigation: Use the scan-and-confirm phase before any move operation and rely on the generated operation log for rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realorange1994/dandan-file-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with inline shell commands and organization summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file moves, created folder names, a local operation log path, and rollback command guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
