## Description: <br>
Checkers Sixty60 helps an agent shop on Checkers.co.za by browsing groceries, managing a basket, selecting delivery options, handling backup preferences, reordering regular items, and evaluating deals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snopoke](https://clawhub.ai/user/snopoke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to have an agent help shop for groceries in a Checkers Sixty60 account, including finding products, comparing deals, managing quantities, choosing backups, and preparing a cart for user review. <br>

### Deployment Geography for Use: <br>
South Africa, where Checkers.co.za and Sixty60 delivery are available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect a live grocery cart, including quantities, substitutions, delivery address context, and checkout preparation. <br>
Mitigation: Before any purchase, review the delivery address, cart contents, quantities, backup choices, substitutions, and total, then give explicit approval for checkout or payment. <br>
Risk: Stock, delivery eligibility, promotions, and cart updates may change while the agent is shopping. <br>
Mitigation: Verify the page state after each add, remove, or quantity change, and report stock or cart errors instead of assuming an action succeeded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snopoke/checkers-sixty60) <br>
- [Checkers.co.za](https://www.checkers.co.za/) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text shopping guidance and browser-action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product choices, quantities, deal comparisons, backup preferences, cart-state checks, and checkout review items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
