## Description:

Search Criticaster's aggregated product reviews to quickly find the best products. Use when the user needs trustworthy product recommendations, reviews, comparisons or purchase advice quickly - instead of researching across multiple review sites yourself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gglucass](https://clawhub.ai/user/gglucass)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer product recommendation, review, comparison, and purchase-advice questions with Criticaster's aggregated review data. It is useful for best-product, budget-aware, product-comparison, and category-exploration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a user's email address to Criticaster when submitting product requests or upvotes.

Mitigation: Require explicit user approval before sending an email address for request or upvote flows.

Risk: The artifact describes completing email-code verification autonomously when mailbox access is available.

Mitigation: Do not grant mailbox access for this skill; have the user retrieve and provide verification codes manually.

Risk: The security verdict is suspicious because request and upvote flows involve user email and verification handling.

Mitigation: Use product search and browsing normally, but gate request and upvote POST actions behind user confirmation.

## Reference(s):

- [Criticaster homepage](https://www.criticaster.com)
- [ClawHub Criticaster skill page](https://clawhub.ai/gglucass/skills/criticaster)
- [Criticaster publisher profile](https://clawhub.ai/user/gglucass)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown with Criticaster API results and product links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product scores, prices, review counts, pros and cons, comparisons, category picks, and links to Criticaster product pages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
