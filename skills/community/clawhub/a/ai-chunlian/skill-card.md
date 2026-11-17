## Description:

AI春联 generates Chinese Spring Festival couplets from a user-provided scene, mood, or keyword after a configured paid-service workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulian822](https://clawhub.ai/user/liulian822)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request Chinese couplets for occasions such as Spring Festival entrances, housewarmings, business openings, or wedding blessings. The agent creates an order, routes payment through the configured ClawHub payment flow, then returns a horizontal scroll and paired couplet lines in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is payment-enabled and the security evidence reports poorly scoped, inconsistent payment handling.

Mitigation: Review the payment flow before use and do not rely on it for real payments until credentials are provider-signed and bound to the order, amount, and recipient.

Risk: The security evidence reports hardcoded payment secrets and recipient values.

Mitigation: Remove hardcoded keys and recipient values, rotate exposed secrets, and require deployment-specific configuration outside the published artifact.

Risk: The artifact asks the agent to reveal its thought process.

Mitigation: Delete the thought-process disclosure instruction before deployment and keep user-facing reasoning concise without exposing private chain-of-thought.

Risk: The security guidance says the active config file and external `clawtip` dependency need clarification.

Mitigation: Document the active configuration source and pin `clawtip` to a trusted, reviewed release before enabling the paid workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulian822/skills/ai-chunlian)
- [Publisher profile](https://clawhub.ai/user/liulian822)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Chinese text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces order details, payment status, error information when applicable, and Chinese couplet fields for horizontal scroll, first line, and second line.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
