## Description: <br>
Converts spreadsheet rows into structured task objects for Jira, Markdown, or JSON outputs while preserving field mapping and validating input and output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow maintainers use this skill to convert CSV-style spreadsheet rows into structured task representations for Jira imports, Markdown tables, or JSON task lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it asks for an unexplained API key and underspecifies write behavior. <br>
Mitigation: Do not provide an API key unless the publisher names the service, explains why it is needed, and discloses what spreadsheet data is sent. <br>
Risk: Spreadsheet contents may contain sensitive data or secrets. <br>
Mitigation: Review inputs before conversion, use explicit input and output paths, and inspect generated Jira, Markdown, or JSON before importing it into another system. <br>
Risk: Conversion defaults can affect downstream task fields such as status or priority. <br>
Mitigation: Validate field mappings and review defaulted values before using the converted task output operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/convert-spreadsheet-rows) <br>
- [Publisher profile](https://clawhub.ai/user/wangjipeng977) <br>
- [Declared metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills) <br>
- [Skill reference index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, Jira-oriented text, or concise guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write converted output to an explicit output path when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and changelog, released 2026-05-27; SKILL.md metadata says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
