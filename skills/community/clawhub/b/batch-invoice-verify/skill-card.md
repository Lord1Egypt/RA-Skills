## Description:

批量识别并查验文件夹内发票，校验抬头、提示重复风险，生成最终清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningmengyun12366](https://clawhub.ai/user/ningmengyun12366)

### License/Terms of Use:

MIT-0

## Use Case:

External finance and operations users can use this skill to batch-process invoice folders or invoice lists, verify invoices, check title consistency, flag duplicate reimbursement risk, and generate invoice ledger workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs native binaries distributed outside the reviewed ZIP package.

Mitigation: Install only from the server-resolved publisher and documented distribution channel, verify the downloaded binary independently where possible, and scan before deployment.

Risk: The workflow uses invoice documents and an invoice verification API key.

Mitigation: Provide the API key only at runtime, keep it out of configuration and logs, and use the skill only where invoice data handling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningmengyun12366/skills/batch-invoice-verify)
- [Publisher profile](https://clawhub.ai/user/ningmengyun12366)
- [Installation and update documentation](https://download.ningmengyun.com/Skills/batch-invoice-verify/batch-invoice-verify-install.md)
- [Invoice verification API endpoint](https://openapi.nmy.cn/api/v1/skill/national-invoice-check)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, JSON]

**Output Format:** [Markdown guidance with CLI commands; runtime commands return JSON status and XLSX workbooks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a runtime invoice verification API key; expected files include an intermediate verification XLSX and a final invoice ledger XLSX.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and install docs list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
