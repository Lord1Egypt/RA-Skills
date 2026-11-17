## Description:

Helps users find and compare pants from supported public retail sites using size, budget, and style preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

External users use this skill to search public retailer pages for pants, compare options by price, size, availability, and fit, and receive ranked shopping recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retail browsing can expose account-specific page state if the agent is run in logged-in retailer sessions or saves troubleshooting screenshots.

Mitigation: Use the skill only for pants-shopping requests on public product pages, avoid logged-in retail sessions, and review or remove temporary screenshots after troubleshooting.

Risk: Retail prices, availability, shipping details, and currency conversions can change or be approximate.

Mitigation: Treat recommendations as shopping guidance and confirm final price, stock, shipping, and sizing details on the retailer page before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/am-will/skills/get-you-some-britches)
- [Store-Specific Navigation and Extraction Guide](references/stores.md)
- [Target Men's Pants Collection](https://www.target.com/c/pants-men-s-clothing/-/N-5xu29)
- [Global Brands Store Men's Jeans](https://www.globalbrandsstore.com/en/c/men/clothing/jeans)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with product rankings, prices, availability notes, links, and optional JSON or formatted text from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sizing conversions, currency conversion notes, retailer navigation steps, and product recommendation reasoning.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
