## Description:

Builds, audits, and operates GDPR Article 15 and Article 20 DSAR data export pipelines, with guidance for CCPA/CPRA right-to-know requests and UK subject access requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Privacy, legal, and engineering teams use this skill to design or audit DSAR export workflows, including data inventory, identity verification, export packaging, secure delivery, audit logging, SLA tracking, shared-record handling, and vendor coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the skill includes erasure and deletion guidance that is broader than its stated data export purpose.

Mitigation: Keep deletion and erasure actions behind separate legal authorization, identity verification, retention checks, and human approval.

Risk: DSAR export workflows can expose sensitive personal data or data about other subjects if identity checks, redaction, or delivery controls are weak.

Mitigation: Require sensitivity-appropriate subject verification, minimize third-party data, use documented redaction reason codes, encrypt exports, expire delivery links, and keep audit logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/gdpr-data-export-tool)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, code]

**Output Format:** [Markdown guidance with tables, workflow steps, schemas, architecture notes, and implementation-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
