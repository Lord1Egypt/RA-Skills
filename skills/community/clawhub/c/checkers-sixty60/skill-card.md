## Description:

Guides an agent through shopping on Checkers.co.za Sixty60, including product search, cart management, backup preferences, regular-item reordering, deal evaluation, and delivery-type selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snopoke](https://clawhub.ai/user/snopoke)

### License/Terms of Use:


## Use Case:

External users and shopping agents use this skill to browse Checkers.co.za, select Sixty60-eligible groceries, manage basket contents, evaluate deals, and prepare orders with user confirmation before checkout or payment.

### Deployment Geography for Use:

South Africa

## Known Risks and Mitigations:

Risk: The agent could prepare an order with the wrong delivery type, quantities, substitutions, or total.

Mitigation: Confirm delivery type, quantities, substitutions, and total with the user before checkout or any payment step.

Risk: Shopping actions may fail because items are out of stock, delivery-incompatible, or not reflected correctly in the cart.

Mitigation: Verify the cart state after each add, increase, decrease, or removal action and report any site error to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snopoke/skills/checkers-sixty60)
- [Publisher profile](https://clawhub.ai/user/snopoke)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance for browser-based shopping workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on Sixty60 filtering, cart verification, substitution preferences, deal evaluation, and checkout confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
