## Description: <br>
eShop routes shopping and food-delivery requests to platform or merchant guidance for product search, ordering, coupon handling, address lookup, order status, and meal planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fireium](https://clawhub.ai/user/fireium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to search for products, order food, manage coupons, review saved addresses, create or close orders, and check order status across supported shopping and delivery services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use shopping tokens, saved addresses, and order tools, including buying, cancelling, claiming coupons, and showing addresses. <br>
Mitigation: Require explicit user confirmation of the platform, item, quantity, total price, selected address, coupon or points use, and order ID before those actions proceed. <br>
Risk: The Luogang flow may use a default address and available token without enough confirmation. <br>
Mitigation: Treat any address lookup, order creation, order cancellation, coupon claim, or points use as a sensitive action that needs a final user approval step. <br>
Risk: External MCP services process shopping and delivery requests and may return prices, payment links, addresses, and order data. <br>
Mitigation: Install only when the Luogang and McDonald's MCP services are trusted, and avoid exposing tokens or personal order details in assistant output. <br>


## Reference(s): <br>
- [ClawHub eShop release page](https://clawhub.ai/fireium/eshop) <br>
- [Publisher profile](https://clawhub.ai/user/fireium) <br>
- [McDonald's MCP service](https://mcp.mcd.cn) <br>
- [Luogang MCP service](https://yuju-mcp.wxhoutai.com/mcp) <br>
- [Luogang H5 product detail](https://eshop.wxhoutai.com/h5/pages/goods/detail?goods_id=xxx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-RPC request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product, coupon, nutrition, address, pricing, payment-link, and order-status details returned by external shopping or delivery services.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
