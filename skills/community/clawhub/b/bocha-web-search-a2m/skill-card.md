## Description: <br>
Bocha Web Search A2M provides paid Bocha web search through an A2M HTTP 402 flow, returning web links and summaries after Alipay payment is completed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iuriak](https://clawhub.ai/user/iuriak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to perform web searches, retrieve source links, and receive concise summaries that can be processed by an AI agent. It is intended for requests where the user accepts a disclosed paid Bocha search flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Bocha and may contain sensitive user intent or private terms. <br>
Mitigation: Use this skill only when the user wants Bocha as the provider, and avoid submitting sensitive search terms. <br>
Risk: The skill can initiate a paid HTTP 402 flow that requires Alipay payment before results are returned. <br>
Mitigation: Tell the user the resource is paid before making the request, and proceed with payment only after the user agrees. <br>
Risk: Payment handling depends on a separate Alipay 402 payment skill. <br>
Mitigation: Use the official Alipay payment skill referenced by the release and avoid substituting untrusted payment handlers. <br>


## Reference(s): <br>
- [Bocha Web Search A2M on ClawHub](https://clawhub.ai/iuriak/bocha-web-search-a2m) <br>
- [Bocha A2M Web Search API endpoint](https://api.bocha.cn/v1/marketplace/alipay/bochawebsearch) <br>
- [Alipay 402 Payment Skill on ClawHub](https://clawhub.ai/alipay/alipay-pay-for-402-service) <br>
- [Alipay 402 Payment Skill GitHub repository](https://github.com/alipay/payment-skills/tree/main/alipay-pay-for-402-service) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown search results with source links and summaries, plus inline shell command examples for API requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a paid A2M HTTP 402 flow and may require Alipay payment before search results are available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
