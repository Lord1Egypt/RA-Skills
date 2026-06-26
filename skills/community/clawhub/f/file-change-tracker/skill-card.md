## Description: <br>
Mandatory before the first file-changing action in a new edit batch. Use before creating, editing, overwriting, patching, renaming, moving, deleting, or generating files. Run PRE once at batch start with the explicit target paths, then run POST when the batch is complete. Do not use for read-only inspection, search, grep, diff-only review, or explanation-only tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxf1024](https://clawhub.ai/user/songxf1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill before file-changing work to create path-scoped local Git recovery points, record post-change results, and report rollback guidance for the protected paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill deliberately creates local Git recovery snapshots around file edits, which may preserve secrets, generated output, or other sensitive files if they are inside declared target paths and not ignored. <br>
Mitigation: Use narrow target paths and review .gitignore and guarded-edit.ignore before broad directory changes or generated output snapshots. <br>
Risk: The helper initializes or uses a local Git repository and records path-scoped PRE and POST commits, which can affect local repository history. <br>
Mitigation: Install only when local Git recovery commits are desired, avoid broad target scopes, and review the reported PRE and POST snapshot details after each batch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songxf1024/file-change-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain-text status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs local Git recovery snapshot identifiers, session status, protected paths, recent records, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
