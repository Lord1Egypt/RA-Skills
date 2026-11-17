## Description:

AI compliance analysis for EU AI Act, ISO 42001, NIST AI RMF, GDPR, OECD, financial services regulations, and other frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opietaylor911](https://clawhub.ai/user/opietaylor911)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, security, legal, procurement, and AI governance teams use this skill to assess AI tools or use cases against regulatory and governance frameworks, produce checklists or gap analyses, score risk, draft acceptable use policies, assess vendors, and recommend remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Artifact references include apparent fi.com current-state operational data, event counts, training statistics, inventory records, and personal names.

Mitigation: Remove the current-state data before release or replace it with clearly fictionalized examples that cannot be mistaken for live organizational records.

Risk: Some playbooks describe accessing internal telemetry and raw prompts without enough role scoping or privacy review.

Mitigation: Require authorized roles, scoped queries, redaction, audit logging, and legal or privacy review before using telemetry or prompt contents.

Risk: A remediation playbook includes a quick option for persistent plaintext secrets in /etc/openclaw/secrets.env.

Mitigation: Prefer managed secret storage; if a file-based procedure remains, label it as temporary approved break-glass handling with strict permissions and rotation requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/opietaylor911/skills/ai-compliance)
- [EU AI Act Reference](references/eu-ai-act.md)
- [ISO/IEC 42001:2023 Reference](references/iso-42001.md)
- [NIST AI Risk Management Framework](references/nist-ai-rmf.md)
- [Other AI Compliance Frameworks](references/other-frameworks.md)
- [Financial Services AI Regulatory Overlay](references/finserv-regulations.md)
- [AI Regulatory Jurisdiction Map](references/jurisdiction-map.md)
- [ISO 42001 and ISO 27001 Alignment Map](references/iso27001-alignment.md)
- [Compliance Checklist Templates](references/checklist-templates.md)
- [Vendor AI Risk Assessment Questionnaire](references/vendor-assessment.md)
- [AI Acceptable Use Policy Template](references/aup-template.md)
- [Data Classification and AI Tool Matrix](references/data-classification.md)
- [AI System Inventory Template](references/ai-inventory.md)
- [AI Risk Scoring Model](references/risk-scoring.md)
- [AI Training Requirements Matrix](references/training-requirements.md)
- [AI Incident Response Playbooks](references/incident-response.md)
- [Remediation Playbooks](references/remediation-playbooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with structured headings, tables, checklists, worksheets, policy drafts, and remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory compliance artifacts that require qualified human review before operational, legal, or regulatory use.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
