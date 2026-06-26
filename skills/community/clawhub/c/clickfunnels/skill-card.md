## Description: <br>
ClickFunnels API integration with managed OAuth for managing contacts, products, orders, courses, forms, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to connect an agent to ClickFunnels through Maton, inspect account resources, and manage sales funnel data such as contacts, products, orders, courses, forms, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change sensitive ClickFunnels business data through a connected account. <br>
Mitigation: Require the agent to show the exact workspace, account, resource, and intended change before any write, delete, GDPR redaction, fulfillment, enrollment, order, image, or webhook action. <br>
Risk: MATON_API_KEY, OAuth connection URLs, and webhook secrets could expose account access if shared or logged. <br>
Mitigation: Keep credentials and secrets private, pass the API key through the environment, and avoid displaying connection URLs or webhook secrets in user-visible output. <br>
Risk: Requests may target the wrong ClickFunnels account when multiple Maton connections exist. <br>
Mitigation: Use the Maton-Connection header for multi-account setups and confirm the target account or workspace before state-changing requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/clickfunnels) <br>
- [ClickFunnels API Introduction](https://developers.myclickfunnels.com/docs/intro) <br>
- [ClickFunnels API Reference](https://developers.myclickfunnels.com/reference) <br>
- [ClickFunnels Pagination Guide](https://developers.myclickfunnels.com/docs/pagination) <br>
- [ClickFunnels Filtering Guide](https://developers.myclickfunnels.com/docs/filtering) <br>
- [ClickFunnels Webhooks Overview](https://developers.myclickfunnels.com/docs/webhooks-overview) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP, Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid ClickFunnels OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
