## Description:

Checks GDPR compliance across 12 core items and uses compliancehub.cn cloud scoring to produce bilingual guidance and local reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users, compliance teams, and developers use this skill to preview GDPR checklist items, collect status answers, and generate a local GDPR compliance report. It provides general compliance guidance only and is not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored checks send GDPR checklist answers to compliancehub.cn for cloud scoring.

Mitigation: Run the skill only after the user opts in to gdpr-check and is comfortable sending those answers to compliancehub.cn.

Risk: Generated HTML reports may include cloud-provided report text that is not HTML-escaped in this version.

Mitigation: Prefer text or JSON output for sensitive use, or treat generated HTML reports as untrusted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/gdpr-check)
- [Publisher profile](https://clawhub.ai/user/wwumit)
- [ComplianceHub account page](https://compliancehub.cn/account.html?skill=gdpr-check)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, markdown, configuration, guidance]

**Output Format:** [Interactive checklist prompts and local reports in text, JSON, or HTML; skill guidance is Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored runs send checklist answers to compliancehub.cn; preview mode lists items without sending answers.]

## Skill Version(s):

1.1.3 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
