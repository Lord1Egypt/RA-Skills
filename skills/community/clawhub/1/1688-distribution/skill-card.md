## Description: <br>
1688 Distribution helps agents handle 1688 distribution workflows, including product search and listing, order management, knowledge-base lookup, and shop binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 distribution operators and agents use this skill to search products, inspect distribution details, bind shops, publish products to downstream stores, query orders, send seller follow-ups, and retrieve 1688 workflow knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent 1688 Access Key handling can expose business account credentials if storage location, retention, or rotation is not managed. <br>
Mitigation: Confirm where the AK file is stored before use, restrict workspace access, and delete or rotate the key when it is no longer needed. <br>
Risk: The skill can publish or sync products to downstream shops, which may create commercial or compliance impact. <br>
Mitigation: Require explicit user confirmation of the product list and destination shop before publishing or syncing products. <br>
Risk: The skill can send seller messages during order follow-up workflows. <br>
Mitigation: Review seller-facing message content before sending and keep the message tied to confirmed order data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-distribution) <br>
- [1688aiinfra publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [README](README.md) <br>
- [Product search helper reference](scripts/biz/product_search_helper/reference.md) <br>
- [Offer information helper reference](scripts/biz/offer_info/reference.md) <br>
- [Distribution execution helper reference](scripts/biz/distribute_helper/reference.md) <br>
- [Shop information helper reference](scripts/biz/shop_info/reference.md) <br>
- [Order helper reference](scripts/biz/order_helper/reference.md) <br>
- [Knowledge helper reference](scripts/biz/knowledge_helper/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON objects containing markdown strings, plus CLI command guidance for agent execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a configured 1688 Access Key for authenticated business workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
