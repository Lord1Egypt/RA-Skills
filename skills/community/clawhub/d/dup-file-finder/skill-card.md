## Description: <br>
Quickly identify and list duplicate files in a specified directory to help manage and free up disk space efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users run this skill to scan a chosen local directory and list files with matching SHA-256 hashes so duplicate copies can be reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scan reads every file under the selected directory and prints full paths and hashes. <br>
Mitigation: Run it only on directories intended for duplicate-file review, avoid broad system directories unless intentional, and do not run it as root. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output with file paths and hashes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads files under the user-specified directory and prints duplicate groups; it does not delete files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
