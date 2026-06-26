## Description: <br>
Batch rename files with customizable prefixes, suffixes, and sequential numbering, with a dry-run mode for previewing changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and file-management users use this skill to prepare and run batch file renaming workflows for a target directory. It is useful when files need consistent prefixes, suffixes, preserved extensions, and numbered names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the rename script without dry-run changes filenames in the selected local directory. <br>
Mitigation: Use dry-run first, review the JSON preview, and keep a backup before applying changes to important files. <br>
Risk: The tool processes the entries returned from the target directory, so an overly broad directory can affect more files than intended. <br>
Mitigation: Run it only on a narrowly scoped directory that contains the files intended for renaming. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freedompixels/cn-batch-file-renamer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the script emits JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run previews are available; non-dry-run execution can rename local filesystem entries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
