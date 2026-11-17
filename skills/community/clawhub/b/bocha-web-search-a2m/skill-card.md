## Description:

Bocha Web Search A2M gives agents a paid A2M workflow for requesting web search results, summaries, and links from Bocha's marketplace API after user-approved payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iuriak](https://clawhub.ai/user/iuriak)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when they need current web search results with source links and summaries, and are willing to complete the disclosed paid A2M payment flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a disclosed paid web-search flow.

Mitigation: Confirm cost and payment prompts with the user before requesting the paid resource.

Risk: Search queries may contain sensitive or private information.

Mitigation: Avoid putting secrets, credentials, personal data, or confidential business details into search queries.

Risk: The artifact includes a shell-style curl example for making the HTTP request.

Mitigation: Prefer a runtime that sends requests through a structured HTTP/JSON API instead of direct shell-string substitution.

## Reference(s):

- [Bocha Web Search A2M skill page](https://clawhub.ai/iuriak/skills/bocha-web-search-a2m)
- [Bocha marketplace web search API](https://api.bocha.cn/v1/marketplace/alipay/bochawebsearch)
- [Alipay 402 payment skill on ClawHub](https://clawhub.ai/alipay/alipay-pay-for-402-service)
- [Alipay 402 payment skill source](https://github.com/alipay/payment-skills/tree/main/alipay-pay-for-402-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown search results with source links, summaries, timestamps, and inline HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-approved payment for paid search results; default result count is 10 and documented maximum is 50.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
