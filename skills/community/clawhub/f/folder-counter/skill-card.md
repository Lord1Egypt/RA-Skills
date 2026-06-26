## Description: <br>
Folder Counter helps agents count files in a selected folder and summarize file-type distribution before indexing or other file-scale decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjkvbnwe](https://clawhub.ai/user/xjkvbnwe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to estimate the number of files and file-type mix in a directory before deciding whether and how to index it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill examples reference a PowerShell helper script that was not included in the reviewed artifact. <br>
Mitigation: Inspect the installed count_files.ps1 script before running it, and only execute it against folders you intend to analyze. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjkvbnwe/folder-counter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include total file counts, file-type distribution, and indexing guidance based on folder size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
