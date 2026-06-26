## Description: <br>
Baidu ecommerce one-stop service, including product knowledge (product comparison / brand knowledge / category knowledge / product specifications / brand rankings / product rankings) and transaction execution (search / order placement / after-sales). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crossallen](https://clawhub.ai/user/crossallen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to answer Baidu ecommerce product questions, compare products, search Baidu Youxuan listings, manage addresses, place orders, check order history, and query after-sales options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Baidu ecommerce token tied to shopping actions. <br>
Mitigation: Install only when the publisher and Baidu integration are trusted, keep BAIDU_EC_SEARCH_TOKEN scoped appropriately, and remove or rotate the token when no longer needed. <br>
Risk: Order creation can involve real products, prices, shipping addresses, and account activity. <br>
Mitigation: Before creating an order, verify the selected product, SKU, price, shipping address, and account with the user. <br>
Risk: Address workflows may process personal address and phone information. <br>
Mitigation: Collect only the address details needed for the purchase and avoid retaining or repeating unnecessary personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crossallen/baidu-ecommerce-search) <br>
- [Publisher profile](https://clawhub.ai/user/crossallen) <br>
- [Baidu Open Platform](https://openai.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_EC_SEARCH_TOKEN; BAIDU_EC_SEARCH_QPS can tune request pacing.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
