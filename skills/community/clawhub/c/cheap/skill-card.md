## Description: <br>
Find the cheapest meaningful visible price for a product across major Chinese shopping platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare visible prices for products, and in one documented scenario flight tickets, across relevant Chinese shopping and travel platforms. It helps identify the lowest meaningful current price while flagging caveats about variants, coupons, seller trust, fees, and incomplete platform access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Visible prices may be incomplete, stale, or dependent on coupons, membership, pre-sale terms, bundles, shipping, taxes, or platform access limits. <br>
Mitigation: Treat the result as a current-price lead, compare like-for-like listings, and confirm final checkout price, fees, and terms on the platform before buying. <br>
Risk: The documented flight-ticket scenario can involve unnecessary sharing of personal travel details. <br>
Mitigation: Share only the route, date flexibility, and preferences needed for comparison, and avoid providing personal identity or payment details to the agent. <br>
Risk: The lowest visible price may come from a less reliable seller or a listing that is not actually comparable. <br>
Mitigation: Review seller reliability, product variant, bundle contents, and match confidence before treating the cheapest option as the best option. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/cheap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown with price comparison sections, confidence notes, caveats, and final advice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask one clarifying question when the product is ambiguous; switches to a cautious limited conclusion when price evidence is weak.] <br>

## Skill Version(s): <br>
0.1.1 (source: release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
