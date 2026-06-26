## Description: <br>
流水报告生成，基于用户输入的Excel/PDF流水文件路径和问题，自动上传文件并生成分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ufcfengbin](https://clawhub.ai/user/ufcfengbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to upload bank statement PDF or Excel files and request a generated analysis report. It is intended for workflows where the user explicitly wants bank statement processing and a report link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads sensitive bank statement files to a remote service for report generation. <br>
Mitigation: Use it only when the user intends to send those files, verify exact file paths before upload, protect ZY_TOKEN from logs or shell history, and review the provider's privacy, retention, deletion, and report-link access practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ufcfengbin/bankstatement) <br>
- [Token setup instructions](https://mp.weixin.qq.com/s/5AE3mQhsW_g-3R6C26i-9Q) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Text or Markdown with a report link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZY_TOKEN and user-provided local file paths; uploaded files are processed by the dfwytech/Ziya service.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
