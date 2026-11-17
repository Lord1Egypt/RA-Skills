## Description:

宝宝取名 generates Chinese baby-name suggestions from family or birth-detail requests after a configured paid order flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulian822](https://clawhub.ai/user/liulian822)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a paid order, confirm payment, and receive a short set of Chinese baby-name recommendations based on their stated naming needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment, credential, and local-file behavior is mismatched or under-disclosed.

Mitigation: Review before real payment use and require one documented authoritative payment configuration.

Risk: Bundled recipient and secret values may route funds or validate payment credentials unexpectedly.

Mitigation: Remove bundled production recipient and secret values and require operators to supply deployment-specific values.

Risk: Local symmetric payment checks may not provide the assurance expected from a payment provider.

Mitigation: Replace local symmetric payment checks with provider-issued signed credentials and verify the payment dependency.

Risk: Local order-file handling can expose or misuse order data if paths are not constrained.

Mitigation: Validate order paths and limit reads and writes to the expected order directory.

Risk: The skill text asks for hidden reasoning to be shown to the user.

Mitigation: Remove instructions asking for hidden reasoning and provide concise user-facing explanations instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulian822/skills/baby-name)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces order identifiers, payment status messages, error messages, and recommended Chinese names.]

## Skill Version(s):

1.2.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
