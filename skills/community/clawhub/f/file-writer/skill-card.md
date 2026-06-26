## Description: <br>
Safely write or update large files by reading current content, making precise incremental edits, verifying each change, and using fallback recovery methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when creating or modifying large local files where single writes may truncate content or corrupt the file. It guides incremental edits, verification, backups, and recovery for safer file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables file creation and editing, which can affect important or sensitive local files. <br>
Mitigation: Confirm the target path and intended change before use, keep backups for critical work, and review diffs before accepting large overwrites. <br>
Risk: Incomplete or incorrect edits can leave a large file truncated, syntactically invalid, or inconsistent. <br>
Mitigation: Use the skill's incremental editing approach and verify file size, changed sections, endings, and syntax after each modification. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/YKaiXu/file-writer) <br>
- [Publisher profile](https://clawhub.ai/user/YKaiXu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and editing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes small incremental changes, verification after each edit, and fallback recovery steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
