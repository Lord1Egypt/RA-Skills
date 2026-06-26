## Description: <br>
A cosmetics e-commerce shopping assistant that supports product search, cart actions, ordering, order management, logistics lookup, and shipping-address management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bvcg204](https://clawhub.ai/user/bvcg204) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search for cosmetics products, manage carts and orders, track logistics, and maintain shipping addresses through the Filtalgo shopping service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or cancel orders and change shipping addresses. <br>
Mitigation: Require explicit user approval after showing the exact item, quantity, price, address, order number, and consequence before any state-changing action. <br>
Risk: The skill handles phone numbers, SMS login, shipping addresses, accessToken values, and refreshToken values. <br>
Mitigation: Treat credentials and personal data as secrets, avoid logging or retaining them unnecessarily, and share them only with the Filtalgo shopping service. <br>
Risk: Payment links and order actions depend on third-party Filtalgo API responses. <br>
Mitigation: Show returned order and payment details to the user and do not present purchases as complete until the service confirms the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bvcg204/beautiful-shop) <br>
- [Filtalgo Shopping API Guide](references/api_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text guidance with shell-command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return product details, cart and order data, address data, logistics status, and payment links from the Filtalgo service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
