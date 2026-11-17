## Description:

自动化填写 12321 网络不良与垃圾信息举报受理中心的骚扰电话举报表单，并通过浏览器交互和用户确认完成举报流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnqxu](https://clawhub.ai/user/johnqxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to prepare and submit harassment-call reports to the 12321 reporting form with interactive review of CAPTCHA, phone numbers, report details, SMS verification, and final submission.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can automate a real harassment-call complaint workflow.

Mitigation: Require explicit user confirmation before requesting SMS verification and before final form submission.

Risk: The artifact includes a hard-coded reporter phone number and handles personal phone data.

Mitigation: Remove default personal phone values before use and avoid retaining phone numbers beyond the reporting session.

Risk: The flow can opt into an optional service-consent checkbox.

Mitigation: Leave optional consent unchecked unless the user explicitly opts in.

Risk: The workflow creates temporary CAPTCHA image files.

Mitigation: Delete temporary CAPTCHA text and image files after the user confirms or abandons the report.

Risk: The automation describes bypassing page safeguards such as waiting periods and CAPTCHA handling.

Mitigation: Review the target site's permitted use before deployment and avoid steps that bypass safeguards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnqxu/skills/12321-harass-report)
- [12321 reporting center](https://www.12321.cn)
- [12321 harassment-call reporting form](https://www.12321.cn/notifyHomePhone)
- [Field mapping reference](artifact/references/field-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a single interactive reporting flow that depends on user confirmation and SMS verification.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
