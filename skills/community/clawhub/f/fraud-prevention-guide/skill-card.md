## Description:

Build an ecommerce fraud prevention framework covering chargeback mitigation, order screening rules, and identity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and fraud, payments, or risk teams use this skill to design practical fraud prevention frameworks, including order screening rules, velocity checks, identity verification triggers, chargeback response playbooks, monitoring metrics, and optimization routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fraud-screening recommendations may involve privacy-sensitive behavioral, device, network, and identity data.

Mitigation: Use legal and privacy review before implementation, disclose tracking practices, minimize collected data, set retention limits, and restrict access.

Risk: Aggressive decline, block, or verification rules can create false positives and harm legitimate customers.

Mitigation: Use human review or rollback paths for high-impact rules, monitor false positive rates, and tune thresholds against observed outcomes.

Risk: The skill provides policy-design guidance rather than a turnkey fraud automation system.

Mitigation: Validate recommendations against the merchant's payment processor, card-network obligations, privacy requirements, and operational capacity before rollout.

## Reference(s):

- [Output Template](references/output-template.md)
- [Chargeback Response Guide](references/chargeback-response-guide.md)
- [Risk Scoring Model Reference](references/risk-scoring-reference.md)
- [Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured tables, checklists, thresholds, and implementation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory fraud-prevention frameworks; it does not install code or access systems.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
