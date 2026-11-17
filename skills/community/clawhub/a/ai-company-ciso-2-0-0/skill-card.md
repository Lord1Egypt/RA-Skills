## Description:

Provides CISO governance guidance for AI-company security workflows, including STRIDE threat modeling, incident response, AI gateway governance, zero-trust controls, crisis-channel approval, audit, and license-compliance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and governance or security teams use this skill to request CISO-style security assessments, incident-response plans, STRIDE reviews, and risk mitigations for AI-company operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emergency approval paths for powerful crisis actions may conflict, especially around timeout handling.

Mitigation: Review before production use; make timeouts fail closed or route to an independent backup security approver rather than treating timeout as approval.

Risk: The skill can affect production, public communications, or agent operations when adopted into governance workflows.

Mitigation: Narrow activation to explicit CISO governance requests and require human review before installation in workflows that can trigger operational changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/ai-company-ciso-2-0-0)
- [AI Company CISO homepage](https://clawhub.com/skills/ai-company-ciso)
- [STRIDE assessment - CEO-EXEC crisis channel](artifact/references/stride-assessment-crisis-channel.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with security assessment, incident response, and risk mitigation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured security_assessment, incident_response, and risk_mitigation fields when used through its declared interface.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
