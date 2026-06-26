## Description: <br>
Negotiate car buy/lease deals: Research MSRP/invoice/rebates/inventory, calc total cost/payment, generate scripts/questions/bids/emails using mirroring/labels/calibrated questions/Ackerman model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ml348126](https://clawhub.ai/user/ml348126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External car shoppers and agents use this skill to research vehicle pricing, compare buy and lease economics, and prepare negotiation scripts, bids, and dealer emails. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle prices, rebates, taxes, residual values, money factors, and dealer terms can be inaccurate or change before purchase. <br>
Mitigation: Confirm current numbers with authoritative dealer, lender, manufacturer, and state sources before relying on generated calculations or negotiation targets. <br>
Risk: Generated dealer emails or negotiation scripts may commit to timing, pricing, or personal details the user does not intend to share. <br>
Mitigation: Review and edit all generated messages before sending, and proceed with a purchase only after explicit user approval. <br>


## Reference(s): <br>
- [Car Negotiator skill page](https://clawhub.ai/ml348126/car-negotiator) <br>
- [Car Values & Formulas Reference](references/car-values.md) <br>
- [Voss Negotiation Tactics for Car Deals](references/voss-tactics.md) <br>
- [Dealer email template](assets/email.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, scripts, questions, bids, email templates, and optional calculator command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use public vehicle-pricing sites and local calculator inputs supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
