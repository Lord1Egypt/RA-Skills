## Description:

Provides global compliance checklists, market-specific regulation mapping, China outbound data transfer assessment, and remediation guidance for Chinese products expanding overseas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, compliance reviewers, and launch operators use this skill to triage GDPR, CCPA, data localization, app store, AI transparency, payment licensing, and China outbound data transfer obligations before overseas release. It produces structured audit reports and remediation roadmaps that should be reviewed with qualified legal counsel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance guidance may be incomplete, outdated, or mistaken if treated as legal advice.

Mitigation: Use the skill as checklist and risk triage only, and verify current obligations with qualified counsel in each target market before launch.

Risk: API-backed regulation lookups use an external web endpoint.

Mitigation: Do not submit confidential or personal data to web or API endpoints unless the third-party trust boundary is accepted.

Risk: Product-specific obligations can be missed when profile details are incomplete.

Mitigation: Complete the product profile, market mapping, gap analysis, risk classification, and remediation roadmap before relying on the output.

## Reference(s):

- [Compliance Checklist](references/compliance-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/lm203688/skills/cn-global-compliance)
- [Regulations API Backend](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown compliance audit reports, JSON quick-check reports, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference an external regulations API for market lookups; results are checklist and risk-triage guidance, not legal advice.]

## Skill Version(s):

2.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
