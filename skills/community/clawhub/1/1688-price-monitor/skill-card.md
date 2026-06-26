## Description: <br>
监控 1688 批发商品价格，支持一件代发价格查询、厂家信息、同款比价。适合电商卖家、代购、副业创业者。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[275254cl-hash](https://clawhub.ai/user/275254cl-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, sourcing agents, and developers use this skill to query 1688 product prices, supplier information, dropshipping options, comparable listings, minimum order quantities, and simple profit estimates before making sourcing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: 1688 product URLs, item IDs, and search keywords are sent to 1688 during lookup operations, and returned prices or supplier details may be incomplete or stale. <br>
Mitigation: Use a trusted Python environment for dependencies, avoid submitting sensitive sourcing data when inappropriate, and verify returned prices and supplier details before business decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/275254cl-hash/1688-price-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/275254cl-hash) <br>
- [1688 search endpoint](https://s.1688.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and JSON-formatted price, supplier, search, and profit data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests may send 1688 product URLs, item IDs, and search keywords to 1688; returned prices and supplier details should be treated as reference data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
