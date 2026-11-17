## Description:

Cargo Claim Drafter helps freight-claim analysts, shippers, consignees, 3PLs, and transportation counsel draft review-ready Carmack Amendment cargo loss, damage, or shortage claim packets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Freight claims teams, shippers, consignees, 3PL operations teams, and transportation counsel use this skill to collect shipment facts, classify cargo exceptions, compute claim amounts, and draft a Carmack-compliant claim letter with an evidence index and deadline tracker. The generated packet is intended for claims-team and counsel review before submission.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill may process sensitive commercial shipment, vendor, pricing, and claim details.

Mitigation: Limit the draft to facts needed for the claim narrative and avoid echoing internal pricing, customer lists, or cost structure beyond what the claim requires.

Risk: Users may mistake the generated cargo claim packet for legal advice or a filing-ready legal determination.

Mitigation: Keep outputs marked as draft material for claims-team and counsel review, and avoid opinions on litigation outcome, enforceability, settlement language, or litigation strategy.

Risk: Unsupported shipment facts could create inaccurate liability assertions or claim amounts.

Mitigation: Anchor claim-letter assertions to numbered evidence-index entries and mark unsupported facts as open evidence needs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown claim packet with a draft letter, evidence index, computation worksheet, deadline tracker, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft output for claims-team and counsel review; no executable code or external tool calls.]

## Skill Version(s):

0.1.1 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
