## Description:

Helps HR teams review compensation bands, market and internal pay signals, offer decisions, and China payroll filing prechecks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashley-aihr](https://clawhub.ai/user/ashley-aihr)

### License/Terms of Use:

MIT-0

## Use Case:

HR compensation, HRBP, payroll, and shared services teams use this skill to triage offer pricing and month-end payroll filing prechecks for China workflows. It produces decision summaries, supporting basis, risks, missing information, next actions, message drafts, and record updates.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated reports may contain sensitive employee, compensation, payroll, bank, tax, or identity data.

Mitigation: Use a restricted local output directory, avoid shared or synced folders, and redact direct identifiers when possible.

Risk: Generated CSV files may be unsafe to open when inputs are untrusted because formula-injection hardening is not evidenced.

Mitigation: Treat CSV outputs from untrusted inputs as unsafe until hardened; review or sanitize cells before opening them in spreadsheet software.

Risk: Payroll and compliance outputs are prechecks and may be mistaken for authoritative legal or payroll advice.

Mitigation: Require human payroll, legal, or compliance confirmation before filing or acting on high-impact decisions.

## Reference(s):

- [Skill homepage](https://github.com/Ashley-AIHR/hrskill-compensation-module)
- [Real user scenario](references/real-user-scenario.md)
- [China HR compensation workflows](references/compensation-workflows.md)
- [China compensation policy knowledge base 2026](references/china-compensation-policy-kb-2026.md)
- [Dynamic market data architecture](references/dynamic-market-data-architecture.md)
- [Shanghai 2026 social insurance wage declaration notice](https://shanghai.chinatax.gov.cn/zcfw/zcfgk/sbf/202604/t480144.html)
- [Shanghai 2026 social insurance wage declaration overview](https://shanghai.chinatax.gov.cn/zcfw/tjss/202605/t480288.html)
- [Beijing housing fund base declaration FAQ](https://gjj.beijing.gov.cn/web/zwfw5/1747335/1747336/743669918/index.html)
- [Shenzhen housing fund management update](https://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/content/post_12687780.html)
- [Shanghai withholding client operations FAQ](https://shanghai.chinatax.gov.cn/jstax/ztzl/yshj/sycz/202512/t478537.html)
- [Natural person e-tax web withholding guide](https://guangdong.chinatax.gov.cn/gdsw/zqsw_tzgg/2020-11/18/content_75df0d6a19634d9596f0bffd81492a5c.shtml)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, docx files, shell commands, guidance]

**Output Format:** [Markdown or text responses, with optional JSON, CSV, and DOCX report files generated from local input JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports can contain confidential HR and payroll records; COMP_EXPORT_PATH may be used as an optional local export path.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
