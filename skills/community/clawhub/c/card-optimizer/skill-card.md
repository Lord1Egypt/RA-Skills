## Description:

Credit card rewards optimizer that helps maximize cashback, points, and miles by recommending the best card for purchase categories, tracking caps, calculating annual-fee ROI, managing rotating quarterly categories, and suggesting new cards based on spending patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottfo](https://clawhub.ai/user/scottfo)

### License/Terms of Use:


## Use Case:

External users use this skill to choose the best credit card for purchase categories, evaluate annual-fee ROI, manage rotating-category activations, and identify reward gaps from optional spending estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store card names, annual fees, reward preferences, signup bonus details, and optional spending estimates in a local cards.json file.

Mitigation: Enter only the minimum information needed for rewards optimization and do not include full card numbers, account credentials, transaction history, or other account-access data.

Risk: Credit-card reward rates, fees, caps, signup bonuses, and quarterly categories can change.

Mitigation: Verify researched card terms against issuer sources before relying on recommendations or updating local card data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottfo/skills/card-optimizer)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown recommendations and reports, with JSON configuration data for local card records when setup or updates are requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local cards.json file containing user-provided card details, reward preferences, signup bonus details, and optional spending estimates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
