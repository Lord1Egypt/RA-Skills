## Description: <br>
Rename image datasets and corresponding annotation files with custom patterns, prefixes, suffixes, and sequential numbering, including preview support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and dataset curators use this skill to rename image datasets and matching annotation files before training, labeling, or organizing computer vision assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rename local dataset files in place and can overwrite files when force mode is used. <br>
Mitigation: Run preview first, keep a separate backup, review target names for collisions, and avoid force mode unless overwrites are intentional. <br>
Risk: The release advertises undo support, but the security evidence says the script does not create a restore backup before renaming. <br>
Mitigation: Do not rely on restore until the tool is fixed to create backups; maintain external backups or versioned copies before applying changes. <br>


## Reference(s): <br>
- [ClawHub Batch Rename page](https://clawhub.ai/Mingo-318/batch-rename) <br>
- [Publisher profile](https://clawhub.ai/user/Mingo-318) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead to local in-place file renames; preview mode is available before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
