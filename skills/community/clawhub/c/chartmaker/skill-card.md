## Description: <br>
Chartmaker records, searches, summarizes, and exports chart-related data entries from a local command-line data store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to log chart, visualization, transformation, schema, and validation notes locally, then search or export those accumulated entries for reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain free-form user text in local log files, which may include sensitive or proprietary information if entered. <br>
Mitigation: Use it only for data that is acceptable to store under ~/.local/share/chartmaker, and avoid entering secrets, credentials, personal data, or proprietary business data. <br>
Risk: The release summary and behavior differ: it is presented as chart visualization but primarily logs, searches, and exports text entries. <br>
Mitigation: Review the installed behavior before operational use and treat the tool as a local text logging and export utility rather than a chart renderer. <br>


## Reference(s): <br>
- [Chartmaker on ClawHub](https://clawhub.ai/bytesagain1/chartmaker) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local log and export files under ~/.local/share/chartmaker when its shell script is installed and run.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
