## Description:

流水报告生成，基于用户输入的Excel/PDF流水文件路径和问题，自动上传文件并生成分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ufcfengbin](https://clawhub.ai/user/ufcfengbin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to upload PDF or Excel bank statement files and request an automatically generated transaction analysis report. It is intended for cases where the user explicitly asks to analyze, process, or report on bank statement files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads complete bank statement files and related questions to an external service.

Mitigation: Use it only with clear user consent and after confirming the service's privacy, retention, and deletion policy.

Risk: API tokens passed as command-line arguments may be exposed in shell history, logs, or process listings.

Mitigation: Use a protected environment variable or secret manager for ZY_TOKEN and rotate any token that may have been logged.

Risk: The artifact does not enforce file-type or path restrictions before upload.

Mitigation: Confirm the exact file path before upload and avoid using the skill on unrelated private files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ufcfengbin/skills/bankstatement)
- [API key setup instructions](https://mp.weixin.qq.com/s/5AE3mQhsW_g-3R6C26i-9Q)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or text responses with shell command examples and generated report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads local bank statement files to an external report service and returns the generated report result or link.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
