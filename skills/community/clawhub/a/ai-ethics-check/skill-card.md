## Description:

AI Ethics Check is a free compliance-check skill that evaluates 10 self-reported AI technology ethics review items under China's 2026 AI 科技伦理审查与服务办法 and generates local text, JSON, or HTML reports with cloud scoring or offline preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly request an AI ethics compliance check, preview the checklist offline, submit y/n/na answers for cloud scoring, and generate local compliance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored checks transmit compliance checklist answers and API key authentication to compliancehub.cn.

Mitigation: Use offline preview when no data should leave the machine; run scored mode only when the user accepts sharing answers and API key authentication with complianceHub.

Risk: HTML reports may render unescaped cloud-controlled content.

Mitigation: Prefer text or JSON output, and avoid opening generated HTML reports from untrusted or unexpected runs until remote report fields are escaped.

Risk: The report is based on self-reported answers and is not a regulatory, audit, or legal conclusion.

Mitigation: Treat results as preliminary compliance guidance and route material decisions through qualified legal or compliance review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/ai-ethics-check)
- [Publisher profile](https://clawhub.ai/user/wwumit)
- [ComplianceHub account and API key page](https://compliancehub.cn/account.html?skill=ai-ethics-check)
- [ComplianceHub service](https://compliancehub.cn)
- [ComplianceHub privacy policy](https://compliancehub.cn/privacy.html)

## Skill Output:

**Output Type(s):** [text, json, html, files, guidance]

**Output Format:** [Text, JSON, or HTML compliance report; offline preview can emit text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored runs send checklist answers to compliancehub.cn; offline preview does not send data.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
