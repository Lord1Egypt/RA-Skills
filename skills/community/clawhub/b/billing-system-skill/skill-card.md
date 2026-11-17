## Description:

对账单生成系统 — 零配置通用版。自动注册试用账户，自动下载模板。Excel含汇总分析+客户余额趋势图（万元），PDF含双利息主体明细。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihao-ok](https://clawhub.ai/user/nihao-ok)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate reconciliation statements from customer, loan, and repayment spreadsheet data. It supports an online workflow through a hosted endpoint and a local Windows EXE workflow described by the artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The online workflow sends customer and loan spreadsheets to an external cloud endpoint.

Mitigation: Use the online path only when the operator, retention, deletion, and confidentiality terms are acceptable for the workbook data.

Risk: The workflow issues and uses an access key for registration and generation.

Mitigation: Store the key outside shared folders and source control, and rotate or discard it when the work is complete.

Risk: The generated result is returned as a ZIP archive.

Mitigation: Inspect the ZIP file contents before extraction and only open expected Excel and PDF outputs.

Risk: The artifact describes a local Windows EXE workflow, but the executable was not included as verifiable evidence.

Mitigation: Use the local EXE only after separately verifying its source, hash, and publisher.

## Reference(s):

- [Server-resolved source repository](https://github.com/nihao-ok/billing-system-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash and Python examples; generated ZIP output containing Excel and PDF billing statements when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Online use uploads workbook data to a hosted service; local EXE use depends on separately verifying the executable provenance.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
