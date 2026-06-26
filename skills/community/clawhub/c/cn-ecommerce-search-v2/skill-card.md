## Description: <br>
Searches major Chinese e-commerce platforms for products, product links, and price comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vince199907](https://clawhub.ai/user/vince199907) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask an agent to search Taobao, Tmall, JD, Pinduoduo, Goofish, Xiaohongshu, Douyin, and 1688 for a product, compare prices, and summarize buying considerations before any purchase decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches may open multiple third-party shopping sites and expose product interests or account session context. <br>
Mitigation: Keep login, address, payment, and order placement under explicit user confirmation, and avoid entering sensitive information unless required. <br>
Risk: Prices, seller status, and authenticity claims can vary across platforms and may change after the agent gathers results. <br>
Mitigation: Verify the final product page, seller reputation, current price, and platform protections before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vince199907/cn-ecommerce-search-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown tables with product links, prices, platform notes, and short recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires web browsing across eight named Chinese shopping platforms before summarizing results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
