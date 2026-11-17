## Description:

国内全平台比价工具。Compare prices on Taobao/JD/Pinduoduo. Supports member pricing (88VIP/Plus). 电商比价、购物助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare shopping prices for products across Taobao, JD, and Pinduoduo, including member pricing when their browser session can access it. It produces a concise comparison report and buying suggestion in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's logged-in browser session to read shopping search results and member prices.

Mitigation: Use it deliberately and only when comfortable exposing the relevant Taobao, JD, or Pinduoduo session pages to the agent.

Risk: Shopping prices and member discounts can change before purchase.

Mitigation: Verify the final price directly on the merchant site before buying.

Risk: Marketplace page or DOM changes can cause incomplete or failed price extraction.

Mitigation: Treat failed or missing entries as incomplete data and confirm important results on the source platform.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-shopping-oracle)
- [ClawHub publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown comparison report with tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's input language and may include product titles, prices, member prices, shop names, sales signals, and purchase recommendations.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
