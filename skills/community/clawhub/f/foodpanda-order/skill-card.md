## Description:

Order food from foodpanda.ph using the foodpanda-cli command-line tool for restaurant search, menu browsing, cart management, and food delivery orders in the Philippines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnwhoyou](https://clawhub.ai/user/johnwhoyou)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Foodpanda Philippines restaurants, browse menus, manage a cart, preview totals, and place cash-on-delivery food orders after explicit user confirmation.

### Deployment Geography for Use:

Philippines

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global npm CLI that handles Foodpanda login session and delivery details.

Mitigation: Review the npm package and publisher before installation, and prefer a pinned, locally installed, auditable version.

Risk: The CLI can place real cash-on-delivery food orders.

Mitigation: Confirm the restaurant, items, delivery address, total, and payment_on_delivery method with the user before running any order command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnwhoyou/skills/foodpanda-order)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, npm, shell access, Foodpanda login, and a Philippines delivery location.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
