## Description: <br>
Search, compare, and buy products from verified merchants, returning structured Decision Pack data with pros, cons, best-fit uses, allergens, verified pricing, and checkout links instead of raw web scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evoleinik](https://clawhub.ai/user/evoleinik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search verified merchant catalogs, compare product options, inspect pricing and allergens, and create checkout links for purchases completed on merchant sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product searches and checkout-link creation are sent through AirShelf. <br>
Mitigation: Use the skill only when that data flow is acceptable, and avoid unnecessary personal, medical, child-related, or contact details in search queries. <br>
Risk: A checkout URL can lead to a real purchase on a merchant site. <br>
Mitigation: Confirm the product, merchant, price, quantity, shipping, returns, allergens, and checkout destination before completing payment. <br>
Risk: Providing an email in checkout data may use it for order tracking. <br>
Mitigation: Provide an email only when the user intentionally wants it used for order tracking. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/evoleinik/airshelf) <br>
- [AirShelf API base](https://dashboard.airshelf.ai) <br>
- [Product search API](https://dashboard.airshelf.ai/api/search?q=QUERY&limit=5) <br>
- [Product comparison API](https://dashboard.airshelf.ai/api/compare?products=PRODUCT_ID_1,PRODUCT_ID_2) <br>
- [Checkout API](https://dashboard.airshelf.ai/api/merchants/MERCHANT_ID/checkout) <br>
- [Merchant directory API](https://dashboard.airshelf.ai/api/directory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands and structured API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; no API key is required by the documented endpoints.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
