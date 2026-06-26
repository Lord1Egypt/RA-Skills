## Description: <br>
File Sorter helps organize local files by type, size, date, or documented keyword rules for workflows such as download cleanup, photo archiving, and document classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users can use this skill to organize batches of local files into folder structures by file type, size, or date. It is suited for routine cleanup and archiving tasks where preview and undo behavior help reduce accidental changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, copy, or create symlinks in folders the user explicitly points it at. <br>
Mitigation: Use preview first, restrict runs to intended directories, and keep the backup log until undo is no longer needed. <br>
Risk: Move is the default action, so a confirmed run can reorganize files. <br>
Mitigation: Review proposed operations before confirming, or choose copy for lower-impact runs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/utopiabenben/file-sorter) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe preview, move, copy, symlink, and undo workflows for local file organization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
