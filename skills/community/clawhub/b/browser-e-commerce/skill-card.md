## Description: <br>
Browser shopping assistant. Input a product link or keyword; compare browser-visible prices, seller type, reviews, promotions, delivery/return signals, and after-sales risk across shopping sites, then output buy/wait/switch-platform advice. Safe boundary: no login, no order submission, no checkout, and no payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for browser-visible shopping research across ecommerce sites, comparing listings by price, seller trust, reviews, delivery, returns, promotions, and caveats before deciding whether to buy, wait, compare another platform, or avoid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping recommendations can be based on prices, stock, coupons, delivery promises, or return terms that change after review. <br>
Mitigation: Require the user to recheck final price, stock, delivery, coupons, and after-sales terms before making any purchase. <br>
Risk: Shopping workflows can expose credentials, identity checks, addresses, payment details, or order-submission actions. <br>
Mitigation: Keep the skill limited to browser-visible or user-provided information and do not enter credentials, checkout, submit orders, or initiate payment. <br>
Risk: Seller and review signals may be incomplete, manipulated, or insufficient to establish purchase safety. <br>
Mitigation: Compare visible seller trust, reviews, returns, promotions, delivery, and caveats, and recommend avoid or further comparison when risk signals are unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/browser-e-commerce) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown shopping comparison with a buy, wait, switch-platform, or avoid recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser-visible or user-provided shopping information only; excludes login, checkout, order submission, and payment.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
