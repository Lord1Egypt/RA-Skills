## Description: <br>
Buying compares the same product across Taobao, Tmall, JD, PDD, VIPSHOP, and similar marketplaces, distinguishes seller trust levels, normalizes coupon-adjusted costs and fulfillment tradeoffs, and recommends a risk-adjusted purchase path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and agents use Buying to compare public marketplace listings, normalize real final prices and seller trust, and choose an action-oriented purchase route for lowest price, safest purchase, fastest arrival, or best value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A shopping recommendation could be mistaken for authority to spend money. <br>
Mitigation: Treat the skill as decision support only and require the user to verify prices, seller identity, return terms, coupons, and checkout details before any purchase. <br>
Risk: Public listing prices, coupons, seller status, and fulfillment terms can change or differ by user account or location. <br>
Mitigation: Use current public listing evidence when available, state assumptions clearly, and avoid claiming real-time prices or private order details without evidence. <br>
Risk: A low-price route may have higher authenticity, warranty, return, or seller-quality risk. <br>
Mitigation: Explain whether savings appear to come from lower seller trust, weaker warranty or invoice support, conditional subsidies, group-buy requirements, slower shipping, or return friction. <br>


## Reference(s): <br>
- [Buying ClawHub page](https://clawhub.ai/harrylabsj/buying) <br>
- [Platform Lenses](references/platform-lenses.md) <br>
- [Risk-Adjusted Pricing](references/risk-adjusted-pricing.md) <br>
- [Purchase Paths](references/purchase-paths.md) <br>
- [Example Prompts](references/example-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendations with concise comparison tables and action-oriented purchase paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only decision support; verify current prices, seller identity, return terms, and coupons before checkout.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
