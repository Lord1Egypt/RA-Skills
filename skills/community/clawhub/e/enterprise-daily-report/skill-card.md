## Description: <br>
Generates structured daily work reports from CSV, JSON, or Git activity and can output Markdown, HTML, or PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mizhimin](https://clawhub.ai/user/mizhimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and developers use this skill to collect daily work items from local CSV/JSON files or Git commits, classify them into report sections, and generate a shareable daily status report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git repository paths can trigger command injection because the Git integration runs a shell command. <br>
Mitigation: Use only trusted repository paths without shell metacharacters, or disable Git input until the command is changed to avoid shell=True. <br>
Risk: The skill has broad file, execution, and network permissions and can write reports or send email. <br>
Mitigation: Review inputs, output paths, recipients, and generated report contents before enabling email delivery or running in sensitive environments. <br>
Risk: CSV and JSON inputs may contain untrusted or misleading work-report content. <br>
Mitigation: Use trusted source files and review generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mizhimin/enterprise-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/mizhimin) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, PDF, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads CSV, JSON, or Git repository inputs; may write report files and optionally send email when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
