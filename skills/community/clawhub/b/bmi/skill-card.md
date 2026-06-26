## Description: <br>
Calculate BMI, log weight entries, and chart body composition trends. Use when tracking fitness progress, setting weight goals, or reviewing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to log fitness and body-composition entries locally, review trends, set goals, and export their records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health-related entries are saved as plain local files under ~/.local/share/bmi. <br>
Mitigation: Avoid entering sensitive medical details unless local file permissions, backups, retention, and deletion practices are acceptable for the user. <br>
Risk: Advertised BMI, charting, and export behavior may not match the script's actual behavior. <br>
Mitigation: Review and test the installed commands before relying on the output for fitness tracking or reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/bmi) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with optional JSON, CSV, or plain-text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores timestamped local logs under ~/.local/share/bmi.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
