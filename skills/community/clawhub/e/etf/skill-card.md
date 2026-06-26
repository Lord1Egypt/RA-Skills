## Description: <br>
Etf is advertised for ETF analysis, but the submitted artifacts primarily provide a terminal utility for recording, searching, exporting, and summarizing locally stored text entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users can use this skill as a local command-line logger for recording, searching, exporting, and summarizing text entries. Do not rely on it for ETF research or investment analysis unless the publisher adds real ETF functionality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as an ETF analysis tool, but the artifacts implement a generic local logger. <br>
Mitigation: Review the behavior before installation and treat outputs as local log records, not investment research or fund analysis. <br>
Risk: Command inputs are saved locally under ~/.local/share/etf and can later be viewed, searched, or exported. <br>
Mitigation: Avoid entering account numbers, portfolio details, proprietary research, credentials, or other sensitive text. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/etf) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>
- [BytesAgain Feedback](https://bytesagain.com/feedback/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal-output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed command writes user-entered text and activity history to ~/.local/share/etf and can export saved entries as JSON, CSV, or plain text.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
