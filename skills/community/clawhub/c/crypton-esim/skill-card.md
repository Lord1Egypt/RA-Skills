## Description: <br>
Purchases anonymous eSIMs with Bitcoin, Monero, or card without requiring an account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajarmoszuk](https://clawhub.ai/user/ajarmoszuk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to browse Crypton.sh guest eSIM plans, create purchases with BTC, XMR, or card payments, and check order status from chat. It is intended for travel or mobile-data workflows where users want accountless eSIM checkout and activation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkout, payment, and activation details may expose sensitive order or eSIM access information if shared. <br>
Mitigation: Avoid sharing transcripts or logs that contain order UUIDs, payment links or addresses, ICCIDs, or activation codes. <br>
Risk: Purchase commands can create a checkout and lead users to send funds to a payment destination. <br>
Mitigation: Use buy commands intentionally and verify the package, country, price, payment method, and payment destination before sending money. <br>
Risk: The skill depends on Crypton.sh for eSIM purchase, order status, and activation data. <br>
Mitigation: Install and use the skill only when the user trusts Crypton.sh for eSIM purchases and checkout handling. <br>


## Reference(s): <br>
- [Crypton Guest eSIM API documentation](https://crypton.sh/esim/guest) <br>
- [Crypton website](https://crypton.sh) <br>
- [ClawHub skill page](https://clawhub.ai/ajarmoszuk/crypton-esim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown-formatted chat text with plan, checkout, payment, order-status, and activation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Crypton.sh guest eSIM API responses; purchase and activation details may include sensitive order UUIDs, payment links or addresses, ICCIDs, and activation codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
