## Description:

Fin-PIPL is a Chinese-language, local financial privacy compliance checklist tool for PIPL, JR/T 0171, and JR/T 0197 self-checks across banking, securities and funds, insurance, and payment scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, legal, risk, and engineering teams use this skill to run local self-checks for Chinese financial-industry personal information protection requirements. It supports scenario-specific assessments for banking, securities and funds, insurance, and payment workflows, with results intended as a checklist rather than legal advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Compliance results may be mistaken for legal advice or proof of regulatory compliance.

Mitigation: Treat the output as a checklist and have qualified legal or compliance professionals review important decisions.

Risk: The tool can write reports to a user-specified output path, which may overwrite an existing file.

Mitigation: Choose output paths carefully and keep backups for files that should not be replaced.

Risk: The checklist is scoped to Chinese financial PIPL and JR/T compliance scenarios and may not cover other jurisdictions or every regulator-specific requirement.

Mitigation: Confirm jurisdiction, regulator, and business-specific requirements before relying on the checklist.

## Reference(s):

- [JR/T 0171-2020 Personal Financial Information Protection Technical Specification](references/jr-t-0171.md)
- [JR/T 0197-2020 Financial Data Security Data Classification Guide](references/jr-t-0197.md)
- [Fin-PIPL ClawHub Skill Page](https://clawhub.ai/wwumit/skills/fin-pipl)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, JSON, HTML]

**Output Format:** [Interactive checklist responses and optional Markdown, JSON, or HTML compliance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without network access; writes report files only when an output path is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
