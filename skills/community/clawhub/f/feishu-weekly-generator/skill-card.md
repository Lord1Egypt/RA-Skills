## Description: <br>
Generate professional weekly work reports for Feishu/Lark users and create formatted Markdown that can be pasted into Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahui220](https://clawhub.ai/user/jiahui220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to generate weekly work reports from date ranges, optional Git commit history, and report templates for sharing in Feishu or Lark. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Node.js script can build a shell command from user-supplied options, which may run unintended commands if untrusted repository paths or arguments are used. <br>
Mitigation: Use trusted date and repository path arguments, avoid passing untrusted text into command options, choose output paths carefully, and review or redact generated reports before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahui220/feishu-weekly-generator) <br>
- [standard.md](references/templates/standard.md) <br>
- [detailed.md](references/templates/detailed.md) <br>
- [minimal.md](references/templates/minimal.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional shell command usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local weekly-report Markdown file using the selected date range, template, user name, department, and optional Git repository path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
