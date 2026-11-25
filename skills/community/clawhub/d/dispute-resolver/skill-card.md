## Description:

Generates professional, evidence-grounded responses to refund disputes and customer complaints that protect the seller while keeping the buyer relationship intact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and operators use this skill to triage refund disputes, platform claims, chargebacks, negative-review escalations, and customer complaints, then draft a platform evidence submission, buyer message, resolution recommendation, and prevention log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated refund, report, chargeback, or block-list recommendations may affect customers, seller account standing, or dispute outcomes.

Mitigation: Review the generated package and approve the final action before submitting it to a buyer, marketplace, payment processor, carrier, or fraud-reporting channel.

Risk: Dispute work can involve buyer identifiers, payment evidence, tracking records, chat logs, and other sensitive business data.

Mitigation: Use only approved storage and communication systems, redact unnecessary identifiers, and avoid placing raw buyer, payment, or tracking data in unapproved locations.

Risk: Marketplace and payment-processor policies, evidence formats, and deadlines can change.

Mitigation: Verify current platform rules, evidence requirements, and response deadlines in the relevant seller or processor portal before acting.

## Reference(s):

- [Dispute Resolver skill page](https://clawhub.ai/leooooooow/skills/dispute-resolver)
- [Dispute Resolver - Output Template](references/output-template.md)
- [Resolution Decision Matrix](references/resolution-decision-matrix.md)
- [Platform Rules & Evidence Standards](references/platform-rules.md)
- [Response Templates & Tone Calibration](references/response-templates.md)
- [Dispute Response Quality Checklist](assets/dispute-response-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown dispute response package with assessment, platform submission, buyer message, prevention notes, and checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human-supplied dispute facts and evidence; generated refund, report, chargeback, or block-list recommendations should be reviewed before action.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
