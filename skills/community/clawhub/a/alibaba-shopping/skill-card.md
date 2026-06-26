## Description: <br>
Alibaba Shopping Assistant guides Alibaba ecosystem shopping across Taobao, Tmall, and 1688 by comparing platform fit, seller trust, visible price, MOQ, returns, and authenticity risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to route a buying need or product link to Taobao, Tmall, or 1688, compare seller and platform trade-offs, and prepare human-reviewed shopping recommendations. Logged-in cart or pre-order steps require explicit user supervision and must stop before payment or final order submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill's instructions conflict about logged-in shopping sessions and preparing orders. <br>
Mitigation: Treat public product comparison as the default boundary; require explicit user confirmation before any authenticated cart, coupon, address, or order-preview step. <br>
Risk: Authenticated shopping workflows can expose address, cart, coupon, and order details or change cart state. <br>
Mitigation: Keep the user supervising every authenticated step, avoid collecting credentials or verification codes, and stop immediately at CAPTCHA, password, identity, final submission, or payment screens. <br>
Risk: Prices, coupons, stock, shipping, and return terms can change during browsing. <br>
Mitigation: Re-snapshot product and checkout-adjacent pages after SKU, region, coupon, or shipping changes, and require the user to recheck final terms before purchase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/alibaba-shopping) <br>
- [Browser Workflow for Alibaba Shopping](artifact/references/browser-workflow.md) <br>
- [Platform Guide](artifact/references/platform-guide.md) <br>
- [Store Types Guide](artifact/references/store-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Browser actions] <br>
**Output Format:** [Markdown shopping comparisons, order-preview summaries, and browser workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product comparison tables, seller trust notes, coupon and shipping checks, and user handoff instructions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
