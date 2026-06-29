## Description: <br>
零配置即装即用，提供跨平台比价工具，支持在京东、淘宝、拼多多三大平台搜索同款商品并比较价格，自动识别品牌和优惠券，返回最优购买建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare prices for a specific product or shopping link across JD, Taobao, and Pinduoduo, including coupon-aware recommendations and purchase links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product searches and submitted shopping links are sent to the skill publisher's cloud proxy and marketplace-related endpoints. <br>
Mitigation: Use the skill only for non-sensitive product research, and avoid submitting private, account-specific, or tokenized shopping URLs. <br>
Risk: Price, coupon, and availability results can change quickly or be unavailable for some products. <br>
Mitigation: Treat recommendations as shopping guidance and confirm final price, coupon eligibility, seller, and product variant on the marketplace before purchase. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON string containing platform-specific product results, notes, and hints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on external marketplace and publisher proxy availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
