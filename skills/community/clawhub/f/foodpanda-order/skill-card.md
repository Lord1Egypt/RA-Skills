## Description: <br>
Order food from foodpanda.ph using the foodpanda-cli command-line tool for restaurant search, menu browsing, cart building, and food delivery orders in the Philippines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnwhoyou](https://clawhub.ai/user/johnwhoyou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to interact with foodpanda.ph through a command-line ordering workflow. It supports finding restaurants, reviewing menus, managing a cart, previewing totals, and placing an order after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Philippines <br>

## Known Risks and Mitigations: <br>
Risk: The required external CLI captures a Foodpanda session. <br>
Mitigation: Verify the npm package and publisher independently, prefer a pinned version, and understand how to revoke the stored Foodpanda session before use. <br>
Risk: The ordering command can place a real cash-on-delivery order. <br>
Mitigation: Run the preview first and place the order only after the user explicitly confirms the restaurant, items, address, payment method, and total. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnwhoyou/foodpanda-order) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Node.js 18+, npm, shell access, and a foodpanda.ph account session.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
