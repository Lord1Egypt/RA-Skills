## Description:

Runs a 25-item GDPR compliance audit that previews checks locally and can submit answers to CQDev's compliancehub.cn cloud engine for scoring and local report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run a structured GDPR readiness check, preview the 25 audit items, and generate text, JSON, or HTML compliance reports. Scored audits send item answers to compliancehub.cn and are general guidance, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored audits send GDPR answer status, an API key or anonymous trial id, and related scoring metadata to compliancehub.cn.

Mitigation: Use preview mode first; run scored audits only when the organization permits this data transfer, review the provider's privacy terms, and remove local drafts or key files when no longer needed.

Risk: The audit report may be mistaken for legal advice.

Mitigation: Treat results as general compliance guidance and consult qualified counsel for legal decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/gdpr-audit)
- [CQDev account and API key page](https://compliancehub.cn/account.html?skill=gdpr-audit)
- [ComplianceHub cloud endpoint](https://compliancehub.cn)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, files, guidance]

**Output Format:** [Interactive prompts, preview listings, and text, JSON, or HTML audit reports with optional file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored reports use the compliancehub.cn cloud engine with API-key or anonymous-trial authentication; preview mode lists checks without submitting answers.]

## Skill Version(s):

2.0.2 (source: package.json, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
