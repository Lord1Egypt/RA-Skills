## Description: <br>
Cmms provides a local command-line computerized maintenance management system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Maintenance teams and developers use this skill to keep a local command-line maintenance log, add and search entries, remove records, review status and statistics, manage simple configuration, and export records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maintenance entries and configuration are stored locally in plain text under ~/.cmms by default. <br>
Mitigation: Avoid recording secrets or highly sensitive business data unless plain-text local storage is acceptable; set CMMS_DIR to an approved location when needed. <br>
Risk: The export command writes JSON or CSV files into the current directory. <br>
Mitigation: Run exports from an intended workspace and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [Cmms on ClawHub](https://clawhub.ai/bytesagain-lab/cmms) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text stdout with JSONL local records and JSON or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data under ~/.cmms by default, or under CMMS_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
