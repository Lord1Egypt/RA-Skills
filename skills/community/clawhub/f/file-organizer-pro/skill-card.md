## Description: <br>
Smart File Organizer automatically organizes files into folders by type, date, or custom naming rules with preview and undo options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mizhimin](https://clawhub.ai/user/mizhimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preview and organize local folders by file type, modification date, or custom filename patterns. It is intended for routine file cleanup workflows where users can review planned moves before applying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the organizer without preview can move files in the selected folder in ways the user did not intend. <br>
Mitigation: Use --dry-run first and run the skill on a non-critical or backed-up folder before applying changes. <br>
Risk: Undo is best-effort and may not restore every edge case, including some name-collision scenarios. <br>
Mitigation: Keep a backup of important folders and review the generated organization plan before executing file moves. <br>
Risk: The documented entry path may not match the packaged artifact layout. <br>
Mitigation: If python scripts/main.py is unavailable, run the packaged main.py directly with the same arguments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mizhimin/file-organizer-pro) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May move files in a user-specified local folder when executed without --dry-run; undo is best-effort.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
