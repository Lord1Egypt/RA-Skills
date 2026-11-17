## Description:

Generates detailed compliance audits with risk-prioritized findings and remediation plans for frameworks like SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS, SOX, and CCPA/CPRA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers, security teams, compliance leads, and operators use this skill to generate internal readiness assessments, gap analyses, remediation roadmaps, and evidence checklists for common security, privacy, healthcare, payment, and financial-control frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated readiness guidance as legal, compliance, or certified audit advice.

Mitigation: Position outputs as internal readiness guidance and have qualified legal, compliance, or audit professionals review decisions before relying on them.

Risk: Audit prompts can invite sensitive business, customer, health, payment, credential, or security-gap details.

Mitigation: Use high-level summaries and approved internal workflows; do not provide secrets, credentials, customer identifiers, PHI, PCI data, or detailed exploitable security gaps.

Risk: Framework mappings, control references, cost estimates, and remediation priorities may be incomplete or outdated.

Mitigation: Validate generated control references and remediation plans against current authoritative framework documentation and organization-specific requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1kalin/skills/afrexai-compliance-audit)
- [AfrexAI Toolkit](https://afrexai-cto.github.io/context-packs/)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown compliance audit report with summaries, control assessments, remediation roadmap, and evidence checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include readiness scores, framework control references, priority ratings, effort estimates, timelines, and cost estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
