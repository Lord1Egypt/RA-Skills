## Description: <br>
Enterprise asset management tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use Eam to add, list, search, remove, export, and summarize local asset-management entries from a shell. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local asset records are stored under ~/.eam and may contain sensitive operational details. <br>
Mitigation: Avoid entering secrets or highly sensitive asset data unless local storage is acceptable, and manage file access according to organizational policy. <br>
Risk: Removing an entry permanently deletes it from the local JSONL data file. <br>
Mitigation: Back up ~/.eam/data.jsonl or export records before using remove. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/eam) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text command output with JSONL, JSON, or CSV data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local records under ~/.eam by default; export writes JSONL or CSV files; exits 0 on success and 1 on error.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
