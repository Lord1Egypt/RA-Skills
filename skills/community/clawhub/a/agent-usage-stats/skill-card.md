## Description: <br>
Token Stats helps users view local token consumption for Hermes, Claude Code, CodeX, OpenClaw, Reasonix, and DeepSeek TUI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhaoyong](https://clawhub.ai/user/zhouhaoyong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and power users with local AI assistant usage records use this skill to inspect token usage, monitor live deltas, compare time periods, and export local usage summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maintenance commands can persistently change PATH and remove token-stats or agent-usage-stats directories. <br>
Mitigation: Review setup, update, and uninstall behavior before installing; run these commands only if PATH changes and directory removal are acceptable. <br>
Risk: Stats features read local assistant usage files that may reveal local usage patterns. <br>
Mitigation: Use the skill only on machines where reading local assistant records is acceptable, and review exported files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouhaoyong/agent-usage-stats) <br>
- [Publisher profile](https://clawhub.ai/user/zhouhaoyong) <br>
- [README](README.md) <br>
- [CHANGELOG](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Terminal text output with optional CSV, JSON, and XLSX exports; Markdown setup and usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local assistant usage files and reports statistics for the selected agent, time range, or export mode.] <br>

## Skill Version(s): <br>
2.7.13 (source: SKILL.md frontmatter, CHANGELOG.md, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
