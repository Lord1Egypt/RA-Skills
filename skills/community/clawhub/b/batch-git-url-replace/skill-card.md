## Description: <br>
Batch-replaces remote URLs for Git repositories under a specified directory to help migrate repositories between Git servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxfcn](https://clawhub.ai/user/zxfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to generate PowerShell or Bash commands that update matching Git remote URLs across repositories in a chosen directory during server migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk replacement can unintentionally change many repository remote URLs if the scan directory or URL strings are too broad. <br>
Mitigation: Use a narrow scan directory, verify the old and new URL strings carefully, consider backing up affected .git/config files, test on a small folder first, and check representative repositories with git remote -v before pushing code. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PowerShell and Bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scan directory, old URL, and new URL before command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
