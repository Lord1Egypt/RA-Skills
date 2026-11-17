## Description:

Upload a contract to receive an AI-generated risk analysis with flagged clauses, plain-language explanations, negotiation tips, and missing-protection checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a799549967-lang](https://clawhub.ai/user/a799549967-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, freelancers, HR teams, procurement teams, founders, and contract reviewers use this skill for first-pass contract risk triage before signing or negotiating. It reviews uploaded or pasted contracts, flags risk levels and missing protections, and suggests negotiation language while reminding users to consult a qualified attorney for binding decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract contents may include confidential, privileged, or regulated information and may be sent to the AI provider configured in OpenClaw.

Mitigation: Install only if that data flow is acceptable; review the configured provider's retention and privacy terms before processing sensitive files.

Risk: AI-generated legal analysis can miss context-specific issues or be mistaken if treated as definitive legal advice.

Mitigation: Use the report as informational triage, keep the disclaimer visible, and consult a qualified attorney for binding legal decisions.

Risk: The artifact's safety wording understates that contract content may leave the local environment for the configured AI provider.

Mitigation: Ask the agent before processing sensitive documents and avoid uploading highly confidential material unless the provider handling terms are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a799549967-lang/skills/ai-contract-reviewer)
- [Skill Definition](artifact/SKILL.md)
- [操作说明](artifact/操作说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown contract risk report with suggested clause revisions and follow-up drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mandatory legal-disclaimer language and follows the contract language where possible, including Chinese for Chinese contracts.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
