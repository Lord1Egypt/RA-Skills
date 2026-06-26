## Description: <br>
Disk Space Analyzer scans local disk drives, identifies major space consumers, and generates JSON and HTML reports with cleanup and optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raingingkleec](https://clawhub.ai/user/raingingkleec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and end users use this skill to inspect local disk usage, find large directories, and prepare reports that support cleanup decisions. It is especially useful when a Windows drive is nearly full and the user needs a prioritized explanation before deleting or moving data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON and HTML reports can expose local folder paths, software layout, cache locations, drive structure, and hostname. <br>
Mitigation: Review generated reports before sharing them and remove sensitive local details when needed. <br>
Risk: Cleanup suggestions can affect user data if acted on without review. <br>
Mitigation: Approve deletion or migration actions separately after checking the listed paths; the skill should present candidates before cleanup. <br>
Risk: The skill performs a broad local disk-usage survey. <br>
Mitigation: Install and run it only when a broad local storage scan is expected and appropriate for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raingingkleec/disk-space-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/raingingkleec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON scan data, and an HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include local folder paths, drive layout, cache locations, and hostname.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
