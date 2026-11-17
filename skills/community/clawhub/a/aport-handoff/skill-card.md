## Description:

Package completed work for handoff to another agent or a human, with every handoff item backed by a verified APort decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uchibeke](https://clawhub.ai/user/uchibeke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and teams use this skill to create verifiable handoff documents for completed work in multi-agent or human review workflows. It helps recipients confirm completed items, identify incomplete work, and verify signed APort decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references mutable remote setup instructions and unpinned external execution paths.

Mitigation: Review remote instructions before use, prefer the web setup flow or a pinned and verified CLI version, and do not let an agent blindly execute remote setup guidance.

Risk: Handoff documents may include sensitive project details, secrets, or recipient/channel mistakes when saved or posted.

Mitigation: Redact secrets and sensitive details, confirm the recipient and delivery channel are approved, and store local copies only where retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uchibeke/skills/aport-handoff)
- [APort passport setup](https://aport.id)
- [APort agent skill](https://aport.id/skill)
- [APort decision verification endpoint](https://aport.io/api/verify/decisions/get/DECISION_ID)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local handoff document and may provide delivery guidance for approved external channels.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
