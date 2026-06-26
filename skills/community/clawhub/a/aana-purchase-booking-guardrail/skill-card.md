## Description: <br>
Ensures any purchase, booking, or financial commitment is verified for item, price, terms, authorization, payment privacy, and reversibility before proceeding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to review purchase, booking, reservation, subscription, renewal, cancellation, refund, bid, donation, transfer, and other financially binding workflows before final submission. It helps separate browsing and drafting from commitments, require explicit approval, and minimize sensitive payment and identity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A separately configured tool could spend money, make a booking, change a subscription, or access payment data. <br>
Mitigation: Keep those tools permissioned separately and require final confirmation of the exact cost, terms, and payment method before any binding action. <br>
Risk: Purchase, booking, payment, identity, or reservation data could expose sensitive details. <br>
Mitigation: Use minimal redacted summaries and avoid full payment numbers, bank details, credentials, identity documents, raw receipts, full reservation codes, and unrelated account history. <br>
Risk: Ambiguous, high-value, recurring, non-refundable, legally binding, or third-party actions may create commitments the user did not intend. <br>
Mitigation: Separate browsing and drafting from final submission, verify terms and reversibility, and ask for explicit approval or route to human review before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-purchase-booking-guardrail) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [manifest.json](artifact/manifest.json) <br>
- [purchase-booking-review.schema.json](artifact/schemas/purchase-booking-review.schema.json) <br>
- [redacted-purchase-booking-review.json](artifact/examples/redacted-purchase-booking-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with optional redacted JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guardrail; does not execute commands, call services, install dependencies, persist memory, or place orders by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
